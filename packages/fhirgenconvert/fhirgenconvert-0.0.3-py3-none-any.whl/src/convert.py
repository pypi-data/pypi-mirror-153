from src.expand_value_set import expand_value_set
import os

def convert_to_fhir_gen_wrapper(structure_definition: dict):
    profile_url = structure_definition["url"]
    profile_name = structure_definition["name"]
    resource_type = structure_definition["type"]

    differential_elements = structure_definition["differential"]["element"]

    for element in differential_elements:
        # print(element)
        if element["path"] == "Observation.code":
            fixed_code = element["fixedCodeableConcept"]["coding"][0]
        elif element["path"] == "Observation.value[x]":
            value_set = element["binding"]["valueSet"]

    value_set_codes = expand_value_set(value_set)
    enum_set_list = []
    for code in value_set_codes:
        enum_set_list.append(
            { "coding" : [code] }
        )

    output_contents = create_output_file(resource_type, profile_name, profile_url, fixed_code, enum_set_list)
    write_generator_file(profile_name, output_contents)
    test_contents = create_test_file(profile_name)
    write_test_file(profile_name, test_contents)


def create_output_file(resource_type, profile_name, profile_url, fixed_code, enum_set_list) -> str:
    output_contents = f'''\
from fhirgenerator.resources.r4.{resource_type.lower()} import generate{resource_type.capitalize()}
from fhir.resources.{resource_type.lower()} import {resource_type.capitalize()}

def generate{profile_name[:1].upper() + profile_name[1:]}(patient_id, start_date, days):
    resource_detail = {{}}
    resource_detail["codes"] = [{fixed_code}]
    resource_detail["profile"] = ["{profile_url}"]
    resource_detail["enumSetList"] = {enum_set_list}
    {resource_type.lower()} = generate{resource_type.capitalize()}(resource_detail, patient_id, start_date, days)

    {resource_type.lower()} = {resource_type.capitalize()}(**{resource_type.lower()}).dict()
    return {resource_type.lower()}
'''
    return output_contents


def create_test_file(profile_name) -> str:
    test_contents = f'''\
import orjson, uuid
from fhirgenerator.helpers.helpers import default
from src.profiles.generate_{profile_name} import generate{profile_name[:1].upper() + profile_name[1:]}

def test_generate{profile_name[:1].upper() + profile_name[1:]}():
    patient_id = uuid.uuid4()
    start_date = '01-01-2022'
    days = 1

    resource = generate{profile_name[:1].upper() + profile_name[1:]}(patient_id, start_date, days)
    
    with open(f'tests/output/test_{profile_name}.json', 'wb') as outfile:
        outfile.write(orjson.dumps(resource, default=default, option=orjson.OPT_NAIVE_UTC))
'''
    return test_contents


def write_generator_file(profile_name, output_contents):
    file_name = f"generate_{profile_name}.py"
    if os.path.isfile(file_name):
        overwrite = input(f'{file_name} already exists. Overwrite (Y/n)? ')
        if overwrite.lower() == 'y':
            with open(file_name, 'w') as outfile:
                outfile.write(output_contents)
            print(f'Saved new Profile file as {file_name}')
        else:
            print('File not saved')
    else:
        with open(file_name, 'w') as outfile:
            outfile.write(output_contents)
        print(f'Saved new Profile file as {file_name}')


def write_test_file(profile_name, test_contents):
    file_name = f"test_generate_{profile_name}.py"
    if os.path.isfile(file_name):
        overwrite = input(f'{file_name} already exists. Overwrite (Y/n)? ')
        if overwrite.lower() == 'y':
            with open(file_name, 'w') as outfile:
                outfile.write(test_contents)
            print(f'Saved new Pytest file as {file_name}')
        else:
            print('File not saved')
    else:
        with open(file_name, 'w') as outfile:
            outfile.write(test_contents)
        print(f'Saved new Pytest file as {file_name}')