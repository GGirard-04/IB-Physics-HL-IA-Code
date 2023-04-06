# Gavin Girard - April 2023

from modules import stats, util, vector
from typing import List
import csv

DEBUG = True
PRINT_SLICES = False
CSV_HEADERS = ["bodyname", "avgarea", "maxareaerror", "trueperih", "calcperih", "periherror", "trueaph", "calcaph", "apherror"]
SOURCE_PATH = "input/"
SOURCE_TYPE = ".txt"
SOURCE_FILES = [
    "C:2017_K2_PANSTARRS",
    "C:2020_V2_ZTF",
    "C:2022_A2_PANSTARRS",
    "C:2022_E3_ZTF",
    "C:2019_L3_ATLAS",
    "C:2020_K1_PANSTARRS",
    "C:2019_U5_PANSTARRS",
    "C:2019_T4_ATLAS",
    "C:2021_T4_LEMMON",
    "C:2021_Y1_ATLAS",
    "C:2021_S3_PANSTARRS",
    "P:2013_R3-A_CATALINA-PANSTARRS",
    "C:2022_L2_ATLAS"
]

data_points = 0

def run_test_on_file(source_file: str) -> List[str]:

    full_source_path = SOURCE_PATH + source_file + SOURCE_TYPE

    body_name = source_file.replace(".txt", "").replace("_", " ").replace(":", "/")
    print(f"\nRunning tests on {body_name} @ {full_source_path}")

    with open(full_source_path, "r") as source:
        source_content = util.parse_jpl_content(source)
        vector_set = util.generate_vector_set(source_content)
        orbit_slices = vector.construct_slice_set(vector_set)

        global data_points
        data_points += len(vector_set)

    areas = []
    angles = []

    for orbit_slice in orbit_slices:
        if DEBUG and PRINT_SLICES: 
            print(f"Slice: {round(orbit_slice.traversed_area)} km2 @ {round(orbit_slice.traversed_angle, 8)} rad")
        areas.append(orbit_slice.traversed_area)
        angles.append(orbit_slice.traversed_angle)

    average_area = stats.get_stat_mean(areas)

    area_errors = [stats.get_stat_error(average_area, area) for area in areas]
    max_area_error = stats.get_stat_max(area_errors)
    if DEBUG:
        print(f"\nMaximum Area Error: {max_area_error}")

    smallest_angle_slice = stats.get_stat_min(orbit_slices, selector=lambda s: s.traversed_angle)
    true_perihelion_dist = smallest_angle_slice.longest_vector_length
    calc_perihelion_dist = smallest_angle_slice.get_calculated_slice_distance(average_area)
    perihelion_error = stats.get_stat_error(true_perihelion_dist, calc_perihelion_dist)
    if DEBUG:
        print("\nPerihelion Distance")
        print(f"True: {true_perihelion_dist}")
        print(f"Calc: {calc_perihelion_dist}")
        print(f"Error: {perihelion_error}%")

    largest_angle_slice = stats.get_stat_max(orbit_slices, selector=lambda s: s.traversed_angle)
    true_aphelion_dist = largest_angle_slice.longest_vector_length
    calc_aphelion_dist = largest_angle_slice.get_calculated_slice_distance(average_area)
    aphelion_error = stats.get_stat_error(true_aphelion_dist, calc_aphelion_dist)
    if DEBUG:
        print("\nAphelion Distance")
        print(f"True: {true_aphelion_dist}")
        print(f"Calc: {calc_aphelion_dist}")
        print(f"Error: {aphelion_error}%")

    return [str(i) for i in [body_name, average_area, max_area_error, true_perihelion_dist, calc_perihelion_dist, perihelion_error, true_aphelion_dist, calc_aphelion_dist, aphelion_error]]

with open("output/data.csv", "w+") as output:
    writer = csv.writer(output, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
    writer.writerow(CSV_HEADERS)
    for source_file in SOURCE_FILES:
        writer.writerow(run_test_on_file(source_file))

print(f"\nData set size: {data_points} Position Vectors")