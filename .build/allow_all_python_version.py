import toml

pyproject = toml.load("pyproject.toml")

pyproject["tool"]["poetry"]["dependencies"]["python"] = "*"

with open("pyproject.toml", "w") as toml_file:
    toml.dump(pyproject, toml_file)