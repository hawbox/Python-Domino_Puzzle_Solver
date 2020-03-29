import copy



def dominos(d):
    ld=[]
    for n in range(d+1):
        for n2 in range(n+1):
            ld+=[[str(n2),str(n)]]
    return ld
def print_format(g):
    s='+-'*len(g[0])+'+\n'
    for i in range(len(g)):
        s2='+'
        for j in range(len(g[0])):
            c=g[i][j]
            if j==0:s+='|'
            else:s+=c[1][1]
            if i<len(g)-1:s2+=c[1][0]+'+'
            else:s2+='-+'
            s+=c[0]
        s+='|\n'
        s+=s2+'\n'
    return s[:-1]
def index(g,x,y):return -1<x<len(g[0])and -1<y<len(g)
def occ(g,d):
    occ=[]
    chk=[]
    for y in range(len(g)):
        for x in range(len(g[0])):
            if [x,y] not in chk and g[y][x][0]==d[0]:
                if index(g,x,y-1)and g[y-1][x][0]==d[1]and g[y-1][x][1][0]==' ':occ.append([[x,y],[x,y-1],d]);chk+=[[x,y],[x,y-1]]
                if index(g,x+1,y)and g[y][x+1][0]==d[1]and g[y][x+1][1][1]==' ':occ.append([[x,y],[x+1,y],d]);chk+=[[x,y],[x+1,y]]
                if index(g,x,y+1)and g[y+1][x][0]==d[1]and g[y][x][1][0]==' ':occ.append([[x,y],[x,y+1],d]);chk+=[[x,y],[x,y+1]]
                if index(g,x-1,y)and g[y][x-1][0]==d[1]and g[y][x][1][1]==' ':occ.append([[x,y],[x-1,y],d]);chk+=[[x,y],[x-1,y]]
    return occ
def remove(g,d,dom,d_doms):
    dom.remove(d[2])
    d_doms+=d[:2]
    a1,a2,b1,b2=d[0][0],d[0][1],d[1][0],d[1][1]
    x,y=b1-a1,b2-a2
    if x==1:
        g[a2][a1][1]=['-','|']
        g[b2][b1][1][0]='-'
        if index(g,a1,a2-1):g[a2-1][a1][1][0]='-'
        if index(g,b1,b2-1):g[b2-1][b1][1][0]='-'
        if index(g,b1+1,b2):g[b2][b1+1][1][1]='|'
    if x==-1:
        g[b2][b1][1]=['-','|']
        g[a2][a1][1][0]='-'
        if index(g,b1,b2-1):g[b2-1][b1][1][0]='-'
        if index(g,a1,a2-1):g[a2-1][a1][1][0]='-'
        if index(g,a1+1,a2):g[a2][a1+1][1][1]='|'
    if y==1:
        g[a2][a1][1][1]='|'
        g[b2][b1][1]=['-','|']
        if index(g,b1+1,b2):g[b2][b1+1][1][1]='|'
        if index(g,a1+1,a2):g[a2][a1+1][1][1]='|'
        if index(g,a1,a2-1):g[a2-1][a1][1][0]='-'
    if y==-1:
        g[b2][b1][1][1]='|'
        g[a2][a1][1]=['-','|']
        if index(g,a1+1,a2):g[a2][a1+1][1][1]='|'
        if index(g,b1+1,b2):g[b2][b1+1][1][1]='|'
        if index(g,b1,b2-1):g[b2-1][b1][1][0]='-'
    return g,dom,d_doms
def wall_cnt(g,x,y):
    w=0
    w_=[]
    if (index(g,x,y-1)and g[y-1][x][1][0]=='-')or not index(g,x,y-1):w+=1
    elif index(g,x,y-1):w_+=[[x,y-1,0]]
    if (index(g,x+1,y)and g[y][x+1][1][1]=='|')or not index(g,x+1,y):w+=1
    elif index(g,x+1,y):w_+=[[x+1,y,1]]
    if g[y][x][1][0]=='-':w+=1
    elif index(g,x,y+1):w_+=[[x,y+1,2]]
    if g[y][x][1][1]=='|':w+=1
    elif index(g,x-1,y):w_+=[[x-1,y,3]]
    return [w,w_]
