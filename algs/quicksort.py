def quicksort(arr: list[int]):
    if len(arr) < 2: return arr

    pivot_index = round(len(arr) // 2)
    pivot = arr[pivot_index]
    arr.pop(pivot_index)

    return quicksort([x for x in arr if x <= pivot]) + [pivot] + quicksort([x for x in arr if x > pivot])