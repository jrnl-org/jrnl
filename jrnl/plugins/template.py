import re
import yaml

VAR_RE = r"[_a-zA-Z][a-zA-Z0-9_]*"
EXPRESSION_RE = r"[\[\]():.a-zA-Z0-9_]*"
PRINT_RE = r"{{ *(.+?) *}}"
START_BLOCK_RE = r"{% *(if|for) +(.+?) *%}"
END_BLOCK_RE = r"{% *end(for|if) *%}"
FOR_RE = r"{{% *for +({varname}) +in +([^%]+) *%}}".format(
    varname=VAR_RE, expression=EXPRESSION_RE
)
IF_RE = r"{% *if +(.+?) *%}"
BLOCK_RE = r"{% *block +(.+?) *%}((?:.|\n)+?){% *endblock *%}"
INCLUDE_RE = r"{% *include +(.+?) *%}"


class Template:
    def __init__(self, template):
        self.template = template
        self.clean_template = None
        self.blocks = {}

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            front_matter, body = f.read().strip("-\n").split("---", 2)
            front_matter = yaml.load(front_matter, Loader=yaml.FullLoader)
            template = cls(body)
        template.__dict__.update(front_matter)
        return template

    def render(self, **vars):
        if self.clean_template is None:
            self._get_blocks()
        return self._expand(self.clean_template, **vars)

    def render_block(self, block, **vars):
        if self.clean_template is None:
            self._get_blocks()
        return self._expand(self.blocks[block], **vars)

    def _eval_context(self, vars):
        import asteval

        e = asteval.Interpreter(use_numpy=False, writer=None)
        e.symtable.update(vars)
        e.symtable["__last_iteration"] = vars.get("__last_iteration", False)
        return e

    def _get_blocks(self):
        def s(match):
            name, contents = match.groups()
            self.blocks[name] = self._strip_single_nl(contents)
            return ""

        self.clean_template = re.sub(BLOCK_RE, s, self.template, flags=re.MULTILINE)

    def _expand(self, template, **vars):
        stack = sorted(
            [
                (m.start(), 1, m.groups()[0])
                for m in re.finditer(START_BLOCK_RE, template)
            ]
            + [
                (m.end(), -1, m.groups()[0])
                for m in re.finditer(END_BLOCK_RE, template)
            ]
        )

        last_nesting, nesting = 0, 0
        start = 0
        result = ""
        block_type = None
        if not stack:
            return self._expand_vars(template, **vars)

        for pos, indent, typ in stack:
            nesting += indent
            if nesting == 1 and last_nesting == 0:
                block_type = typ
                result += self._expand_vars(template[start:pos], **vars)
                start = pos
            elif nesting == 0 and last_nesting == 1:
                if block_type == "if":
                    result += self._expand_cond(template[start:pos], **vars)
                elif block_type == "for":
                    result += self._expand_loops(template[start:pos], **vars)
                elif block_type == "block":
                    result += self._save_block(template[start:pos], **vars)
                start = pos
            last_nesting = nesting

        result += self._expand_vars(template[stack[-1][0] :], **vars)
        return result

    def _expand_vars(self, template, **vars):
        safe_eval = self._eval_context(vars)
        expanded = re.sub(
            INCLUDE_RE, lambda m: self.render_block(m.groups()[0], **vars), template
        )
        return re.sub(PRINT_RE, lambda m: str(safe_eval(m.groups()[0])), expanded)

    def _expand_cond(self, template, **vars):
        start_block = re.search(IF_RE, template, re.M)
        end_block = list(re.finditer(END_BLOCK_RE, template, re.M))[-1]
        expression = start_block.groups()[0]
        sub_template = self._strip_single_nl(
            template[start_block.end() : end_block.start()]
        )

        safe_eval = self._eval_context(vars)
        if safe_eval(expression):
            return self._expand(sub_template)
        return ""

    def _strip_single_nl(self, template, strip_r=True):
        if template[0] == "\n":
            template = template[1:]
        if strip_r and template[-1] == "\n":
            template = template[:-1]
        return template

    def _expand_loops(self, template, **vars):
        start_block = re.search(FOR_RE, template, re.M)
        end_block = list(re.finditer(END_BLOCK_RE, template, re.M))[-1]
        var_name, iterator = start_block.groups()
        sub_template = self._strip_single_nl(
            template[start_block.end() : end_block.start()], strip_r=False
        )

        safe_eval = self._eval_context(vars)

        result = ""
        items = safe_eval(iterator)
        for idx, var in enumerate(items):
            vars[var_name] = var
            vars["__last_iteration"] = idx == len(items) - 1
            result += self._expand(sub_template, **vars)
        del vars[var_name]
        return self._strip_single_nl(result)
