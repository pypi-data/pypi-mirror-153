import argparse
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
import sys


@dataclass
class Driver:
    abbreviation: str
    name: str
    team: str
    time_start: datetime = None
    time_end: datetime = None

    @property
    def lap_time(self):
        time_delta = self.time_end - self.time_start
        if time_delta.days < 0 or time_delta.seconds > 1200:
            return None
        else:
            return time_delta


def data_from_file(file_path):
    file_elements = {}
    with open(file_path) as file:
        for line in file:
            info = line.rstrip()
            driver = info[:3]
            time = datetime.strptime(info[3:], '%Y-%m-%d_%H:%M:%S.%f')
            file_elements[driver] = time
    return file_elements


def get_abbreviations(folder_path):
    abbreviations = {}

    with open(f'{folder_path}/abbreviations.txt', encoding='utf-8') as f:
        for line in f:
            abbr, name, team = line.rstrip('\n').split('_')
            abbreviations[abbr] = [name, team]
    return abbreviations


def join_info(racer_info, time_start, time_end):
    result = []
    for key in racer_info:
        start = time_start.get(key)
        end = time_end.get(key)
        result.append(Driver(key, racer_info[key][0], racer_info[key][1], start, end))
    return result


def load_data(path):
    racer_info = get_abbreviations(path)
    time_start = data_from_file(f'{path}/start.log')
    time_end = data_from_file(f'{path}/end.log')
    return join_info(racer_info, time_start, time_end)


def build_report(folder_path):
    data = load_data(folder_path)
    ready_report = {}
    place = 1
    report = sorted(data, key=lambda time: time.lap_time if isinstance(time.lap_time, timedelta) else timedelta.max)
    for driver in report:
        ready_report[driver.name] = [place, driver.team, str(driver.lap_time)]
        place += 1
    return ready_report


def print_report(folder_path, asc_sort=True):
    result = build_report(folder_path)
    next_stage_positions = 16
    report = []
    for driver in result:
        if result[driver][0] == next_stage_positions:
            report.append('-' * 65)
        report.append('{0:2}.{1:17} | {2:25} | {3}'.format(result[driver][0], driver,
                                                           result[driver][1], result[driver][2]))
    if not asc_sort:
        report.reverse()
    for driver in report:
        print(driver)


def get_racer_info(path, racer_name):
    data = load_data(path)
    for racer in data:
        if racer.name == racer_name:
            return f'{racer.name} | {racer.team} | {racer.lap_time}'


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str, help='Folder path')
    parser.add_argument('--driver', type=str, help='Driver\'s name')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--asc', action='store_const', dest='order', const='asc', help='Ascending sort')
    group.add_argument('--desc', action='store_const', dest='order', const='desc', help='Ascending sort')
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    if args.files is not None:
        if args.driver:
            print(get_racer_info(args.files, args.driver))
        else:
            asc = False if args.order else True
            print_report(args.files, asc)


if __name__ == '__main__':
    main()
