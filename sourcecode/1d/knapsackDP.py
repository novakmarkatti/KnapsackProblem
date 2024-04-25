def knapsackDP(capacity, w, v, n):  
    c = [[0 for i in range(0, capacity + 1)] for j in range(0, n + 1)] 
    for i in range(0, n + 1):
        for j in range(0, capacity + 1):
            if i == 0 or j == 0:
                c[i][j] = 0
            elif w[i-1] <= j:
                c[i][j] = max(c[i-1][j], v[i-1] + c[i-1][j - w[i-1]])
            else:
                c[i][j] = c[i-1][j]
    i, j, maxWeight, selectedItems = n, capacity, 0, []
    while i > 0 and j > 0:
        if c[i][j] != c[i-1][j]:
            selectedItems.append(i)
            maxWeight += w[i-1]
            j -= w[i-1]
        i -= 1
    return c[n][capacity], maxWeight, selectedItems