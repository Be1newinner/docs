// This pattern is about finding the most frequent or largest/smallest K elements in a collection, which is very common in coding interviews.

// ### Why use the Top K Elements Pattern?
// - Efficiently answers "What are the top K ...?" questions.
// - Helps when full sorting is unnecessary and costly.
// - Common in recommendations, search engines, and data analytics.

// ### Benefits:
// - Avoids expensive full sorting when you only need k results.
// - Optimized approaches (like heaps) can reduce runtime.

// ### Time Complexity:
// - Using a Min Heap or Max Heap approach generally gives $$O(n \log k)$$ time, where $$n$$ is number of elements.
// - Sorting the entire array is $$O(n \log n)$$, so heap-based is better when $$k \ll n$$.

// Interview Question: Top K Frequent Elements
// Problem:
// Given a non-empty integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

// Example:
// Input: nums = [1][1][1][2][2][3], k = 2
// Output: [1][2]

function topKFrequent2(nums: number[], k: number): number[] {
    // Step 1: Frequency Map - Count frequency of each element
    const frequencyMap: Map<number, number> = new Map();
    for (const num of nums) {
        frequencyMap.set(num, (frequencyMap.get(num) || 0) + 1);
    }

    // Step 2: Create array of [num, frequency] pairs
    const freqArray: [number, number][] = Array.from(frequencyMap.entries());

    // Step 3: Sort the freqArray by frequency in descending order
    freqArray.sort((a, b) => b[1] - a[1]);

    // Step 4: Extract top k elements
    const result: number[] = [];
    for (let i = 0; i < k; i++) {
        result.push(freqArray[i][0]);
    }

    return result;
}


`
Interview Question: Top K Frequent Characters in a String
Problem Statement:
Given a string s and an integer k, find the k most frequent characters in the string. Return the characters in any order.

Example:
Input: s = "aabbbccde", k = 3
Output: ["b", "a", "c"]

Note:

The order of the output characters does not matter.
Characters could be repeated; only return unique characters.
Sample Solution Approach:
a. Count the frequency of each character using a hash map.
b. Use a max-heap or min-heap (depending on approach) to keep track of top k characters based on frequency.
c. Extract the top k characters and return them.
`
function topKFrequentChars(s: string, k: number): string[] {
    // Step 1: Frequency Map - Count each character's frequency
    const freqMap: Map<string, number> = new Map();
    for (const char of s) {
        freqMap.set(char, (freqMap.get(char) || 0) + 1);
    }

    // Step 2: Convert map entries to array of [char, freq]
    const freqArray: [string, number][] = Array.from(freqMap.entries());

    // Step 3: Sort array by frequency descending
    freqArray.sort((a, b) => b[1] - a[1]);

    // Step 4: Extract top k characters
    const result: string[] = [];
    for (let i = 0; i < k; i++) {
        result.push(freqArray[i][0]);
    }

    return result;
}

