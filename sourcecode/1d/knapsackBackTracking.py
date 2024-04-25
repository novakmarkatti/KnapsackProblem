def knapsackBacktrackGreedy(capacity, weights, values, n):
    maxValue, maxWeight, selectedItems = 0, 0, []
    p = [(values[i] / weights[i], i) for i in range(0, n)]  
    p.sort(reverse=True)
    for _, i in p:
        if maxWeight + weights[i] <= capacity: 
            selectedItems.append(i + 1)
            maxValue  += values[i]
            maxWeight += weights[i]
        elif len(selectedItems) > 0:
            index = selectedItems.pop()
            maxValue  -= values[index - 1]
            maxWeight -= weights[index - 1]
    return maxValue, maxWeight, selectedItems


def knapsackBacktrack(capacity, weights, values, n):
    maxValue, maxWeight, selectedItems = -1, -1, []
    
    def backtrackHelper(i, actualWeight, actualValue, actualSelectedItems):
        nonlocal maxValue, maxWeight, selectedItems
        if actualWeight > capacity: 
            return
        if actualValue > maxValue:
            maxValue, maxWeight, selectedItems = actualValue, actualWeight, actualSelectedItems.copy()
        if i == n:
            return
        
        actualSelectedItems.append(i + 1)
        backtrackHelper(i + 1, actualWeight + weights[i], actualValue + values[i], actualSelectedItems)
        actualSelectedItems.pop()

        backtrackHelper(i + 1, actualWeight             , actualValue            , actualSelectedItems)

    backtrackHelper(0, 0, 0, [])
    return maxValue, maxWeight, selectedItems