type matrix = number[][];

const matrix2: matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20],
];



// function diagonalTraversal(matrix: number[][]): number[] {
//     const result: number[] = [];
//     const rows = matrix.length;
//     const cols = matrix[0].length;

//     for (let diag = 0; diag < rows + cols - 1; diag++) {
//         let row = diag < cols ? 0 : diag - cols + 1;
//         let col = diag < cols ? diag : cols - 1;

//         while (col >= 0 && row < rows) {
//             const item = matrix[row][col];
//             result.push(item);
//             row++;
//             col--;
//         }

//     }

//     return result;
// }

// Ooutput = [1, 2, 5, 3, 6, 9, 4, 7, 10, 13, 8, 11, 14, 17, 12, 15, 18, 16, 19, 20]


// function spiralTraveral(matrix: matrix): number[] {
//     const result: number[] = [];
//     let top = 0, left = 0, bottom = matrix.length - 1, right = matrix[0].length - 1;

//     while (top <= bottom && left <= right) {
//         // left to right
//         for (let i = left; i <= right; i++) {
//             result.push(matrix[top][i])
//         }
//         top++;

//         // top to bottom
//         for (let i = top; i <= bottom; i++) {
//             result.push(matrix[i][right])
//         }
//         right--;

//         // right to left
//         for (let i = right; i >= left; i--) {
//             result.push(matrix[bottom][i])
//         }
//         bottom--;

//         // bottom to top
//         for (let i = bottom; i >= top; i--) {
//             result.push(matrix[i][left])
//         }
//         left++;
//     }

//     return result
// }

// console.log(spiralTraveral(matrix2))


console.log(bfsMatrixTraversal(matrix2))
