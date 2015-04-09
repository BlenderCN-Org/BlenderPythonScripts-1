#Mondrian like subdivision generator
import bpy
import random
dimx = 50
dimy = 65
totalnodes = 3
meshName = "Mondrian"
obName = "MondrianObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
##track edges on mondrian generator and vertices
nodes = {}
nodepostoi = {}
for i in range(0,totalnodes):
   attr = {}
   randposx = random.randint(0,dimx)
   randposy = random.randint(0,dimy)
   attr['position'] = (randposx,randposy)
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   attr['crossing'] = None
   nodes[i] = attr
   nodepostoi[(randposx,randposy)] = i
nodeposlist = list(nodepostoi.keys())   
#node ordering
nodexrank = nodeposlist[0:len(nodeposlist)]
nodeyrank = nodeposlist[0:len(nodeposlist)]
nodexrank.sort(key=lambda tup: tup[0])
nodeyrank.sort(key=lambda tup: tup[1])
#nodes keyed by ypos
ypnodes = {}
for node in nodes:
   ypnodes[nodes[node]['position'][1]] = node

#nodes keyed by xpos
xpnodes = {}
for node in nodes:
   xpnodes[nodes[node]['position'][0]] = node
#finished keying nodes by x and y pos
nodexirank = []
for pos in nodexrank:
    nodexirank.append(nodepostoi[pos])
nodeyirank = []
for pos in nodeyrank:
    nodeyirank.append(nodepostoi[pos])
##set node crossings
crossingnodes = {}
crossingnodesrev = {}
factor = 10
if len(nodeyirank) > 9:
   factor = 100
elif len(nodeyirank) > 99:
   factor = 1000

for node in nodes:
    yrank = nodeyirank.index(node)
    posx = nodes[node]['position'][0]
    copynranks = nodeyirank[0:len(nodeyirank)]
    del copynranks[yrank]
    for cr in range(0,totalnodes-1):
        attr = {}
        nodeval = yrank*factor+copynranks[cr]
        posy = nodes[copynranks[cr]]['position'][1]
        attr['position'] = (posx,posy) 
        attr['left'] = None
        attr['right'] = None
        nodevald = None
        crnodepos = nodeyirank.index(copynranks[cr])
        if crnodepos > 0:
            if nodeyirank[crnodepos-1] == yrank:
                nodevald = yrank
                nodes[yrank]['top'] = copynranks[cr]
            else:
                nodevald = yrank*factor + nodeyirank[crnodepos-1]
        attr['down'] = nodevald
        nodevald = None
        if crnodepos < len(nodeyirank)-1:
            if nodeyirank[crnodepos+1] == yrank:
                nodevald = yrank
                nodes[yrank]['down'] = copynranks[cr]
            else:
                nodevald = yrank*factor + nodeyirank[crnodepos+1]
        attr['top'] = nodevald
        crossingnodes[nodeval] = attr
        crossingnodesrev[attr['position']] = nodeval
#2nd pass working on nodexirank indexing
for node in nodes:
   xrank = nodexirank.index(node)
   posy = nodes[node]['position'][1]
   copynranks = nodexirank[0:len(nodexirank)]
   del copynranks[xrank]
   for cr in range(0,totalnodes-1):
      posx = nodes[copynranks[cr]]['position'][0]
      nodeval = crossingnodesrev[(posx,posy)]
      attr = crossingnodes[nodeval]
      nodevald = None
      crnodepos = nodexirank.index(copynranks[cr])
      if crnodepos > 0:
         if nodexirank[crnodepos-1] == xrank:
             nodevald = xrank
             nodes[xrank]['right'] = copynranks[cr]
         else:
             nposx = nodes[nodexirank[cr-1]]['position'][0]
             nodevald = crossingnodesrev[(nposx,posy)]
      attr['left'] = nodevald
      nodevald = None
      if crnodepos < len(nodexirank)-1:
         if nodexirank[crnodepos+1] == yrank:
             nodevald = xrank
             nodes[xrank]['left'] = copynranks[cr]
         else:
             nposx = nodes[nodexirank[cr+1]]['position'][0]
             nodevald = crossingnodesrev[(nposx,posy)]
      attr['right'] = nodevald
      crossingnodes[nodeval] = attr
