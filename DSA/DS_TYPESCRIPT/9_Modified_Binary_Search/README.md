# Modified Binary Search Pattern Explained

Modified Binary Search is an enhanced version of classic binary search designed to work efficiently on rotated sorted arrays or special sorted arrays where the normal sorted order is disrupted.

## What is Modified Binary Search?

It is a tweak of classic binary search that adjusts how the mid-point check is performed to handle cases where the array is rotated or partially sorted.

## Why Do We Need It?

Classic binary search only works on strictly sorted arrays. If the array has been rotated — meaning a sorted array has been “shifted” at some pivot — the normal binary search approach fails. Modified binary search finds which half is properly sorted and uses that to decide where to search next.

## How Does It Work?

- Calculate the middle index.
- Check if the left half from start to mid is sorted:
  - If yes, check if the target lies within this sorted half. If it does, search left; otherwise, search right.
- Otherwise, the right half from mid to end must be sorted:
  - Check if the target lies there; if yes, search right; else search left.
- Repeat until the target is found or search space is exhausted.

## Key Insight

At any step, **one half is always sorted** despite the rotation. By identifying which half is sorted and whether the target can lie there, you eliminate half the search space each time—retaining logarithmic complexity.
