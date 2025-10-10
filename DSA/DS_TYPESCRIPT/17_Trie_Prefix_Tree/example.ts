class TrieNode {
    children: Map<string, TrieNode>;
    isEndOfWord: boolean;

    constructor() {
        this.children = new Map();
        this.isEndOfWord = false;
    }
}

class Trie {
    root: TrieNode;

    constructor() {
        this.root = new TrieNode();
    }

    // Insert a word into the trie
    insert(word: string): void {
        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) {
                node.children.set(char, new TrieNode());
            }
            node = node.children.get(char)!;
        }
        node.isEndOfWord = true;
    }

    // Search for a full word in the trie
    search(word: string): boolean {
        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) {
                return false;
            }
            node = node.children.get(char)!;
        }
        return node.isEndOfWord;
    }

    // Check if any word in the trie starts with the given prefix
    startsWith(prefix: string): boolean {
        let node = this.root;
        for (const char of prefix) {
            if (!node.children.has(char)) {
                return false;
            }
            node = node.children.get(char)!;
        }
        return true;
    }
}

`
Dry-Run Example
Suppose we do the following:

Insert: "car", "care"

Search: "car", "cap"

StartsWith: "ca"

Step-by-step:

Insert "car" creates path c→a→r, and marks r as end-of-word.

Insert "care" follows c→a→r (already exists), then adds e—marks e as end-of-word.

Search "car": finds the path and sees r is end-of-word → returns true.

Search "cap": path exists for c→a, but not for p → returns false.

StartsWith "ca": path exists for c→a → returns true.
`