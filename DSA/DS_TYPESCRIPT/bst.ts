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

class BST {
  root: TreeNode | null;

  constructor(val?: number) {
    this.root = val === undefined ? null : new TreeNode(val);
  }

  insert(val: number) {
    const node = new TreeNode(val);

    if (this.root === null) {
      this.root = node;
      return;
    }

    let curr: TreeNode | null = this.root;
    let parent: TreeNode = curr;

    while (curr != null) {
      parent = curr;

      if (val < curr.val) {
        curr = curr.left;
      } else if (val > curr.val) {
        curr = curr.right;
      } else {
        // skip dublicates!
        return;
      }
    }

    if (val < parent.val) {
      parent.left = node;
    } else {
      parent.right = node;
    }
  }

  preorder(): number[] {
    const nodeVals: number[] = [];

    if (!this.root) {
      return nodeVals;
    }

    function _preorder(node: TreeNode, nodeVals: number[]) {
      nodeVals.push(node.val);
      if (node.left) _preorder(node.left, nodeVals);
      if (node.right) _preorder(node.right, nodeVals);
    }

    _preorder(this.root, nodeVals);

    return nodeVals;
  }

  inorder(): number[] {
    const nodeVals: number[] = [];

    if (!this.root) {
      return nodeVals;
    }

    function _inorder(node: TreeNode, nodeVals: number[]) {
      if (node.left) _inorder(node.left, nodeVals);
      nodeVals.push(node.val);
      if (node.right) _inorder(node.right, nodeVals);
    }

    _inorder(this.root, nodeVals);

    return nodeVals;
  }

  postorder(): number[] {
    const nodeVals: number[] = [];

    if (!this.root) {
      return nodeVals;
    }

    function _postorder(node: TreeNode, nodeVals: number[]) {
      if (node.left) _postorder(node.left, nodeVals);
      if (node.right) _postorder(node.right, nodeVals);
      nodeVals.push(node.val);
    }

    _postorder(this.root, nodeVals);

    return nodeVals;
  }
}

const bst = new BST(5);
bst.insert(2);
bst.insert(4);
bst.insert(1);
bst.insert(9);
bst.insert(5);
bst.insert(3);

console.log(bst.preorder());
