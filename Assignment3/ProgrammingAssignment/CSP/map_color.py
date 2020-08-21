# R is a set of restrictions
# this functions colors the given province with the given color
# returns false if not possible, returns the set of new restrictions if possible
def addColor(R, province, color):
    ans = []
    for rr in R:
        res = checkRestriction(rr, province, color)
        if res == False:
            return False
        elif res == None:
            continue
        else:
            ans.append(res)
    return ans


# checks if the restrition rr allows the given province to have the given color
# returns false if not possible, otherwise returns the new restriction
def checkRestriction(rr, province, color):
    # finding the index of the province (saved to index)
    index = -1
    other = -1
    if rr[0] == province:
        index = 0
        other = 1
    elif rr[1] == province:
        index = 1
        other = 0
    else:
        return rr

    if isinstance(rr[other], int):
        # other component is a color
        if (color != rr[other]):
            return None
        else:
            return False
    else:
        return [rr[other], color]

colormap = {}
# solving the CSP by variable elimination
# recursive structure: ci is the province index to be colored (0 = bc, 1 = ab, etc)
# n is the number of colors
# provinces is a list of provinces
# if coloring is possible returns the province-> color map, otherwise False
# for 3 colors outputs should be like {'ab': 1, 'bc': 2, 'mb': 1, 'nb': 1, 'ns': 2, 'nl': 1, 'nt': 3, 'nu': 2, 'on': 2, 'pe': 3, 'qc': 3, 'sk': 2, 'yt': 1}
def solveCSP(provinces, n, R, ci):
    # no choice for the current province
    #print(colors)
    #print(provinces)
    #print(R)
    #for province in provinces:
    #    for color in colors:
    #        print(addColor(R,province,color))3

    #   print(R)
    #   x = addColor(R,provinces[ci],1)
    #   print(x)

    #   y = addColor(x,provinces[ci+1],2)
    #   print(y)

    #   z = addColor(y,provinces[ci+2],1)
    #   print(z)

    #   a = addColor(z,provinces[ci+3],1)
    #   print(a)

    #   b = addColor(a,provinces[ci+4],2)
    #   print(b)

    #   c = addColor(b,provinces[ci+5],1)
    #   print(c)

    #   d = addColor(c,provinces[ci+6],3)
    #   print(d)

    #   e = addColor(d,provinces[ci+7],2)
    #   print(e)

    #   f = addColor(e,provinces[ci+8],2)
    #   print(f)

    #   g = addColor(f,provinces[ci+9],3)
    #   print(g)

    #   h = addColor(g,provinces[ci+10],3)
    #   print(h)

    #   i = addColor(h,provinces[ci+11],2)
    #   print(i)

    #   j = addColor(i,provinces[ci+12],1)
    #print(j)
    global colormap
    if ci == len(provinces) and ci == len(colormap):
        return colormap
    if ci == len(provinces) and ci !=  len(colormap):
        return "More Colors Required"
    else:
        colors = []
        for i in range(1, n + 1):
            colors.append(i)
        #while ci < len(provinces):
        for color in colors:
            if addColor(R,provinces[ci],color) is not None and addColor(R, provinces[ci], color) is not False:
                R = addColor(R, provinces[ci],color)
                colormap[provinces[ci]] = color
                break
        return solveCSP(provinces,n,R,ci+1)

# main program starts
# ===================================================

n = 5  # int(input("Enter the number of color"))
colors = []
for i in range(1, n + 1):
    colors.append(i)
#print(colors)

# creating map of canada
# cmap[x] gives the neighbors of the province x
cmap = {}
cmap["ab"] = ["bc", "nt", "sk"]
cmap["bc"] = ["yt", "nt", "ab"]
cmap["mb"] = ["sk", "nu", "on"]
cmap["nb"] = ["qc", "ns", "pe"]
cmap["ns"] = ["nb", "pe"]
cmap["nl"] = ["qc"]
cmap["nt"] = ["bc", "yt", "ab", "sk", "nu"]
cmap["nu"] = ["nt", "mb"]
cmap["on"] = ["mb", "qc"]
cmap["pe"] = ["nb", "ns"]
cmap["qc"] = ["on", "nb", "nl"]
cmap["sk"] = ["ab", "mb", "nt"]
cmap["yt"] = ["bc", "nt"]

# CSP restrictions
# each restriction is modeled as a pair [a,b] which means the province a's
# color is not equal to b, where b is either a color (a number 1 to n) or
# another province. Examples ['bc', 'ab'] means the color of bc should
# not be equal to ab -- ["bc",4] means the color of bc should not be 4
# R is the list of restrictions

R = []

# initiaitiong restrictions based on the province neighborhood

for x in cmap:
    for y in cmap[x]:
        R.append([x, y])

# initiating a list of provinces
provinces = []
for p in cmap:
    provinces.append(p)



while (1):
    num = int(input("Enter number of  colors? "))
    print(solveCSP(provinces, num, R, 0))

