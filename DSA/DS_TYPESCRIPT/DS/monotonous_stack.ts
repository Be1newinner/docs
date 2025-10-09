const arr = [2, 1, 2, 4, 3];
const result = new Array(arr.length).fill(-1);

const stack: number[] = [];

for (let i = 0; i < arr.length; i++) {
    while (stack.length > 0 && arr[i] > arr[stack[stack.length - 1]]) {
        const idx = stack.pop();
        result[idx!] = arr[i];
    }
    stack.push(i);
}

console.log(result);