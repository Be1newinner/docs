const input = [[1,3], [2,6], [15,18], [8,10]]
// output = [[1,6], [8,10], [15,18]]

function bruteForce(data: [number, number][]){
  const sortedData = data.toSorted((a,b)=>a[1] - b[1]);
  return sortedData; 
}


console.log(bruteForce(input))