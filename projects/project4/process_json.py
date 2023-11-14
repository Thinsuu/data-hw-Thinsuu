import gzip
import json
 
from pprint import pprint

import matplotlib.pyplot as plt
import datetime

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

def get_all_bikes_by_places(nb_dict: dict) -> dict[str, list]:
    places = nb_dict['countries'][0]['cities'][0]['places']
    bicycle_stations = {}

    for p in places:
        place_name = p['name']
        bike_list = p['bike_list']
        for bike in bike_list:
            bike_numbers = bike['number']

            if place_name not in bicycle_stations:
                bicycle_stations[place_name] = []

            bicycle_stations[place_name].append(bike_numbers)

    return bicycle_stations
    # bicycle_stations = {
    #     place['name']: [b['number'] for b in place['bike_list']]
    #     for place in places
    # }


def draw_station_bike_amount(station_bike_amount, file_path):
    total_bike_amount = sum(station_bike_amount.values())
    title_of_plot = extract_date_from_file(file_path)

    fig, ax = plt.subplots(figsize=(40, 5))
    ax.bar(
        station_bike_amount.keys(),
        station_bike_amount.values(),
    )
    ax.set_title(f'Total bikes: {total_bike_amount} ' + title_of_plot)
    plt.xticks(rotation = 90, size=4)
    plt.savefig('./Output_data/total_bike_amount.jpg')


def main():
    file_name = './input_data/20231106_005252.json.gz'
    nb = read_nextbike_json(file_name)
    station_bikes = get_all_bikes_by_places(nb)

    x = {
        station: len(bikes_list)
        for station, bikes_list in station_bikes.items()
        if not station.startswith('BIKE ')
    }
    draw_station_bike_amount(x, file_name)


if __name__ == '__main__':
    main()