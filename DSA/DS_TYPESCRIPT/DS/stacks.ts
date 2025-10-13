import { StackInterface } from "./interfaces";


export class Stack implements StackInterface<number> {
    private data: number[] = []
    push(item: number) {
        this.data.push(item)
    }
    pop(): number | undefined {
        return this.data.pop();
    }
    peek(): number | undefined {
        return this.data[this.size() - 1];
    }

    isEmpty(): boolean {
        return this.data.length === 0;
    }

    size(): number {
        return this.data.length;
    }
}