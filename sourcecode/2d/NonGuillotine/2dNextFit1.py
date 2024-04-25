class NonGuillotine:
    def __init__(self, width, height):
        self.width            = width
        self.height           = height
        self.placedRectangles = []
        self.maxValue         = 0
        self.lastX            = 0
        self.lastY            = 0
        self.rowHeight        = 0

    def canFitNew(self, width, height):
        if self.lastX + width <= self.width and self.lastY + height <= self.height:
            return (True, self.lastX, self.lastY)
        elif self.lastY + self.rowHeight + height <= self.height:
            self.lastX = 0
            self.lastY += self.rowHeight
            self.rowHeight = height
            return (True, self.lastX, self.lastY)
        return (False, -1, -1)
    
    def placeRectangle(self, index, width, height, value):
        canFit, x, y = self.canFitNew(width, height)
        if canFit:
            self.placedRectangles.append((index + 1, x, y, width, height))
            self.maxValue += value
            self.lastX    += width
            self.rowHeight = max(self.rowHeight, height)
        return canFit

def nonGuillotineCut(rectangles, containerWidth, containerHeight):
    nonGuillotine = NonGuillotine(containerWidth, containerHeight)
    sortedRectangles = sorted(enumerate(rectangles), key=lambda value: value[1][2], reverse=True)
    for index, (width, height, value) in sortedRectangles:
        nonGuillotine.placeRectangle(index, width, height, value)
    return nonGuillotine.placedRectangles, nonGuillotine.maxValue