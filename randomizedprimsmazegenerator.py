import random
global dimx
global dimy
dimx = 10
dimy = 10
nodes = {}
## Nodes are keyed by coordinate tuple position (x,y)
## dictionary values are neighboring position tuples
## 'left', 'right', 'up', 'down'
## and wall open closed values
## wleft, wright, wup, wdown which is either 0, or 1

## Build nodes
for x in range(0,dimx):
    for y in range(0,dimy):
       attr = {}
       attr['left'] = None
       attr['right'] = None
       attr['up'] = None
       attr['down'] = None
       attr['wleft'] = None
       attr['wright'] = None
       attr['wup'] = None
       attr['wdown'] = None 
       if x != 0:
           attr['left'] = (x-1,y)
           attr['wleft'] = {'self': 'left', 'position': (x,y), 'neighbor': (x-1,y), 'closed': 1}
       else:
           attr['wleft'] = {'self': 'left', 'position': (x,y), 'neighbor': None, 'closed': 1}
       if x != dimx-1:
           attr['right'] = (x+1,y)
           attr['wright'] = {'self': 'right', 'position': (x,y), 'neighbor': (x+1,y), 'closed': 1}
       else:
           attr['wright'] = {'self': 'right', 'position': (x,y), 'neighbor': None, 'closed': 1}
       if y != 0:
           attr['down'] = (x,y-1)
           attr['wdown'] = {'self': 'down', 'position': (x,y), 'neighbor': (x,y-1), 'closed': 1}
       else:
           attr['wdown'] = {'self': 'down', 'position': (x,y), 'neighbor': None, 'closed': 1}
       if y != dimy-1:
           attr['up'] = (x,y+1)
           attr['wup'] = {'self': 'up', 'position': (x,y), 'neighbor': (x,y+1), 'closed': 1}
       else:
           attr['wup'] = {'self': 'up', 'position': (x,y), 'neighbor': None, 'closed': 1}
       nodes[(x,y)] = attr

##build maze
maze = []
##Start with a grid full of walls.
##Pick a cell, mark it as part of the maze. Add the walls of the cell to the wall list.
##While there are walls in the list:
##Pick a random wall from the list. If the cell on the opposite side isn't in the maze yet:
##Make the wall a passage and mark the cell on the opposite side as part of the maze.
##Add the neighboring walls of the cell to the wall list.
##Remove the wall from the list.
position = (0,0)
oppositewall = {'left': 'wright', 'right':'wleft', 'up':'wdown', 'down':'wup'}
## initialize list with walls from position
walls = []
wdirections = ['wleft','wright','wup', 'wdown'] 
nodedict = nodes[position]
for wdir in wdirections:
    if nodedict[wdir]['neighbor'] != None:
        walls.append(nodedict[wdir])

##ended initializing walls list for start

##add start position to the maze
maze.append(position)

## start prims random algorithm
while (len(walls) > 0):
    wind = random.randint(0,len(walls)-1)
    wallpick = walls[wind]
    if not wallpick['neighbor'] in maze:
        wallpick['closed'] = 0
        npos = wallpick['neighbor']
        nodedict = nodes[npos]
        noppwall = oppositewall[wallpick['self']]
        nodedict[noppwall]['closed'] = 0
        maze.append(wallpick['neighbor'])
        for wdir in wdirections:
            if nodedict[wdir]['neighbor'] != None:
                walls.append(nodedict[wdir])        
        del walls[wind]
    else:
        del walls[wind]

wallsize = .5 ## thickness
cellsize = 1.0 ## or NxN

##build vertices
## for each cell there is a passage of wallsize in 4 possible directions
## start left exterior wall of the maze
vertices = []
faces = []
mwalls = []
tramt = (0,0)
for y in range(0,dimy):
    ##local coordinates for 1rstwall section exceptions case
    verticesind = []
    if tramt[0] == 0 and tramt[1] == 0:
        vert1 = (0.0,0.0,0.0)
        vert2 = (0.0,wallsize,0.0)
        vert3 = (wallsize,wallsize,0.0)
        vert4 = (wallsize,0.0,0.0)
        for vert in [vert1,vert2,vert3,vert4]:
            vert = (vert[0]+tramt[0],vert[1] + tramt[1],vert[2])
            vertices.append(vert)
            verticesind.append(len(vertices)-1)
        
        faces.append(verticesind)
        mwalls.append(verticesind)
        verticesind = []
        tramt = (tramt[0],tramt[1]+wallsize)
    #local coordinates for 2nd wall section
    vert5 = (0.0,0.0,0.0)
    vert6 = (0.0,cellsize,0.0)
    vert7 = (wallsize,cellsize,0.0)
    vert8 = (wallsize,0.0,0.0)
    for vert in [vert5,vert6,vert7,vert8]:
        vert = (vert[0]+tramt[0],vert[1] + tramt[1],vert[2])
        vertices.append(vert)
        verticesind.append(len(vertices)-1)
    faces.append(verticesind)
    mwalls.append(verticesind)
    verticesind = []
    tramt = (tramt[0],tramt[1]+cellsize)
    #local coordinates for 3rd wall section
    vert1 = (0.0,0.0,0.0)
    vert2 = (0.0,wallsize,0.0)
    vert3 = (wallsize,wallsize,0.0)
    vert4 = (wallsize,0.0,0.0)
    for vert in [vert1,vert2,vert3,vert4]:
        vert = (vert[0]+tramt[0],vert[1] + tramt[1],vert[2])
        vertices.append(vert)
        verticesind.append(len(vertices)-1)
    
    faces.append(verticesind)
    mwalls.append(verticesind)
    verticesind = []
    tramt = (tramt[0],tramt[1]+wallsize)

##finished left exterior wall now we iterate building the maze
## tracking walls vertices for selection and later procedural extrusion
##increment tramt by wallsize for the new translation amount

