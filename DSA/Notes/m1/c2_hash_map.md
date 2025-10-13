### 2\. Hash Maps / Hash Tables (Python Dictionaries)

#### Core Concepts

A hash map (also known as a hash table, dictionary, or associative array) is a data structure that implements an associative array abstract data type, a structure that can map keys to values. A hash map uses a **hash function** to compute an index into an array of buckets or slots, from which the desired value can be found.

**Key Characteristics:**

  * **Key-Value Pairs:** Stores data as pairs of (key, value). Each key is unique within the hash map.
  * **Fast Lookups:** On average, hash maps offer $O(1)$ (constant time) complexity for insertion, deletion, and retrieval operations. This is their primary advantage.
  * **Hashing:** The core mechanism. A hash function takes a key and converts it into a fixed-size integer (the hash code), which is then used to determine the index where the value (or a reference to it) is stored in an underlying array.
  * **Collision Resolution:** Different keys can sometimes produce the same hash code, leading to a "collision." Hash maps employ strategies to handle collisions:
      * **Separate Chaining:** Each bucket in the underlying array points to a linked list (or another dynamic array) of key-value pairs that hash to that same bucket. When a collision occurs, the new item is added to the list.
      * **Open Addressing (e.g., Linear Probing, Quadratic Probing):** If a hash collision occurs, the algorithm systematically searches for the next available empty slot in the array.
  * **Dynamic Resizing (Load Factor):** As more elements are added, the number of collisions can increase, degrading performance. Hash maps dynamically resize (rehash) their underlying array when the "load factor" (number of elements / number of buckets) exceeds a certain threshold. This resizing operation can be $O(N)$ in the worst case (as all elements must be re-hashed and moved), but it's amortized $O(1)$ due to exponential growth.
  * **Unordered (Historically):** Traditionally, hash maps did not maintain insertion order. However, as of Python 3.7, standard `dict` objects preserve insertion order. While convenient, rely on this property cautiously in competitive programming unless explicitly stated or if order is a non-functional requirement. For interview problems, it's generally safer to assume a basic hash map is unordered unless you need the ordering guarantee, in which case a `collections.OrderedDict` might be explicitly mentioned.

**Practical Intuition:**
Imagine a large library where each book has a unique ID (key). Instead of searching every shelf, there's an index system (hash function). You plug in the book ID, and the index tells you exactly which shelf (bucket) and even which spot on that shelf to find it. If multiple books end up on the same shelf (collision), they are placed in sequence on that shelf, and you just quickly scan that specific shelf.

**Use Cases:**

  * **Frequency Counting:** Counting occurrences of items (e.g., characters in a string, words in a document).
  * **Caching/Memoization:** Storing results of expensive computations to avoid re-calculating them.
  * **Lookup Tables:** Mapping identifiers to objects (e.g., user IDs to user profiles, URLs to content).
  * **Graph Adjacency Lists:** Representing connections between nodes.
  * **Implementing Sets:** Sets are essentially hash maps where only keys are stored (values are usually null or a placeholder).

**Time and Space Complexity (Python `dict`):**

| Operation              | Average Time Complexity | Worst Case Time Complexity | Notes                                                              |
| :--------------------- | :---------------------- | :------------------------- | :----------------------------------------------------------------- |
| Insertion (`dict[key] = val`) | $O(1)$                  | $O(N)$                     | Due to potential resizing/re-hashing.                              |
| Deletion (`del dict[key]`) | $O(1)$                  | $O(N)$                     | Due to potential resizing/re-hashing.                              |
| Lookup (`dict[key]`)   | $O(1)$                  | $O(N)$                     | In case of severe hash collisions (e.g., malicious input).         |
| Checking Membership (`key in dict`) | $O(1)$                  | $O(N)$                     | Same as lookup.                                                    |
| Iteration              | $O(N)$                  | $O(N)$                     | Visiting each key-value pair once.                                 |

**Space Complexity:** $O(N)$ where $N$ is the number of key-value pairs. There's also some overhead for the underlying array and pointers/chains.

#### Python 3.11 Usage (`dict`, `defaultdict`, `Counter`)

Python's built-in `dict` is an extremely powerful and optimized hash map implementation. The `collections` module provides specialized dictionary-like classes that are very useful for competitive programming and general development.

