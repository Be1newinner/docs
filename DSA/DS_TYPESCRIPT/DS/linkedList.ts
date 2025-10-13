import { DoublyLinkedListInterface, DoublyListNodeInterface, LinkedListInterface, ListNodeInterface } from "./interfaces";

class LLNode implements ListNodeInterface<number> {
    val: number;
    next: ListNodeInterface<number> | null;

    constructor(val: number) {
        this.val = val;
        this.next = null
    }
}

export class LinkedList implements LinkedListInterface<number> {
    private head: ListNodeInterface<number> | null;
    private tail: ListNodeInterface<number> | null;

    constructor(val?: number) {
        this.head = val ? new LLNode(val) : null;
        this.tail = this.head;
    }

    append(item: number): void {
        const node = new LLNode(item);
        if (!this.head) {
            this.head = this.tail = node;
        } else {
            this.tail!.next = node;
            this.tail = this.tail!.next;
        }
    }

    prepend(item: number): void {
        const node = new LLNode(item);
        if (!this.head) {
            this.head = this.tail = node;
        } else {
            let curr = this.head
            node.next = curr;
            this.head = node;
        }
    }

    delete(item: number): void {
        let curr = this.head;
        let parent: ListNodeInterface<number> | null = null;

        while (curr !== null) {
            if (curr.val === item) {
                if (!parent) {
                    this.head = curr.next;
                    if (this.tail === curr) {
                        this.tail = this.head;
                    }
                } else {
                    parent.next = curr.next;
                    if (this.tail === curr) {
                        this.tail = parent;
                    }
                }
                break;
            }
            parent = curr;
            curr = curr.next;
        }
    }


    find(item: number): ListNodeInterface<number> | null {
        let curr = this.head;

        while (curr != null) {
            if (curr.val === item) return curr
            curr = curr.next
        }

        return null
    }

    isEmpty(): boolean {
        return this.head === null;
    }

    size(): number {
        let count = 0;
        let curr = this.head;

        while (curr != null) {
            count++;
            curr = curr.next
        }

        return count
    }
}

class DoublyLinkedListNode implements DoublyListNodeInterface<number> {
    public val: number;
    public next: DoublyListNodeInterface<number> | null;
    public prev: DoublyListNodeInterface<number> | null;

    constructor(val: number) {
        this.val = val;
        this.next = null;
        this.prev = null
    }
}

export class DoublyLinkedList implements DoublyLinkedListInterface<number> {
    private head: DoublyListNodeInterface<number> | null;
    private tail: DoublyListNodeInterface<number> | null;

    constructor(val?: number) {
        this.head = val ? new DoublyLinkedListNode(val) : null;
        this.tail = this.head;
    }


    append(item: number): void {
        const node = new DoublyLinkedListNode(item);
        if (this.head === null) {
            this.head = this.tail = node;
        } else {
            this.tail!.next = node;
            node.prev = this.tail;
            this.tail = node;
        }
    }

    prepend(item: number): void {
        const node = new DoublyLinkedListNode(item);
        if (this.head === null) {
            this.head = this.tail = node;
        } else {
            this.head.prev = node;
            node.next = this.head;
            this.head = node;
        }

    }

    delete(item: number): void {
        if (this.head !== null) {
            let curr: DoublyListNodeInterface<number> | null = this.head;

            while (curr !== null) {
                if (curr.val === item) {
                    if (curr.prev) {
                        curr.prev.next = curr.next;
                    } {
                        this.head = curr.next;
                    }

                    if (curr.next) {
                        curr.next.prev = curr.prev;
                    } else {
                        this.tail = curr.prev
                    }
                    break;
                }

                curr = curr.next;
            }

        }
        else return;

    }

    deleteBack(): number | null {
        if (this.isEmpty()) {
            return null;
        } else {
            const nodeVal = this.tail!.val;
            if (this.tail === this.head) {
                this.tail = this.head = null
            } else {
                this.tail = this.tail!.prev;
                this.tail!.next = null;
            }
            return nodeVal;
        }
    }

    deleteFront(): number | null {
        if (this.isEmpty()) {
            return null;
        } else {
            const nodeVal = this.head!.val;
            if (this.tail === this.head) {
                this.tail = this.head = null
            } else {
                this.head = this.head!.next;
                this.head!.prev = null;
            }
            return nodeVal;
        }
    }

    find(item: number): DoublyListNodeInterface<number> | null {
        let curr = this.head;

        while (curr != null) {
            if (curr.val === item) return curr
            curr = curr.next
        }

        return null
    }

    isEmpty(): boolean {
        return this.head === null;
    }

    size(): number {
        let count = 0;
        let curr = this.head;

        while (curr != null) {
            count++;
            curr = curr.next
        }

        return count
    }

    clear(): void {
        this.head = null
        this.tail = null
    }

    toArray(): number[] {
        const nodeVals: number[] = [];
        let curr = this.head;

        while (curr != null) {
            nodeVals.push(curr.val);
            curr = curr.next
        }
        return nodeVals;
    }
}