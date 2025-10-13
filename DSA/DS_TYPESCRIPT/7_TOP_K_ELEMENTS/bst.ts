`
Given the root of a binary search tree and an integer k, return the kth largest value in the BST.
Step-by-Step Collection of Top 3 Largest Elements

           11
         /    \
       6       16
     /  \    /    \
    3    9  14    19
   / \  / \ / \   /  \
  2  5 8 10 13 15 18 20
 /      /      /     /
1      12     17    -

`

class TreeNode {
    val: number;
    left: TreeNode | null;
    right: TreeNode | null;
    constructor(val: number) {
        this.val = val;
        this.left = null;
        this.right = null;
    }
}

function topKLargestInBST(root: TreeNode | null, k: number): number[] {
    const result: number[] = [];
    function reverseInorder(node: TreeNode | null) {
        if (!node || result.length >= k) return;
        reverseInorder(node.right);
        if (result.length < k) {
            result.push(node.val);
            reverseInorder(node.left);
        }
    }
    reverseInorder(root);
    return result;
}
