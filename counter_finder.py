# This tool is designed to efficiently locate and analyze 16-bit counters embedded within the headers of raw image frames.
# It uniquely addresses the challenge posed by potential padding bytes that might separate parts of the counter,
# ensuring accurate detection even when counters are not continuously aligned.
# Author: Artur Andrzejczak (andrzejczak.artur@gmail.com)
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.


import sys
from concurrent.futures import ThreadPoolExecutor

def read_file(path):
    with open(path, 'rb') as file:
        return file.read()

def read_files_parallel(file_paths):
    with ThreadPoolExecutor() as executor:
        file_contents = list(executor.map(read_file, file_paths))
    return file_contents

def bytes_to_int(bytes_seq, byteorder):
    return int.from_bytes(bytes_seq, byteorder)

def find_counters_in_file(data, start_byte, end_byte):
    counters = []
    data = data[start_byte:end_byte+1]
    length = len(data)
    for i in range(length - 1):
        for offset in [0, 1, 2]:  # Considering separation of 0, 1, and 2 bytes
            if i + 1 + offset < length:
                slice_le = data[i:i + 2 + offset:1 + offset]  # Little endian
                slice_be = data[i:i + 2 + offset:1 + offset]  # Big endian
                counters.append((start_byte + i, bytes_to_int(slice_le, 'little'), 'little', offset))
                counters.append((start_byte + i, bytes_to_int(slice_be, 'big'), 'big', offset))
    return counters

def find_incrementing_counter_across_files(files_data, start_byte, end_byte):
    print("Starting counter comparison across files...")
    first_file_counters = find_counters_in_file(files_data[0], start_byte, end_byte)
    for file_index in range(1, len(files_data)):
        current_counters = find_counters_in_file(files_data[file_index], start_byte, end_byte)
        matched = []
        for prev_pos, prev_value, prev_endian, prev_offset in first_file_counters:
            for curr_pos, curr_value, curr_endian, curr_offset in current_counters:
                if prev_pos == curr_pos and prev_endian == curr_endian and prev_offset == curr_offset and prev_value + 1 == curr_value:
                    matched.append((curr_pos, curr_value, curr_endian, curr_offset))
        if not matched:
            print(f"No matching counter found at file index {file_index}.")
            break
        print(f"File {file_index} processed, {len(matched)} counters increment by one.")
        first_file_counters = matched
    return first_file_counters

def main(file_paths, start_byte, end_byte):
    files_data = read_files_parallel(file_paths)
    matching_counters = find_incrementing_counter_across_files(files_data, start_byte, end_byte)
    if matching_counters:
        print("Possible counters found across files:")
        for index, value, endian, offset in matching_counters:
            print(f"Position {index}, Value {value}, Endian {endian}, Byte Offset {offset}")
    else:
        print("No consistent counter found across all files.")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python counter_finder.py <start_byte> <end_byte> <file1> <file2> [...fileN]")
        sys.exit(1)
    start_byte = int(sys.argv[1])
    end_byte = int(sys.argv[2])
    file_paths = sys.argv[3:]
    main(file_paths, start_byte, end_byte)

