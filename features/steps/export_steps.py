import json

from behave import then


@then("the output should be parsable as json")
def check_output_json(context):
    out = context.stdout_capture.getvalue()
    assert json.loads(out), out


@then('"{field}" in the json output should have {number:d} elements')
@then('"{field}" in the json output should have 1 element')
def check_output_field(context, field, number=1):
    out = context.stdout_capture.getvalue()
    out_json = json.loads(out)
    assert field in out_json, [field, out_json]
    assert len(out_json[field]) == number, len(out_json[field])


@then('"{field}" in the json output should not contain "{key}"')
def check_output_field_not_key(context, field, key):
    out = context.stdout_capture.getvalue()
    out_json = json.loads(out)
    assert field in out_json
    assert key not in out_json[field]


@then('"{field}" in the json output should contain "{key}"')
def check_output_field_key(context, field, key):
    out = context.stdout_capture.getvalue()
    out_json = json.loads(out)
    assert field in out_json
    assert key in out_json[field]


@then('the json output should contain {path} = "{value}"')
def check_json_output_path(context, path, value):
    """ E.g.
    the json output should contain entries.0.title = "hello"
    """
    out = context.stdout_capture.getvalue()
    struct = json.loads(out)

    for node in path.split("."):
        try:
            struct = struct[int(node)]
        except ValueError:
            struct = struct[node]
    assert struct == value, struct

