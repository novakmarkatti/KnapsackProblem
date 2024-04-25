class NonGuillotine:
    def __init__(self, width, height):
        self.width            = width
        self.height           = height
        self.placedRectangles = []
        self.maxValue         = 0

    def placeRectangle(self, index, width, height, value):
        for (i, j) in leftToRightThenBottomToTop(self.width, self.height, width, height):
            canFit = True
            for (_, x, y, w, h) in self.placedRectangles:
                if not(i + width <= x or i >= x + w or j + height <= y or j >= y + h):
                    canFit = False
                    break
            if canFit:
                self.placedRectangles.append((index + 1, i, j, width, height))
                self.maxValue += value
                return True
        return False

def leftToRightThenBottomToTop(width, height, itemWidth, itemHeight):
    for j in range(0, height - itemHeight + 1):     
        for i in range(0, width - itemWidth + 1): 
            yield i, j

def bottomToTopThenLeftToRight(width, height, itemWidth, itemHeight):
    for i in range(0, width - itemWidth + 1): 
        for j in range(0, height - itemHeight + 1): 
            yield i, j

def spiralCoordinates(width, height, itemWidth, itemHeight):
    level = 0
    while level <= max(width - itemWidth, height - itemHeight):
        x, y = 0, level
        for i in range(0, y):
            if i + itemWidth <= width and y + itemHeight <= height:
                yield i, y
        x = y   
        for j in range(y, -1, -1):
            if x + itemWidth <= width and j + itemHeight <= height:
                yield x, j
        level += 1    

def diagonalCoordinates(width, height, itemWidth, itemHeight):
    for sum in range(0, width + height - itemWidth - itemHeight + 1):
        for x in range(max(0, sum - height + itemHeight), min(sum, width - itemWidth) + 1):
            y = sum - x
            if x + itemWidth <= width and y + itemHeight <= height:
                yield x, y

def nonGuillotineCut(rectangles, containerWidth, containerHeight):
    nonGuillotine = NonGuillotine(containerWidth, containerHeight)
    sortedRectangles = sorted(enumerate(rectangles), key=lambda value: value[1][2], reverse=True)
    for index, (width, height, value) in sortedRectangles:
        nonGuillotine.placeRectangle(index, width, height, value)
        #if not nonGuillotine.placeRectangle(index, width, height, value):
        #    nonGuillotine.placeRectangle(index, height, width, value)
    return nonGuillotine.placedRectangles, nonGuillotine.maxValue