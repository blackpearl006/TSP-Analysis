def nearestNeighbourHueristics(n,tsp):
    path = []
    startNode = n
    minValue = 999999
    for i in tsp[startNode]:
        if i < minValue: minValue=i
    return path

# This is not the full implementation
# We can Improve the Nearest Neighbour Hueristics if we choose different start node for each iterration of the nearestNeighbourHueristics call