def solve(grid,dom):
    W,H=len(grid[0]),len(grid)
    d_doms=[]
    if type(grid[0][0])!=list:
        g=[]
        [[g.append([]),[g[i].append([grid[i][j],[' ',' ']])for j in range(W)]] for i in range(H)]
    else:
        g=grid
        del grid
    while True:
        done=True
        #M1
        rm_l=[]
        [rm_l.append(occ(g,d)[0]) for d in dom if len(occ(g,d))==1]
        for r in rm_l:g,dom,d_doms=remove(g,r,dom,d_doms);done=False
        #M2
        for y in range(H):
            for x in range(W):
                if [x,y] not in d_doms:
                    w=wall_cnt(g,x,y)[1]
                    for d in w:
                        if [g[y][x][0],g[d[1]][d[0]][0]] not in dom and [g[d[1]][d[0]][0],g[y][x][0]] not in dom:
                            if d[2]==0 and index(g,x,y-1):g[y-1][x][1][0]='-'
                            elif d[2]==1 and index(g,x+1,y):g[y][x+1][1][1]='|'
                            elif d[2]==2:g[y][x][1][0]='-'
                            elif d[2]==3:g[y][x][1][1]='|'
        #M3
        """for y in range(H):
            for x in range(W):
                if [x,y] not in d_doms:
                    if 4-wall_cnt(g,x,y)[0]>1:
                        w=wall_cnt(g,x,y)[1]
                        exit_=False
                        for opt in w:
                            if not exit_:
                                g_,dom_,d_doms_=copy.deepcopy(g),copy.deepcopy(dom),copy.deepcopy(d_doms)
                                d=[g[y][x][0],g[opt[1]][opt[0]][0]]
                                if d not in dom:d.reverse()
                                if d in dom:
                                    s=solve(*remove(g_,[[x,y],opt[:2],d],dom_,d_doms_)[:2])
                                    if len(s[0])==0:exit_=True
                                    if exit_:g,dom,d_doms=remove(g,[[x,y],opt[:2],d],dom,d_doms);done=False
                                else:
                                    if opt[2]==0 and index(g,x,y-1):g[y-1][x][1][0]='-'
                                    elif opt[2]==1 and index(g,x+1,y):g[y][x+1][1][1]='|'
                                    elif opt[2]==2:g[y][x][1][0]='-'
                                    elif opt[2]==3:g[y][x][1][1]='|'
                                d=[g[y][x][0],g[opt[1]][opt[0]][0]]
                                if d not in dom_:d.reverse()
                                if d in dom:
                                    g_,dom_,d_doms_=remove(g_,[[x,y],opt[:2],d],dom_,d_doms_)
                                    p=[]
                                    exit_=True
                                    for d in dom_:
                                        o=occ(g_,d)
                                        if len(o)==1 and o[0][:2] in p:exit_=False
                                        else:
                                            b=False
                                            for a in o:
                                                if a[:2] not in p:p+=a[:2];b=True
                                            if not b:exit_=False
                                     if exit_:g,dom,d_doms=remove(g,[[x,y],opt[:2],d],dom,d_doms);done=False
                                else:
                                    if opt[2]==0 and index(g,x,y-1):g[y-1][x][1][0]='-'
                                    elif opt[2]==1 and index(g,x+1,y):g[y][x+1][1][1]='|'
                                    elif opt[2]==2:g[y][x][1][0]='-'
                                    elif opt[2]==3:g[y][x][1][1]='|'"""
        #M4
        for d in dom:
            if len(occ(g,d))>0:
                o=occ(g,d)
                a=[]
                for p in o:a+=p[:2]
                if a.count(a[0])==len(o):
                    x,y=a[0][0],a[0][1]
                    for w in wall_cnt(g,x,y)[1]:
                        if g[w[1]][w[0]][0]!=d[1]:
                            if w[2]==0 and index(g,x,y-1):g[y-1][x][1][0]='-'
                            elif w[2]==1 and index(g,x+1,y):g[y][x+1][1][1]='|'
                            elif w[2]==2:g[y][x][1][0]='-'
                            elif w[2]==3:g[y][x][1][1]='|'
                elif a.count(a[1])==len(o):
                    x,y=a[1][0],a[1][1]
                    for w in wall_cnt(g,x,y)[1]:
                        if g[w[1]][w[0]][0]!=d[0]:
                            if w[2]==0 and index(g,x,y-1):g[y-1][x][1][0]='-'
                            elif w[2]==1 and index(g,x+1,y):g[y][x+1][1][1]='|'
                            elif w[2]==2:g[y][x][1][0]='-'
                            elif w[2]==3:g[y][x][1][1]='|'
        #M5
        #M6
        for y in range(H):
            for x in range(W):
                if index(g,x,y+1) and (g[y][x][1][1]=='|' or x==0) and((index(g,x,y-1)and g[y-1][x][1][0]=='-') or (not index(g,x,y-1))) and ((index(g,x+1,y)and g[y][x+1][1][1]=='|') or (not index(g,x+1,y))):
                    d=False
                    if [g[y][x][0],g[y+1][x][0]] in dom:d=[g[y][x][0],g[y+1][x][0]]
                    if [g[y+1][x][0],g[y][x][0]] in dom:d=[g[y+1][x][0],g[y][x][0]]
                    if d:g,dom,d_doms=remove(g,[[x,y],[x,y+1],d],dom,d_doms);done=False
                if index(g,x,y-1) and (g[y][x][1][1]=='|' or x==0) and (g[y][x][1][0]=='-' or y==H-1) and((index(g,x+1,y)and g[y][x+1][1][1]=='|') or (not index(g,x+1,y))):
                    d=False
                    if [g[y][x][0],g[y-1][x][0]] in dom:d=[g[y][x][0],g[y-1][x][0]]
                    if [g[y-1][x][0],g[y][x][0]] in dom:d=[g[y-1][x][0],g[y][x][0]]
                    if d:g,dom,d_doms=remove(g,[[x,y],[x,y-1],d],dom,d_doms);done=False
                if index(g,x+1,y) and (g[y][x][1][1]=='|' or x==0) and (g[y][x][1][0]=='-' or y==H-1) and((index(g,x,y-1)and g[y-1][x][1][0]=='-') or (not index(g,x,y-1))):
                    d=False
                    if [g[y][x][0],g[y][x+1][0]] in dom:d=[g[y][x][0],g[y][x+1][0]]
                    if [g[y][x+1][0],g[y][x][0]] in dom:d=[g[y][x+1][0],g[y][x][0]]
                    if d:g,dom,d_doms=remove(g,[[x,y],[x+1,y],d],dom,d_doms);done=False
                if index(g,x-1,y) and (g[y][x][1][0]=='-' or y==H-1) and((index(g,x,y-1)and g[y-1][x][1][0]=='-') or (not index(g,x,y-1))) and ((index(g,x+1,y)and g[y][x+1][1][1]=='|') or (not index(g,x+1,y))):
                    d=False
                    if [g[y][x][0],g[y][x-1][0]] in dom:d=[g[y][x][0],g[y][x-1][0]]
                    if [g[y][x-1][0],g[y][x][0]] in dom:d=[g[y][x-1][0],g[y][x][0]]
                    if d:g,dom,d_doms=remove(g,[[x,y],[x-1,y],d],dom,d_doms);done=False
        if done:break
    return [dom,g,print_format(g)]
if __name__=='__main__':
    #g=['304022','141432','130221','010333','214044'];d=dominos(4)
    #g=['064150165','121663757','164222710','432665634','014023635','373252075','521743477','450041703'];d=dominos(6)
    #g=['1370158430','5752704883','4702755234','4268873600','6106122671','6535817401','5241276853','4261880463','6514378302'];d=dominos(8)
    g=['57420004554','33960773219','71640263397','52516875993','92634381490','38290517845','05288460846','88674627936','30111765912','97185412082'];d=dominos(9)
    s=solve(g,d)
    print(f'{len(s[0])}\n{s[2]}\n{s[0]}')
