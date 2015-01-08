import sys
import numpy 

class CUT:
	def __init__(self, RULES, rule):
		self.number=RULES.index(rule)
        	rule=rule.split(" ")
        	self.left=rule[0]
        	self.right=rule[2:]

class findRULES:
	def __init__(self, left):
		self.candidate=[]
		for rule in RULES[1:]:
	        	if left == rule[0]:
				self.candidate.append(RULES.index(rule))

class findRIGHT:
        def __init__(self, left):
                self.candidate=[]
                for rule in RULES[1:]:
			cut=CUT(RULES,rule)
                        if left in cut.right:
                                self.candidate.append(RULES.index(rule))

class BT:
	def __init__(self, left, right, cn, OL, number):
        	self.left = left
        	self.right = right
		self.number=number
        	self.ol=OL
		self.cn=cn

	def first(self, left, right, cn, OL, number):
		L=1
		for item in right:
			if item in UT:
				L=L*LUT[UT.index(item)]
			if(item in T4):
				if Table[UT.index(OL)][T4.index(item)]==0:
					print("Origin LEFT:", OL, "ITEM", item, "NO.", number, "left", left, "cn", cn)
					Table[UT.index(OL)][T4.index(item)]=number
				return
			elif(item == "lambda"):
				LUT[UT.index(left)]=1
				LR[cn]=1
			elif(item in UT):
				tmp=findRULES(item)
				for can in tmp.candidate:
			       		newcut=CUT(RULES,RULES[can])
					newbt=BT(newcut.left, newcut.right, can, OL, number)
					newbt.first(newcut.left, newcut.right, can, OL, number) 			
			else:
				print("The input string does not match any token.\n")
		if L==1 and left not in right :
			LR[cn]=1

	def follow(self, left, cn, OL, number):
		if LR[cn]==1:
			tmp=findRIGHT(left)
			for can in tmp.candidate:
	                        newcut=CUT(RULES,RULES[can])
				newbt=BT(newcut.left, newcut.right, can, OL, number)
				print("LEFT:",left,"CAN",can,"NO.",number,"R",newcut.right)
				print(LR[1:])
				if newcut.right[len(newcut.right)-1]==left:
					print("GET")
					newbt.follow(newcut.left, can, OL, number)
				for s in range(newcut.right.index(left),len(newcut.right)):
					print("S:",s,"NOW",newcut.right[s],"INDEX",newcut.right.index(left))
					if newcut.right[s] in UT and newcut.right[s] != left:
						if LR[can]==1 :
							print("Follow 1")
							newbt.first(newcut.left, newcut.right[s:], can, OL, number)
							if can != cn:
								newbt.follow(newcut.left, can, OL, number)
							
						else:
                                        	        print("Follow 2")
                                                        if can != cn and newcut.left !=newcut.right:
	                                                	newbt.first(newcut.left, newcut.right[s:], can, OL, number)
					elif newcut.right[s] in T4:
                                	        print("Follow 3")
                                        	Table[UT.index(OL)][T4.index(newcut.right[len(newcut.right)-1])]=number
						

UT=[]
T1=set()
T2=[]
T3=[]
T4=[]
RULES=["Syntax Error"]
right=[]
left=[]

#Record UT,T1,RULES
for line in open('cfg.txt','r'):
	print(line)
	while("->" in line):
		#RULES
       		line=line.replace("\n","")
		RULES.append(line)
		line=line.split(" ")
		#UT
		LEFT=line[0]
		UT.append(line[0])
		#T1
		for remain in line[2:]:
			T1.add(remain)
		break

        while("|" in line):
		#RULES
                line=line.replace("\n","")
		RULES.append(LEFT+" "+line)
		#T1
                line=line.split(" ")
                for remain in line[1::-2]:
                        T1.add(remain)
                break

print("Unterminal:")
print(UT)

print("\nT1:")
print(T1)

T2=T1.difference(UT)

print("\nTerminal(T2):")
print(T2)
print("\nRULES:")
print(RULES[1:])

T3=T2
T3.remove("lambda")
T3=list(T3)
print("\nNo lambda Terminal(T3):")
print(T3)

T4=sorted(T3)
print("\nSorted Terminal(T4):")
print(T4)

Table=numpy.zeros((len(UT),len(T4)),int)
print("\nTable:")
print(Table)

LR=[0]*len(RULES)
print(LR)
LUT=[0]*len(UT)
print(LUT)

for rule in RULES[1:]:
	print("MARK")
	cut=CUT(RULES,rule)
	bt=BT(cut.left, cut.right, cut.number, cut.left, cut.number)
	bt.first(cut.left, cut.right, cut.number, cut.left, cut.number)
        bt.follow(cut.left, cut.number, cut.left, cut.number)

print("\nAfter First:")
print(T4)
print(Table)
