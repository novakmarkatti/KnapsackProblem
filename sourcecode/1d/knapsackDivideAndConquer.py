def knapsackDivideAndConquer(capacity, weights, values, n):
    if n == 0 or capacity == 0:
        return 0, 0, []
    if weights[n-1] > capacity:
        return knapsackDivideAndConquer(capacity, weights, values, n-1)

    includeValue, includeWeight, includeItems = knapsackDivideAndConquer(capacity - weights[n-1], weights, values, n-1)
    includeValue  += values[n-1]
    includeWeight += weights[n-1]
    includeItems.append(n)

    excludeValue, excludeWeight, excludeItems = knapsackDivideAndConquer(capacity, weights, values, n-1)
    
    if includeValue > excludeValue:
        return includeValue, includeWeight, includeItems
    else:
        return excludeValue, excludeWeight, excludeItems