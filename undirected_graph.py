import unittest
from queue import Queue

class Graph:
    """The Graph class represents an undirected graph with vertices and edges and 
    accepts a list of 2-tuples representing edges as an argument"""
    def __init__(self,edges=None):
        
        self.V = set() #set of vertices
        self.adj = dict() #this dictionary will be a hash table to map edges
        
        for u,v in edges:
            self.V.add(u) #each end of an edge is a vertex, so add
            self.V.add(v)
            
        for i in self.V:
            self.adj[i] = list() #each vertex will have an adjacency list containing nodes immediately adjacent to them
            
        for u,v in edges:
            self.adj[u].append(v) #unpack edges and populate adjacency lists for each vertex
            self.adj[v].append(u) 
        
    def add_node(self,nd):
        """The add_node method accepts an integer as an argument and adds it to the set of vertices if not already present"""
        if(nd in self.adj.keys()):
            pass #node is already in set of vertices
        else:
            self.adj[nd] = list() #this is a new node, create an adjacency list for it
            self.V.add(nd) #add to set of vertices
        
    def add_edge(self,u,v):
        """ The add_edge method accepts two nodes that are to be connected as arguments and 'connects' them
        by placing the second node in the adjacency list corresponding to the first node and vice versa"""
        if(v in self.adj[u]): 
            pass #we've already come across this edge
        else:
            self.adj[u].append(v) #add v to adjacency list of u
            self.adj[v].append(u) #existence of (u,v) implies (v,u) because graph is undirected
    
    def distance(self,n1,n2):
        """ The distance method takes two arguments (n1,n2) that are nodes and returns the length of shortest path between them.
        In its implementation, it unpackages the corresponding tuple from a breadth-first search using n1 as the starting node"""
        
        for (i,j) in self.bfs(n1): #perform a breadth-first search with n1 as starting point
            if(i == n2): #look for corresponding tuple
                return j #result of a bfs is always shortest path
        
    def bfs(self,sn):#g.bfs(2)
        """The bfs method performs a breadth-first search beginning with a starting node given as an argument.
        It utilizes a queue data structure in its implementation"""
        visited = list() #maintain list of nodes visited already
        level = list() #maintain the level we've been to at each vertex
        
        for i in range(len(self.V)):
            level.append(0) #initialize level to all 0s
        
        q = Queue() #use queue data structure throughout bfs
        q.put(sn) #put starting node into queue
        
        visited.append(sn) #mark starting node as visited
        
        while(q.empty() is False): 
            
            v = q.get() #pop from queue (FIFO)
            
            for i in self.adj[v]: #for every node in the adjacency list of current node being examined
                if(i not in visited): #if we haven't already visited it
                    level[i-1] = level[v-1]+1 #mark it's level as one level deeper than its parent
                    q.put(i) #add it to the end of the queue
                    visited.append(i) #mark it as visited
                    
        return list(zip(self.V,level))  #return list of 2-tuples
    
    def __contains__(self,n): #this overloads in operator
        if(n in self.V): #if it's in the set of vertices, its 'in' the graph
            return True
        else:
            return False #otherwise it isn't in the graph
        
    def __iter__(self):
        
        return iter(self.V) #we want to be able to iterate over the vertices
    
    def __getitem__(self,index):
        
        return self.adj[index]  #indexing of the nodes should return its adjacency list
    
class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.gr = Graph([(1,2),(1,5),(2,3),(2,5),(3,4),(4,5),(4,6)])#gr is the test graph that has been initialized
        
    def test_add_node(self):
        self.gr.add_node(15) #add 15
        self.assertTrue(15 in self.gr) #test whether it's been added
        self.assertFalse(20 in self.gr)#test whether add_node works for False case as well

    def test_add_edge(self):
        self.gr.add_edge(4,2) #add an edge
        self.assertTrue(self.gr.distance(4,2) == 1) #if it's been added, then distance is 1
        self.assertFalse(self.gr.distance(2,4) == 2) #reverse edge, distance should still be 1
    
    def test_in(self): #test true and false scenarios for in operator
        self.assertTrue(4 in self.gr) 
        self.assertFalse(18 in self.gr)
    
    def test_index(self):
        x = self.gr[5] 
        y = [1,2,4] #indexing should return the correct adjacency list
        
        self.assertTrue(x == y)
        self.assertFalse(x == [1,2,4,5])
        
    def test_bfs(self): #a set would eliminate duplicate entries 
        x = self.gr.bfs(1)
        y = set(x)
        
        self.assertTrue(len(x) == len(y)) #if their length is the same, then x had no duplicates
        self.assertFalse(len(x) == len(y) == 0)
    
    def test_distance(self):
        x = self.gr.distance(2,2)
        y = self.gr.distance(4,3)
        
        self.assertTrue(x == 0) #distannce between a node and itself should be 0
        self.assertFalse(y == 0)
        self.assertTrue(y == 1) #we know distance between 4 and 3 is 1, test to see if distance working correctly

if __name__ == '__main__':
    unittest.main()





















    








