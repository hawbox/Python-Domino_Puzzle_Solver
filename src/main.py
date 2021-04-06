import random



def print_board(b,dm=None):
	def set_char(s,i,c):
		if (s[i]=="+"):return s
		return s[:i]+c+s[i+1:]
	w=len(b[0])
	h=len(b)
	s="+"+"-"*(2*w-1)+"+\n"
	for i in range(0,h):
		s+="|"
		for j in range(0,w):
			s+=b[i][j]+" "
		s=s[:len(s)-1]+"|\n|"+"  "*w
		s=s[:len(s)-1]+"|\n"
	s=s[:len(s)-w*2-2]+"+"+"-"*(2*w-1)+"+"
	if (dm is None):
		print(s+"\n")
	else:
		s=s.split("\n")
		for d in dm:
			s[d["p1"][1]*2]=set_char(s[d["p1"][1]*2],d["p1"][0]*2,"+")
			s[d["p1"][1]*2]=set_char(s[d["p1"][1]*2],d["p1"][0]*2+1,"-")
			s[d["p1"][1]*2+1]=set_char(s[d["p1"][1]*2+1],d["p1"][0]*2,"|")
			if (d["p1"][0]<d["p2"][0]):
				s[d["p1"][1]*2+2]=set_char(s[d["p1"][1]*2+2],d["p1"][0]*2,"+")
				s[d["p1"][1]*2]=set_char(s[d["p1"][1]*2],d["p1"][0]*2+4,"+")
				s[d["p1"][1]*2+2]=set_char(s[d["p1"][1]*2+2],d["p1"][0]*2+4,"+")
				s[d["p1"][1]*2]=set_char(s[d["p1"][1]*2],d["p1"][0]*2+1,"-")
				s[d["p1"][1]*2]=set_char(s[d["p1"][1]*2],d["p1"][0]*2+2,"-")
				s[d["p1"][1]*2]=set_char(s[d["p1"][1]*2],d["p1"][0]*2+3,"-")
				s[d["p1"][1]*2+2]=set_char(s[d["p1"][1]*2+2],d["p1"][0]*2+1,"-")
				s[d["p1"][1]*2+2]=set_char(s[d["p1"][1]*2+2],d["p1"][0]*2+2,"-")
				s[d["p1"][1]*2+2]=set_char(s[d["p1"][1]*2+2],d["p1"][0]*2+3,"-")
				s[d["p1"][1]*2+1]=set_char(s[d["p1"][1]*2+1],d["p1"][0]*2+4,"|")
			else:
				s[d["p1"][1]*2+4]=set_char(s[d["p1"][1]*2+4],d["p1"][0]*2,"+")
				s[d["p1"][1]*2]=set_char(s[d["p1"][1]*2],d["p1"][0]*2+2,"+")
				s[d["p1"][1]*2+4]=set_char(s[d["p1"][1]*2+4],d["p1"][0]*2+2,"+")
				s[d["p1"][1]*2+1]=set_char(s[d["p1"][1]*2+1],d["p1"][0]*2,"|")
				s[d["p1"][1]*2+2]=set_char(s[d["p1"][1]*2+2],d["p1"][0]*2,"|")
				s[d["p1"][1]*2+3]=set_char(s[d["p1"][1]*2+3],d["p1"][0]*2,"|")
				s[d["p1"][1]*2+1]=set_char(s[d["p1"][1]*2+1],d["p1"][0]*2+2,"|")
				s[d["p1"][1]*2+2]=set_char(s[d["p1"][1]*2+2],d["p1"][0]*2+2,"|")
				s[d["p1"][1]*2+3]=set_char(s[d["p1"][1]*2+3],d["p1"][0]*2+2,"|")
				s[d["p1"][1]*2+4]=set_char(s[d["p1"][1]*2+4],d["p1"][0]*2+1,"-")
		print("\n".join(s))
def print_dominos(dl):
	for  d in dl:
		print(str(d[0])+"|"+str(d[1]))



