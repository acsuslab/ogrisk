import json

input_file="/Users/ivanov/acsus/out-of-gas-ml/features_and_labels.json"
#output_file="/home/nick/Documents/pad/padded.json"


with open(input_file) as f:
    json_object = json.load(f)
    f.close()

st = set()


for item in json_object:
    for x in item["flow_vector"]:
        st.add(x[2])

print(len(st))




# with open(output_file, "w") as of:
#     json.dump(json_object, of, indent=4)
#     f.close()
