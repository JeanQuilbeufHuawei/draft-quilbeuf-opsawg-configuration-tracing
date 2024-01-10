import json
import sys
from datetime import date
import os.path
import subprocess
from typing import List

from jinja2 import Environment, select_autoescape, FileSystemLoader

BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
YANG_DIR = os.path.join(os.path.dirname(BUILDER_DIR), "yang")
JSON_DIR = os.path.join(os.path.dirname(BUILDER_DIR), "json")


env = Environment(
    loader=FileSystemLoader(BUILDER_DIR),
    autoescape=select_autoescape("xml")
)


def _execute_pyang(options: List[str], filenames: List[str]):
    options += ["-p", YANG_DIR]
    args = ["pyang"] + options + filenames
    result = subprocess.run(args, capture_output=True, text=True)
    print()
    print("******************************************************")
    print(" ".join(args))
    print("******************************************************")
    print(" ERRORS ")
    print(result.stderr)
    print("******************************************************")
    print(" OUT ")
    print(result.stdout)
    print("******************************************************")
    return result.stderr, result.stdout


def _build_tree(filenames):
    return _execute_pyang(["-f", "tree", "--tree-line-length", "69"], filenames)


def _format_yang(filenames):
    return _execute_pyang(["--ietf", "-f", "yang",
                           "--yang-canonical",
                           "--yang-line-length", "69"], filenames)


def _find_yang_file(prefix: str):
    for yang_file in os.listdir(YANG_DIR):
        if yang_file.startswith(prefix) and yang_file.endswith("yang"):
            return os.path.join(YANG_DIR, yang_file)
    raise Exception(f"Yang file with prefix {prefix} not found.")


def _format_json(filename):
    try:
        return "", json.dumps(json.load(open(filename)), indent=2)
    except Exception as e:
        return str(e), ""


EXT_TX_ID = _find_yang_file("ietf-external-transaction-id")


def draft_content():
    pyang_results = {
        "external_transaction_id_tree": _build_tree([EXT_TX_ID]),
        "external_transaction_id_yang": _format_yang([EXT_TX_ID]),
        }
    errors = []
    contents = {}
    for key, (error, output) in pyang_results.items():
        contents[key] = output.strip()
        if error != "":
            errors.append(key + "\n" + error)
    if errors:
        for error in errors:
            print("************ERROR********************")
            print(error)
        exit(1)
    add_date(contents)
    return contents


def add_date(contents):
    today = date.today()
    contents["day"] = today.day
    contents["month"] = today.month
    contents["year"] = today.year


if __name__ == '__main__':
    version = int(sys.argv[1])
    output = os.path.join(os.path.dirname(BUILDER_DIR), f"draft-ietf-netconf-configuration-tracing-{version:02}.xml")
    draft_text = env.get_template("draft-quilbeuf-opsawg-configuration-tracing.xml")
    with open(output, 'w') as xml_generated:
        xml_generated.write(draft_text.render(**draft_content(), version=f"{version:02}"))