```python
from collections import defaultdict, Counter

# --- Basic Dict Operations ---

# 1. Initialization
my_dict = {}  # Empty dictionary
user_ages = {"Alice": 30, "Bob": 24, "Charlie": 35}
print(f"Initialized dicts: {my_dict}, {user_ages}")

# 2. Accessing Values
print(f"Alice's age: {user_ages['Alice']}") # Output: 30
# print(user_ages['David']) # KeyError if key not found

# Using .get() for safe access (returns None or default value if key not found)
print(f"David's age (using get): {user_ages.get('David')}") # Output: None
print(f"Eve's age (using get with default): {user_ages.get('Eve', 25)}") # Output: 25

# 3. Adding/Updating Elements
user_ages['David'] = 40 # Add new key-value pair
user_ages['Alice'] = 31 # Update existing value
print(f"After adding/updating: {user_ages}") # Output: {'Alice': 31, 'Bob': 24, 'Charlie': 35, 'David': 40}

# 4. Removing Elements
del user_ages['Bob'] # Remove by key
print(f"After deleting Bob: {user_ages}") # Output: {'Alice': 31, 'Charlie': 35, 'David': 40}

popped_age = user_ages.pop('Charlie') # Removes and returns value by key
print(f"Popped Charlie's age ({popped_age}), dict now: {user_ages}") # Output: {'Alice': 31, 'David': 40}

# 5. Iteration
print("Iterating through keys:")
for name in user_ages: # Iterates through keys by default
    print(name)

print("Iterating through values:")
for age in user_ages.values():
    print(age)

print("Iterating through key-value pairs:")
for name, age in user_ages.items():
    print(f"{name} is {age} years old.")

# 6. Length
print(f"Number of users: {len(user_ages)}") # Output: 2

# 7. Checking Membership
print(f"'Alice' in user_ages: {'Alice' in user_ages}") # Output: True
print(f"'Bob' in user_ages: {'Bob' in user_ages}") # Output: False

# --- collections.defaultdict ---
# Automatically initializes a value for a key if it doesn't exist, using a factory function.
# Very useful for frequency counting or grouping.

# Example: Counting character frequencies
char_counts = defaultdict(int) # int() produces 0
s = "banana"
for char in s:
    char_counts[char] += 1
print(f"Char counts (defaultdict): {char_counts}") # Output: defaultdict(<class 'int'>, {'b': 1, 'a': 3, 'n': 2})

# Example: Grouping items
grouped_data = defaultdict(list) # list() produces []
data = [('apple', 1), ('banana', 2), ('apple', 3), ('orange', 4)]
for key, value in data:
    grouped_data[key].append(value)
print(f"Grouped data (defaultdict): {grouped_data}") # Output: defaultdict(<class 'list'>, {'apple': [1, 3], 'banana': [2], 'orange': [4]})

# --- collections.Counter ---
# A specialized dict subclass for counting hashable objects.
# Excellent for frequency problems.

# Example: Counting word frequencies
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
word_counts = Counter(words)
print(f"Word counts (Counter): {word_counts}") # Output: Counter({'apple': 3, 'banana': 2, 'orange': 1})

# Common Counter operations
print(f"Most common 2 words: {word_counts.most_common(2)}") # Output: [('apple', 3), ('banana', 2)]
print(f"Count of 'grape': {word_counts['grape']}") # Output: 0 (accesses non-existent keys as 0, like defaultdict(int))
```

**Best Practices:**

  * **`dict` is your go-to:** For most key-value mapping needs, the built-in `dict` is sufficient and highly optimized.
  * **`defaultdict` for frequency/grouping:** When you need to increment counts or append to lists for keys that might not yet exist, `defaultdict` simplifies the code and avoids `KeyError` checks.
  * **`Counter` for counting:** For pure frequency counting of hashable objects, `Counter` is the most concise and efficient.
  * **Hashable Keys:** Dictionary keys *must* be hashable. Immutable types like strings, numbers, and tuples are hashable. Mutable types like lists, sets, and other dictionaries are *not* hashable and cannot be used as keys.
  * **`get()` vs. `[]` for lookup:** Use `dict.get(key, default_value)` when you want to retrieve a value safely without raising a `KeyError` if the key isn't present. Use `dict[key]` when you expect the key to always be present or want to explicitly catch `KeyError`.

#### Problem-Solving Patterns

Hash maps are indispensable for many algorithmic problems, particularly those involving frequency, unique elements, or relationships between data points.

1.  **Frequency Counting:**

      * **Concept:** Use a hash map to store the count of occurrences of each item in a collection.
      * **Examples:** Anagrams, unique character string, finding the most frequent element.
      * **Pythonic Tools:** `collections.Counter` or `defaultdict(int)`.

2.  **Lookup/Existence Checks:**

      * **Concept:** Store elements in a hash map (or a hash set, which is just a hash map with dummy values) to quickly check for their presence.
      * **Examples:** Two Sum, checking for duplicates, finding intersection of two arrays.

3.  **Optimization (reducing time complexity):**

      * **Concept:** Hash maps can often reduce time complexity from $O(N^2)$ to $O(N)$ by providing $O(1)$ lookups. For example, instead of iterating through a list to find a complement for a sum, you can store seen numbers in a hash map and check for the complement directly.
      * **Examples:** Two Sum, Longest Substring Without Repeating Characters, Subarray Sum Equals K.

4.  **Memoization (Dynamic Programming/Recursion):**

      * **Concept:** Store the results of expensive function calls in a hash map (cache) so that subsequent calls with the same inputs can return the cached result immediately. This prevents redundant computations in recursive or dynamic programming solutions.
      * **Pythonic Tool:** `functools.lru_cache` decorator provides an easy way to add memoization.

