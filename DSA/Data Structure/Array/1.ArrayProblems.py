# Extras ----------------------------------

'''
# Reverse the array

'''

def reverse(arr, start, end):
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1

'''
🧪 Problem 1: Rotate Array by k Positions (Right)
Input: arr = [1, 2, 3, 4, 5, 6, 7], k = 3
Output: [5, 6, 7, 1, 2, 3, 4]
'''

# When space is enough => O(n) , Time = O(n)
# but only one loop

# def move(arr, k):
#     right_arr = []
#     left_arr = []
#     for x in range(len(arr)):
#         if(len(arr) - x - 1 >= k):
#             right_arr.append(arr[x])
#         else:
#             left_arr.append(arr[x])
#     return left_arr + right_arr

# When space is limited or in-place operation is required!

def rotate_right(arr, k):
    n = len(arr)
    k = k % n

    reverse(arr, 0, n - 1)
    reverse(arr, 0, k - 1)
    reverse(arr, k, n - 1)

    return arr

arr = [1, 2, 3, 4, 5, 6, 7]
k = 3  

rotate_right(arr, k)

print(arr)

'''
🧪 Problem 2: Move All Zeroes to End
Input: [0,1,0,3,12]
Output: [1,3,12,0,0]
'''

# def moveZeroes(arr):
#     temp = arr.copy()
#     if(len(arr) == 0):
#         return []
    
#     zeroes = 0
#     counts = range(len(arr))
#     for x in counts:
#         if(arr[x] == 0):
#             zeroes += 1
#             temp.pop(x + 1 - zeroes)
            
#     return temp + [0 for x in range(zeroes)]


# print(moveZeroes([0,1,0,3,12]))