## randomize crossings
## crossing = 1 vertical  crossing = 0 lateral
for node in crossingnodes:
   randval = random.random()
   if randval >= .5:
      crossingnodes[node]['crossing'] = 1
   else:
      crossingnodes[node]['crossing'] = 0
      
##build boundary nodes
xboundaries = [0,dimx]
yboundaries = [0,dimy]
boundarydict = {}
boundarydictrev = {}
i = -1
checki = 0
for xboundary in xboundaries:
   attr = {}
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   attr['crossing'] = None
   ypos = 0
   attr['position'] = (xboundary, ypos)
   boundarydictrev[(xboundary,ypos)] = i
   boundarydict[i] = attr
   prevnode = i
   if i == -1:
      nprevnode = i
      for node in nodexirank:
         attr = {}
         attr['left'] = None
         attr['right'] = None
         attr['up'] = None
         attr['down'] = None
         attr['crossing'] = None
         xpos = nodes[node]['position'][0]
         yminpos = nodes[nodeyirank[0]]['position'][1]
         coord = (xpos,yminpos)
         upnode = None
         if coord in crossingnodesrev:
            upnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            upnode = nodepostoi[coord]
         attr['up'] = upnode
         attr['position'] = (xpos,0)
         attr['left'] = nprevnode
         boundarydict[nprevnode]['right'] = i
         boundarydictrev[(xpos,0)] = i
         boundarydict[i] = attr
         nprevnode = i
         i -= 1         
   for node in nodeyirank:
      attr = {}
      attr['left'] = None
      attr['right'] = None
      attr['up'] = None
      attr['down'] = None
      attr['crossing'] = None
      ypos = nodes[node]['position'][1]
      if checki == 0:
         xminpos = nodes[nodexirank[0]]['position'][0]
         coord = (xminpos, ypos)
         rightnode = None
         if coord in crossingnodesrev:
            rightnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            rightnode = nodepostoi[coord]
         attr['right'] = rightnode
      else:
         xmaxpos = nodes[nodexirank[len(nodeyirank)-1]]['position'][0]
         coord = (xmaxpos, ypos)
         leftnode = None
         if coord in crossingnodesrev:
            leftnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            leftnode = nodepostoi[coord]
         attr['left'] = rightnode         
      attr['position'] = (xboundary,ypos)
      attr['down'] = prevnode
      boundarydict[prevnode]['up'] = i
      boundarydictrev[(xboundary,ypos)] = i
      boundarydict[i] = attr
      prevnode = i
      i -= 1
   attr = {}
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   attr['crossing'] = None
   ypos = dimy
   attr['position'] = (xboundary, ypos)
   attr['down'] = prevnode
   boundarydictrev[(xboundary,ypos)] = i
   boundarydict[i] = attr
   if checki == 0:
      nprevnode = i
      i -= 1
      for node in nodexirank:
         attr = {}
         attr['left'] = None
         attr['right'] = None
         attr['up'] = None
         attr['down'] = None
         attr['crossing'] = None
         xpos = nodes[node]['position'][0]
         ymaxpos = nodes[nodeyirank[len(nodeyirank)-1]]['position'][1]
         coord = (xpos,ymaxpos)
         downnode = None
         if coord in crossingnodesrev:
            downnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            downnode = nodepostoi[coord]
         attr['down'] = downnode
         attr['position'] = (xpos,dimy)
         attr['left'] = nprevnode
         boundarydict[nprevnode]['right'] = i
         boundarydictrev[(xpos,0)] = i
         boundarydict[i] = attr
         nprevnode = i
         i -= 1  
   checki = i
## finished building boundary nodes
   
## compile all nodes into a position lookup dictionary
completerefrev = {}
for pos in nodepostoi:
   completerefrev[pos] = nodepostoi[pos]
for pos in crossingnodesrev:
   completerefrev[pos] = crossingnodesrev[pos]
for pos in boundarydictrev:
   completerefrev[pos] = boundarydictrev[pos]
## finished compiling all nodes into a complete position lookup
##compile all nodes in a lookup directory
completeref = {}
for node in nodes:
   completeref[node] = nodes[node]
