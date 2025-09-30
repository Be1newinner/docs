import { BSTNodeInterface, BSTInterface } from "./interfaces";

class TreeNode implements BSTNodeInterface {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;

  constructor(val: number) {
    this.val = val;
    this.left = null;
    this.right = null;
  }
}

class BST implements BSTInterface {
  root: TreeNode | null;

  constructor(val?: number) {
    this.root = val === undefined ? null : new TreeNode(val);
  }

  private _postorder(node: TreeNode, nodeVals: number[]) {
    if (node.left) this._postorder(node.left, nodeVals);
    if (node.right) this._postorder(node.right, nodeVals);
    nodeVals.push(node.val);
  }

  private _deleteNode(node: TreeNode | null, val: number): TreeNode | null {
    if (!node) {
      return null;
    }

    if (val < node.val) {
      node.left = this._deleteNode(node.left, val)
    } else if (val > node.val) {
      node.right = this._deleteNode(node.right, val)
    } else {
      if (!node.left) {
        return node.right;
      } else if (!node.right) {
        return node.left;
      } else {
        const minRight = this.findMin(node.right);
        node.val = minRight!.val;
        node.right = this._deleteNode(node.right, minRight!.val);
      }
    }

    return node;
  }


  private _search(node: TreeNode | null, val: number): boolean {
    if (node == null) return false;

    if (node.val === val) return true;

    if (val < node.val) return this._search(node.left, val)

    // Last condition i.e. when val > node.val
    return this._search(node.right, val)
  }

  public insert(val: number) {
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

  public preorder(): number[] {
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

  public inorder(): number[] {
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

  public postorder(): number[] {
    const nodeVals: number[] = [];

    if (!this.root) {
      return nodeVals;
    }

    this._postorder(this.root, nodeVals);
    return nodeVals;
  }

  public levelorder() {
    const result: number[] = []
    if (!this.root) return result;

    const queue: TreeNode[] = []
    queue.push(this.root);

    while (queue.length > 0) {
      const node = queue.shift()!;
      result.push(node?.val);

      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }

    return queue;
  }

  public delete(val: number): TreeNode | null {
    this.root = this._deleteNode(this.root, val)
    return this.root;
  }

  public search(val: number): boolean {
    return this._search(this.root, val)
  }

  public findMin(node: TreeNode): TreeNode | null {
    while (node.left != null) {
      node = node.left
    }
    return node
  }

  public findMax(node: TreeNode): TreeNode {
    while (node.right) {
      node = node.right
    }
    return node
  }

  public getHeight(node: TreeNode | null = this.root): number {
    if (node === null) return -1;
    const leftHeight = this.getHeight(node.left);
    const rightHeight = this.getHeight(node.right);
    return Math.max(leftHeight, rightHeight) + 1;
  }
  public isValidBST(node: TreeNode | null = this.root, min: number | null = null, max: number | null = null): boolean {
    if (node === null) return true;

    if ((min !== null && node.val <= min) || (max !== null && node.val >= max)) {
      return false;
    }

    if (!this.isValidBST(node.left, min, node.val)) return false;
    if (!this.isValidBST(node.right, node.val, max)) return false;

    return true;
  }

  public isEmpty(): boolean {
    return this.root === null
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
