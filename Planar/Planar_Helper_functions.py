
def onLine(a, b, c):
    def on(i): return (min(a[i], c[i]) <= b[i] <= max(a[i], c[i]))
    on_x = on(0)
    on_y = on(1)
    return on_x and on_y


def intersuctionFromTwoPoints(a, b, c):
    def dif1(i): return (b[i] - a[i])
    def dif2(i): return (c[i] - b[i])
    dif1_x = dif1(0)
    dif1_y = dif1(1)
    dif2_x = dif2(0)
    dif2_y = dif2(1)
    direc1 = (dif1_y * dif2_x)
    direc2 = (dif1_x * dif2_y)
    return (direc2 < direc1) + 2 * (direc1 < direc2)



def points_crossing(a1, b1, a2, b2):
    d1 = intersuctionFromTwoPoints(a1, b1, a2)
    d2 = intersuctionFromTwoPoints(a1, b1, b2)
    d3 = intersuctionFromTwoPoints(a2, b2, a1)
    d4 = intersuctionFromTwoPoints(a2, b2, b1)
    return ((d1 != d2) and (d3 != d4)) or \
           ((not d1) and onLine(a1, a2, b1)) or \
           ((not d2) and onLine(a1, b2, b1)) or \
           ((not d3) and onLine(a2, a1, b2)) or \
           ((not d4) and onLine(a2, b1, b2))



def areCrossing(edge1, edge2):
    # a late addition!! -  i dont want to allow line that share a node to be considered intesecting:
    if((edge1[0 ]==edge2[0]) or(edge1[0 ]== edge2[1]) or(edge1[1 ]==edge2[0] ) or(edge1[1]==edge2[1])):
        return False

    x1 = edge1[0][0]
    y1 = edge1[0][1]
    x2 = edge1[1][0]
    y2 = edge1[1][1]
    x3 = edge2[0][0]
    y3 = edge2[0][1]
    x4 = edge2[1][0]
    y4 = edge2[1][1]
    a1 = (x1, y1)
    b1 = (x2, y2)
    a2 = (x3, y3)
    b2 = (x4, y4)
    return points_crossing(a1, b1, a2, b2)