for node in crossingnodes:
   completeref[node] = crossingnodes[node]
for node in boundarydict:
   completeref[node] = boundarydict[node]
##finished compiling all nodes

##reindex nodes to vertex list and position to index vert index
##a bit goofy doing this now, but saves work, and I don't feel like
##re writing the above.
vertices = []
vertpostoindex = {}
i = 0
for nodepos in completerefrev:
   vertices.append(nodepos)
   verpostoindex[nodepos] = i
   i += 1
##finished reindexing vertices

##indexing simple polygons over the completeref set
stopcheck = False
startposition = (0,0)
currentnode = completerefrev[startposition]
currentposition = startposition
nextrowval = completeref[startnode]['right']
polynodesrev = {}
polynodes = {}
i = 0
while not stopcheck:
   columnstopcheck = False
   while not columnstepcheck:
      polypos = [completeref[currentnode]['position']]
      for j in range(0,3):
         currentposition = completeref[currentnode]['position']
         if j = 0:
            nextpos = completeref[currentnode]['up']
            if nextpos == None:
               columnstepcheck = True
               break
         elif j = 1:
            nextpos = completeref[currentnode]['right']
            if nextpos == None:
               columnstepcheck = True
               stopcheck = True
               break
         elif j = 2:
            nextpos = completeref[currentnode]['down']
         elif j = 3:
            nextpos = completeref[currentnode]['left']
         if j != 3:
            polypos.append(currentposition)
         
         currentnode = nextpos
      polynodesrev[polypos] = i
      polynodes[i] = polypos
      i += 1
   currentnode = nextrowval
   nextrowval = completeref[currentnode]['right']
##finished indexing simple polygons
   
