import json

letter_to_draw = 'А'

canvas_width = 1000
canvas_height = 1000

svg_beginning = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}">
<rect width="100%" height="100%" fill="black" />'''
svg_ending = '</svg>'
svg_line_template = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="white" stroke-width="12" stroke-linecap="round" />'

if __name__ == '__main__':
    data_dict = {}

    with open('font_data.json', 'r', encoding='utf-8') as f:
        data_dict = json.load(f)

    lines = data_dict[letter_to_draw]

    svg_lines = [svg_line_template.format(
        x1=int((x1 + 2) / 8 * canvas_width),
        y1=int((y1 + 1) / 8 * canvas_height),
        x2=int((x2 + 2) / 8 * canvas_width),
        y2=int((y2 + 1) / 8 * canvas_height),
    ) for x1, y1, x2, y2 in lines]

    svg_content = svg_beginning + '\n' + '\n'.join(svg_lines) + '\n' + svg_ending

    with open('font_data.svg', 'w') as f:
        f.write(svg_content)
