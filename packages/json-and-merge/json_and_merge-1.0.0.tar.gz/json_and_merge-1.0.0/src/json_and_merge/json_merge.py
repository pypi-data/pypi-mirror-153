# json_merge.py
import os
import json

# todo Once the following packages are available from PyPI, change these
#  imports:  dict_and_union_with, json_and_validation
from modules.json_and_validation import *
from modules.dict_and_union_with import union_with


# cycle files in ./data/json/merge/ and process only valid JSON files (
# try-except clause)
# update a result dictionary with each JSON file processed
# save the result dictionary as ./merge.json


def json_merge(merge_dir: str = './data/json/merge/',
               output_dir: str = './data/json/output/'):
    """ Reads all files with .json extension from merge_dir folder, skipping
    any file containing invalid JSON syntax, and writes a JSON file named
    'merge.json' in output_dir. """
    merge_output = 'merge.json'
    json_extension = ".json"
    # print(os.listdir(merge_dir))
    # ['collection_one.json', 'collection_two.json']
    json_files_to_validate = []
    for filename in os.listdir(merge_dir):
        if filename.endswith(json_extension):
            json_files_to_validate.append(merge_dir + filename)

    # Validate JSON files
    valid_json_to_merge = []
    for filename in json_files_to_validate:
        if is_valid_json_file(filename):
            print("  >>  Found JSON file: %s" % filename)
            with open(filename, "r") as current_filename:
                # Append (filename + JSON dict) as tuple
                valid_json_to_merge.append(
                    (filename, json.load(current_filename)))
        else:  # is not valid JSON file
            print("  >>  File %s skipped: not a valid JSON file" % filename)
    print()
    print("Acquired a total of %s JSON files." % str(len(valid_json_to_merge)))

    print()
    print("Merging JSON dictionaries")
    merge_result = {}
    for (current_json_filename, current_dict) in valid_json_to_merge:
        print("  >>  Processing file: %s" % current_json_filename)
        ##
        # Note that this operation can be done with the union operator:
        #  merge_result |= current_dict
        ##
        merge_result = union_with(merge_result, current_dict)

    print()
    print("Saving '%s' file..." % merge_output)
    with open(output_dir + merge_output, "w") as file:
        json.dump(merge_result, file, indent=4)

    print()
    print("Operation complete.")


if __name__ == "__main__":
    print("Running JSON merger directly.")
    json_merge()
