import json

input_file="/home/nick/acsus/out-of-gas-ml/features_and_labels.json"
output_file="/home/nick/Documents/pad/padded.json"


with open(input_file) as f:
    json_object = json.load(f)
    f.close()

max_flow = 0
for item in json_object:
    if len(item["flow_vector"]) > max_flow:
        max_flow = len(item["flow_vector"])

for i in range(len(json_object)):
    if len(json_object[i]["flow_vector"]) < max_flow:
        while len(json_object[i]["flow_vector"]) < max_flow:
            json_object[i]["flow_vector"].append((0, 0, 0))


with open(output_file, "w") as of:
    json.dump(json_object, of, indent=4)
    f.close()
