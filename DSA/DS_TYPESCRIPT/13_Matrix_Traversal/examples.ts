const matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

// 1. Row-wise Traversal
// Question: Print all elements row by row (left to right).

function rowWiseTraversal(matrix: number[][]): void {
    if (matrix.length === 0) return;

    for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < matrix[i].length; j++) {
            console.log(matrix[i][j]);
        }
    }
}

// Output: elements printed row-wise → 1, 2, 3, 4, 5, 6, 7, 8, 9

// 2. Column-wise Traversal
// Question: Print all elements column by column (top to bottom).

function columnWiseTraversal(matrix: number[][]): void {
    if (matrix.length === 0) return;
    const rows = matrix.length;
    const cols = matrix[0].length;
    for (let j = 0; j < cols; j++) {
        for (let i = 0; i < rows; i++) {
            console.log(matrix[i][j]);
        }
    }
}

// Output: elements printed column-wise → 1, 4, 7, 2, 5, 8, 3, 6, 9

// 3. Spiral Traversal
// Question: Print elements in a spiral order(clockwise).

function spiralTraversal(matrix: number[][]): number[] {
    const result: number[] = [];
    if (matrix.length === 0) return result;

    let top = 0;
    let bottom = matrix.length - 1;
    let left = 0;
    let right = matrix[0].length - 1;

    while (top <= bottom && left <= right) {
        // Traverse from left to right
        for (let col = left; col <= right; col++) {
            result.push(matrix[top][col]);
        }
        top++;

        // Traverse downwards
        for (let row = top; row <= bottom; row++) {
            result.push(matrix[row][right]);
        }
        right--;

        if (top <= bottom) {
            // Traverse from right to left
            for (let col = right; col >= left; col--) {
                result.push(matrix[bottom][col]);
            }
            bottom--;
        }

        if (left <= right) {
            // Traverse upwards
            for (let row = bottom; row >= top; row--) {
                result.push(matrix[row][left]);
            }
            left++;
        }
    }
    return result;
}

// Output: spiral order → 1, 2, 3, 6, 9, 8, 7, 4, 5
// const matrix2: matrix = [
//     [1, 2, 3, 4],
//     [5, 6, 7, 8],
//     [9, 10, 11, 12],
//     [13, 14, 15, 16],
//     [17, 18, 19, 20],
// ];
// 4. Diagonal Traversal
// Question: Print all elements diagonally from top - left to bottom - right.
function diagonalTraversal(matrix: number[][]): number[] {
    const rows = matrix.length;
    const cols = matrix[0].length;
    const result: number[] = [];

    for (let diag = 0; diag < rows + cols - 1; diag++) {
        let r = diag < cols ? 0 : diag - cols + 1;
        let c = diag < cols ? diag : cols - 1;
        while (r < rows && c >= 0) {
            result.push(matrix[r][c]);
            r++;
            c--;
        }
    }

    return result;
}

// Output: diagonal order → 1, 2, 4, 3, 5, 7, 6, 8, 9

// 5. Zigzag Traversal
// Question: Print elements zigzag row by row (left to right, then right to left, alternately).

function zigzagTraversal(matrix: number[][]): void {
    for (let i = 0; i < matrix.length; i++) {
        if (i % 2 === 0) {
            // Left to right
            for (let j = 0; j < matrix[i].length; j++) {
                console.log(matrix[i][j]);
            }
        } else {
            // Right to left
            for (let j = matrix[i].length - 1; j >= 0; j--) {
                console.log(matrix[i][j]);
            }
        }
    }
}

// Output: zigzag order → 1, 2, 3, 6, 5, 4, 7, 8, 9

// 6. BFS Traversal on Matrix
// Question: Given a grid, traverse neighbors level - by - level starting from the top - left.

function bfsMatrixTraversal(grid: number[][]): void {
    const rows = grid.length;
    const cols = grid[0].length;
    const visited = Array.from({ length: rows }, () => Array(cols).fill(false));
    const queue: [number, number][] = [];

    const directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]; // right, down, left, up

    queue.push([0, 0]);
    visited[0][0] = true;

    while (queue.length > 0) {
        const [r, c] = queue.shift()!;
        console.log(grid[r][c]);

        for (const [dr, dc] of directions) {
            const nr = r + dr;
            const nc = c + dc;
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc]) {
                visited[nr][nc] = true;
                queue.push([nr, nc]);
            }
        }
    }
}


`
 input : [
    [1,2,3],
    [4,5,6],
    [7,8,9]
 ]

`
// Output: BFS traversal → 1, 2, 4, 3, 5, 7, 6, 8, 9