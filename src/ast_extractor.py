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

import requests
import json
import subprocess
import os

# def retrieve_compiler_version(ogrisk_config_json, contract_address):
#     params = {
#         'module': "contract",
#         'action': "getsourcecode",
#         'address': f"{contract_address}",
#         'apikey': ogrisk_config_json["etherscan_api_key"]
#     }

#     response = requests.get(ogrisk_config_json["etherscan_api_url"], params=params)
#     data = response.json()

#     if data['status'] == '1':
#         return data["result"][0]["CompilerVersion"]
#     else:
#         print(f"API request error: {data['message']}\n")
#         return None



# def run_solc_with_ast(ogrisk_config_json, compiler_exec_name, contract_path):
#     compiler_exec_path = os.path.join(ogrisk_config_json["solidity_compilers_dir"], compiler_exec_name)

#     ast_output = None

#     process = subprocess.run([compiler_exec_path, '--ast-compact-json', '--ignore-missing', contract_path], capture_output=True, text=True)

#     if process.returncode == 0:
#         ast_output = process.stdout
#     else:
#         process = subprocess.run([compiler_exec_path, '--ast-compact-json', contract_path], capture_output=True, text=True)
#         if process.returncode == 0:
#             ast_output = process.stdout
#         else:
#             process = subprocess.run([compiler_exec_path, '--ast-compact-json', contract_path], capture_output=True, text=True)
#             if process.returncode == 0:
#                 ast_output = process.stdout
#             else:
#                 process = subprocess.run([compiler_exec_path, '--ast-json', contract_path], capture_output=True, text=True)
#                 if process.returncode == 0:
#                     ast_output = process.stdout
#                 else:
#                     print("Error: The executable failed to generate the AST in both formats.")
#                     print(process.stderr)

#     return ast_output


def ast_extractor(ogrisk_config_json, file_path, filename, cat):
    compiler_exec_path = ogrisk_config_json["universal_parser_path"]

    ast_output = None

    process = subprocess.run([compiler_exec_path, file_path], capture_output=True, text=True)

    if process.returncode == 0:
        ast_output = process.stdout
    else:
        print("Error: Failed to generate AST:")
        print(process.stderr)


    res_ast = None
    try:
        res_ast = json.loads(ast_output, strict=False)
    except json.JSONDecodeError:
        print(f"Error parsing the JSON data: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")  

    return res_ast
