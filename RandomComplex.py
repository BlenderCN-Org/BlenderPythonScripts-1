## Generate Random Complex K (for circle packing algorithm)
import random
import bpy
## 1rst Generating Random polygon 
##   
## Starting by generating point maxima and minima.
##  In this method, for n>=3, iteratively start by generating 3 points.

## Iterated point procedures randomly chooses an edge, then with minima,
## and maxima constraints picks a point randomly between edge minima and
## maxima, forming a new edge.
## A limit can be placed on subdivisions such that no further subdivision
## of any newly formed edge can take place without the subdivision
## of any older higher Queue priority edges in the randomization process.

MaxSize = 10
PolygonSize = 20  ## must be 3 or higher

def clockwisewalktest(walk):
    ## works with nonconvex polygons should be safe
    ## I believe for the primitive polygon type (3 vertices)
    ## constructed in this algorithm.
    prev = None
    samt = 0.0
    newwalk = walk[0:len(walk)]
    newwalk.append(walk[0])
    for vert in newwalk:
        if prev == None:
            prev = vert
            continue
##        samt += (vert[0]-prev[0])*(vert[1]+prev[1])
        samt += (prev[0]*vert[1]-prev[1]*vert[0])
##        if walk.index(vert) == len(walk)-1:
##            samt += (walk[0][0] - vert[0])*(walk[0][1]+vert[1])
        prev = vert
    print('samt: ', samt)
    if samt < 0:
        print('original walk is clockwise')
        return True
    else:
        print('original walk is counter clockwise')
        return False

def polygonwalk(vert,last,target,vedges, walk):
    for edge in vedges[vert]:
        va, vb = edge
        prev = vert
        nextv = None
        if va == vert:
            if vb != last:
                walk.append(vb)
                if vb != target:
                    nextv = vb
                    polygonwalk(nextv,prev,target,vedges,walk)

        else:
            if va != last:
                walk.append(va)
                if va != target:
                    nextv = va
                    polygonwalk(nextv,prev,target,vedges,walk)
def convextest(v1,v2,v3,v4):
    def crossproduct(p1,p2):
        return (p1[0]*p2[1] - p1[1]*p2[0])
    ## assumed v1,v2,v3,v4 are sequentially ordered on the
    ##polygon walk
    ## this is cross product comparison
    t1 = crossproduct(v1,v2) == crossproduct(v2,v3)
    t2 = crossproduct(v3,v4) == crossproduct(v1,v2)
    if t1 and t2:
        return True
    else:
        return False
    

def generateRandomVertex():
    return (random.random()*MaxSize, random.random()*MaxSize)

def generateRandomVertexMM(minX,maxX,minY,maxY):
    return (random.uniform(minX,maxX),random.uniform(minY,maxY))

def cubicInterpolate (p, x):
    return p[1] + 0.5 * x*(p[2] - p[0] + x*(2.0*p[0] - 5.0*p[1] + 4.0*p[2] - p[3] + x*(3.0*(p[1] - p[2]) + p[3] - p[0])))

def distance(a,b):
    ax,ay = a
    bx,by = b
    return ((ax-bx)**2+(ay-by)**2)**.5

def getMinMax(edge):
    edgex = edge[0:len(edge)]
    edgey = edge[0:len(edge)]
    edgex = list(edgex)
    edgey = list(edgey)
    edgex.sort(key = lambda tup:tup[0])
    edgey.sort(key = lambda tup:tup[1])
    minx = edgex[0][0]
    maxx = edgex[1][0]
    miny = edgey[0][1]
    maxy = edgey[1][1]
    return (minx,maxx,miny,maxy)

def getXScale(minx,maxx):
    return 1.0/abs(maxx-minx)

def scale(scale, points):
    rpoints = []
    for point in points:
        rpoints.append((scale*point[0], scale*point[1]))
    return rpoints

def translateX(tr, points):
    rpoints = []
    for point in points:
        rpoints.append((tr + point[0], point[1]))
    return rpoints

def slope(edge):
    a, b = edge
    ax,ay = a
    bx,by = b
    return (by - ay)/(bx - ax)

def midpoint(edge):
    a,b = edge
    return ((a[0]+b[0])/2,(a[1]+b[1])/2)

def slopenormal(edgeslope):
    return - 1/edgeslope

