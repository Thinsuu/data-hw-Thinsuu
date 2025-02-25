import gzip
import json
import os
from pprint import pprint

import matplotlib.pyplot as plt
import datetime
from shapely.geometry import Point, Polygon

import coordinates


def extract_date_from_file(filename):
    needed_part = filename.split('/')[-1].split('.')[0]
    date_obj = datetime.datetime.strptime(needed_part, '%Y%m%d_%H%M%S')
    final_string = date_obj.strftime('%A %d.%m.%Y %H:%M:%S')
    return final_string

def read_nextbike_json(path: str) -> dict:
    with open(path, 'rb') as f:
        json_str = gzip.decompress(f.read())
    nb = json.loads(json_str)
    return nb

def get_all_bikes_by_places(nb: list) -> dict[str, list]:
    # places = nb_dict['countries'][0]['cities'][0]['places']
    bicycle_stations = {}

    for p in nb:
        place_name = p["station name"]
        bike_list = p["bikes"]
        bicycle_stations[place_name]= bike_list

    return bicycle_stations
    # bicycle_stations = {
    #     place['name']: [b['number'] for b in place['bike_list']]
    #     for place in places
    # }


def draw_station_bike_amount(station_bike_amount, file_path):
    total_bike_amount = sum(station_bike_amount.values())
    title_of_plot = extract_date_from_file(file_path)
    needed_part = file_path.split('/')[-1].split('.')[0]

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(
        station_bike_amount.keys(),
        station_bike_amount.values(),
    )
    ax.set_title(f'Total bikes: {total_bike_amount} ' + title_of_plot)
    plt.xticks(rotation = 90, size=4)
    plt.savefig('./output_data/' + needed_part + '.jpg')
    plt.close()


def main():
    areas = {
        'Hisingen' : coordinates.areas['Hisingen'],
        'City center': coordinates.areas['City center'],
        'Molndal' : coordinates.areas['Molndal']
    }

    compact_json_path = './output_data/compact_jsonFiles.json'
    dict_of_compact_items = []
    with open(compact_json_path, 'r') as fileName:
        dict_of_compact_items = json.load(fileName)
    # print(dict_of_compact_items)
     
    total_number_of_bikes = {}
    total_number_of_lost_bike = {}
    area_stations = {area: []  for area in areas.keys()}
    area_stations['Other'] = []

    for file_name, nb in dict_of_compact_items.items():  
        print(f'Processing {file_name}')
        for element in nb:
            station_name = element["station name"]
            nb_values = element["station coordinates"]
            appended = False

            for area_name, area_polygon in areas.items():
                if Point(nb_values).within(area_polygon):
                    area_stations[area_name].append(station_name)
                    appended = True
                    break

            if not appended:
                area_stations['Other'].append(station_name)
        break

    pprint(area_stations)
    for file_name, nb in dict_of_compact_items.items():  
        # nb = read_nextbike_json(file_name)
        station_bikes = get_all_bikes_by_places(nb)

        eliminated_bike_list = {
            station: len(bikes_list)
            for station, bikes_list in station_bikes.items()
            if not station.startswith('BIKE ')
        }
        draw_station_bike_amount(eliminated_bike_list, file_name)

        total_number_of_bikes[extract_date_from_file(file_name)] = sum(eliminated_bike_list.values())

        lost_bike_number = len([
            station_name
            for station_name in station_bikes.keys()
            if station_name.startswith('BIKE')
        ])
        total_number_of_lost_bike[file_name] = lost_bike_number

        fig, ax = plt.subplots(figsize=(16, 9))
        ax.bar(
            total_number_of_lost_bike.keys(),
            total_number_of_lost_bike.values(),
        )   
        ax.set_title(f'Total lost bike list: {sum(total_number_of_lost_bike.values())}')
        plt.xticks(rotation = 90, size=4)
        plt.savefig('./output_data/' + 'lost bike list.jpg')


    max_number_of_bikes = max(total_number_of_bikes.values())

    current_use_of_bicycles = {
        key : max_number_of_bikes - value
        for key, value in total_number_of_bikes.items()
    }
    average_use_of_bicycle = sum(current_use_of_bicycles.values()) // len(current_use_of_bicycles)
    print(average_use_of_bicycle)

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(
        current_use_of_bicycles.keys(),
        current_use_of_bicycles.values(),
    )
    ax.set_title(
        f'Current Use of Bicycles: {sum(current_use_of_bicycles.values())},'
        + f' Average: {average_use_of_bicycle},'
        + f' Maximum: {max(current_use_of_bicycles.values())}'
    )
    plt.xticks(rotation = 90, size=4)
    plt.savefig('./output_data/'+'Current Use of Bicycle on Monday'+ '.jpg')

        
