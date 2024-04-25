class Guillotine:
    def __init__(self, width, height):
        self.width            = width
        self.height           = height
        self.freeSpaces       = [(0, 0, width, height)]
        self.placedRectangles = []
        self.maxValue         = 0

    def placeRectangle(self, index, width, height, value):
        self.freeSpaces.sort(key=lambda space: space[2] * space[3])
        for i, (x, y, w, h) in enumerate(self.freeSpaces):
            if width <= w and height <= h:
                self.placedRectangles.append((index + 1, x, y, width, height))
                self.freeSpaces.pop(i)
                self.maxValue += value
                if w - width > h - height:
                    if w - width > 0 and height > 0:
                        self.freeSpaces.append((x + width, y         , w - width,     height))
                    if w > 0 and h - height > 0:
                        self.freeSpaces.append((x        , y + height, w        , h - height))
                else:
                    if w - width > 0 and h > 0:
                        self.freeSpaces.append((x + width, y         , w - width, h         ))
                    if width > 0 and h - height > 0:
                        self.freeSpaces.append((x        , y + height,     width, h - height))
                return True
        return False
    
def guillotineGreedy(rectangles, containerWidth, containerHeight):
    guillotine = Guillotine(containerWidth, containerHeight)
    sortedRectangles = sorted(enumerate(rectangles), key=lambda value: value[1][2], reverse=True)
    for index, (width, height, value) in sortedRectangles:
        guillotine.placeRectangle(index, width, height, value)
        #if not guillotine.placeRectangle(index, width, height, value):
        #    guillotine.placeRectangle(index, height, width, value)
    return guillotine.placedRectangles, guillotine.maxValue