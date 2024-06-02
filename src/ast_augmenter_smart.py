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


import math

def maugs_dfs_traversal(node, idcounter):

    if isinstance(node, dict):
        if "type" in node.keys():
            node["ogrisk_id"] = idcounter[0]
            idcounter[0] += 1

        if "name" in node.keys():
            node["ogrisk_extension_name"] = {}
            node["ogrisk_extension_name"]["type"] = "ogrisk_ext_name"
            node["ogrisk_extension_name"]["ogrisk_value"] = node["name"]

        if "number" in node.keys():
            node["ogrisk_extension_number"] = {}
            node["ogrisk_extension_number"]["type"] = "ogrisk_ext_number"
            node["ogrisk_extension_number"]["ogrisk_value"] = node["number"]

        if "isStateVar" in node.keys():
            node["ogrisk_extension_isStateVar"] = {}
            node["ogrisk_extension_isStateVar"]["type"] = "ogrisk_ext_isStateVar"
            node["ogrisk_extension_isStateVar"]["ogrisk_value"] = node["isStateVar"]

        if "isImmutable" in node.keys():
            node["ogrisk_extension_isImmutable"] = {}
            node["ogrisk_extension_isImmutable"]["type"] = "ogrisk_ext_isImmutable"
            node["ogrisk_extension_isImmutable"]["ogrisk_value"] = node["isImmutable"]

        if "isConstructor" in node.keys():
            node["ogrisk_extension_isConstructor"] = {}
            node["ogrisk_extension_isConstructor"]["type"] = "ogrisk_ext_isConstructor"
            node["ogrisk_extension_isConstructor"]["ogrisk_value"] = node["isConstructor"]  

        if "isVirtual" in node.keys():
            node["ogrisk_extension_isVirtual"] = {}
            node["ogrisk_extension_isVirtual"]["type"] = "ogrisk_ext_isVirtual"
            node["ogrisk_extension_isVirtual"]["ogrisk_value"] = node["isVirtual"]

        if "stateMutability" in node.keys():
            node["ogrisk_extension_stateMutability"] = {}
            node["ogrisk_extension_stateMutability"]["type"] = "ogrisk_ext_stateMutability"
            node["ogrisk_extension_stateMutability"]["ogrisk_value"] = node["stateMutability"]

        
        if "visibility" in node.keys():
            node["ogrisk_extension_visibility"] = {}
            node["ogrisk_extension_visibility"]["type"] = "ogrisk_ext_visibility"
            node["ogrisk_extension_visibility"]["ogrisk_value"] = node["visibility"]

        if "type" in node.keys():
            if node["type"] == "StringLiteral":
                node["ogrisk_extension_stringLiteral"] = {}
                node["ogrisk_extension_stringLiteral"]["type"] = "ogrisk_ext_stringLiteral"
                node["ogrisk_extension_stringLiteral"]["ogrisk_value"] = int(2**(len(node["value"])/10) - 1)

        if "type" in node.keys():
            if node["type"] == "NumberLiteral":
                node["ogrisk_extension_numberLiteral"] = {}
                node["ogrisk_extension_numberLiteral"]["type"] = "ogrisk_ext_numberLiteral"
                node["ogrisk_extension_numberLiteral"]["ogrisk_value"] = int(math.log10(int(eval(node["number"]))))


        if "modifiers" in node.keys():
            node["ogrisk_extension_modifiers"] = []

            for m in node["modifiers"]:
                mm = {}
                mm["type"] = "ogrisk_ext_modifier"
                mm["ogrisk_value"] = m
                node["ogrisk_extension_modifiers"].append(mm)
                

        # context.count += 1
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                maugs_dfs_traversal(value, idcounter)
    elif isinstance(node, list):
        for item in node:
            maugs_dfs_traversal(item, idcounter)
    else:
        pass


def ast_augmenter_smart(ast):
    counter = list()
    counter.append(0)
    maugs_dfs_traversal(ast, counter)
    return counter[0]

