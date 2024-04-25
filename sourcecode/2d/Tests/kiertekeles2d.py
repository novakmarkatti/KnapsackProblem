class Guillotine:
    def __init__(self, width, height):
        self.width            = width
        self.height           = height
        self.freeSpaces       = [(0, 0, width, height)]
        self.placedRectangles = []
        self.maxValue         = 0

    def splitFreeSpaces(self, approach, width, height, x, y, w, h):
        if approach == "nagyobbFentmaradoHely": 
            self.nagyobbFentmaradoHely(width, height, x, y, w, h)
        elif approach == "merettelParhuzamos": 
            self.merettelParhuzamos(width, height, x, y, w, h)
        elif approach == "merettelMeroleges": 
            self.merettelMeroleges(width, height, x, y, w, h)
        elif approach == "csakVizszintes": 
            self.csakVizszintes(width, height, x, y, w, h)                                  
        elif approach == "csakFuggoleges": 
            self.csakFuggoleges(width, height, x, y, w, h)

    def nagyobbFentmaradoHely(self, width, height, x, y, w, h):
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

    def merettelParhuzamos(self, width, height, x, y, w, h):
        if width > height:
            if w - width > 0 and height > 0:
                self.freeSpaces.append((x + width, y         , w - width,     height))
            if w > 0 and h - height > 0:
                self.freeSpaces.append((x        , y + height, w        , h - height))
        else:
            if w - width > 0 and h > 0:
                self.freeSpaces.append((x + width, y         , w - width, h         ))
            if width > 0 and h - height > 0:
                self.freeSpaces.append((x        , y + height,     width, h - height))

    def merettelMeroleges(self, width, height, x, y, w, h):
        if width < height:
            if w - width > 0 and height > 0:
                self.freeSpaces.append((x + width, y         , w - width,     height))
            if w > 0 and h - height > 0:
                self.freeSpaces.append((x        , y + height, w        , h - height))
        else:
            if w - width > 0 and h > 0:
                self.freeSpaces.append((x + width, y         , w - width, h         ))
            if width > 0 and h - height > 0:
                self.freeSpaces.append((x        , y + height,     width, h - height))               

    def csakVizszintes(self, width, height, x, y, w, h):
        if w - width > 0 and height > 0:
            self.freeSpaces.append((x + width, y         , w - width,     height))
        if w > 0 and h - height > 0:
            self.freeSpaces.append((x        , y + height, w        , h - height))

    def csakFuggoleges(self, width, height, x, y, w, h):
        if w - width > 0 and h > 0:
            self.freeSpaces.append((x + width, y         , w - width, h         ))
        if width > 0 and h - height > 0:
            self.freeSpaces.append((x        , y + height,     width, h - height))   

    def placeRectangleBestFit(self, approach, index, width, height, value):
        self.freeSpaces.sort(key=lambda space: space[2] * space[3])
        for i, (x, y, w, h) in enumerate(self.freeSpaces):
            if width <= w and height <= h:
                self.placedRectangles.append((index + 1, x, y, width, height))
                self.freeSpaces.pop(i)
                self.maxValue += value
                
                self.splitFreeSpaces(approach, width, height, x, y, w, h)
                return True
        return False
    
    def placeRectangleWorstFit(self, approach, index, width, height, value):
        self.freeSpaces.sort(key=lambda space: space[2] * space[3], reverse=True)
        for i, (x, y, w, h) in enumerate(self.freeSpaces):
            if width <= w and height <= h:
                self.placedRectangles.append((index + 1, x, y, width, height))
                self.freeSpaces.pop(i)
                self.maxValue += value
                
                self.splitFreeSpaces(approach, width, height, x, y, w, h)
                return True
        return False

    def placeRectangle(self, placeRectangle ,approach, index, width, height, value):
        if placeRectangle == "placeRectangleBestFit": 
            return self.placeRectangleBestFit(approach, index, width, height, value)
        elif placeRectangle == "placeRectangleWorstFit": 
            return self.placeRectangleWorstFit(approach, index, width, height, value)


def guillotineGreedy(rectangles, containerWidth, containerHeight, placeRectangleAp, splitAp, rotate):
    guillotine = Guillotine(containerWidth, containerHeight)
    sortedRectangles = sorted(enumerate(rectangles), key=lambda value: value[1][2], reverse=True)
    for index, (width, height, value) in sortedRectangles:
        if rotate == 0:
            guillotine.placeRectangle(placeRectangleAp, splitAp, index, width, height, value)
        elif not guillotine.placeRectangle(placeRectangleAp, splitAp, index, width, height, value):
            guillotine.placeRectangle(placeRectangleAp, splitAp, index, height, width, value)
    return guillotine.placedRectangles, guillotine.maxValue, guillotine.freeSpaces

##################################################
import json
inputFile = open("test01.json") 
jsonArray = json.load(inputFile)

result = []
for test in jsonArray:
    testNumber = test['testNumber']
    note       = test['note']
    capacity   = test['capacity']
    rectangles = test['rectangles']
    containerWidth, containerHeight = capacity[0], capacity[1]

    # guilotine greedy
    splitAp = ["nagyobbFentmaradoHely", "merettelParhuzamos", "merettelMeroleges", "csakVizszintes", "csakFuggoleges"]
    placedRectangleAp = ["placeRectangleBestFit", "placeRectangleWorstFit"]
    for i in range(0, len(splitAp)):
        for j in range(0, len(placedRectangleAp)):
            for rotate in range(0, 2):
                placedRectangles, maxValue, freeSpaces = guillotineGreedy(rectangles, containerWidth, containerHeight, placedRectangleAp[j], splitAp[i], rotate)
                result.append((placedRectangleAp[j], splitAp[i], maxValue, rotate != 0, placedRectangles))

    # guillotine random
    import guillotine_random
    for rotate in range(0, 2):
        placedRectangles, maxValue, freeSpaces = guillotine_random.guillotineRandom(rectangles, containerWidth, containerHeight, rotate)
        result.append(("G. Random", "nagyobbFentmaradoHely", maxValue, rotate != 0, placedRectangles))

    # non - guillotine random
    import non_guillotine_random
    placedRectangles, maxValue = non_guillotine_random.nonGuillotineRandom(rectangles, containerWidth, containerHeight)   
    result.append(("N. G. Random", "-", maxValue, False, placedRectangles))

    # first fit
    import non_guillotine_first_fit
    approach = ["leftToRightThenBottomToTop", "bottomToTopThenLeftToRight", "spiralCoordinates", "diagonalCoordinates"]
    for i in range(0, len(approach)):
        for rotate in range(0, 2):
            placedRectangles, maxValue = non_guillotine_first_fit.nonGuillotineCut(rectangles, containerWidth, containerHeight, rotate, approach[i])   
            result.append(("N. G. First-Fit", approach[i], maxValue, rotate != 0, placedRectangles))

    # next fit 1 
    import non_guillotine_next_fit_1
    placedRectangles, maxValue = non_guillotine_next_fit_1.nonGuillotineCut(rectangles, containerWidth, containerHeight)  
    result.append(("N. G. Next-Fit 1", "-", maxValue, False, placedRectangles))

    # next fit 2 
    import non_guillotine_next_fit_2
    placedRectangles, maxValue = non_guillotine_next_fit_2.nonGuillotineCut(rectangles, containerWidth, containerHeight)  
    result.append(("N. G. Next-Fit 2", "-", maxValue, False, placedRectangles))

# Result
result.sort(reverse=True, key=lambda value: value[2])
for res in result:
    print(res[0], res[1], res[2], res[3])
