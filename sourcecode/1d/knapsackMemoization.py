def knapsackMemoizationHelper(c, capacity, weights, values, n):
    if n == 0 or capacity == 0:
        return 0
    if c[n][capacity] != 0:
        return c[n][capacity]
    if weights[n-1] <= capacity:
        c[n][capacity] = max(values[n-1] + knapsackMemoizationHelper(c, capacity - weights[n-1], weights, values, n-1),
                                           knapsackMemoizationHelper(c, capacity               , weights, values, n-1))
    else:
        c[n][capacity] = knapsackMemoizationHelper(c, capacity, weights, values, n-1)
    return c[n][capacity]
    
def knapsackMemoization(capacity, weights, values, n):
    c = [[0 for i in range(0, capacity + 1)] for j in range(0, n + 1)]
    maxValue = knapsackMemoizationHelper(c, capacity, weights, values, n)
    maxWeight, selectedItems, i, j = 0, [], n, capacity
    while i > 0 and j > 0:
        if c[i][j] != c[i-1][j]:
            selectedItems.append(i)
            maxWeight += weights[i-1]
            j -= weights[i-1]
        i -= 1
    return maxValue, maxWeight, selectedItems