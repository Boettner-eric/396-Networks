from graph import Graph, Node, Arc

class Königsberg(Graph):
    def __init__(self, filename):
        super().__init__()
        self.load(filename)
        self.start = None

    def visit(self, node, path):
        for arc in node.getArcsFrom():
            self.removeArc(arc)
            for i in node.getArcsTo():
                if i._start == arc._finish and i._finish == arc._start:
                    backwards, _ = i, self.removeArc(i); break # deals with identical arcs
            path.append(arc)
            if (self.start == arc.getFinish() and self.getArcs() == []) or self.visit(arc.getFinish(), path):
                return path
            path.remove(arc) # try a different arc instead
            self.addArc(arc)
            self.addArc(backwards)

    def eulerian_path(self):
        for i in graph.getNodes():
            self.start = i
            x = self.visit(i,[]) # for each source node
            if x:
                return x

graph = Königsberg("Bridges.txt")
print(f"Bridges: {graph.eulerian_path()}")
graph = Königsberg("easy.txt")
print(f"Triangle: {graph.eulerian_path()}")
