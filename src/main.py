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
import numpy as np

import dfa_pass
import feature_extraction_pass
import matrix_building_pass
import trimmed_matrix_building_pass


class Context:
    def __init__(self):
        self.count = 0
        self.symtable = {}
        self.syntax_stack = []
        self.calls = {}
        self.parent = 0
        self.parent_type = ""


def main():
    ogrisk_config_json_filepath = "ogrisk_config.json"

    features_and_labels = []


    try:
        with open(ogrisk_config_json_filepath, 'r') as file:
            ogrisk_config_json = json.load(file)

            try:
                with open(ogrisk_config_json["ast_blob"], 'r') as file:
                    data = json.load(file)
                
                if isinstance(data, list):
                    for item in data:
                        contract_context = Context()
                        contract_item = {}
                        contract_item["address"] = item["address"]
                        contract_item["label"] = item["category"]
                        #contract_item["feature_vector"] = [0] * ogrisk_config_json["number_of_features"]
                        #contract_item["adjacency_matrix"] = np.zeros((item["ast_nodes"], 3)).tolist()
                        contract_item["flow_vector"] = []
                        #N = item["ast_nodes"]
                        #contract_item["adjacency_matrix"] = [[0 for _ in range(N)] for _ in range(N)]
                        #dfa_pass.dfa_pass(item["ast"], contract_context)
                        #matrix_building_pass.matrix_building_pass(item["ast"], contract_context)

                        #feature_extraction_pass.feature_extraction_pass(contract_item["feature_vector"], item["ast"], contract_context)
                        trimmed_matrix_building_pass.trimmed_matrix_building_pass(contract_item["flow_vector"], item["ast"], contract_context)

                        features_and_labels.append(contract_item)
                        #print("address:", contract_item["address"], ", feature_vector:", contract_item)

                    
                    with open(ogrisk_config_json["features_and_labels"], 'w') as json_file:
                        json.dump(features_and_labels, json_file, indent=4)

                else:
                    print("The file does not contain a JSON array.")
            except FileNotFoundError:
                print(f"The config file was not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON from the file.")
            
    except FileNotFoundError:
        print(f"The file {ogrisk_config_json_filepath} was not found.")
    except json.JSONDecodeError:
        print("Error parsing the JSON data.")
    except Exception as e:
        print(f"An error occurred: {e}")  

if __name__ == "__main__":
    main()
