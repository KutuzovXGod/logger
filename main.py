import argparse
import datetime
import logging
import os
import sys
from typing import List, Set

FILENAME = "temp.txt"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Log parser",
        description="Finding log files in a directory between two dates",
    )
    parser.add_argument(
        "--date_start",
        type=str,
        help="First date argument start (inclusive)",
    )
    parser.add_argument(
        "--date_end",
        type=str,
        help="Second date argument end (inclusive)",
    )

    return parser


def find_logs_in_dir() -> List[str]:
    logs = []

    for file_in_dir in os.listdir():
        file_name, file_ext = os.path.splitext(file_in_dir)
        try:
            convert = convert_string_to_date(file_name)
        except ValueError:
            convert = None

        if convert and file_ext == ".log":
            logs.append(file_in_dir)

    return logs


def find_logs_date(
    logs_in_dir: List[str],
    date_start: datetime.date,
    date_end: datetime.date,
) -> list:
    res = []

    for log_file in logs_in_dir:
        log_name, _ = os.path.splitext(log_file)
        log_name_to_date = convert_string_to_date(log_name)

        if log_name_to_date and date_start <= log_name_to_date <= date_end:
            res.append(log_file)

    return res


def find_unique_lines(logs_in_dir: list) -> Set[str]:
    lines_from_file = [read_files(log_file) for log_file in logs_in_dir]
    unique_lines = set()

    for lines in lines_from_file:
        for line in lines:
            unique_lines.add(line)

    return unique_lines


def convert_string_to_date(string_date: str) -> datetime.date:
    return datetime.datetime.strptime(string_date, "%Y%m%d").date()


def read_files(file_name: str) -> set:
    with open(file_name, encoding="utf-8") as file_buffer:
        return {line.rstrip() for line in file_buffer.readlines()}


def write_file(unique_lines: set) -> None:
    with open(FILENAME, encoding="utf-8", mode="w") as file_buffer:
        for line in unique_lines:
            file_buffer.writelines(line + "\n")


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    args = create_parser().parse_args()

    logs_in_dir = find_logs_in_dir()
    try:
        logs_by_date = find_logs_date(
            logs_in_dir,
            convert_string_to_date(args.date_start),
            convert_string_to_date(args.date_end),
        )
    except ValueError as ex:
        sys.exit(f"Wrong {ex}")
    unique_lines = find_unique_lines(logs_by_date)

    write_file(unique_lines)


if __name__ == "__main__":
    logging.debug("App startup")
    main()
    logging.debug("App shutdown")
