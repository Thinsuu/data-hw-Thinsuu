import gzip
import json
import os
from pprint import pprint

import matplotlib.pyplot as plt


def read_nextbike_json(path: str) -> dict:
    with open(path, 'rb') as f:
        json_str = gzip.decompress(f.read())
    nb = json.loads(json_str)
    return nb

def main():
    dir_path = 'input_data'
    list_of_inputData = []
    for fileName in os.listdir(dir_path):
        filePath = os.path.join(dir_path, fileName)
        if fileName == '.DS_Store':
            continue
        list_of_inputData.append(filePath)

    
    compact_jsonFiles = {}
    output_file_path = './output_data/compact_jsonFiles.json'
    for json_file in list_of_inputData:
        nb = read_nextbike_json(json_file)
        station_list_in_jsonFile = []
        places = nb['countries'][0]['cities'][0]['places']
        for station in places:
            list_of_bike = station['bike_list']
            bikes_of_the_station = []
            for bike in list_of_bike:
                bikes_of_the_station.append(int(bike['number']))

            station_list_in_jsonFile.append({
                "station name" : station['name'],
                "station coordinates": [station['lat'], station['lng']],
                "bikes": bikes_of_the_station,
                })
        compact_jsonFiles[json_file] = station_list_in_jsonFile
    
    with open(output_file_path, 'w') as output_file:
        json.dump(compact_jsonFiles, output_file, indent = 2)
    
    print(compact_jsonFiles)


if __name__ == '__main__':
    main()


# {
#     "date1": [
#         {
#             "station name": "Nordstan",
#             "station coordinates": [123.456, 798.123],
#             "bikes": [711123, 711456, 711789]
#         },
#         {
#             "station name": "Central station",
#             "station coordinates": [123.456, 798.123],
#             "bikes": [711123, 711456, 711789]
#         },
#     ],
#     "date2": [
#         {
#             "station name": "Nordstan",
#             "station coordinates": [123.456, 798.123],
#             "bikes": [711123, 711456, 711789]
#         },
#         {
#             "station name": "Central station",
#             "station coordinates": [123.456, 798.123],
#             "bikes": [711123, 711456, 711789]
#         },
#     ]
# }

# result_dict = {}

# for json in input_data_files:
#     station_list_in_the_json = []

#     for station in stations:
#         station_list_in_the_json.append({
#             "station name": station['name'],
#             "station coordinates": [station['lat'], station['lng']],
#             "bikes": station['bikes'],
#         })

#     result_dict[json['date']] = station_list_in_the_json


# output_file.write(result_dict)