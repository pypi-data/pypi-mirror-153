import os
import json
from src.convert import convert_to_fhir_gen_wrapper

def main():
    print("Running")
    structure_definitions = load_files()
    for structure_definition in structure_definitions:
        convert_to_fhir_gen_wrapper(structure_definition)

def load_files():
    files = []
    input_path = os.getcwd() + '/input'
    for filename in os.listdir(input_path):
        print(f"Loading File: {os.path.join(input_path, filename)}")
        file = open(os.path.join(input_path, filename))
        contents = json.load(file)
        file.close()
        files.append(contents)

    return files

if __name__ == "__main__":
    main()