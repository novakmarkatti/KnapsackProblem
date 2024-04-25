
from queue import PriorityQueue
class Node:
    def __init__(self, capacity, weight, value, level, selectedItems):
        self.capacity      = capacity
        self.weight        = weight
        self.value         = value
        self.level         = level
        self.selectedItems = selectedItems
        self.bound         = 0

    def __lt__(self, other):
        return self.bound > other.bound

    def include(self, items):
        weight        = self.weight        + items[1]
        value         = self.value         + items[2]
        level         = self.level         + 1
        selectedItems = self.selectedItems + [items[3] + 1]
        return Node(self.capacity, weight, value, level, selectedItems)

    def exclude(self): 
        return Node(self.capacity, self.weight, self.value, self.level + 1, self.selectedItems)
    
    def calculateBound(self, items):
        if self.weight >= self.capacity:
            return 0
        bound, totalWeight, i = self.value, self.weight, self.level
        while i < len(items) and (totalWeight + items[i][1]) <= self.capacity:
            totalWeight += items[i][1]
            bound       += items[i][2]
            i += 1
        if i < len(items):
            bound += (self.capacity - totalWeight) * (items[i][2] / items[i][1])
        return bound

############################################ alap modszer ######################################################### 

def knapsackBranchAndBound(capacity, weights, values, n):
    items = sorted([(values[i] / weights[i], weights[i], values[i], i) for i in range(0, n)], reverse=True)
    queue = PriorityQueue()
    root = Node(capacity, 0, 0, 0, [])
    root.bound = root.calculateBound(items)
    queue.put(root)
    maxValue, maxWeight, selectedItems = 0, 0, []

    while not queue.empty():
        node = queue.get()
        if node.bound > maxValue and node.level < n:
            level = node.level

            includeNode = node.include(items[level])
            if includeNode.weight <= capacity:
                if includeNode.value > maxValue:
                    maxValue, maxWeight, selectedItems = includeNode.value, includeNode.weight, includeNode.selectedItems
                includeNode.bound = includeNode.calculateBound(items)
                if includeNode.bound > maxValue:
                    queue.put(includeNode)

            excludeNode = node.exclude()
            excludeNode.bound = excludeNode.calculateBound(items)
            if excludeNode.bound > maxValue:
                queue.put(excludeNode)
    return maxValue, maxWeight, selectedItems

############################################### 1. modszer ######################################################

def knapsackBranchAndBound2(capacity, weights, values, n, nodePercentage=10):
    items = sorted([(values[i] / weights[i], weights[i], values[i], i) for i in range(0, n)], reverse=True)
    queue = PriorityQueue()
    root = Node(capacity, 0, 0, 0, [])
    root.bound = root.calculateBound(items)
    queue.put(root)
    maxValue, maxWeight, selectedItems = 0, 0, []
    processedNodes, maxNodes = 0, (2**n) * nodePercentage // 100
    while not queue.empty() and processedNodes < maxNodes:
        node = queue.get()
        processedNodes += 1
        if node.bound > maxValue and node.level < n:
            level = node.level

            includeNode = node.include(items[level])
            if includeNode.weight <= capacity:
                if includeNode.value > maxValue:
                    maxValue, maxWeight, selectedItems = includeNode.value, includeNode.weight, includeNode.selectedItems
                includeNode.bound = includeNode.calculateBound(items)
                if includeNode.bound > maxValue:
                    queue.put(includeNode)

            excludeNode = node.exclude()
            excludeNode.bound = excludeNode.calculateBound(items)
            if excludeNode.bound > maxValue:
                queue.put(excludeNode)
    return maxValue, maxWeight, selectedItems

################################################### 2. modszer ##################################################

def knapsackBranchAndBound3(capacity, weights, values, n):
    items = sorted([(values[i] / weights[i], weights[i], values[i], i) for i in range(0, n)], reverse=True)
    queue = PriorityQueue()
    root = Node(capacity, 0, 0, 0, [])
    root.bound = root.calculateBound(items)
    queue.put(root)
    maxValue, maxWeight, selectedItems = 0, 0, []

    while not queue.empty():
        node = queue.get()
        if node.bound < maxValue: 
            break
        if node.bound > maxValue and node.level < n:
            level = node.level
            includeNode = node.include(items[level])
            if includeNode.weight <= capacity:
                if includeNode.value > maxValue:
                    maxValue, maxWeight, selectedItems = includeNode.value, includeNode.weight, includeNode.selectedItems
                includeNode.bound = includeNode.calculateBound(items)
                if includeNode.bound > maxValue:
                    queue.put(includeNode)

            excludeNode = node.exclude()
            excludeNode.bound = excludeNode.calculateBound(items)
            if excludeNode.bound > maxValue:
                queue.put(excludeNode)
    return maxValue, maxWeight, selectedItems

################################################## 3. modszer ###################################################

def knapsackBranchAndBound4(capacity, weights, values, n, nodePercentage=10):
    items = sorted([(values[i] / weights[i], weights[i], values[i], i) for i in range(0, n)], reverse=True)
    queue = PriorityQueue()
    root = Node(capacity, 0, 0, 0, [])
    root.bound = root.calculateBound(items)
    queue.put(root)
    maxValue, maxWeight, selectedItems = 0, 0, []
    processedNodes, maxNodes = 0, (2**n) * nodePercentage // 100
    while not queue.empty() and processedNodes < maxNodes:
        node = queue.get()
        if node.bound < maxValue: 
            break
        processedNodes += 1
        if node.bound > maxValue and node.level < n:
            level = node.level

            includeNode = node.include(items[level])
            if includeNode.weight <= capacity:
                if includeNode.value > maxValue:
                    maxValue, maxWeight, selectedItems = includeNode.value, includeNode.weight, includeNode.selectedItems
                includeNode.bound = includeNode.calculateBound(items)
                if includeNode.bound > maxValue:
                    queue.put(includeNode)

            excludeNode = node.exclude()
            excludeNode.bound = excludeNode.calculateBound(items)
            if excludeNode.bound > maxValue:
                queue.put(excludeNode)
    return maxValue, maxWeight, selectedItems