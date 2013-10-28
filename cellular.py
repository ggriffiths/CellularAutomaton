# Author: Grant Griffiths
# Date: 10/24/13
import os
import Tkinter
import pygame	
import re
import random
import math

from pygame.locals import *

# Screen Initialization
screen_size = 500
background_color = (0,0,0)
(width, height) = (screen_size,screen_size)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cellular Automaton')
screen.fill(background_color)

# Program Parameters
scale = 0.5 
cellDim = int(screen_size * scale)
stepTime = 25
randomlyGenerate = False
gridPixels = screen_size/cellDim
stepDelay = False
showPicture = True
autoGenerate = True

# Randomly row w/ even distribution
def getFirstRow():
	# insert 10 0's and 1's, then shuffle them
	row=[]	
	for i in range(cellDim/2):
		row.append(1)
		row.append(0)
	random.shuffle(row)

	return row

# Draws a row, given the row & rowId
def automatonDrawRow(row,rowId):
	for i in range(cellDim):
		# draw black cell if 0
		if(row[i]==0):
			pygame.draw.rect(screen,(255,255,255), (i*gridPixels,rowId*gridPixels,gridPixels,gridPixels), 0)

		# draw white cell if 1
		else:
			pygame.draw.rect(screen,(0,0,0), (i*gridPixels,rowId*gridPixels,gridPixels,gridPixels), 0)
	return rowId < cellDim 

# Run the Automaton
def runAutomaton(ruleNum):
	# initialize variables
	grid = [[0 for x in xrange(cellDim)] for x in xrange(cellDim)] 
	base = True
	mod = cellDim

	# format binary values for rule
	ruleBits = bin(ruleNum)
	ruleBits = ruleBits[2:]
	padding = ['0']*(8-len(ruleBits))
	ruleBits = ''.join(padding) + ruleBits

	if(randomlyGenerate):
		grid[0] = getFirstRow()
	else:
		grid[0] = [0 for x in xrange(cellDim)]
		grid[0][(mod/2)-1]=1
	
	# iterate through rows in a grid
	for row in grid:
		# for row 1
		if(base):
			prevRow = row
			base=False

		#for row > 1 
		else:	
			for x in range(cellDim):
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
	dirStr+="size_"+str(cellDim)+"/"

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

	for r in range(cellDim):
		# draw rows
		if(showPicture):
			automatonDrawRow(grid[r],r)
			pygame.display.flip()

		# delay if step enabled
		if(stepDelay): pygame.time.delay(stepTime)

	# save image once done rendering
	pygame.image.save(screen,dirStr)
	# run until exit
	while running:			
		 	for event in pygame.event.get():
		 		if event.type == pygame.QUIT:
		 			running=False


		 				
def generateRuleImages():
	for i in range(256):
		print i
		main(i)

def findEntropy(ruleId):
	grid=runAutomaton(ruleId)
	blackCells=float(0)
	whiteCells=float(0)
	for row in grid:
		blackCells = sum(row)+blackCells

	whiteCells =(cellDim*cellDim)-blackCells

	pA = whiteCells/(cellDim*cellDim)
	pB = 1-pA
	e = -(((blackCells*pA*math.log(pA,2))/math.log(2,2)))-((whiteCells*pB*math.log(pB,2)/math.log(2,2)))
	
	return e

def findMeanEntropy(ruleId,numTimes):
	values = []
	for i in range(numTimes):
		values.append(findEntropy(ruleId))
	return (sum(values)/len(values))

def generateEntropyReport():
	file = open("entropy.txt", "w")
	for rule in range(256):
		entropy = findMeanEntropy(rule,50)
		file.write(str(entropy)+"\n")
	file.close()

generateRuleImages()
