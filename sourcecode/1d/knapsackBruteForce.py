def knapsackBruteForce(capacity, weights, values, n):
    maxValue, maxWeight, selectedItems = 0, 0, []
    for i in range(0, 2**n):
        actualValue, actualWeight, actualSelectedItems = 0, 0, []
        for j in range(0, n):
            if (i >> j) & 1:
                actualSelectedItems.append(j+1)
                actualWeight += weights[j]
                actualValue  += values[j]     
        if actualWeight <= capacity and actualValue > maxValue:
            maxValue, maxWeight, selectedItems = actualValue, actualWeight, actualSelectedItems
    return maxValue, maxWeight, selectedItems