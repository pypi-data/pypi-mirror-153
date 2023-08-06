# example.py

# import dict_and_html to use dict_and_html()
from dict_and_html import *

output_directory = "./data/html/output/"

example_input_dictionary = {
    "version": 0.1,
    "nested object": {
        "potentially-broken": "high",
        "nerfed": True
    },
    "singleton": "some value",
    "contents": {
        "version": 1,
        "authors": ["me", "the guys"],
        "tests passed": {
            "1.2": "failed",
            "1.0": "pass",
            "0.9": "pass"
        },
        "first_chapter": {
            "blob_of_data": "values"
        },
        "second_chapter": {
            "blob_of_data": "values",
            "addendum_to_blob": "values"
        }
    }
}

output_html_table: str = dict_and_html(example_input_dictionary)
output_filename = "example.htm"

with open(output_directory + output_filename, 'w') as filename:
    for line in output_html_table.splitlines(keepends=True):
        filename.write(line)

print("Wrote %s to disk." % (output_directory + output_filename))
