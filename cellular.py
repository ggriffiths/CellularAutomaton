# Author: Grant Griffiths
# Date: 10/24/13
import os
import Tkinter
import pygame	
import re
import random
import math

from pygame.locals import *

# Program Parameters	
ringSize = 5
numIterations = 5
stepTime = 25
randomlyGenerate = True
cellPixelSize = 80
stepDelay = False
renderTimespace = True
autoGenerate = True
fixedRandom = True
debugEnabled = False

# Screen Initialization
screen_height = cellPixelSize*numIterations
screen_width = cellPixelSize*ringSize
background_color = (0,0,0)
(width, height) = (screen_width,screen_height)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cellular Automaton')
screen.fill(background_color)

# Debug function. Only prints if debug enabled.
def debug(s):
	if(debugEnabled):
		print s

def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

# Randomly row w/ even distribution
def getFirstRow():
	# insert 10 0's and 1's, then shuffle them
	row=[]	
	for i in range(ringSize):
		row.append(1)
		row.append(0)
	random.shuffle(row)

	return row

# Global Fixed Initial State
fixedRandomInitialState = getFirstRow()

# Draws a row, given the row & rowId
def automatonDrawRow(row,rowId):
	for i in range(ringSize):
		# draw white cell if 0
		if(row[i]==0):
			pygame.draw.rect(screen,(255,255,255), (i*cellPixelSize,rowId*cellPixelSize,cellPixelSize,cellPixelSize), 0)

# Run the Automaton
def runAutomaton(ruleNum):
	# initialize variables
	grid = [[0 for x in xrange(ringSize)] for x in xrange(numIterations)] 
	base = True
	mod = ringSize

	# format binary values for rule
	ruleBits = bin(ruleNum)
	ruleBits = ruleBits[2:]
	padding = ['0']*(8-len(ruleBits))
	ruleBits = ''.join(padding) + ruleBits

	# if we want to randomly generate the initial state
	if(randomlyGenerate):
		# if first state should be fixed (when calculate avg)
		if(fixedRandom):
			grid[0] = fixedRandomInitialState

		# if we want to generate a new first row every run
		else:
			grid[0] = getFirstRow()
	else:
		grid[0] = [0 for x in xrange(ringSize)]
		grid[0][(mod/2)-1]=1
	
	# iterate through rows in a grid
	for row in grid:
		# for row 1
		if(base):
			prevRow = row
			base=False

		#for row > 1 
		else:	
			for x in range(ringSize):
				# get bits p,q,r
				p = prevRow[(x-1)%mod]
				q = prevRow[(x)%mod]
				r = prevRow[(x+1)%mod]

				# boolean algebra to generate current cell
				triple = (p,q,r)
				if(triple==(0,0,0)):
					row[x] = int(ruleBits[7])

				elif(triple==(0,0,1)):
					row[x] = int(ruleBits[6])

				elif(triple==(0,1,0)):
					row[x] = int(ruleBits[5])

				elif(triple==(0,1,1)):
					row[x] = int(ruleBits[4])

				elif(triple==(1,0,0)):
					row[x] = int(ruleBits[3])

				elif(triple==(1,0,1)):
					row[x] = int(ruleBits[2])

				elif(triple==(1,1,0)):
					row[x] = int(ruleBits[1])

				elif(triple==(1,1,1)):
					row[x] = int(ruleBits[0])
		prevRow = row
	return grid



def generateImgDirectory(ruleNum):
	dirStr = ""
	if randomlyGenerate:
		dirStr+="imgRand/"
	else:
		dirStr+="img/"

	# resolution
	dirStr+="res_"+str(ringSize)+"x"+str(numIterations)+"/"

	# Create Directory for picture save if doesn't exist
	try:
		os.stat(dirStr)
	except:
		os.mkdir(dirStr)   

	# rule #
	ruleStr = str(ruleNum)
	for i in range(3-len(ruleStr)):
		ruleStr = "0"+ruleStr
	dirStr+=ruleStr

	# file extension
	dirStr+=".png"

	return dirStr

def main(ruleNum):
	#initialization
	if autoGenerate:
		running = False
	else:
		running = True

	# generate grid through cellular Automaton
	grid = runAutomaton(ruleNum)

	# get directory to print image to
	dirStr = generateImgDirectory(ruleNum)

	for r in range(numIterations):
		# draw rows
		if(renderTimespace):
			automatonDrawRow(grid[r],r)
			pygame.display.flip()	

			# save image once done rendering
			pygame.image.save(screen,dirStr)

		# delay if step enabled
		if(stepDelay): pygame.time.delay(stepTime)


	


	# run until exit
	while running:			
		 	for event in pygame.event.get():
		 		if event.type == pygame.QUIT:
		 			running=False

# Script to auto-generate 256 timespace diagram images 
def generateAllTimespaceDiagrams():
	for i in range(256):
		main(i)

# Finds the entropy of a given ruleId
def findShannonEntropy(ruleId,arbitraryColumnId,grid):
	blackCells=float(0)
	whiteCells=float(0)
	totalCells = numIterations

	# get num black cells
	for r in range(numIterations):
		blackCells = grid[r][arbitraryColumnId]+blackCells
	
 	# get num white cells
	whiteCells = totalCells-blackCells
	
	# Probability that cell is a given color in a column
	probWhite = whiteCells/(numIterations)
	probBlack = 1-probWhite
	if(probBlack==1):
		#print "Rule "+str(ruleId)+" -- colID: "+str(arbitraryColumnId)+" -- Entropy: " + str(0)
		return 0
	if(probWhite==1):
		#print "Rule "+str(ruleId)+" -- colID: "+str(arbitraryColumnId)+" -- Entropy: " + str(1)
		return 1
	
	# Shannon Entropy formula
	try:
		e = -((probWhite*math.log(probWhite,2))+(probBlack*math.log(probBlack,2)))
		#print "Rule "+str(ruleId)+" -- colID: "+str(arbitraryColumnId)+" -- Entropy: " + str(e)

		return e
	except ValueError:
		print "Math error for rule #" + str(ruleId) + "."
		
		print "Total Cells: " + str(totalCells)

		print "White Cells: " + str(whiteCells)
		print "Black Cells: " + str(blackCells)

		print "probWhite: " + str(probWhite)
		print "probBlack: " + str(probBlack)

	
	

# Find avg entropy of a given rule
def findMeanEntropy(ruleId,grid):
	values = []	
	for col in range(ringSize):
		values.append(findShannonEntropy(ruleId,col,grid))
	return (sum(values)/len(values))

# Generates a report of all 256 entropies
def generateEntropyReport():
	es = []
	for rule in range(256):
		grid=runAutomaton(rule)	
		ei = findMeanEntropy(rule,grid)
		print "Rule #" + str(rule) +" avg e: "+ str(ei)
		es.append(ei)

	file = open("entropy.txt", "w")
	file.write(str(fixedRandomInitialState)+"\n")
	for e in es:
		file.write(str(e)+"\n")
	file.close()

main(1)
#generateEntropyReport()
#generateAllTimespaceDiagrams()