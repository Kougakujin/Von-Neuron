#Library of binding operations.

#################################################################
# WARNING! - Meant to work with elements of a, b within [0, 1]! #
#################################################################

import numpy as np

#Binding 1 - Barrel add
def add(a,b):
	c = []
	for i in range(np.size(a)):
		c = np.append(c, (a[i] + b[i%np.size(b)]) % base)
		
	return c

#Binding 2 - Ordered selection.
## CAUTION!!!: Really should work with dimensions as powers of 2.
def osel(k): #Receives an ORDERED list of arrays to bind.
	nbind = len(k)-1 #Number of bindings to be carried out.
	dim = len(k[0]) #Dimensionality of SP.
	idx = range(len(k[0]))
	c = list(k[0])
	i = 0 #Counter variable
	
	#Compute max. number of bindings possible.
	maxbinds = 0

	for i0 in range(int(np.floor(np.log2(dim)))):
		maxbinds += 2**i0
	
	print(np.log2(dim), dim, nbind, maxbinds)
	#Check no. of requested bindings is possible.
	if maxbinds < nbind:
		print('Too many bindings requested for dimensionality of SP.')
		return k[0]
	else:
		while i <= range(nbind):
			dim = dim/2 #The array will be split in chunks of this size at this step.
			starts = idx[0::dim]
			for j in range(len(starts)):
				if(j % 2 == 1):
					if i+1 > nbind:
						return c
					c[starts[j]:starts[j]+dim] = k[i+1][starts[j]:starts[j]+dim]
					i = i+1
					
	return np.array(c)
	
#Binding 2b - Random selection.
## Will only work for a, b of equal length. Sizes that are powers of 2 preferred.
## CAUTION!!! : Every binding will look different in this case! When used as a
## search-key there is an expected overlap value which may decay quickly for repeated
## bindings...
def rsel(a,b):
	c = np.array(np.size(a)*[0.]) # Answer variable
	rand = np.random.rand(len(a)) #Generate array of random numbers.
	for i in range(len(a)):
		if(rand[i] > np.median(rand)): #If number > median.
			c[i] = list(a[i])
		else:
			c[i] = list(b[i])
			
	return c
	## NOTE: This function has an extraordinarily large chance of returning a vector
	## with exactly 50% (even no. of elements) of elements from a and b.
	
#Binding 3 - a*b is different from both a and b.
def circonv(a,b):
	if(np.size(b) > np.size(a)): #Ensure that the longer vetor always is always 'a'.
		a,b = b,a

	c = np.array(np.size(a)*[0.]) # Answer variable
	for i in range(np.size(a)):
		for j in range(np.size(b)):
			c[i] += np.concatenate((a,a), axis=0)[i+np.size(a)-j]*b[j] #Convoluton op.
			
	return c
	
##### INCOMPLETE #####
#Binding 3 - 
def permute1(a,b,base):
	for i in range(np.size(a)):
		c[i] = (a[i] + b[i%np.size(b)]) % base
		
	return c
	
##### BAD OPERATION #####
#Binding 4 -
def circ2add(a,b):
	for i in range(np.size(a)):
		c[i] = a[i] + np.sum(b)

	return c
		
#Permutation should be 1 vector 'turning/bitwise shifting' the other.
#Addition is similar under standard ANN, but no longer under differencing ANN!
#Similarity or difference uder assumptions of sparsity or density will differ.
#Perhaps addition may be siilar in SPARSE differencing ANN.

#########################
# NON BINDING OPERATORS #
#########################

# Invert SP.
def inv(K):
	return np.roll(K[::-1],1)
	
# Distance between SPs.
## NOTE: Will only work for SPs of the same length.
def dist(a,b,res):
	dist = 0 #Answer variable.
	for i in range(len(a)):
		if(np.abs(a[i]-b[i]) > res):
			dist += 1
			
	return dist