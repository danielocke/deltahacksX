words = ['charm','adorn','metal','worth','angle']

def startX(tree):
    h = 1
    min = 0
    x = 0
    for i in tree:
        if h == 1:
            x += i[2][0]
        else:
            x -= i[2][1]
            if x < min:
                min = x

    return -1*min

    
def startY(tree):
    h = -1
    min = 0
    y = 0
    for i in tree:
        if h == -1:
            y += i[2][0]
        else:
            y -= i[2][1]
            if y < min:
                min = y
            
    return -1*min



def plot(tree, d):
    if(len(tree) == 0):
        return
    
    grid = [[" " for _ in range(d)] for _ in range(d)]

    i = startY(tree)
    j = startX(tree)

    dir = -1 # 1 for vertical, -1 for horizontal
    loc = {tree[0][0]:(i,j,dir)}

    if j + len(tree[0][0]) > d:
        return False

    for k in tree[0][0]:
        grid[i][j] = k
        j += 1

    for w in tree:

        
        i,j,dir = loc[w[0]][0],loc[w[0]][1],-1*loc[w[0]][2]

        if dir == 1:
            i -= w[2][1]
            j += w[2][0]
            
            loc[w[1]] = (i,j,dir)

            if i + len(tree[0][0]) > d:
                return False

            for k in w[1]:
                if not grid[i][j] == " " and not grid[i][j] == k:
                    return False
                grid[i][j] = k
                i += 1

        else:
            i += w[2][0]
            j -= w[2][1]

            loc[w[1]] = (i,j,dir)

            if j + len(tree[0][0]) > d:
                return False

            for k in w[1]:
                if not grid[i][j] == " " and not grid[i][j] == k:
                    return False
                grid[i][j] = k
                j += 1
        

    return grid

def testAdd(tree,new,d):
    if plot(tree + [new],d) == False:
        return False
    return True

class Puzzle:
    def __init__(self):
        self.words = set()
        self.adjacencyList = {}
        self.edges = []

    def add_edge(self, u, v, connection):
        self.words.add(u)
        self.words.add(v)

        # Add the edge to the adjacency list
        self.adjacencyList.setdefault(u, []).append((v, connection))
        self.adjacencyList.setdefault(v, []).append((u, connection))
        
        # Add the edge to the list of edges
        self.edges.append((u, v, connection))

    def dfs_spanning_tree(self, start_word):
        visited = set()
        spanningTreeEdges = []

        def dfs(word):
            visited.add(word)
            for neighbor, connection in self.adjacencyList[word]:
                if neighbor not in visited and testAdd(spanningTreeEdges,(word, neighbor, connection),10):
                    spanningTreeEdges.append((word, neighbor, connection))
                    dfs(neighbor)

        dfs(start_word)
        return spanningTreeEdges

# For each word find all letters in other words
# that match up with current word
def findPairs(p, words):

    for i in range(len(words) - 1):
        s1 = words[i]
        for j in range(i + 1,len(words)):
            
            s2 = words[j]
            x,y = 0,0

            for x in range(len(s1)):
                for y in range(len(s2)):
                    #If there is a letter match between two words, add the position to pairs
                    if s1[x] == s2[y]:
                        p.add_edge(words[i],words[j],(x,y))

def print_grid(grid):
    for i in grid:
        print(i)


p = Puzzle()
findPairs(p,words)
print_grid(plot(p.dfs_spanning_tree("charm"),6))


tree = (("charm","adorn",(2,0)),("charm","metal",(4,0)),("adorn","worth",(2,1)),("adorn","angle",(4,1)))





