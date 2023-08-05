from datetime import datetime
import argparse
import os.path
from operator import itemgetter

FORMAT_DATE = "%Y-%m-%d_%I:%M:%S.%f"

START_LOG = "start.log"
END_LOG = "end.log"
ABBR_TXT = "abbreviations.txt"


def get_files_paths(dir_path):
    path_files = [START_LOG, END_LOG, ABBR_TXT]
    files_path = ()
    for i in path_files:
        full_path = os.path.join(dir_path, i)
        if not os.path.exists(full_path):
            print(f'File {i} not found.')
            exit()

        files_path += (full_path,)

    return files_path


def open_log_file(path_to_file):
    with open(path_to_file, "r") as report:
        data = report.readlines()
        racer_report = {}
        for i in data:
            i = i.strip()
            racer = i[:3]
            racer_report[racer] = datetime.strptime(i[3:], FORMAT_DATE)
        return racer_report


def open_abbr_file(path_to_file):
    with open(path_to_file, "r") as abbreviations:
        data_abbr = abbreviations.readlines()
        abbr_dict = {}

        for i in data_abbr:
            abbr, name, team = i.strip().split("_")
            abbr_dict[abbr] = (name, team)
        return abbr_dict


def get_time_delta(data_start, data_end):
    racer_start_report = open_log_file(data_start)
    racer_end_report = open_log_file(data_end)
    racer_result = {}
    for key, date in racer_start_report.items():
        racer_time_end = racer_end_report[key]
        racer_time_start = racer_start_report[key]
        if racer_time_end > racer_time_start:
            result = racer_time_end - racer_time_start
        else:
            result = f"{racer_time_end - racer_time_start} -- invalid value"
        racer_result[key] = str(result)
    return racer_result


def build_report(start_file, end_file, abbreviations_file, desc: bool = False, driver: str = None):
    racer_result = get_time_delta(start_file, end_file)
    sorted_racer_time = dict(sorted(racer_result.items(), key=lambda x: x[1]))
    abbr_dict = open_abbr_file(abbreviations_file)
    results = []
    for i, k in abbr_dict.items():
        results += [(abbr_dict[i][0], abbr_dict[i][1], sorted_racer_time[i])]
    sorted_results = sorted(results, key=itemgetter(2))
    if desc == True:
        sorted_results = sorted(results, key=itemgetter(2), reverse=True)
    if driver:
        stat = sorted_results
        for k in enumerate(stat, 1):
            place = k[0]
            driver_ = k[1][0]
            team = k[1][1]
            time = k[1][2]
            if driver == driver_:
                print(f"Driver: {driver}\nPlace:  {place}\nTeam:   {team}\nTime:   {time}")
    return sorted_results


def print_report(report):
    res = ""
    print_results = report
    for k in enumerate(print_results, 1):
        res += f'{k[0]} {k[1][0]}   | {k[1][1]}   | {k[1][2]}\n'
        if k[0] == 15:
            res += ("_" * 80 + "\n")
    print(res)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files_dir", help="folder_path", nargs="?")
    parser.add_argument("--driver", help="Enter driver's name")
    parser.add_argument("--desc", help="optional")
    parser.add_argument("--asc", help="optional")
    args = parser.parse_args()
    path = ()
    if args.files_dir:
        path += get_files_paths(args.files_dir)
    else:
        path += get_files_paths("../data")
    if args.driver:
        build_report(path[0], path[1], path[2], driver=args.driver)
    if args.desc:
        print_report(build_report(path[0], path[1], path[2], desc=True))
    if args.asc:
        print_report(build_report(path[0], path[1], path[2]))


if __name__ == '__main__':
    main()
