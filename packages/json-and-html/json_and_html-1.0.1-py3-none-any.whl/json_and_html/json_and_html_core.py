# json_and_html_core.py

# import dict_and_html for creating HTML from dict
# import JSON for loading JSON file as Python dict
# import os for reading the filesystem

from dict_and_html import *
import json
import os


def json_in_html_out(
        json_input_dir: str = "./data/json/input/",
        html_output_dir: str = "./data/html/output/"):
    json_input_files = os.listdir(json_input_dir)
    html_output_files = []

    for current_json_input_file in json_input_files:
        current_html_output_file = current_json_input_file + ".htm"
        html_output_files.append(current_html_output_file)

        with open(json_input_dir + current_json_input_file,
                  'r') as json_input_file:
            json_input_dict = json.load(json_input_file)
            html_table_from_json_dict: str = dict_and_html(
                json_input_dict,
                table_root_name=current_json_input_file
            )

        with open(html_output_dir + current_html_output_file,
                  'w') as html_output_file:
            html_output_file.write(html_table_from_json_dict)

    print(" Input files:", json_input_files)
    print("Output files:", html_output_files)


if __name__ == "__main__":
    print("Running with default settings.")
    json_in_html_out()
