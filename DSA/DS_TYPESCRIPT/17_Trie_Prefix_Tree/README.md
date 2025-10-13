# Trie (Prefix Tree) — The Basics

### What is a Trie?

A **Trie** is a special tree-based data structure used to efficiently store and look up strings, especially when you need to check prefixes. Think of a **Trie** like a giant branching phonebook — every node represents a character, and every path from the root to a leaf forms a word.

### Why do we use Tries?

- **Fast word/prefix search:** Instead of scanning strings or searching a flat list, you follow edges character by character.
- **Autocomplete & spell-check:** Tries let you quickly find all words starting with a given prefix — just follow the prefix path!
- **Dictionary compression:** Common prefixes share space, saving memory compared with storing every word independently.

### Time and Space Complexity

- **Insert word:** Up to O(L), where L is the length of the word.
- **Search/exist:** Also O(L).
- **Prefix search (startsWith):** Again O(L).
- **Space:** Tries can use a lot of memory, especially with large alphabets (e.g., English), up to O(N \times L) for N words of length L.

### How do we use a Trie?

Picture adding "cat" and "car":"

- `c` at root branches to `a`, which then branches to `t` (end of "cat") and `r` (end of "car").
- Each node can have up to as many children as there are characters in your alphabet!

Most Tries have three main operations:

1. **Insert:** Add word letter-by-letter, making new nodes as needed.
2. **Search:** Follow the path character-by-character; if you don't hit a dead end and it's marked as ending, the word exists.
3. **StartsWith:** Like search, but don't require word-ending marker — you just want to know if such a prefix exists.

### Typical Interview Questions

- **Implement Trie:** Can you write TypeScript code for insert/search/startsWith?
- **Word Dictionary:** Given a set of words, support fast lookup and prefix matching.
- **Autocomplete:** Return all words beginning with a prefix.
- **Longest common prefix:** Find the shared prefix in a list of strings.
- **Word Search in matrix/grid:** Advanced — combine Tries with DFS/BFS!

### What Patterns Pair With Tries?

- **DFS on Tries:** Explore for autocomplete and prefix listing.
- **Backtracking + Trie:** E.g. "Word Search II" (LeetCode) uses Tries plus recursive exploration for finding words in a grid.
- **Hash Maps:** Sometimes, you want a hybrid — storing children as hash maps for quick access.
- **Dynamic Programming:** Tries can help with memoization for substring problems.
