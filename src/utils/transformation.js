
// Rotate an array of lines ([x1, y1, x2, y2]) by 90 degrees clockwise with respect to the anchor point
function rotateArray90Degree(lines, anchorIn, anchorOut) {
    return { new_lines: lines.map((points, _) => {
        const centeredLine = [
            points[0] - anchorIn[0],
            points[1] - anchorIn[1],
            points[2] - anchorIn[0],
            points[3] - anchorIn[1],
        ];

        return [
            -centeredLine[1] + anchorOut[0],
            +centeredLine[0] + anchorOut[1],
            -centeredLine[3] + anchorOut[0],
            +centeredLine[2] + anchorOut[1],
        ];
    }), new_anchor_out: [
        -anchorOut[1] + anchorIn[1] + anchorOut[0],
        +anchorOut[0] - anchorIn[0] + anchorOut[1],
    ]};
}

// Flip an array of lines ([x1, y1, x2, y2])
function flipArrayHorizontally(lines, axis, anchorIn, anchorOut) {
    if (axis === 0)
        return  { new_lines: lines.map((points, index) => {
            const x1 = points[0];
            const y1 = points[1];
            const x2 = points[2];
            const y2 = points[3];

            const newX1 = 2 * anchorOut[0] - x1;
            const newX2 = 2 * anchorOut[0] - x2;

            return [newX1, y1, newX2, y2];
        }), new_anchor_out: [
            2 * anchorOut[0] - anchorIn[0],
            anchorIn[1],
        ]};
    else
        return  { new_lines: lines.map((points, index) => {
            const x1 = points[0];
            const y1 = points[1];
            const x2 = points[2];
            const y2 = points[3];

            const newY1 = 2 * anchorOut[1] - y1;
            const newY2 = 2 * anchorOut[1] - y2;

            return [x1, newY1, x2, newY2];
        }), new_anchor_out: [
            anchorIn[0],
            2 * anchorOut[1] - anchorIn[1],
        ]};
}

function changeShape(shape, iteration, anchorIn = [1, 1], anchorOut = [1, 5]) {
    const { new_lines, new_anchor_out } =
        iteration % 2 === 0 ?
            rotateArray90Degree(shape, anchorIn, anchorOut):
            flipArrayHorizontally(shape, (iteration % 4 - 1) / 2, anchorIn, anchorOut);

    return { new_shape: shape.concat(new_lines), new_anchor_out: new_anchor_out };
}

export { changeShape };
