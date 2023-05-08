def nearestNeighbourHueristics(n,tsp):
    path = []
    startNode = n
    minValue = 999999
    for i in tsp[startNode]:
        if i < minValue: minValue=i
    return path

