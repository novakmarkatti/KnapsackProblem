class Guillotine3D:
    def __init__(self, width, height, depth):
        self.width         = width
        self.height        = height
        self.depth         = depth
        self.freeSpaces    = [(0, 0, 0, width, height, depth)]
        self.placedCuboids = []
        self.maxValue      = 0

    def chooseCuttingOrder(self, width, height, depth):
        dimensions = [('X', width), ('Y', height), ('Z', depth)]
        dimensions.sort(key=lambda x: x[1], reverse=True)
        cuttingOrder = dimensions[0][0] + dimensions[1][0] + dimensions[2][0]
        return cuttingOrder
    
    def placeCuboid(self, index, width, height, depth, value):
        self.freeSpaces.sort(key=lambda space: space[3] * space[4] * space[5])
        for i, (x, y, z, w, h, d) in enumerate(self.freeSpaces):
            if width <= w and height <= h and depth <= d:
                self.placedCuboids.append((index+1, x, y, z, width, height, depth))
                self.freeSpaces.pop(i)
                self.maxValue += value

                cuttingOrder = self.chooseCuttingOrder(width, height, depth)
                self.addFreeSpaces(cuttingOrder, x, y, z, w, h, d, width, height, depth)
                return True
        return False

    def addFreeSpaces(self, cuttingOrder, x, y, z, w, h, d, width, height, depth):
        if cuttingOrder == "XYZ":
            self.freeSpaces.append((x + width, y         , z        , w - width, h         , d))
            self.freeSpaces.append((x        , y + height, z        , width    , h - height, d))
            self.freeSpaces.append((x        , y         , z + depth, width    , height    , d - depth))
        elif cuttingOrder == "XZY":
            self.freeSpaces.append((x + width, y         , z        , w - width, h         , d))
            self.freeSpaces.append((x        , y         , z + depth, width    , h         , d - depth))
            self.freeSpaces.append((x        , y + height, z        , width    , h - height, depth))
        elif cuttingOrder == "YXZ":
            self.freeSpaces.append((x + width, y         , z        , w - width, height    , d))  
            self.freeSpaces.append((x        , y + height, z        , w        , h - height, d)) 
            self.freeSpaces.append((x        , y         , z + depth, width    , height    , d - depth))
        elif cuttingOrder == "YZX":
            self.freeSpaces.append((x + width, y         , z        , w - width, height    , depth))  
            self.freeSpaces.append((x        , y + height, z        , w        , h - height, d)) 
            self.freeSpaces.append((x        , y         , z + depth, w        , height    , d - depth))
        elif cuttingOrder == "ZXY":
            self.freeSpaces.append((x + width, y         , z        , w - width, h         , depth)) 
            self.freeSpaces.append((x        , y + height, z        , width    , h - height, depth))
            self.freeSpaces.append((x        , y         , z + depth, w        , h         , d - depth))
        elif cuttingOrder == "ZYX":
            self.freeSpaces.append((x + width, y         , z        , w - width, height    , depth))  
            self.freeSpaces.append((x        , y + height, z        , w        , h - height, depth)) 
            self.freeSpaces.append((x        , y         , z + depth, w        , h         , d - depth))

def guillotineCut3D(cuboids, containerWidth, containerHeight, containerDepth):
    guillotine = Guillotine3D(containerWidth, containerHeight, containerDepth)
    sortedCuboids = sorted(enumerate(cuboids), key=lambda value: value[1][3], reverse=True)
    for index, (width, height, depth, value) in sortedCuboids:
        guillotine.placeCuboid(index, width, height, depth, value) 
    return guillotine.placedCuboids, guillotine.maxValue