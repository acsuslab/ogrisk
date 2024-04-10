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


def dfa_dfs_traversal(node, context):

    if isinstance(node, dict):
        if "type" in node.keys():
            #print(node["type"])
            pass

        context.count += 1
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                dfa_dfs_traversal(value, context)
    elif isinstance(node, list):
        for item in node:
            dfa_dfs_traversal(item, context)
    else:
        #print(node)
        pass


def dfa_pass(ast, context):
    dfa_dfs_traversal(ast, context)
