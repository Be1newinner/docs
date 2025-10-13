### 16\. Bit Manipulation

Bit manipulation involves operating on integers at the bit level. It's often used for optimizing performance, solving problems with bitmasking, and handling specific data encoding challenges. A strong understanding of binary representation is fundamental.

#### Core Concepts

Integers are stored in memory as a sequence of bits (binary digits, 0s and 1s). Bitwise operations directly manipulate these individual bits.

**Python's Bitwise Operators:**

1.  **Bitwise AND (`&`)**:

      * Sets each bit to 1 if both corresponding bits are 1.
      * **Use Cases:** Checking if a bit is set, clearing a bit, masking (isolating) specific bits.
      * `A & B`: `1010 & 1100 = 1000` (8 & 12 = 8)

2.  **Bitwise OR (`|`)**:

      * Sets each bit to 1 if at least one of the corresponding bits is 1.
      * **Use Cases:** Setting a bit, combining flags.
      * `A | B`: `1010 | 1100 = 1110` (8 | 12 = 14)

3.  **Bitwise XOR (`^`)**:

      * Sets each bit to 1 if the corresponding bits are different (one is 0 and the other is 1).
      * **Properties:** `A ^ A = 0`, `A ^ 0 = A`, `A ^ B ^ A = B`. Commutative and associative.
      * **Use Cases:** Toggling a bit, finding the single unique element, swapping numbers without a temporary variable.
      * `A ^ B`: `1010 ^ 1100 = 0110` (8 ^ 12 = 6)

