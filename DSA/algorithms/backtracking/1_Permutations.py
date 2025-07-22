from typing import List


def find_all_permutations(original_list: List[str]) -> List[List[str]]:
    result_list = []
    current_list = []
    used_list = [False] * len(
        original_list
    )  # Initialize a boolean array to track used numbers

    def backtrack(original_list, current_list, used_list, result_list):
        # Base Case: If the current permutation is complete
        if len(current_list) == len(original_list):
            result_list.append(list(current_list))  # Add a copy!
            return

        # Iterate through all possible choices
        for i in range(len(original_list)):
            # If the number at index i hasn't been used yet
            if not used_list[i]:
                # 1. Make a choice
                current_list.append(original_list[i])
                used_list[i] = True

                # 2. Recurse (explore further)
                backtrack(original_list, current_list, used_list, result_list)

                # 3. Unmake the choice (Backtrack)
                used_list[i] = False
                current_list.pop()

    # Initial call to start the backtracking process
    backtrack(original_list, current_list, used_list, result_list)
    return result_list


ls1 = ["A", "B", "C"]
print(find_all_permutations(ls1))
