import random

def randomPlacedRectangles(rectangles, containerWidth, containerHeight, maxAttempts):
    placedRectangles, maxValue = [], 0
    random.shuffle(rectangles)
    for (index, (width, height, value)) in rectangles:
        for _ in range(0, maxAttempts): 
            i = random.randint(0, containerWidth  - width)
            j = random.randint(0, containerHeight - height)
            canFit = True
            for (_, x, y, w, h) in placedRectangles:
                if not(i + width <= x or i >= x + w or j + height <= y or j >= y + h):
                    canFit = False
                    break
            if canFit:
                placedRectangles.append((index + 1, i, j, width, height))
                maxValue += value
                break  
    return placedRectangles, maxValue

def nonGuillotineRandom(rectangles, containerWidth, containerHeight, maxIteration=100, maxAttempts=50):
    placedRectangles, maxValue = [], -1
    rectangles = [(i, rectangle) for i, rectangle in enumerate(rectangles)]
    for _ in range(0, maxIteration):
        tempPlacedRectangles, tempMaxValue = randomPlacedRectangles(rectangles, containerWidth, containerHeight, maxAttempts)
        if tempMaxValue > maxValue:
            placedRectangles, maxValue = tempPlacedRectangles, tempMaxValue
    return placedRectangles, maxValue