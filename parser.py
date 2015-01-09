import sys
import numpy 
CFG="cfg.txt"
INPUT="input string.txt"

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
					print("\tWriting Table.")
					print("left",left,"current no.",cn,"Origin LEFT:", OL, "ITEM", item,"NO.",number)
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
				print("\tCompleting Follow Set...")
				print("left:",left,"can:",can,"NO.",number,"R",newcut.right)
				#print(LR[1:])
				if newcut.right[len(newcut.right)-1]==left:
					#print("GET")
					newbt.follow(newcut.left, can, OL, number)
				for s in range(newcut.right.index(left),len(newcut.right)):
					#print("S:",s,"NOW",newcut.right[s],"INDEX",newcut.right.index(left))
					if newcut.right[s] in UT and newcut.right[s] != left:
						if LR[can]==1 :
							#print("Follow 1")
							newbt.first(newcut.left, newcut.right[s:], can, OL, number)
							if can != cn:
								newbt.follow(newcut.left, can, OL, number)
							
						else:
                                        	        #print("Follow 2")
                                                        if can != cn and newcut.left !=newcut.right:
	                                                	newbt.first(newcut.left, newcut.right[s:], can, OL, number)
					elif newcut.right[s] in T4:
                                	        #print("Follow 3")
                                        	Table[UT.index(OL)][T4.index(newcut.right[len(newcut.right)-1])]=number

class Apply:
	def __init__(self, start, string):
		self.start=start.reverse()
		self.string=string.reverse()
		
	def compare(self, stack, remain):
		print("MARK",stack[-1],remain[-1])
		r=Table[UT.index(stack[-1])][T4.index(remain[-1])]
		if r!=0:
			print(stack,remain)
			print("Apply Rule",r,RULES[r])
			cut=CUT(RULES,RULES[r])
			cut.right.reverse()
			if "lambda" in cut.right:
				cut.right=[]
			stack.pop()
			stack.extend(cut.right)
			print(stack,remain)
			while(stack[-1]==remain[-1]):
				print("Match %s\n"%stack[-1])
				stack.pop()
				remain.pop()
				if len(stack)==0 and len(remain)==0:
					print("Legal.\n")
					return
				elif len(remain)==0 and len(stack)>0 :
					derivetest=stack
					#print(LUT)
					for l in range(len(derivetest)-1,-1,-1):
						if derivetest[l] in UT:
							if LUT[UT.index(derivetest[l])]==1:
								derivetest.pop()
					if len(derivetest)==0:
						print("Legal(2).\n")
						return
					else:
						print("Failed... May be illegal or ambiguous.\n")
                                        	return
						
				elif len(stack)==0 or len(remain)==0: 
					print("Failed...(2) May be illegal or ambiguous.\n")
					return
			self.compare(stack,string)
		else:
			print("Can not find an appropriate rule to apply.\nFailed.\n")				

UT=[]
T1=set()
T2=[]
T3=[]
T4=[]
RULES=["Syntax Error"]

#Record UT,T1,RULES
for line in open(CFG,'r'):
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
                for remain in line[1:]:
                        T1.add(remain)
                break

print("Unterminal:")
print(UT)

#print("T1:")
#print(T1)

T2=T1.difference(UT)

#print("Terminal(T2):")
#print(T2)
print("RULES:")
print(RULES[1:])

T3=T2
if "lambda" in T3:
	T3.remove("lambda")
T3=list(T3)
#print("No lambda Terminal(T3):")
#print(T3)

T4=sorted(T3)
print("Sorted Terminal(T4):")
print(T4)

Table=numpy.zeros((len(UT),len(T4)),int)
print("\nTable:")
print(Table)

LR=[0]*len(RULES)
print(LR)
LUT=[0]*len(UT)
print(LUT)

for rule in RULES[1:]:
	cut=CUT(RULES,rule)
	print("\nChecking rule %d:\n\tCompleting First Set..."%(cut.number))
	bt=BT(cut.left, cut.right, cut.number, cut.left, cut.number)
	bt.first(cut.left, cut.right, cut.number, cut.left, cut.number)
        bt.follow(cut.left, cut.number, cut.left, cut.number)

print("\nLL(1) Table:")
print(T4)
print(Table)

for line in open(INPUT,'r'):
        print("\nInput string:\n%s\n"%line)
	stack=[]
	stack.append(UT[0])
	string=line.split(" ")
	print(string)
	app=Apply(stack, string)
	app.compare(stack, string)
