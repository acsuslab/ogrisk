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
import full_tuples_building_pass


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
                with open(ogrisk_config_json["features_and_labels"], 'r') as file:
                    data = json.load(file)

                st = set()

                for item in data:
                    for x in item["flow_vector"]:
                        st.add(x[2])

                stlist = list(st)
                N = len(stlist)

                for item in data:
                    hist = [0] * N

                    for x in item["flow_vector"]:
                        for i in range(N):
                            if stlist[i] == x[2]:
                                hist[i] += 1

                    item["flow_vector"] = hist
                    
                with open(ogrisk_config_json["features_and_labels_hist"], 'w') as json_file:
                    json.dump(data, json_file, indent=4)


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
