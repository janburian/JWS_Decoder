import json
import os
import jwt
from pathlib import Path


def get_filenames_list(licenses_path):
    filenames_list = []
    print("FILENAMES FOUND: ")

    try:
        for dirpath, dirnames, filenames in os.walk(licenses_path):
            for filename in filenames:
                if filename.endswith(".jws"):  # Adjust the file extension as needed
                    full_path = os.path.join(dirpath, filename)
                    filenames_list.append(full_path)
                    print(filename)
    except FileNotFoundError:
        print(f"Error: The directory '{licenses_path}' does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to access '{licenses_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return filenames_list


# Printing result and saving result
def get_output_information(filenames_list):
    decoded_outputs_list = []
    idx = 0
    for filename in filenames_list:
        f = open(filename)
        print(filename)
        decoded = jwt.decode(f.read(), options={"verify_signature": False})
        decoded_outputs_list.append(decoded)
        print(json.dumps(decoded, sort_keys=True, indent=4))
        print()
        print()
        idx += 1
        f.close()
    save_output_to_json(decoded_outputs_list)


# Saving output to .json file
def save_output_to_json(decoded_outputs_list):
    try:
        with open('license_data.json', 'w', encoding='utf-8') as f:
            json.dump(decoded_outputs_list, f, sort_keys=True, ensure_ascii=False, indent=4)
        f.close()
    except Exception as e:
        print(f"An error occurred while saving the JSON file: {e}")


if __name__ == "__main__":
    print("Please, insert path to JWS files: ")
    licenses_path = input()
    full_filenames_list = get_filenames_list(Path(licenses_path))
    print()
    get_output_information(full_filenames_list)