def random_board(s):
	def set_char(s,i,c):
		return s[:i]+c+s[i+1:]
	b=[" "*(s+1)]*s
	dominos=[]
	for n in range(s):
		for n2 in range(s):
			if ([n2,n] in dominos):continue
			dominos+=[[n,n2]]
	random.shuffle(dominos)
	x,y=0,0
	while (len(dominos)>0):
		while (x>s or b[y][x]!=" "):
			x+=1
			if (x>s):
				x=0
				y+=1
		d=random.randint(0,1)
		if (random.randint(0,1)==0):
			dominos[0].reverse()
		move=False
		for e in range(0,2):
			if (d==0):
				if (x+1<=s and b[y][x+1]==" "):
					b[y]=set_char(b[y],x,str(dominos[0][0]))
					b[y]=set_char(b[y],x+1,str(dominos[0][1]))
					dominos.remove(dominos[0])
					move=True
					break
			if (d==1):
				if (y+1<s and b[y+1][x]==" "):
					b[y]=set_char(b[y],x,str(dominos[0][0]))
					b[y+1]=set_char(b[y+1],x,str(dominos[0][1]))
					dominos.remove(dominos[0])
					move=True
					break
			d=1-d
		if (move==False):
			return random_board(s)
	return b



def solve_board(b,log=False,dt=None):
	def copy_data(dominos,dl,done_tiles):
		dt=[[],[],[]]
		for d in dominos:
			dt[0].append({"d":[d["d"][0],d["d"][1]],"p1":[d["p1"][0],d["p1"][1]],"p2":[d["p2"][0],d["p2"][1]]})
		for d in dl:
			dt[1].append([d[0],d[1]])
		for t in done_tiles:
			dt[2].append([t[0],t[1]])
		return dt
	def step1(b,done_tiles,w,h,dominos,dl):
		le=[]
		for x in range(0,w):
			for y in range(0,h):
				if ([x,y] in done_tiles):continue
				if (x+1<w and [x+1,y] not in done_tiles and [min(int(b[y][x]),int(b[y][x+1])),max(int(b[y][x]),int(b[y][x+1]))] in dl):
					le+=[[[min(int(b[y][x]),int(b[y][x+1])),max(int(b[y][x]),int(b[y][x+1]))],x,y,x+1,y]]
				if (y+1<h and [x,y+1] not in done_tiles and [min(int(b[y][x]),int(b[y+1][x])),max(int(b[y][x]),int(b[y+1][x]))] in dl):
					le+=[[[min(int(b[y][x]),int(b[y+1][x])),max(int(b[y][x]),int(b[y+1][x]))],x,y,x,y+1]]
		empty=[]
		done=[]
		for dp in le:
			if (dp[0] in done):
				for k in empty:
					if (k["d"]==dp[0]):
						empty.remove(k)
			else:
				done.append(dp[0])
				empty.append({"d":dp[0],"p1":dp[1:3],"p2":dp[3:5]})
		for t in empty:
			done_tiles+=[[t["p1"][0],t["p1"][1]],[t["p2"][0],t["p2"][1]]]
			dl.remove(t["d"])
		dominos+=empty
		return (len(empty)>0)
	def step2(b,done_tiles,w,h,dominos,dl):
		l=[]
		for x in range(0,w):
			for y in range(0,h):
				if ([x,y] in done_tiles):continue
				s=0
				d=0
				i=0
				for da in [[-1,0],[0,-1],[1,0],[0,1]]:
					nx,ny=x+da[0],y+da[1]
					if (nx<0 or nx>=w or ny<0 or ny>=h or [nx,ny] in done_tiles or [min(int(b[y][x]),int(b[ny][nx])),max(int(b[y][x]),int(b[ny][nx]))] not in dl):
						s+=1
					else:
						d=i+0
					i+=1
				if (s==3):
					l+=[[x,y,d]]
		rmd=[]
		done=[]
		for dp in l:
			if (dp[:2] in done):
				for k in rmd:
					if (rmd["p1"][0]==dp[0] and rmd["p1"][1]==dp[1]):
						rmd.remove(k)
			else:
				done.append(dp[:2])
				dr=[[-1,0],[0,-1],[1,0],[0,1]][dp[2]]
				rmd.append({"d":[min(int(b[dp[1]][dp[0]]),int(b[dp[1]+dr[1]][dp[0]+dr[0]])),max(int(b[dp[1]][dp[0]]),int(b[dp[1]+dr[1]][dp[0]+dr[0]]))],"p1":[min(dp[0],dp[0]+dr[0]),min(dp[1],dp[1]+dr[1])],"p2":[max(dp[0],dp[0]+dr[0]),max(dp[1],dp[1]+dr[1])]})
		for t in rmd:
			if (t["d"] not in dl):continue
			done_tiles+=[[t["p1"][0],t["p1"][1]],[t["p2"][0],t["p2"][1]]]
			dl.remove(t["d"])
			dominos.append(t)
		return (len(rmd)>0)
	def step3(b,done_tiles,w,h,dominos,dl):
		for x in range(0,w):
			for y in range(0,h):
				if ([x,y] in done_tiles):continue
				s=0
				d=[]
				i=0
				for da in [[-1,0],[0,-1],[1,0],[0,1]]:
					nx,ny=x+da[0],y+da[1]
					if (nx<0 or nx>=w or ny<0 or ny>=h or [nx,ny] in done_tiles or [min(int(b[y][x]),int(b[ny][nx])),max(int(b[y][x]),int(b[ny][nx]))] not in dl):
						s+=1
					else:
						d+=[i]
					i+=1
				if (s==2):
					for dr in d:
						dr=[[-1,0],[0,-1],[1,0],[0,1]][dr]
						dt=copy_data(dominos,dl,done_tiles)
						m={"d":[int(min(b[y][x],b[y+dr[1]][x+dr[0]])),int(max(b[y][x],b[y+dr[1]][x+dr[0]]))],"p1":[min(x,x+dr[0]),min(y,y+dr[1])],"p2":[max(x,x+dr[0]),max(y,y+dr[1])]}
						dt[0].append(m)
						dt[1].remove(m["d"])
						dt[2]+=[[m["p1"][0],m["p1"][1]],[m["p2"][0],m["p2"][1]]]
						s,_,_=solve_board(b,dt=dt)
						if (s==True):
							dominos.append(m)
							dl.remove(m["d"])
							done_tiles+=[[m["p1"][0],m["p1"][1]],[m["p2"][0],m["p2"][1]]]
							return True
					return False
		return False
	w=len(b[0])
	h=len(b)
	dominos=[]
	dl=[]
	dn=int(max("".join(b).replace("","$").split("$")))+1
	for n in range(dn):
		for n2 in range(dn):
			if ([n2,n] in dl):continue
			dl+=[[n,n2]]
	done_tiles=[]
	if (dt!=None):
		dominos,dl,done_tiles=dt[0],dt[1],dt[2]
	while True:
		if (log==True):
			print_board(b,dominos)
			print("\n")
		s=step1(b,done_tiles,w,h,dominos,dl)
		if (s==False):
			s=step2(b,done_tiles,w,h,dominos,dl)
			if (s==False):
				s=step3(b,done_tiles,w,h,dominos,dl)
		if (len(dl)==0):
			return (True,dominos,dl);
		if (s==False):
			return (False,dominos,dl)



def test():
	score=0
	for i in range(5):
		b=random_board(random.randint(2,9))
		s,d,dl=solve_board(b,log=False)
		if (s==False):
			print("Fail:(")
			print_dominos(dl)
		else:
			print("Success!")
			print_board(b,d)
			score+=1
	print("\n"+"="*30+"\n"+f"Score: {score}/{i+1}".center(30," ")+"\n"+"="*30)



if (__name__=="__main__"):
	test()
