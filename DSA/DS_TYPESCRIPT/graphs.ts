import { GraphInterface } from './interfaces';

class BiDirectionalGraph implements GraphInterface<number> {
    data: number[][] = []

    addVertex(): number {
        return this.data.push([]) - 1;
    }

    addEdge(vertex1: number, vertex2: number): void {
        if (vertex1 >= this.data.length) throw new Error("Vertex doesn't exist");
        this.data[vertex1].push(vertex2);
    }

    removeVertex(vertex: number): void {
        if (vertex >= this.data.length) throw new Error("Vertex doesn't exist");
        const edgesLength = this.data[vertex].length;
        this.data[vertex].splice(0, edgesLength);

        this.data.forEach((item) => {
            const vertexIdx = item.indexOf(vertex);
            if (vertexIdx >= 0) {
                item.splice(vertexIdx, 1);
            }
        })
    }

    removeEdge(vertex1: number, vertex2: number): void {
        if (vertex1 >= this.data.length || vertex2 >= this.data.length) throw new Error("Vertex doesn't exist");
        const vertex1Idx = this.data[vertex1].indexOf(vertex2);
        if (vertex1Idx >= 0) {
            this.data[vertex1].splice(vertex1Idx, 1)
        }
        const vertex2Idx = this.data[vertex2].indexOf(vertex1);
        if (vertex2Idx >= 0) {
            this.data[vertex2].splice(vertex2Idx, 1)
        }
    }

    getNeighbors(vertex: number): number[] {

    }

    hasVertex(vertex: number): boolean {

    }

    hasEdge(vertex1: number, vertex2: number): boolean {

    }

    vertices(): number[] {

    }

    edges(): [number, number][] {

    }
}