4.  **Bitwise NOT (`~`)**:

      * Inverts all the bits (0 becomes 1, 1 becomes 0).
      * **Note in Python:** This is not a simple bit inversion. Python integers have arbitrary precision and are signed (using two's complement internally for negative numbers). `~x` is equivalent to `-(x+1)`.
      * **Use Cases:** Less common directly in competitive programming for simple inversion due to Python's handling, but conceptually useful.
      * `~A`: `~10` (binary `...00001010`) would be `...11110101`. In Python, `~10` is `-11`.

5.  **Left Shift (`<<`)**:

      * Shifts bits to the left by a specified number of positions. Vacated positions are filled with 0s.
      * **Effect:** `x << n` is equivalent to `x * (2**n)`.
      * **Use Cases:** Multiplying by powers of 2, creating bitmasks `(1 << n)` to represent the `n`-th bit.
      * `A << n`: `1010 << 1 = 10100` (10 \<\< 1 = 20)

6.  **Right Shift (`>>`)**:

      * Shifts bits to the right by a specified number of positions. Vacated positions (on the left) are filled with 0s for non-negative numbers (logical right shift). For negative numbers, it's an arithmetic right shift (fills with 1s to preserve sign).
      * **Effect:** `x >> n` is equivalent to `x // (2**n)` (integer division, rounds down).
      * **Use Cases:** Dividing by powers of 2, extracting individual bits (by shifting to position 0 and ANDing with 1).
      * `A >> n`: `1010 >> 1 = 0101` (10 \>\> 1 = 5)

#### Practical Applications and Intuition

1.  **Checking if a number is a power of 2:**

      * A number `N` is a power of 2 if and only if `N > 0` and `(N & (N - 1)) == 0`.
      * Intuition: Powers of 2 in binary have only one bit set (e.g., 4 is `100`, 8 is `1000`). `N-1` will have all bits to the right of the set bit as 1s, and that set bit as 0 (e.g., `100 - 1 = 011`). ANDing them gives 0.
      * `8 (1000) & 7 (0111) = 0`

2.  **Checking if a number is even or odd:**

      * `(N & 1) == 0` for even numbers.
      * `(N & 1) == 1` for odd numbers.
      * Intuition: The least significant bit (LSB) determines parity.

3.  **Setting a bit (turning a bit ON):**

      * To set the `i`-th bit (0-indexed) of `N`: `N = N | (1 << i)`
      * `1 << i` creates a mask with only the `i`-th bit set. ORing with this mask sets that bit in `N`.

4.  **Clearing a bit (turning a bit OFF):**

      * To clear the `i`-th bit of `N`: `N = N & ~(1 << i)`
      * `~(1 << i)` creates a mask with all bits set except the `i`-th bit. ANDing with this mask clears the `i`-th bit.

5.  **Toggling a bit:**

      * To toggle the `i`-th bit of `N`: `N = N ^ (1 << i)`
      * XORing with a mask where only the `i`-th bit is set will flip the `i`-th bit in `N` (0 to 1, 1 to 0).

6.  **Checking if the `i`-th bit is set:**

      * `(N >> i) & 1 == 1` (Shift `i`-th bit to LSB, then check LSB)
      * `N & (1 << i) != 0` (AND with mask, if non-zero, it was set)

7.  **Counting Set Bits (Hamming Weight):**

      * **Brian Kernighan's Algorithm:** `N = N & (N - 1)` repeatedly clears the least significant set bit. Count how many times this operation is performed until `N` becomes 0.
      * **Python `bin().count('1')`:** Easiest for interview, but know the bitwise approach.

8.  **Bitmasks for Sets/States:**

      * An integer can represent a subset of items or a state in a problem.
      * If you have `N` items (e.g., $N \\le 20$), each item can be represented by a bit position.
      * `1 << i` represents the `i`-th item.
      * A number `mask` where `i`-th bit is set means `i`-th item is in the subset.
      * This is common in Dynamic Programming (Bitmask DP), graph problems (e.g., TSP variants), or problems requiring tracking subsets.

#### Python 3.11 Implementations & Idioms

Python handles arbitrary-precision integers, so you don't need to worry about fixed-size integer overflows as in C++/Java. This simplifies some things but `~` behavior is important.

```python
# --- Bitwise Operations Examples ---

num = 42 # Binary: 0010 1010

# 1. Check if a bit is set (e.g., 5th bit, 0-indexed)
# Is 5th bit (value 32) set? Yes.
bit_pos = 5
mask = (1 << bit_pos) # 1 << 5 = 32 (0010 0000)
is_set = (num & mask) != 0
print(f"Is {bit_pos}-th bit of {num} set? {is_set} (mask: {bin(mask)})") # Output: True

# Another way to check: right shift and AND with 1
is_set_shifted = (num >> bit_pos) & 1 == 1
print(f"Is {bit_pos}-th bit of {num} set (shifted)? {is_set_shifted}") # Output: True

# 2. Set a bit (e.g., 1st bit, 0-indexed)
# num = 0010 1010 (42) -> set 1st bit -> 0010 1011 (43)
new_num = num | (1 << 0)
print(f"Set 0-th bit of {num}: {new_num} ({bin(num)} | {bin(1 << 0)} = {bin(new_num)})") # Output: 43

# 3. Clear a bit (e.g., 3rd bit, 0-indexed)
# num = 0010 1010 (42) -> clear 3rd bit -> 0010 0010 (34)
new_num = num & ~(1 << 3)
print(f"Clear 3rd bit of {num}: {new_num} ({bin(num)} & {bin(~(1 << 3))} = {bin(new_num)})") # Output: 34

# 4. Toggle a bit (e.g., 2nd bit)
# num = 0010 1010 (42) -> toggle 2nd bit -> 0010 1110 (46)
new_num = num ^ (1 << 2)
print(f"Toggle 2nd bit of {num}: {new_num} ({bin(num)} ^ {bin(1 << 2)} = {bin(new_num)})") # Output: 46

# 5. Check if power of 2
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

print(f"Is 16 a power of 2? {is_power_of_two(16)}") # Output: True
print(f"Is 15 a power of 2? {is_power_of_two(15)}") # Output: False

# 6. Count set bits (Hamming Weight)
def count_set_bits(n):
    count = 0
    while n > 0:
        n &= (n - 1) # Clears the least significant set bit
        count += 1
    return count

print(f"Set bits in {42} ({bin(42)}): {count_set_bits(42)}") # Output: 3 (101010 has three 1s)
print(f"Set bits in {15} ({bin(15)}): {count_set_bits(15)}") # Output: 4 (00001111 has four 1s)
# Python's built-in:
print(f"Set bits in {42} (built-in): {bin(42).count('1')}")
```

#### Handling Large Inputs / Constraints

  * **Bitmask DP:** As mentioned, if a problem involves subsets of items and $N$ is small (typically up to 20-22, as $2^{20}$ is about 1 million), you can use an integer bitmask to represent states.
      * A state `dp[mask]` could store the result for the subset represented by `mask`.
      * Transitions involve iterating through set bits in `mask` or adding/removing bits.
      * Example: TSP (Traveling Salesperson Problem) variants where `dp[mask][last_node]` represents the minimum cost to visit all nodes in `mask` ending at `last_node`.
  * **Space Optimization:** Bitsets or bit arrays can pack boolean flags efficiently, saving memory when you have many boolean values. In Python, this is less critical due to high-level data structures, but the concept is relevant.
  * **Performance:** Bitwise operations are generally very fast, as they are often directly supported by CPU instructions. This can give a constant factor speedup compared to arithmetic operations or array lookups.

#### Typical FAANG Problem Example

Let's look at a problem where XOR is the key.

**Problem Description: "Single Number"** (LeetCode Easy)

Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.

**Example:**
Input: `nums = [2,2,1]`
Output: `1`

Input: `nums = [4,1,2,1,2]`
Output: `4`

**Constraints:**

  * `1 <= nums.length <= 3 * 10^4`
  * `-3 * 10^4 <= nums[i] <= 3 * 10^4`
  * Each element in the array appears twice except for one element which appears once.

**Thought Process & Hints:**

1.  **Understanding the Goal:** Find the unique element in an array where all other elements appear exactly twice. Constraints are tight: linear time ($O(N)$) and constant space ($O(1)$).

2.  **Initial Thoughts (and why they might fail constraints):**

      * **Hash Map/Set:** Iterate, store counts/seen elements. If count is 1 or seen once, that's the one.
          * Time: $O(N)$
          * Space: $O(N)$ (fails constant space constraint)
      * **Sorting:** Sort the array. Iterate and find the element not equal to its neighbors.
          * Time: $O(N \\log N)$ (fails linear time constraint)
          * Space: $O(1)$ if in-place sort, $O(N)$ if new list (depends on language/sort)

3.  **The Role of XOR (`^`):**

      * Recall XOR properties:
          * `A ^ 0 = A` (XOR with zero is identity)
          * `A ^ A = 0` (XOR with self cancels out)
          * `A ^ B ^ A = (A ^ A) ^ B = 0 ^ B = B` (XOR is commutative and associative)
      * This is the crucial insight\! If we XOR all elements in the array:
          * Every number that appears twice will effectively cancel itself out (`X ^ X = 0`).
          * The single unique number will be XORed with `0` (from all the pairs canceling out), resulting in itself.

4.  **Algorithm Sketch:**

      * Initialize a variable `single_number = 0`.
      * Iterate through each `num` in `nums`:
          * `single_number = single_number ^ num`
      * Return `single_number`.

5.  **Example Walkthrough (`nums = [4,1,2,1,2]`)**

      * `single_number = 0`
      * `num = 4`: `single_number = 0 ^ 4 = 4`
      * `num = 1`: `single_number = 4 ^ 1`
      * `num = 2`: `single_number = (4 ^ 1) ^ 2`
      * `num = 1`: `single_number = (4 ^ 1 ^ 2) ^ 1 = 4 ^ (1 ^ 1) ^ 2 = 4 ^ 0 ^ 2 = 4 ^ 2`
      * `num = 2`: `single_number = (4 ^ 2) ^ 2 = 4 ^ (2 ^ 2) = 4 ^ 0 = 4`
      * Result: `4`

6.  **Complexity Analysis:**

      * Time Complexity: $O(N)$ because we iterate through the array once.
      * Space Complexity: $O(1)$ because we only use a single variable `single_number`.

This is a quintessential example of how understanding bitwise properties can lead to an elegant and optimal solution that meets strict constraints.

#### System Design Relevance

While bit manipulation isn't typically a high-level component in system design, it's fundamental in low-level optimizations and specific domains:

  * **Networking Protocols:** Often rely on bit-level manipulation for headers, checksums, and flags (e.g., TCP/IP headers).
  * **Graphics and Image Processing:** Manipulating pixels (which are often represented as integers with packed color components) involves bitwise operations.
  * **Operating Systems:** Memory management, device drivers, and low-level system calls often use bitwise flags and masks to manage hardware registers and system states efficiently.
  * **Embedded Systems:** Resource-constrained environments frequently use bit manipulation for efficient control of hardware, status flags, and data packing.
  * **Data Serialization/Deserialization:** Packing and unpacking data into compact binary formats.
  * **Hash Functions:** Some components of cryptographic hash functions or simple hash functions use bitwise operations for mixing bits.

**Challenge to the Reader:**
Consider the "Counting Bits" problem (LeetCode Medium). Given a non-negative integer `n`, for every integer `i` in the range `[0, n]`, calculate the number of 1's in their binary representation and return them as an array. Can you solve this efficiently in $O(N)$ time, avoiding the $O(N \\log N)$ naive approach? (Hint: Think about how `dp[i]` relates to `dp[i & (i-1)]` or `dp[i >> 1]`).