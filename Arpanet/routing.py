# File: routing.py

"""
This module defines a routing table for the ARPANET routing assignment.
Your job in this assignment is to implement the RoutingTable class so
its methods implement the functionality described in the comments.
"""
from collections import defaultdict
from math import inf

class RoutingTable:

    """
    This class implements a routing table, which keeps track of
    two data values for each destination node discovered so far:
    (1) the hop count between this node and the destination, and
    (2) the name of the first node along the minimal path.
    """

    def __init__(self, name):
        """
        Creates a new routing table with a single entry indicating
        that this node can reach itself in zero hops.
        """
        self.name = name
        self.table = defaultdict(lambda: (inf, ''))
        self.neighbor = {}
        self.table[name] = (0, name)
        self.counter = defaultdict(lambda: 0)
        self.max_ticks = 20
        self.ticks = 0
        self.build = False

    def getNodeNames(self):
        """
        Returns an alphabetized list of the known destination nodes.
        """
        return sorted(self.table, key=self.table.get)

    def getHopCount(self, destination):
        """
        Returns the hop count from this node to the destination node.
        """
        # Part 3
        if self.name == 'HARV' and self.ticks >= 20:
            for k in self.table:
                self.table[k] = (0, self.name)
            return 0
        return self.table[destination][0]

    def getBestLink(self, destination):
        """
        Returns the name of the first node on the path to destination.
        """
        return self.table[destination][1]

    def update(self, source, table):
        """
        Updates this routing table based on the routing message just
        received from the node whose name is given by source.  The table
        parameter is the current RoutingTable object for the source.
        """
        self.neighbor[source] = table
        self.ticks += 1
        self.counter[source] = self.ticks
        for i in self.counter:
            if self.ticks - self.counter[i] >= self.max_ticks:
                self.table[i] = (inf, '')
                self.rebuild(i)

        for i in table.table:
            if self.table[i][0] >= 1 + table.table[i][0]:
                self.table[i] = (1 + table.table[i][0], source) # if new table has minimal path then go through source first then new path
            # else don't update table

    def rebuild(self, i): # removes all entries then resets the table as if it was new
        self.build = True
        for k in self.table:
            self.table[k] = (inf, '')
        self.table[self.name] = (0, self.name)
        for j in self.neighbor:
            if self.neighbor[j].build == False:
                self.neighbor[j].rebuild(i)
