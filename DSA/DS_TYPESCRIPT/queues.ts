import { DequeInterface, LinkedListInterface, QueueInterface } from './interfaces';
import { LinkedList } from './linkedList';
import { Stack } from "./stacks";

/*
user = 1

when both are empty!
    in = [1]
    out = []

when out has data
    in = []
    out = [1,2]

    transfer all to in
    in = [2,1]
    out = [3]

*/


export class StackQueue implements QueueInterface<number> {
    private stackIn: Stack = new Stack()
    private stackOut: Stack = new Stack()

    public enqueue(item: number) {
        this.stackIn.push(item);
    }

    public dequeue(): number | undefined {
        if (this.stackOut.size() === 0) {
            while (this.stackIn.size() > 0) {
                this.stackOut.push(this.stackIn.pop()!)
            }
        }
        return this.stackOut.pop();
    }

    public peek(): number | undefined {
        if (this.stackOut.size() === 0) {
            while (this.stackIn.size() > 0) {
                this.stackOut.push(this.stackIn.pop()!)
            }
        }
        return this.stackOut.peek()
    }

    public isEmpty(): boolean {
        return this.size() === 0
    }

    public size(): number {
        return this.stackIn.size() + this.stackOut.size()
    }
}

class deque implements DequeInterface<number> {
    private llData: LinkedListInterface<number> | null;
    public length: number
    constructor(val?: number) {
        this.llData = new LinkedList(val);
        this.length = val ? 1 : 0;
    }

    addFront(item: number): void {
        this.llData?.append(item)
    }

    addBack(item: number): void {
        this.llData?.prepend(item)
    }

    removeFront(): number | undefined {
        if (this.llData?.tail) {
            const tailVal = this.llData.tail?.val;
            this.llData?.delete(this.llData.tail?.val)
        }
    }

    removeBack(): number | undefined {
        if (this.llData?.head) {
            const headVal = this.llData?.head.val;
            this.llData?.delete(headVal)
            return headVal
        }
        return undefined;
    }

    peekFront(): number | undefined {

    }

    peekBack(): number | undefined {

    }

    isEmpty(): boolean {

    }

    size(): number {

    }
}