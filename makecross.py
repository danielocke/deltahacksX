import subprocess
import cohere

f = open("input.txt", "r")
words = f.readlines()
f.close()

for i in range(len(words)):
    words[i] = words[i].replace(" ","")
    words[i] = words[i].replace("\n","")
    words[i] = words[i].lower()


co = cohere.Client("j8Q3uuHv8d59FNURAMP3szgk8Az9x3diHgGL6vc0")

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

def toStr(l):
    s = ""
    for i in l:
        s += i
    return s

def scanH(grid):
    for i in grid:
        l = toStr(i).split(" ")
        for j in l:
            if len(j) > 1 and not j in words:
                return False
    return True

def scanV(grid):
    s = ""

    for i in range(len(grid)):
        for j in range(len(grid)):
            s += grid[j][i]
        s += " "

    l = s.split(" ")

    for i in l:
        if len(i) > 1 and not i in words:
            return False
    return True

def plot(tree, d):

    grid = [[" " for _ in range(d)] for _ in range(d)]

    i = startY(tree)
    j = startX(tree)

    dir = -1 # 1 for vertical, -1 for horizontal
    loc = {tree[0][0]:(i,j,dir)}

    if j + len(tree[0][0]) >= d or j < 0:
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

            if i + len(tree[0][0]) >= d or i < 0:
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

            if j + len(tree[0][0]) >= d or j < 0:
                return False

            for k in w[1]:
                if not grid[i][j] == " " and not grid[i][j] == k:
                    return False
                grid[i][j] = k
                j += 1
        
    if not scanH(grid) or not scanV(grid):
        return False

    locS = loc.items()
    locS = sorted(locS,key = lambda t : t[1][0]*d + t[1][1])
    for i in range(len(locS)):
        grid[locS[i][1][0]][locS[i][1][1]] ="[" + str(i + 1) + "]" + grid[locS[i][1][0]][locS[i][1][1]]
    namesS = []
    for i in locS:
        namesS.append(i[0])


    return grid,namesS

def testAdd(tree,new,d):
    if plot(tree + [new],d) == False:
        return False
    return True

def isSpanTree(tree):
    for i in words:
        found = False
        for j in tree:
            if j[0] == i or j[1] == i:
                found = True
                break
        if found == False:
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

    def smallestST(self,start_word):

        for i in range(100):
            st = self.dfs_spanning_tree(start_word,i)
            if not st == False:
                return (st,i)

    def dfs_spanning_tree(self, start_word,dim):
        visited = set()
        spanningTreeEdges = []

        def dfs(word):
            visited.add(word)
            for neighbor, connection in self.adjacencyList[word]:
                if neighbor not in visited and testAdd(spanningTreeEdges,(word, neighbor, connection),dim):
                    spanningTreeEdges.append((word, neighbor, connection))
                    dfs(neighbor)

        dfs(start_word)

        if isSpanTree(spanningTreeEdges):
            return spanningTreeEdges
        return False

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
x = p.smallestST(words[0])


def generateClues():
    f = open("cohere_train.txt", "r")
    trainingData = f.read()
    f.close()

    clues = {}
    for word in words:
        message = trainingData + word + "\nDefinition:" 
        response = co.generate(message,model = "command",temperature=0.75,max_tokens=20)
        answer = (response.generations[0].text).split(".")[0]
        answer = (response.generations[0].text).split("\n")[0]
        if ":" in answer:
            answer = (response.generations[0].text).split(":")[1]
        clues[word] = answer

    return clues

def generateLatexGraphSolved(grid):
    latex = "\\begin{Puzzle}{" + str(len(grid)) + "}{" + str(len(grid)) + "}\n"
    for i in grid:
        for j in i:
            for z in range(10):
                j = j.replace(str(z),"")
            j = j.replace("-","")
            j = j.replace("[]","")

            latex += "|"
            
            if j == " ":
                latex += "*"
            else:
                latex += "[][S]" + j
        latex += "|.\n"
    latex += "\\end{Puzzle}"
    return latex

def generateLatexGraph(grid):
    latex = "\\begin{Puzzle}{" + str(len(grid)) + "}{" + str(len(grid)) + "}\n"
    for i in grid:
        for j in i:
            latex += "|"
            
            if j == " ":
                latex += "*"
            else:
                j = j.replace("][","-")
                latex += j
        latex += "|.\n"
    latex += "\\end{Puzzle}"
    return latex


def generateLatexClues(sortedWords):
    clues = generateClues()
    
    latex = "\\begin{PuzzleClues}{\\textbf{Clues:}\\\}\n\\noindent"
    for i in range(len(sortedWords)):
        latex += "\\Clue{" + str(i+1) + "}{" + sortedWords[i] + "}{" + clues[sortedWords[i]] + "} \\\ \n"
    latex += "\\end{PuzzleClues}"
    return latex

latexStr = "\\documentclass{article}\n\\usepackage[unboxed]{cwpuzzle}\n\\begin{document}" + generateLatexGraph(plot(x[0],x[1])[0]) + "\n" + generateLatexClues(plot(x[0],x[1])[1])  + "\n\\newpage\n" + generateLatexGraphSolved(plot(x[0],x[1])[0]) + "\n\\end{document}"

f = open("latex/main.tex", "w")
f.write(latexStr)
f.close()

try:
    subprocess.run(['pdflatex', "latex/main.tex"],check=True)
    print("Compilation successful!")
except subprocess.CalledProcessError as e:
    print(f"Error during compilation: {e}")