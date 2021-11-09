import json

# This script is intended for testing full-cycle from reading Bill of Materials
# and to push the output as arguments for combobulator to evaluate

file = open("tests/package.json", "r")
body = file.read()
filex = json.loads(body)
print(list(filex['dependencies'].keys()))