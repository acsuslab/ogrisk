# Copyright (C) 2024 ACSUS Lab (https://acsuslab.org/)
#
# This file is part of ORGISK.
#
# OGRISK is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# OGRISK is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with OGRISK. If not, see
# <https://www.gnu.org/licenses/>.

import json
import os

import ast_extractor



def main():
    ogrisk_config_json_filepath = "ogrisk_config.json"

    ast_blob_json = []

    try:
        with open(ogrisk_config_json_filepath, 'r') as file:
            ogrisk_config_json = json.load(file)

            # print("sc_sanctuary:", ogrisk_config_json["contracts_src_dir"])

            contracts_processed, errors_count = 0, 0
            for i in range(1, 4, 1):
                subdir = f"cat{i}"
                subdir_path = os.path.join(ogrisk_config_json["contracts_src_dir"], subdir)

                for item in os.listdir(subdir_path):
                    full_path = os.path.join(subdir_path, item)

                    if os.path.isfile(full_path):
                        ast = ast_extractor.ast_extractor(ogrisk_config_json, full_path, item, i)

                        if ast == None:
                            errors_count += 1
                        else:
                            contract_entry = {}

                            contract_address = "0x" + item[:40]
                            contract_entry["address"] = contract_address
                            contract_entry["category"] = i
                            contract_entry["ast"] = ast
                            ast_blob_json.append(contract_entry)
                            contracts_processed += 1
                        
            with open(ogrisk_config_json["ast_blob"], 'w') as json_file:
                json.dump(ast_blob_json, json_file, indent=4)
            
            print(f"Contracts processed: {contracts_processed}, Errors: {errors_count}")
        
    except FileNotFoundError:
        print(f"The file {ogrisk_config_json_filepath} was not found.")
    except json.JSONDecodeError:
        print("Error parsing the JSON data.")
    except Exception as e:
        print(f"An error occurred: {e}")  

if __name__ == "__main__":
    main()
