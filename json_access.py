import os

json_path = "data_raw/cricsheet_json/cricsheet_json/all_json"   # change if your folder name differs

files = os.listdir(json_path)

print("Files currently extracted:", len(files))
print("Sample files:", files[:5])