##pass to complete connections between boundary and non boundary nodes
for node in boundarydict:
   if completeref[node]['up'] != None:
      neignode = completeref[node]['up']
      if completeref[neignode]['down'] == None:
         completeref[neignode]['down'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['down'] = node
         if neighnode in nodes:
            nodes[neighnode]['down'] = node
   if completeref[node]['down'] != None:
      neignode = completeref[node]['down']
      if completeref[neignode]['up'] == None:
         completeref[neignode]['up'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['up'] = node
         if neighnode in nodes:
            nodes[neighnode]['up'] = node
   if completeref[node]['left'] != None:
      neignode = completeref[node]['left']
      if completeref[neignode]['right'] == None:
         completeref[neignode]['right'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['right'] = node
         if neighnode in nodes:
            nodes[neighnode]['right'] = node
   if completeref[node]['right'] != None:
      neignode = completeref[node]['right']
      if completeref[neignode]['left'] == None:
         completeref[neignode]['left'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['left'] = node
         if neighnode in nodes:
            nodes[neighnode]['left'] = node
## finished completion on boundary pass
         
##recursive function to check crossing
def checkcross(crossval, node, crossingnodes, dirswitch, crosslist):
   check = False
   if crossval:
      if dirswitch:
         topnode = crossingnodes[node]['top']
##         if topnode in nopasscrosslist:
##            return crosslist
         crosslist.append(topnode)
         if topnode in crossingnodes:
            ncrossval = crossingnodes[topnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if ncrossval and not crossingnone:
               return checkcross(crossval,topnode,crossingnodes,dirswitch,
                                 crosslist)
               
            else:
               return crosslist
         else:
            return crosslist

      else:
         downnode = crossingnodes[node]['down']
##         if downnode in nopasscrosslist:
##            return crosslist
         crosslist.append(downnode)
         if downnode in crossingnodes:
            ncrossval = crossingnodes[downnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if ncrossval and not crossingnone:
               return checkcross(crossval,downnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return crosslist
         else:
            return crosslist

   else:
      if dirswitch:
         rightnode = crossingnodes[node]['right']
##         if rightnode in nopasscrosslist:
##            return crosslist
         crosslist.append(rightnode)
         if rightnode in crossingnodes:
            ncrossval = crossingnodes[rightnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if not ncrossval and not crossingnone:
               return checkcross(crossval,rightnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return  crosslist
         else:
            return crosslist

      else:
         leftnode = crossingnodes[node]['left']
##         if leftnode in nopasscrosslist:
##            return crosslist
         crosslist.append(leftnode)
         if leftnode in crossingnodes:
            ncrossval = crossingnodes[leftnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if not ncrossval and not crossingnone:
               return checkcross(crossval,leftnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return crosslist
         else:
            return crosslist


##to check crossing nodes list, if a node is found it marked
## marked at the crossing node in the given direction.
## this is used in identifying the vertices for face construction
def checkneighbornode(crosslist, crossingnodes, nodes, direction):
   cdirection = None
   if direction == 'up':
      cdirection = 'right'
   elif direction == 'left':
      cdirection = 'down'
   elif direction == 'down':
      cdirection = 'right'
   elif direction == 'right':
      cdirection = 'up'
   i = 0
   for cnode in crosslist:
      neighnode = crossingnodes[cnode][cdirection]
      if neighnode in nodes:
         return neighnode,i
      i += 1
   return None, i
      
##function to check within face subdivision area
def nodecolumncheck(minpos, maxpos, pnodes, crosslist, direction,
                    completeref):
   check = True
   eqcheck = False
   i = 0
   for node in crosslist:
      pos = completeref[node]['position']
      npos = None
      if not direction:
         ypos = pos[1]
         nodepos = pnodes[ypos]
         npos = nodes[nodepos]['position'][1]
      else:
         xpos = pos[0]
         nodepos = pnodes[xpos]
         npos = nodes[nodepos]['position'][0]
      check1 = npos >= minpos
      check2 = npos <= maxpos
      check3 = npos == minpos
      check4 = npos == maxpos
      if check1 and check2:
         check = False
         if check3 or check4:
            eqcheck = True
      if not check:
         break
      i += 1
   return check, eqcheck, i

##function used 
def buildnodesedge(axispos, crosslist, completeref, direction):
   rcrosslist = []
   for node in crosslist:
      pos = (None,None)
      posx = None
      posy = None
      if direction:
         posx = completeref[node]['position'][0]
         posy = axispos
      else:
         posy = completeref[node]['position'][1]
         posx = axispos
      pos = (posx, posy)
      rcrosslist.append(pos)
   return rcrosslist

def updatecrossings(completeref, rcrossinglist, pcrossinglist):
   if len(rcrossinglist) >= 3:
      i = 0
      for node in pcrossinglist:
         if (i == 0) or (i == len(pcrossinglist)-1):
         rnode = rcrossinglist[i]
         crossingval = completeref[rnode]['crossing']
         completeref[node]['crossing'] = crossingval
         i += 1
   return completeref
def buildfacesimplepolys(minpos, maxpos, polynodesrev, completerefrev,
                         completeref):
   stopcheck = False
   startposition = minpos
   maxposx = maxpos[0]
   maxposy = maxpos[1]
   currentnode = completerefrev[startposition]
   currentposition = startposition
   nextrowval = completeref[startnode]['right']
   polynodeslist = []

   while not stopcheck:
      columnstopcheck = False
      while not columnstepcheck:
         polypos = [completeref[currentnode]['position']]
         for j in range(0,3):
            currentposition = completeref[currentnode]['position']
            if j = 0:
               nextpos = completeref[currentnode]['up']
               nextposy = completeref[nextpos]['position'][1]
               if nextposy > maxposy:
                  columnstepcheck = True
                  break
            elif j = 1:
               nextpos = completeref[currentnode]['right']
               nextposx = completeref[nextpos]['position'][0]
               if nextposx > maxposx:
                  columnstepcheck = True
                  stopcheck = True
                  break
            elif j = 2:
               nextpos = completeref[currentnode]['down']
            elif j = 3:
               nextpos = completeref[currentnode]['left']
            if j != 3:
               polypos.append(currentposition)
            currentnode = nextpos
         polynodeslist.append(polypos) 
         
      currentnode = nextrowval
      nextrowval = completeref[currentnode]['right']
   return polynodeslist
## end function simple polynode build
      
## construct vertices faces crossings
facecnt = 0
vertcnt = 0
##rules for crossing
##Node have crossing precedent.
##An edge starting from a crossingnode, does not
##have an edge terminating on a non passing neighbor
##crossing node, but may pass into a crossing node
##if positive for crossing, or in other words, all edges
##starting from a crossing node may not have a 4 direction
##radial pattern but instead contingent on the crossing
##positives assigned.
##Crossingnodes and nodes alike have boundary clearance
##direction leeway.  Meaning we can draw a subdivision edge
##in the direction of the nearest boundary, as long as such
##boundary is on a neighboring.
##All edges starting from a node have 4 direction
##radial pattern.
i = 0
faces = []
nopasscrosslist = []
for node in nodes:
   #top crossval = 1, dirswitch = 1
   switches1 = [0,1]
   switches2 = [0,1]
   for switch1 in switches1:
      for switch2 in switches2:
         crosslist = [node] 
         crosslist = checkcross(switch1, node, completeref,
                                switch2, crosslist)
         if len(crosslist) == 1:
            continue
         if switch1 and switch2:
            direction = 'up'
            maxpos = completeref[crosslist[len(crosslist)-1]]['position'][1]
            minpos = completeref[0]['position'][1]
         elif switch1 and not switch2:
            direction = 'down'
            minpos = completeref[crosslist[len(crosslist)-1]]['position'][1]
            maxpos = completeref[0]['position'][1]
         elif not switch1 and switch2:
            direction = 'right'
            maxpos = completeref[crosslist[len(crosslist)-1]]['position'][0]
            minpos = completeref[0]['position'][0]
         else:
            direction = 'left'
            minpos = completeref[crosslist[len(crosslist)-1]]['position'][0]
            maxpos = completeref[0]['position'][0]
         crossendnode = crosslist[len(crosslist)-1]
         if crossendnode == None:
            del crosslist[len(crosslist)-1]
         
         ncheck, nodeindex = checkneighbornode(crosslist, completeref,
                                               nodes, direction)
         if ncheck != None:
            crosslist = crosslist[0:nodeindex+1]
         switch3 = None
         switch4 = None
         direction3 = None
         direction4 = None
         if direction == 'up':
            #right
            switch3 = False
            switch4 = True
            direction3 = 0
            direction4 = 1
         elif direction == 'right':
            #down
            switch3 = True
            swithc4 = False
            direction3 = 1
            direction4 = 0
         elif direction == 'down':
            #left
            switch3 = False
            switch4 = False
            direction3 = 0
            direction4 = 1
         elif direction == 'left':
            #up
            switch3 = True
            switch4 = True
            direction3 = 1
            direction4 = 0
         pnodes = None
         if direction3:
            pnodes = xpnodes
         else:
            pnodes = ypnodes
         cnode = crosslist[len(crosslist)-1]
         crosslist2 = [cnode]
         crosslist2 = checkcross(switch3, cnode, completeref,
                                 switch4, crosslist2)
         if len(crosslist2) == 1:
            continue
         ncolchk, eqcheck, c2nindex = nodecolumncheck(minpos, maxpos,
                                                      pnodes, crosslist2,
                                                      direction3, completeref)
         c2index = None
         if not ncolchk:
            if not eqcheck:
               c2index = c2nindex
            else:
               c2index = c2nindex+1
         else:
            c2index = len(crosslist2)
         crosslist2 = crosslist2[0:c2index]
         cedgepos3 = None
         cedgepos4 = None
         if direction4:
            cedgepos3 = completeref[crosslist2[len(crosslist2)-1]]['position'][0]
            cedgepos4 = completeref[crosslist[0]['position'][1]
         else:
            cedgepos3 = completeref[crosslist2[len(crosslist2)-1]]['position'][1]
            cedgepos4 = completeref[crosslist[0]['position'][0]
         crosslist3 = buildnodesedge(cedgepos3, crosslist, completeref, direction4)
         crosslist4 = buildnodesedge(cedgepos4, crosslist2, completeref, direction3)
         allnodescrosslist = crosslist+crosslist2+crosslist3+crosslist4
         for cnode in allnodescrosslist:
            if not cnode in nopasscrosslist:
               nopasscrosslist.append(cnode)
               
         facegroup = []
         # Two edges of face determined.
         # Build vertices
         
   if crossval:
      
#construct faces and vertices from nodes
for node in nodes:
    
#I get closer to finishing!  Whittling away this little program!