def testdirection(edge1, edge2):
    #assumed edge1 = (a,b) and edge2 = (b,c)
    # where b intersect edge 1 and 2
    a,b = edge1
    b,c = edge2
    if c > b:
        if a > b:
            return False
        else:
            return True
    else:
        if a > b:
            return True
        else:
            return False

def setRotation(edge, rotheir):
    ## closest distance to walk pair root determines
    ## direction of the vector
    root = rotheir[edge]
    ra, rb = root
    rbx, rby = rb
    rax, ray = ra
    vec = [rbx-rax, rby-ray]
##    a,b = edge
##    ax,ay = a
##    bx,by = b
##    ## find which vertex is closest to root a
##    dara = distance(a,ra)
##    dbra = distance(b,ra)
##    if dara < dbra:
##    vec = [bx-ax, by-ay]
##    else:
##    vec = [ax-bx, ay-by]
    ## 90 degree rotation
    print('ab vector: ', vec)
    vec = [-vec[1], vec[0]]
    print('rotation edge: ', edge)
    print('rotation vector: ', vec)
    return vec

def getY(point, slope, x):
    return slope*(x - point[0]) + point[1]

def getneighborverts(edge,vedges):
    a,b = edge
    n1 = None
    n2 = None
    ne1 = None
    ne2 = None
    for nedge in vedges[a]:
        if edge != nedge:
            na,nb = nedge
            ne1 = nedge
            if na == a:
                n1 = nb
            else:
                n1 = na
    for nedge in vedges[b]:
        if edge != nedge:
            na,nb = nedge
            ne2 = nedge
            if na == b:
                n2 = nb
            else:
                n2 = na
    return n1,n2,ne1,ne2
    

def updateEdges(a,b,edges,dedge,vedges):
    edges.append((a,b))
    d = distance(a,b)
    if d in dedge:
        dedge[d].append((a,b))
    else:
        dedge[d] = [(a,b)]
    if a in vedges:
        vedges[a].append((a,b))
    else:
        vedges[a] = [(a,b)]
    if b in vedges:
        vedges[b].append((a,b))
    else:
        vedges[b] = [(a,b)]

def updateRotatheir(edge, parent, rotheir):
    root = rotheir[parent]
    ra, rb = root
    a,b = edge
    ax,ay = a
    bx,by = b
    ## find which vertex is closest to root a
    dara = distance(a,ra)
    dbra = distance(b,ra)
    if dara < dbra:
        rotheir[edge] = (a,b)
    else:
        rotheir[edge] = (b,a)

def deleteEdge(edge,edges,dedge,vedges):
    a,b = edge
    d = distance(a,b)
    edges.remove(edge)
    dedge[d].remove(edge)
    if len(dedge[d]) == 0:
        del dedge[d]
##    print(edge)
##    print(vedges)
    vedges[a].remove(edge)
    vedges[b].remove(edge)

edgecount = 0
vertices = []
edges = []
dedge = {}
vedges = {}
edged = {}
rotheir = {}
for i in range(0,3):
    vertices.append(generateRandomVertex())
    if len(vertices) > 0 and len(vertices) != 1:
        a = vertices[0]
        b = vertices[len(vertices)-1]
        updateEdges(a,b,edges,dedge,vedges)
        rotheir[(a,b)] = (a,b)

    edgecount += 1
a = vertices[2]
b = vertices[1]
updateEdges(a,b,edges,dedge,vedges)
rotheir[(a,b)] = (a,b)
edgecount += 1

## create walk order used in determining rotations
verts = list(vedges.keys())
print(vedges)
a = verts[0]
print('a',a)
tedge = vedges[a][0]
last = None
target = None
walk = [a]
print('walk:', walk)
for vert in tedge:
    if vert != a:
        target = vert
        last = vert
polygonwalk(a,last,target,vedges,walk)

print('original walk: ', walk)
newwalk = []
if not clockwisewalktest(walk):
    walk0 = walk[0]
    walk1 = walk[1:len(walk)]
    walk1 = walk1[::-1]  ## reverse the order for clockwise
    newwalk.append(walk0)
    newwalk += walk1
    walk = newwalk
    
print('rotation order walk: ', walk)

def setrotatheirorder(walk, rotheir):
    prev = None
    for vert in walk:
        if prev == None:
            prev = vert
            continue
        print('vert,prev pair: ', (vert,prev))
        if (vert, prev) in rotheir:
            print('found rev order rotheir key')
            print('vert,prev pair: ', (vert,prev))
            rotheir[(vert,prev)] = (prev,vert)
        if walk.index(vert) == len(walk)-1:
            if (walk[0], vert) in rotheir:
                rotheir[(walk[0],vert)] = (vert,walk[0])
        prev = vert