if __name__ == '__main__':
    main()
 

#  def read_nextbike_json(path: str) -> dict:
#     with open(path, 'rb') as f:
#         json_str = gzip.decompress(f.read())
#     nb = json.loads(json_str)
#     return nb


# total_number_of_bikes.keys() : max_number_of_bikes - total_number_of_bikes.values()
    # total_number_of_bikes = 0
    # total_number_of_bikes += sum(eliminated_bike_list.values())
    # print(total_number_of_bikes)

    # current_in_use = 0
    # for file_name in list_of_inputData:
    #     current_in_use = max(eliminated_bike_list.values()) - total_number_of_bikes
    # print(current_in_use)

    # dir_path = r'/Users/thinsu/Documents/coding/nextbike/input_data'
    # list_of_files_inputData = []

    # for fileName in os.listdir(dir_path):
    #     filePath = os.path.join(dir_path, fileName)
    #     if os.path.isfile(filePath):
    #         list_of_files_inputData.append(filePath)
    # print(list_of_files_inputData)

    # for fileName in os.listdir(dir_path):
    #     list_of_compactFiles.append(fileName.keys())
    # print(list_of_compactFiles)
    
    # dir_path = 'input_data'
    # list_of_inputData = []
    # for fileName in os.listdir(dir_path):
    #     filePath = os.path.join(dir_path, fileName)
    #     if fileName == '.DS_Store':
    #         continue
    #     list_of_inputData.append(filePath)

# def extract_date_from_file(filename):
#     needed_part = filename.split('/')[-1].split('.')[0]
#     date_obj = datetime.datetime.strptime(needed_part, '%Y%m%d_%H%M%S')
#     final_string = date_obj.strftime('%A %d.%m.%Y %H:%M:%S')
#     return final_string

     # print(f'Processing {file_name}')
        # nb = read_nextbike_json(file_name)
        # eliminated_bike_list = {
        #     station: len(bikes_list)
        #     for station, bikes_list in station_bikes.items()
        #     if not station.startswith('BIKE ')
        # }

# `   station_bikes = get_all_bikes_by_places(nb)
  
#         draw_station_bike_amount(eliminated_bike_list, file_name)

#         total_number_of_bikes[extract_date_from_file(file_name)] = sum(eliminated_bike_list.values())
#     max_number_of_bikes = max(total_number_of_bikes.values())

#     current_use_of_bicycles = {
#         key : max_number_of_bikes - value
#         for key, value in total_number_of_bikes.items()
#     }
#     average_use_of_bicycle = sum(current_use_of_bicycles.values()) // len(current_use_of_bicycles)
#     print(average_use_of_bicycle)`

#     fig, ax = plt.subplots(figsize=(16, 9))
#     ax.bar(
#         current_use_of_bicycles.keys(),
#         current_use_of_bicycles.values(),
#     )
#     ax.set_title(
#         f'Current Use of Bicycles: {sum(current_use_of_bicycles.values())},'
#         + f' Average: {average_use_of_bicycle},'
#         + f' Maximum: {max(current_use_of_bicycles.values())}'
#     )
#     plt.xticks(rotation = 90, size=4)
#     plt.savefig('./output_data/'+'Current Use of Bicycle on Monday'+ '.jpg')
    
#     pprint(total_number_of_bikes)

#     pprint(current_use_of_bicycles)  
# def get_all_bikes_by_places(nb_dict: dict) -> dict[str, list]:
#     # places = nb_dict['countries'][0]['cities'][0]['places']
#     bicycle_stations = {}

#     for p in places:
#         place_name = p['name']
#         bike_list = p['bike_list']
#         for bike in bike_list:
#             bike_numbers = bike['number']

#             if place_name not in bicycle_stations:
#                 bicycle_stations[place_name] = []

#             bicycle_stations[place_name].append(bike_numbers)

#     return bicycle_stations
#     # bicycle_stations = {
#     #     place['name']: [b['number'] for b in place['bike_list']]
#     #     for place in places
#     # }


# def draw_station_bike_amount(station_bike_amount, file_path):
#     total_bike_amount = sum(station_bike_amount.values())
#     title_of_plot = extract_date_from_file(file_path)
#     needed_part = file_path.split('/')[-1].split('.')[0]

#     fig, ax = plt.subplots(figsize=(16, 9))
#     ax.bar(
#         station_bike_amount.keys(),
#         station_bike_amount.values(),
#     )
#     ax.set_title(f'Total bikes: {total_bike_amount} ' + title_of_plot)
#     plt.xticks(rotation = 90, size=4)
#     plt.savefig('./output_data/' + needed_part + '.jpg')