#### Handling Large Inputs / Constraints

  * **Memory Usage:** While $O(N)$ space complexity is standard, for extremely large $N$ (e.g., $10^7$ unique items), a hash map can consume significant memory. Be aware of memory limits. Python dictionaries are relatively memory-efficient compared to some other language implementations, but they still have overhead per entry.
  * **Hash Collisions (Worst Case):** Though rare with Python's well-designed hash function, if keys are designed to cause many collisions (e.g., all keys hash to the same bucket), operations could degrade to $O(N)$ for individual lookups/insertions. This is usually not a concern for typical interview problems unless explicitly hinted at or if dealing with custom hash functions.
  * **Key Design:** For custom objects used as keys, ensure they are hashable (implement `__hash__` and `__eq__`).

#### Typical FAANG Problem Example

Let's look at a classic problem that leverages hash maps for optimization:

**Problem Description: "Longest Substring Without Repeating Characters"** (LeetCode Medium)

Given a string `s`, find the length of the longest substring without repeating characters.

**Constraints:**

  * $0 \\le len(s) \\le 5 \\times 10^4$
  * `s` consists of English letters, digits, symbols, and spaces.

**Thought Process & Hints:**

1.  **Understanding the Goal:** Find the longest contiguous sequence of characters where no character appears more than once.

2.  **Brute Force (and why it's bad):**

      * Generate all possible substrings. For each substring, check if it has repeating characters.
      * Generating substrings: $O(N^2)$ substrings.
      * Checking each substring: $O(N)$ for each substring (using a set/array).
      * Total Time Complexity: $O(N^3)$. Too slow for $N=5 \\times 10^4$.

3.  **Optimization - Sliding Window + Hash Map Intuition:**

      * This problem involves finding an optimal *subarray/substring*, which immediately suggests the **Sliding Window** pattern.
      * We need to keep track of characters seen within the *current window* to quickly detect repetitions. A hash map is perfect for this.
      * Maintain a window defined by `left` and `right` pointers.
      * Use a hash map (e.g., `char_index_map`) to store the *last seen index* of each character within the current window.

4.  **Algorithm Sketch:**

      * Initialize `max_length = 0`.
      * Initialize `left = 0` (start of the window).
      * Initialize an empty hash map `char_index_map` (key: character, value: its last seen index).
      * Iterate `right` from `0` to `len(s) - 1`:
          * Get `current_char = s[right]`.
          * **Check for Repetition:** If `current_char` is already in `char_index_map` AND its last seen index (`char_index_map[current_char]`) is *within the current window* (i.e., `char_index_map[current_char] >= left`):
              * This means we found a repeat. To make the window valid again (without repetitions), we must shrink the window from the left.
              * Move `left` to `char_index_map[current_char] + 1`. This effectively discards the repeated character and all characters before it from the window.
          * **Update Map:** Store the current index of `current_char` in the map: `char_index_map[current_char] = right`. This ensures we always have the *latest* position.
          * **Update Max Length:** The current window is `s[left : right+1]`. Its length is `right - left + 1`. Update `max_length = max(max_length, right - left + 1)`.
      * Return `max_length`.

5.  **Complexity Analysis of Optimized Solution:**

      * Time Complexity: $O(N)$ because both `left` and `right` pointers only move forward, and each character is processed at most twice (once by `right`, and potentially once by `left`). Hash map operations are $O(1)$ on average.
      * Space Complexity: $O(min(N, M))$ where $M$ is the size of the character set (e.g., 256 for ASCII). In the worst case, if all characters are unique, the map stores $N$ entries. If the character set is limited (like English alphabet), it's $O(1)$ space.

This problem beautifully showcases how a hash map, combined with the sliding window technique, can optimize a quadratic solution to a linear one.

#### System Design Relevance

  * **Distributed Caching:** Systems like Memcached or Redis are essentially distributed hash maps. Understanding collision resolution, consistent hashing (to distribute keys across nodes), and handling load factors is critical for designing scalable caches.
  * **Database Indexing:** B-trees are common for database indexes, but hash indexes are also used for exact key lookups, especially when fast retrieval is paramount and range queries are less common.
  * **Load Balancers:** Mapping incoming requests (keys) to available servers (values) often involves hash-based distribution to ensure even load.
  * **URL Shorteners:** Mapping a short code (key) to a long URL (value).
  * **Session Management:** Storing user session data (session ID as key, user data as value).
  * **DNS Resolution:** Mapping domain names to IP addresses.
  * **Feature Flags/Configuration:** Storing and retrieving application configurations or feature flag states.

**Challenge to the Reader:**
Consider the `Two Sum` problem. How would you solve it using a hash map to achieve $O(N)$ time complexity, and what would be the space complexity? Can you think of any edge cases where this approach might need careful handling (e.g., duplicate numbers in the input array)?