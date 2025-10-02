import { GraphInterface } from './interfaces';

class BiDirectionalGraph implements GraphInterface<number> {
    data: number[][] = []

    addVertex(): number {
        return this.data.push([]) - 1;
    }

    addEdge(vertex1: number, vertex2: number): void {
        if (!this.hasVertex(vertex1) || !this.hasVertex(vertex2)) throw new Error("Vertexes doesn't exist");
        this.data[vertex1].push(vertex2);
        this.data[vertex2].push(vertex1);
    }

    removeVertex(vertex: number): void {
        if (!this.hasVertex(vertex)) throw new Error("Vertex doesn't exist");
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
        if (!this.hasVertex(vertex1) || !this.hasVertex(vertex2)) throw new Error("Vertexes doesn't exist");

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
        if (!this.hasVertex(vertex)) throw new Error("Vertex doesn't exist");
        return this.data[vertex]
    }

    hasVertex(vertex: number): boolean {
        return vertex < this.data.length
    }

    hasEdge(vertex1: number, vertex2: number): boolean {
        return this.data.length > Math.max(vertex1, vertex2) && this.data[vertex1].includes(vertex2) && this.data[vertex2].includes(vertex1);
    }

    vertices(): number[] {
        return Array.from({ length: this.data.length - 1 }, (_, i) => i)
    }

    edges(): [number, number][] {

    }
}