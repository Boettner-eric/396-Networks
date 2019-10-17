# File: HopcroftTarjanTest.py

"""
This program implements test of the Hopcroft-Tarjan algorithm for
finding articulation points in a graph.
"""

from graph import Graph

def HopcroftTarjan():
    """Tests the Hopcroft-Tarjan algorithm for finding articulation points."""
    g = Graph()
    while True:
        filename = input("Enter name of graph file: ")
        if filename == "":
            break
        if filename.find(".") == -1:
            filename += ".txt"
        g.clear()
        g.load(filename)        
        print("Articulation points:")
        for node in findArticulationPoints(g):
            print("  " + node.getName())

def findArticulationPoints(g):
    """Returns a list of the articulation points in the graph."""
    nodes = g.getNodes()
    for node in nodes:
        node.visited = False
        node.parent = None
    cutpoints = []
    applyHopcroftTarjan(nodes[0], 0, cutpoints)
    return cutpoints

def applyHopcroftTarjan(start, depth, cutpoints):
    """Recursively adds articulation points to the cutpoints list."""
    start.visited = True
    start.depth = depth
    start.low = depth
    isCutPoint = False
    neighbors = start.getNeighbors()
    children = 0
    for node in neighbors:
        if not node.visited:
            node.parent = start
            applyHopcroftTarjan(node, depth + 1, cutpoints)
            children += 1
            if node.low >= start.depth:
                isCutPoint = True
            start.low = min(start.low, node.low)
        elif node != start.parent:
            start.low = min(start.low, node.depth)
    if start.parent is None:
        isCutPoint = children > 1
    if isCutPoint:
        cutpoints.append(start)

# Startup code

if __name__ == "__main__":
    HopcroftTarjan()
