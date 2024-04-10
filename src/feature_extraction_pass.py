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


from feature_extractors.feature000_extractor import feature000_extractor
from feature_extractors.feature001_extractor import feature001_extractor


def fe_dfs_traversal(feature_vector, node, context):
    feature000_extractor(feature_vector, node, context)
    feature001_extractor(feature_vector, node, context)

    if isinstance(node, dict):
        if "type" in node.keys():
            #print(node["type"])
            pass

        context.count += 1
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                fe_dfs_traversal(feature_vector, value, context)
    elif isinstance(node, list):
        for item in node:
            fe_dfs_traversal(feature_vector, item, context)
    else:
        #print(node)
        pass



def feature_extraction_pass(feature_vector, ast, context):
    fe_dfs_traversal(feature_vector, ast, context)