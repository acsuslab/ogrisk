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


import binascii


def full_tuples_dfs_traversal(matrix, node, context):
    if isinstance(node, dict):
        # if "stateMutability" in node.keys():
        #     if node["stateMutability"] == "pure" or node["stateMutability"] == "view":
        #         return
        # elif "isVirtual" in node.keys():
        #     if node["isVirtual"] == True:
        #         return
        # elif "kind" in node.keys():
        #     if node["kind"] == "interface":
        #         return    
        
        if "type" in node.keys():
            if node["type"] == "PragmaDirective":
                return

            if "ogrisk_id" in node.keys():
                if node["ogrisk_id"] == 0:
                    context.parent = 0
                    context.parent_type = node["type"]
                s = str(node["type"]) + str(context.parent_type)
                crc32_hash = binascii.crc32(s.encode())
                crc32_int = int(crc32_hash)
                t = (context.parent, node["ogrisk_id"], crc32_int)
                matrix.append(t)

                context.parent = node["ogrisk_id"]
                context.parent_type = node["type"]

        context.count += 1
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                full_tuples_dfs_traversal(matrix, value, context)
    elif isinstance(node, list):
        for item in node:
            full_tuples_dfs_traversal(matrix, item, context)
    else:
        pass



def full_tuples_building_pass(matrix, ast, context):
    full_tuples_dfs_traversal(matrix, ast, context)