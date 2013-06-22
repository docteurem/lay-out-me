#!/usr/bin/env python

 
from scribus import *


colors = ['black', 'red', 'blue']
fonts = ['Liberation Mono Regular', 'Liberation Sans Regular', 'Liberation Serif Regular']

layers = []
typo = ''


def getNumber():
	nb = valueDialog('the number', 'give me a number Koen')
	return int(nb)

def init():
	#create layers, set the colors
	for i in range(0, 2):
		nb = getNumber()
		layers.append(colors.pop(nb%len(colors)))
		createLayer(layers[i])
	#set the font
	nb = getNumber()
	typo = fonts[nb%len(fonts)]
	T = createText(20, 20 , 100, 100)
	setText('lorem lipsum dolor gnagna', T)
	setFont(typo, T)                        
	
	
	
	
	


if haveDoc():
	init()
	


'''
L = len(draft)                                	# The length of the word 
                                              	# will determine the font size
defineColor("gray", 11, 11, 11, 11)           	# Set your own color here

if haveDoc():
    u  = getUnit()                            	# Get the units of the document
    al = getActiveLayer()                     	# Identify the working layer
    setUnit(UNIT_MILLIMETERS)                 	# Set the document units to mm,                                            
    (w,h) = getPageSize()                     	# needed to set the text box size
 
    createLayer("c")
    setActiveLayer("c")
 
    T = createText(w/6, 6*h/10 , h, w/2)  # Create the text box
    setText(draft, T)                         	# Insert the text
    setTextColor("gray", T)                  	# Set the color of the text
    setFontSize((w/210)*(180 - 10*L), T)     	# Set the font size according to length and width
 
    rotateObject(45, T)                      	# Turn it round antclockwise 45 degrees
    setUnit(u)                               	# return to original document units
    setActiveLayer(al)                       	# return to the original active layer
'''
