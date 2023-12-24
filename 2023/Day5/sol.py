#!/usr/bin/env python3
"""
--- Day 5: If You Give A Seed A Fertilizer ---
https://adventofcode.com/2023/day/5
Part 1: Mapping tables, chained function calls
Part 2: Mapping overlapping intervals

References
- https://docs.python.org/3/library/functools.html
- https://stackoverflow.com/questions/34613543/is-there-a-chain-calling-method-in-python
- https://mathieularose.com/function-composition-in-python
"""
from collections import defaultdict
from functools import reduce


def main():
    seed_data, mappings = read_farming_almanac("input.txt")

    # Adding the rules for the implicit identity mapping ranges is used in Part 2
    mappings = {name: sort_and_complete_mapping_table(mapping_table) for name, mapping_table in mappings.items()}

    # Part 1: Find the lowest location number that corresponds to any of the initial seeds
    # Assumes mappings are ordered to obtain a seed-to-location mapping on composition
    lowest_location_number_part1 = min(reduce(apply_mapping, mappings.values(), seed) for seed in seed_data)
    print(f"Part 1: The lowest location number that corresponds to any of the initial seed numbers is {lowest_location_number_part1}")

    # Part 2: The values on the initial `seeds:` line come in pairs.
    # Within each pair, the first value is the start of the range and the second value is the length of the range.
    seed_ranges: list[tuple[int, int]] = [(start, start + range_len) for start, range_len in zip(seed_data[::2], seed_data[1::2])]

    # Note: Incrementing seed_id generally increments all other ids except at range boundaries
    # Approach 1: Map initial seed ranges to a list of location ranges and take the minimum location_range_start
    lowest_location_number_part2_approach1 = min(
        location_range_start
        for location_range_start, _ in reduce(map_source_ranges_to_destination_ranges, mappings.values(), seed_ranges)
    )

    # Approach 2: Find the lowest location number in each initial seed range then take the minimum of these numbers
    # Compare approaches 1 & 2 to breadth-first vs depth-first search, respectively
    lowest_location_number_part2_approach2 = min(
        min(
            location_range_start
            for location_range_start, _ in reduce(map_source_ranges_to_destination_ranges, mappings.values(), [seed_range])
        ) for seed_range in seed_ranges
    )
    assert lowest_location_number_part2_approach1 == lowest_location_number_part2_approach2
    print(f"Part 2: The lowest location number that corresponds to any of the initial seed numbers (ranges) is {lowest_location_number_part2_approach2}")

    return 0


def read_farming_almanac(filename: str) -> tuple[list[int], dict[str, list[dict[str, int]]]]:
    """Scan through a farming almanac file to extract seed data and mapping information (e.g. seed-to-soil map)
    seed_data is a list of integers either denoting seed IDs (Part 1) or seed ID ranges (Part 2: (range_start, range_length) pairs)
    mappings is a dictionary from mapping name, e.g. 'seed-to-soil', to lists of mapping rules/ranges
    """
    with open(filename, 'r') as file:
        seed_data: list[int] = list(map(int, file.readline().removeprefix("seeds: ").split()))
        assert file.readline() == "\n"
        mappings: dict[str, list[dict[str, int]]] = defaultdict(list)
        for line in file:
            if line.endswith(" map:\n"):
                current_map: str = line.removesuffix(" map:\n")
            elif line != '\n':
                destination_range_start, source_range_start, range_length = map(int, line.strip().split())
                mappings[current_map].append({
                    "src_start": source_range_start,
                    "src_end": source_range_start + range_length,
                    "mapping_diff": destination_range_start - source_range_start,
                    "range_len": range_length,
                    "dest_start": destination_range_start
                })
    return seed_data, mappings


def apply_mapping(id: int, mapping: list[dict[str, int]]) -> int:
    for mapping_range in mapping:
        if mapping_range["src_start"] <= id < mapping_range["src_end"]:
            return id + mapping_range["mapping_diff"]
    # Any source numbers that aren't mapped correspond to the same destination number
    return id


def sort_and_complete_mapping_table(mapping: list[dict[str, int]]) -> list[dict[str, int]]:
    """Sort a single mapping table by src_start and add rows for any hidden identity mappings between ranges"""
    mapping.sort(key=lambda mapping_range: mapping_range.get("src_start"))

    # Identify any gaps between ranges where we have an identity mapping
    new_rows: list[tuple[int, dict[str, int]]] = [
        (
            curr_idx + 1,
            {
                "src_start": curr_range["src_end"],
                "src_end": next_range["src_start"],
                "mapping_diff": 0,
                "range_len": next_range["src_start"] - curr_range["src_end"],
                "dest_start": curr_range["src_end"]
            }
        )
        for curr_idx, (curr_range, next_range) in enumerate(zip(mapping, mapping[1:]))
        if curr_range["src_end"] < next_range["src_start"]
    ]

    # Insert identity mapping ranges into mapping table
    for offset, (insert_idx, identity_range) in enumerate(new_rows):
        mapping.insert(insert_idx + offset, identity_range)

    return mapping


def map_single_source_range_to_destination_ranges(src_start: int, src_end: int, complete_sorted_mapping_table: list[dict[str, int]]) -> list[tuple[int, int]]:
    """Returns a list of destination intervals obtained by mapping the source interval.
    Calculates overlap between two source interval and intervals in the mapping domain and maps from source to destination if non-empty intersection.
    """
    destination_ranges: list[tuple[int, int]] = [
        (
            max(src_start, mapping_range["src_start"]) + mapping_range["mapping_diff"],
            min(src_end, mapping_range["src_end"]) + mapping_range["mapping_diff"]
        )
        for mapping_range in complete_sorted_mapping_table
        if src_start < mapping_range["src_end"] and mapping_range["src_start"] < src_end
    ]
    # Check for any source interval left over past the end of the table (identity mapping)
    # Uses the fact that the mapping table is sorted
    mapping_table_src_end = complete_sorted_mapping_table[-1]["src_end"]
    if src_end > mapping_table_src_end:
        destination_ranges.append((max(src_start, mapping_table_src_end), src_end))
    return destination_ranges


def map_source_ranges_to_destination_ranges(src_ranges: list[tuple[int, int]], complete_sorted_mapping_table: list[dict[str, int]]) -> list[tuple[int, int]]:
    """Map a list of source intervals to a list of destination intervals by calculating overlap with intervals in the mapping domain"""
    return [
        dest_range
        for src_start, src_end in src_ranges
        for dest_range in map_single_source_range_to_destination_ranges(src_start, src_end, complete_sorted_mapping_table)
    ]


if __name__ == "__main__":
    main()
