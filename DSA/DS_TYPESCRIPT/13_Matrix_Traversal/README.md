# Matrix Traversal Pattern

Matrix traversal involves visiting elements in a 2D grid (matrix) in a structured way. It's a fundamental pattern used in many problems like searching, pathfinding, and image processing.

## What is Matrix Traversal?

You look at each cell of the matrix following a particular order, such as row-wise, column-wise, spiral, diagonal, or zigzag.

## Why is it Useful?

- To read or manipulate matrix data completely
- To find elements or paths efficiently
- To transform matrix data in specific patterns

## How to Traverse?

1. **Nested loops** for simple row-column order
2. **Graph traversal algorithms (BFS/DFS)** for pathfinding or connected components in grids

In matrix traversal, common traversal orders include:

1. **Row-wise Traversal**  
   Visit elements row by row, left to right within each row.  
   Example: For a 3x3 matrix, visit order:  
   (0,0) → (0,1) → (0,2) → (1,0) → (1,1) → (1,2) → (2,0) → (2,1) → (2,2)

2. **Column-wise Traversal**  
   Visit elements column by column, top to bottom within each column.  
   Example: For a 3x3 matrix, visit order:  
   (0,0) → (1,0) → (2,0) → (0,1) → (1,1) → (2,1) → (0,2) → (1,2) → (2,2)

3. **Spiral Traversal**  
   Visit layers of the matrix in a spiral (clockwise or anti-clockwise).  
   Starts from the outer layer and moves inward.

4. **Diagonal Traversal**  
   Visit elements along diagonals, typically from top-left to bottom-right diagonals or vice versa.

5. **Zigzag Traversal**  
   Visit elements in a zigzag pattern, alternating direction along rows or columns.

6. **Breadth-First Search (BFS) / Depth-First Search (DFS)**  
   Traverse the matrix treating it like a graph/grid, useful for pathfinding, connected components.

Each traversal order suits different categories of problems depending on what you need to achieve with the matrix data.
