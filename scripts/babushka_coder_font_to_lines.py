import os
import json

letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz0123456789'
font_file_prefix = ''

max_file_number = 1000

grid_width = 4
grid_height = 6

def covert_coords_to_lines(coords: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    if coords[0] > coords[2]:
        return (coords[2], coords[3], coords[0], coords[1])
    elif coords[0] == coords[2] and coords[1] > coords[3]:
        return (coords[2], coords[3], coords[0], coords[1])
    else:
        return coords

def make_lines(data: str) -> list[tuple[int, int, int, int]]:
    """
    Convert SVG path in format
    526.136 263.6V344.1H606.636V753.6H596.836V516.3H283.236V753.6H273.436V344.1H353.936V263.6H526.136Z
    to list of lines in format
    [(x1, y1, x2, y2), ...]
    """

    is_closed = data[-1] == 'Z'
    if is_closed:
        data = data[:-1]
    
    start_point_data_end_H, start_point_data_end_V, start_point_data_end_L = data.find('H'), data.find('V'), data.find('L')
    start_point_data_end = len(data)
    if start_point_data_end_H != -1: start_point_data_end = start_point_data_end_H
    if start_point_data_end_V != -1: start_point_data_end = min(start_point_data_end, start_point_data_end_V)
    if start_point_data_end_L != -1: start_point_data_end = min(start_point_data_end, start_point_data_end_L)

    start_point_data_sep = data.find(' ')

    start_point_x = int(float(data[:start_point_data_sep]))
    start_point_y = int(float(data[start_point_data_sep + 1:start_point_data_end]))
    
    lines = []

    data = data[start_point_data_end:]

    x, y = start_point_x, start_point_y

    while data:
        current_dir = data[0]
        data = data[1:]
        
        next_sep_H, next_sep_V, next_sep_L = data.find('H'), data.find('V'), data.find('L')
        next_sep = len(data)
        if next_sep_H != -1: next_sep = next_sep_H
        if next_sep_V != -1: next_sep = min(next_sep, next_sep_V)
        if next_sep_L != -1: next_sep = min(next_sep, next_sep_L)
        
        current_point_str = data[:next_sep]
        data = data[next_sep:]

        if current_dir == 'H':
            current_point = int(float(current_point_str))
            if x != current_point:
                lines.append(covert_coords_to_lines((x, y, current_point, y)))
            x = current_point
        elif current_dir == 'V':
            current_point = int(float(current_point_str))
            if y != current_point:
                lines.append(covert_coords_to_lines((x, y, x, current_point)))
            y = current_point
        elif current_dir == 'L':
            current_point = current_point_str.split(' ')
            current_x = int(float(current_point[0]))
            current_y = int(float(current_point[1]))
            lines.append(covert_coords_to_lines((x, y, current_x, current_y)))
            x, y = current_x, current_y

    if is_closed and (x, y) != (start_point_x, start_point_y):
        lines.append(covert_coords_to_lines((x, y, start_point_x, start_point_y)))

    return lines


def normalize_lines(lines: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    """
    Normalize lines to grid 6x4
    """

    min_x, min_y = lines[0][:2]
    max_x, max_y = lines[0][:2]

    for x1, y1, x2, y2 in lines:
        min_x = min(min_x, x1, x2)
        min_y = min(min_y, y1, y2)
        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)

    w, h = max_x - min_x, max_y - min_y
    offset_x, offset_y = min_x, min_y

    normalized_lines = [
        (
            (x1 - offset_x) / w,
            (y1 - offset_y) / h,
            (x2 - offset_x) / w,
            (y2 - offset_y) / h,
        )
        for x1, y1, x2, y2 in lines
    ]

    grid_width, grid_height = w // 80, h // 80
    print(grid_width, grid_height, end=' ')

    offset_x, offset_y = max(4 - grid_width + 1, 0) // 2 + 0.5, max(6 - grid_height + 1, 0) // 2 + 0.5

    grid_lines = [
        (
            int(x1 * grid_width + offset_x),
            int(y1 * grid_height + offset_y),
            int(x2 * grid_width + offset_x),
            int(y2 * grid_height + offset_y),
        )
        for x1, y1, x2, y2 in normalized_lines
    ]

    grid_lines = list(set(grid_lines))

    return grid_lines


if __name__ == '__main__':
    data_dict = {}

    for idx in range(max_file_number):
        filename = font_file_prefix + str(idx) + '.svg'
        if not os.path.exists(filename):
            continue

        with open(filename, 'r') as f:
            context = f.read()

        data_path_start = context.find('<path')
        data_start = context.find('d="', data_path_start) + 3
        data_end = context.find('"', data_start)
        data_path_end = context.find('>', data_end)

        data = context[data_start:data_end].split('M')[1:]
        data = [make_lines(d) for d in data]

        data = [item for sublist in data for item in sublist]
        data = normalize_lines(data)

        letter = letters[len(data_dict.keys())]
        print(letter)
        data_dict[letter] = data

    with open('letter-schemes.json', 'w', encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False)
