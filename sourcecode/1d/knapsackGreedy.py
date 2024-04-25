
def knapsackGreedy(capacity, weights, values, n):
    maxValue, maxWeight, selectedItems = 0, 0, []
    p = [(values[i] / weights[i], i) for i in range(0, n)]  
    p.sort(reverse=True)
    for _, i in p:
        if maxWeight + weights[i] <= capacity: 
            selectedItems.append(i+1)
            maxValue  += values[i]
            maxWeight += weights[i]
    return maxValue, maxWeight, selectedItems