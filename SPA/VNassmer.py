#Small symbolic logic processor

#########################
#Imports
import numpy as np
execfile('L1_bindings.py')


#########################
# SYSTEM SET-UP
########################

#########################
#System parameter set-up
D = 256 #No. of dimensions in vector
K = 5 #No. of working memory registers.
F = 1 #Depth of programme counter.
base = 1.0 #All numbers in vector elements range between 0 and 'base'.
SPR = 1./16. #SP resolution - how many numbers/states 'fit' into a [0,1] interval.

#Non-system parameters
k = 20 #Number of numbers known to the system.
i = 0 #Counter to keep track of no of steps made.
T = 1000 #Limit max. number of (time) steps.
DispStep = 20 #Display X outputs at a time.


#########################
#System components
Vision = np.array(D*[0.]) #Vision input register.
Attention = np.array(D*[0.]) #Attention register.
InstrReg = np.array(D*[0.]) #Instruction register.
MQuer = np.array(D*[0.]) #Memory query input.
MRet = np.array(D*[0.]) #Memory return.
PCount = np.array(F*[D*[0.]]) #Programme counter.
BinderIn = np.array(2*[D*[0.]]) #Binder inputs.
BinderOut = np.array(D*[0.]) #Binder output.
CondReg = np.random.rand(D) #Condition register.

MReg = np.array(K*[D*[0]]) #Genereal memory registers.

CORTEX = {} #Declarative memory.
#There is also a binder wih 2 operations: similar & dissimilar bind
#And there is also a comparator testing for vector equiality


########################
#Vocabulary items
CORTEX['END'] = np.array(D*[1])
CORTEX['TRUE'] = np.random.rand(D) #Concept of 'TRUE'.
CORTEX['FALSE'] = np.array(D*[1]) - CORTEX['TRUE'] #Concept of 'FALSE'
for j in range(k):
	CORTEX['NO%d' % j] = np.random.rand(D) #Concept of '1'

#OpCodes
CORTEX['NULL'] = np.array(D*[0])
CORTEX['MxA'] = np.random.rand(K, D) #Working memory to attention opcodes.
CORTEX['AxM'] = np.random.rand(K, D) #Attention to working memory opcodes.
CORTEX['AxMQuer'] = np.random.rand(D) #Attention to memory query opcode.
CORTEX['MRetxA'] = np.random.rand(D) #Memory return to attention opcode.
CORTEX['BindOp1'] = np.random.rand(D) #Execute operation 1 of binder.
CORTEX['BindOp2'] = np.random.rand(D) #Execute operation 2 of binder.

#Higher level commands
CORTEX['COUNT'] = np.random.rand(D) #Initiate count-up.


########################
#Stimuli: components and set-up.
Raw_vis = np.array(T*[D*[0.]])
IRForce = np.array(T*[D*[0.]]) #Force instruction register at specific step.

#Stimuli definition
Raw_vis = np.array(T*CORTEX['NO1']) #Vision stimulus.
IRForce[5] = CORTEX['COUNT'] #Give instruction to count

########################
# SYSTEM OPERATION
########################
#Header - these parts have somehow been executed already.
#MReg[0] #Reg acts to hold task.
MReg[1] = CORTEX['NO1'] #Reg acts as step.
MReg[2] = CORTEX['NO9'] #Reg acts as limit.
MReg[3] = CORTEX['TRUE'] #Reg holds the comparison value.

#Main operation.
while ((InstrReg != CORTEX['END']).all()) and i < T-1:

	#Decision-making.
	### Stage I - Create aggregate state.
	
	
	### Stage II - Project entire state to memory, then find appropriate action.
	
	### Stage III - Find out condition 'most met'. Then push that on the instr. reg.
	
	#Decision execution.
	#Contrived commands (non-primitive).
	if ((InstrReg == CORTEX['COUNT']).all()):
		MReg[0] = CORTEX['COUNT']
	
	#Regular/primitive commands.
	if ((InstrReg == CORTEX['NULL']).all()): #Default case.
		Attention = Vision
	for j in range(K):
		if ((InstrReg == CORTEX['MxA'][j]).all()):
			Attention = MReg[j]
		if ((InstrReg == CORTEX['AxM'][j]).all()):
			MReg[j] = Attention
	if ((InstrReg == CORTEX['AxMQuer']).all()):
		MQuer = Attention
	if ((InstrReg == CORTEX['MRetxA']).all()):
		Attention = MRet
		
	#Aftermath, e.g. triggering memory to respond to query.
	
	##### Trailer: House-keeping and forced actions for next step #####
	if IRForce[i+1].all() != False: #If forced IR is not ALL zeros.
		InstrReg = IRForce[i+1]
	i += 1
	
	
	if (i % DispStep == 0):
		raw_input('Press Enter for next %d steps...' % DispStep)
		# PRINT HEADER HERE! #
		
	
	################################
	# Plotting and display section #
	################################
	keyres = {} #Reset result dictionary.
	for key in CORTEX:
		keyres[key] = np.sum(np.abs(CORTEX[key]-InstrReg))
	print(i, min(keyres, key=keyres.get))