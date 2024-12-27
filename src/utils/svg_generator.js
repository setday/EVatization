
function generateSVG(lines) {
    const svgContent = '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">\n<rect width="100%" height="100%" fill="black" />';
    const svgLineTemplate = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="white" stroke-width="{sw}" stroke-linecap="round" />';
    const canvasWidth = 1000;
    const canvasHeight = 1000;

    const max_x = Math.max(...lines.map(([x1, y1, x2, y2]) => Math.max(x1, x2)));
    const min_x = Math.min(...lines.map(([x1, y1, x2, y2]) => Math.min(x1, x2)));
    const max_y = Math.max(...lines.map(([x1, y1, x2, y2]) => Math.max(y1, y2)));
    const min_y = Math.min(...lines.map(([x1, y1, x2, y2]) => Math.min(y1, y2)));

    const scale = Math.min( canvasWidth / (max_x - min_x) * 0.8, canvasHeight / (max_y - min_y) * 0.8 );

    const offset_x = (canvasWidth - (max_x - min_x) * scale) / 2;
    const offset_y = (canvasHeight - (max_y - min_y) * scale) / 2;

    lines = lines.map(([x1, y1, x2, y2]) => [
        (x1 - min_x) * scale + offset_x,
        (y1 - min_y) * scale + offset_y,
        (x2 - min_x) * scale + offset_x,
        (y2 - min_y) * scale + offset_y,
    ]);

    const strokeWidth = 12 * scale / 100;

    const svgLines = lines.map(([x1, y1, x2, y2]) => svgLineTemplate
        .replace('{x1}', x1)
        .replace('{y1}', y1)
        .replace('{x2}', x2)
        .replace('{y2}', y2)
        .replace('{sw}', strokeWidth)
    );

    return svgContent + '\n' + svgLines.join('\n') + '\n</svg>';
}

export { generateSVG };
