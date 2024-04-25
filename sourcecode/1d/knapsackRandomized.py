import random

def knapsackRandomized(capacity, weights, values, n, maxIteration=50):
    maxValue, maxWeight, selectedItems = 0, 0, []
    for _ in range(0, maxIteration):
        acceptable = False
        while not acceptable:
            tempMaxValue, tempMaxWeight, tempSelectedItems = 0, 0, []
            for i in range(0, n):
                item = random.choice([0, 1])
                tempSelectedItems.append(item)
                if item == 1:
                    tempMaxWeight += weights[i]
                    tempMaxValue  += values[i]
                if tempMaxWeight > capacity: 
                    break   
            if tempMaxWeight <= capacity:
                acceptable = True
                if tempMaxValue > maxValue:
                    maxValue, maxWeight, selectedItems = tempMaxValue, tempMaxWeight, tempSelectedItems
    selectedItems = [i+1 for i, item in enumerate(selectedItems) if item == 1]                
    return maxValue, maxWeight, selectedItems