setrotatheirorder(walk,rotheir)
print('rotheir: ', rotheir)

Q = []
edgec = 0
print(dedge)
qedges = None
pedge = None
parents = []
i = 0
while (edgecount < PolygonSize+1):
    if len(Q) == 0:
       ##fill Q
       ##edgescopy = edges[0:len(edges)]
       ##random.shuffle(edgescopy)
       edgekeys = list(dedge.keys())
       edgekeys.sort(reverse = True)
       Q = edgekeys
       i += 1
    if edgec == 0:
        qedges = dedge[Q[0]][0:len(dedge[Q[0]])]   
        pedge = dedge[Q[0]][edgec]
    else:
        pedge = qedges[edgec]
    minx,maxx,miny,maxy = getMinMax(pedge)
    ##nvert = generateRandomVertexMM(minx,maxx,miny,maxy)
    x = (maxx+minx)/2.0
    n1,n2,ne1,ne2 = getneighborverts(pedge,vedges)
##    if testdirection(ne1,pedge) and testdirection(pedge,ne2):
    if 1 == 0:
        a,b = pedge
        xscale = getXScale(minx,maxx)
    ##    print('n1:',n1)
    ##    print('n2:', n2)
    ##    print('ne1:', ne1)
    ##    print('ne2:', ne2)

        p = [n1,a,b,n2]
        ## we need to set up interpolation which means scaling
        ## and translating positions to end up on interval [0,1]
        ## for p1 and p2, will also need to compute position x =-1
        ## for p0 at y.
        p = scale(xscale, p)
        tr = -minx*xscale
        sxt = xscale*x+tr
        p = translateX(tr, p)
        if p[1][0] != 0.0:
            p = [p[3],p[2],p[1],p[0]]
        ne1 = (p[0],p[1])
        ne2 = (p[2],p[3])
        sne1 = slope(ne1)
        sne2 = slope(ne2)
        ny1 = getY(p[0], sne1, -1)
        ny2 = getY(p[3], sne2, 2)
        print('ny1:', ny1)
        print('ny2:', ny2)
        print('p:',p)
        py = [ny1,p[1][1],p[2][1],ny2]
        syt = cubicInterpolate (py, sxt)
        ##rescale y back to original coordinate
        ## note: we don't worry about retranslating since this isn't an xcoordinate
        y = syt*1/xscale
    else:
        mpoint = midpoint(pedge)
##        pslope = slope(pedge)
##        nslope = slopenormal(pslope)
        rvec = setRotation(pedge, rotheir)
##        y = getY(pedge[0], pslope, x)
        x, y = mpoint
        print('y at midpoint: ', y)
        x = x + rvec[0]/(3.5) ##+ i)
        y = y + rvec[1]/(3.5 )##+ i)
    vertices.append((x,y))
    nvert = (x,y)
    updateEdges(pedge[0],nvert,edges,dedge,vedges)
    updateEdges(pedge[1],nvert,edges,dedge,vedges)

    deleteEdge(pedge,edges,dedge,vedges)
    nedge1 = (pedge[0],nvert)
    nedge2 = (pedge[1],nvert)
    updateRotatheir(nedge1, pedge, rotheir)
    updateRotatheir(nedge2, pedge, rotheir)
    del rotheir[pedge]
    edgecount += 1
    print('Q[0]', Q[0])
    print('qedges', qedges)
    print('length qedges - 1: ',len(qedges)-1)
    if edgec == len(qedges)-1:
        del Q[0]
        edgec = 0
    else:    
        edgec += 1




verts = list(vedges.keys())
print(vedges)
a = verts[0]
print('a',a)
tedge = vedges[a][0]
last = None
target = None
walk = [a]
print('walk:', walk)
for vert in tedge:
    if vert != a:
        target = vert
        last = vert
polygonwalk(a,last,target,vedges,walk)
face = []
for vert in walk:
    face.append(vertices.index(vert))
bvertices = []
for vert in vertices:
    x,y = vert
    bvertices.append((x,y,0.0))
faces = []
faces.append(tuple(face))
meshName = "Polygon"
obName = "PolygonObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(bvertices,[],faces)      
me.update(calc_edges=True) 
