# Binary Search Algorithm Implementation

# Function to perform binary search
def binary_search(arr, target):
    # Initialize low and high pointers
    low = 0
    high = len(arr) - 1

    # Continue searching until low is less than or equal to high
    while low <= high:
        # Calculate mid index
        mid = (low + high) // 2

        # If target is found at mid index, return mid
        if arr[mid] == target:
            return mid
        # If target is less than arr[mid], update high to mid - 1
        elif arr[mid] > target:
            high = mid - 1
        # If target is greater than arr[mid], update low to mid + 1
        else:
            low = mid + 1

    # If target is not found, return -1
    return -1

# Example usage
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23

# Perform binary search
result = binary_search(arr, target)

# Print result
print("Target found at index:", result)