import time
import math

start = time.time()

list = [10,15,16,18,19, 25, 37, 41, 45, 48, 56, 61, 67, 71, 73, 77, 79, 81, 83, 87, 89, 91, 10,15,16,18,19, 25, 37, 41, 45, 48, 56, 61, 67, 71, 73, 77, 79, 81, 83, 87, 89, 91, 10,15,16,18,19, 25, 37, 41, 45, 48, 56, 61, 67, 71, 73, 77, 79, 81, 83, 87, 89, 91, 10,15,16,18,19, 25, 37, 41, 45, 48, 56, 61, 67, 71, 73, 77, 79, 81, 83, 87, 89, 91]

def indicesOf(arr, target):
    lookup = {}
    for i in range(len(arr)):
        complement = target - arr[i]
        if complement in lookup:
            return [lookup[complement], i]
        lookup[arr[i]] = i
    return []
                    

for i in range(1000):    
  data = indicesOf(list,180)
  print(data)

end = time.time()
 
print("The time of execution of above program is :",
      math.ceil((end-start) * 10**6) / 10**3, "ms")