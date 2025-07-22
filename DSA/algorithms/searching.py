ls = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
num_to_find = 17

def binary_search(ls: list[int], num: int) -> int:
    start = 0
    end = len(ls) - 1

    while start <= end:
        mid = (start + end) // 2

        if ls[mid] == num:
            return mid
        elif num < ls[mid]:
            end = mid - 1
        else:
            start = mid + 1

    return -1

print(binary_search(ls, num_to_find))