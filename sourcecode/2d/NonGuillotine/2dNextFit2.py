class NonGuillotine:
    def __init__(self, width, height):
        self.width            = width
        self.height           = height
        self.placedRectangles = []
        self.maxValue         = 0
        self.currentRowY      = 0
        self.currentRowHeight = 0
        self.lastX            = 0

    def canFitInNextRow(self, height):
        if self.currentRowY + self.currentRowHeight + height <= self.height:
            self.currentRowY += self.currentRowHeight
            self.currentRowHeight = height
            self.lastX = 0
            return (True, self.lastX, self.currentRowY)
        return (False, -1, -1)
    
    def canFitInCurrentRow(self, width, height):
        if self.lastX + width <= self.width and self.currentRowY + height <= self.height:
            return (True, self.lastX, self.currentRowY)
        return (False, -1, -1)
    
    def placeRectangle(self, x, y, index, width, height, value):
        self.placedRectangles.append((index+1, x, y, width, height))
        self.maxValue += value
        self.lastX += width
        self.currentRowHeight = max(self.currentRowHeight, height)
    
def nonGuillotineCut(rectangles, containerWidth, containerHeight):
    nonGuillotine = NonGuillotine(containerWidth, containerHeight)
    sortedRectangles = sorted(enumerate(rectangles), key=lambda value: value[1][2], reverse=True)
    rectanglePlaceable = [1 for _ in range(0, len(rectangles))]
    actualRow, nextRow = True, False
    while actualRow or nextRow:

        for rectangle in sortedRectangles:
            index = sortedRectangles.index( rectangle ) 
            canFit, x, y = nonGuillotine.canFitInCurrentRow(rectangle[1][0], rectangle[1][1])
            if canFit:
                nonGuillotine.placeRectangle(x, y, rectangle[0], rectangle[1][0], rectangle[1][1], rectangle[1][2])
                sortedRectangles.pop(index)
                rectanglePlaceable.pop(index)
                break
            else:
                rectanglePlaceable[index] = 0

        if sum(rectanglePlaceable) == 0:
            rectanglePlaceable = [1 for _ in range(0, len(sortedRectangles))]
            for rectangle in sortedRectangles:
                index = sortedRectangles.index( rectangle ) 
                canFit, x, y = nonGuillotine.canFitInNextRow(rectangle[1][1])
                if canFit:
                    nonGuillotine.placeRectangle(x, y, rectangle[0], rectangle[1][0], rectangle[1][1], rectangle[1][2])
                    sortedRectangles.pop(index)
                    rectanglePlaceable.pop(index)
                    break
                else:
                    rectanglePlaceable[index] = 0
            if sum(rectanglePlaceable) == 0:
                actualRow, nextRow = False, False  
            else:     
                actualRow, nextRow = True, False       
    return nonGuillotine.placedRectangles, nonGuillotine.maxValue