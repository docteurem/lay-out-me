#!/usr/bin/env python 
from scribus import *
from os import listdir
from os.path import isfile, join
import re

path = '/home/drem/Desktop/content/'

colors = ['black', 'red', 'blue']
fonts = ['Liberation Sans Regular', 'Liberation Serif Regular']
formats = [{'name':'a5', 'width':138, 'height':196}, {'name':'a6', 'width':138, 'height':98}, {'name':'a7', 'width':69, 'height':98}, {'name':'a8', 'width':69, 'height':49}, {'name':'a9', 'width':34.5, 'height':49}, {'name':'a10', 'width':34.5, 'height':24.5}]
fontSizes = [256, 128, 96, 72, 60, 48, 36, 30, 24, 18, 14, 12, 11, 10, 9, 8, 7]


layers = []
typo = ''

files = []

currentPage = 1

holes = []

output = ''


def permutations (L, depth):
	
	
	if len(L)==1: # cas où il n'y a qu'un seul élément
		return [L] # une seule permutation
	
	##on limite le nombre de permutations pour éviter un freeze
	if depth > 3:return [L]
	
	depth = depth + 1
	
	X=L[0] # sinon en récupère le premier élément
	L1=L[1:len(L)] # et on l'élimine de L
	L2=permutations(L1, depth) # appel récursif
	L4=[] # pour recevoir le résultat
	for L3 in L2: # on parcourt toutes les permutations de la queue de liste
		for i in range(0,len(L3)+1): # on fait circuler le premier élément
			L5=list(L3) #L5 est un clone de L3
			L5.insert(i,X) # on place X au bon endroit
			L4.insert(0,L5)# et on enrichit L4
			
	return L4


def getNumber():
	nb = valueDialog('the number', 'give me a number Koen')
	return int(nb)

def getFilesNames():
	files = [ f for f in listdir(path) if isfile(join(path,f)) ]
	files.sort()
	return files


def getContent(pageNb):
	content = {}
	global files
	#messageBox('message', 'je vais chercher le contenu')
	for fileName in files:
		#print fileName
		if 'page'+str(pageNb)+'-' in fileName:
			#messageBox('mesage', fileName)
			if 'image' in fileName:
				match = re.search('image[0-9]+', fileName)
				content[match.group()] = {'name': match.group(), 'path':path+fileName, 'limitFormat':1}
			elif 'legende' in fileName:
				match = re.search('legende([0-9])+', fileName)
				f = open(path+fileName,'r')
				data = f.read()
				content['image'+match.group(1)]['subItem'] = {'name':'image'+match.group(1), 'text':data, 'limitFormat':0}
			else:
				match = re.search('-([a-z]+)\.', fileName)
				f = open(path+fileName,'r')
				data = f.read()
				if(len(data) > 5000):
					limit = 5
				elif(len(data) > 2000):
					limit = 4
				elif(len(data) > 1000):
					limit = 3
				elif(len(data) >500):
					limit = 2
				
				else:
					limit = 0
				
				content[match.group(1)] = {'name':match.group(1), 'text':data, 'limitFormat':limit}
				
				
	#messageBox('message', 'contenu chargé')
	return content


				
def getOrder(content, nb):
	initial = []
	
		
	for i in range(0, len(content)):
		initial.append(i)
	
	possibles = permutations(initial, 0)
	#messageBox('message', str(len(possibles))+' possibles')
	
	return possibles[nb%len(possibles)]
						
			

def init():
	global files
	global fonts
	global layers
	global typo
	global output
	
	#create layers, set the colors
	for i in range(0, 2):
		nb = getNumber()
		output = output + 'Koen said '+str(nb)+' for document: color'+str(i)+'\n'
		layers.append(colors.pop(nb%len(colors)))
		createLayer(layers[i])
	#set the font
	nb = getNumber()
	output = output + 'Koen said '+str(nb)+' for document: font\n'
	
	typo = fonts[nb%len(fonts)]
	files = getFilesNames()
	
	

def getValidFormat(index, globalArea, neededArea, maxIndex):
	global formats
	testSize = formats[index]['width'] * formats[index]['height']
	
	result = {'index':index, 'blocSize':testSize, 'width':formats[index]['width'], 'height':formats[index]['height']}
	
	if(globalArea - testSize < neededArea):
		index = index+1
		if index > maxIndex:
			return {'index':-1}
		
		result = getValidFormat(index, globalArea, neededArea, maxIndex)
	
	
	return result
	

def textSize(frame, index):
	if(index > len(fontSizes)-1): return -1
	setFontSize(fontSizes[index], frame)
	setLineSpacing(fontSizes[index], frame)
	if textOverflows(frame) > 0:
		textSize(frame, index +1)
	

	

def insertItem(item, posX, posY, width, height):
	global typo
	
	setActiveLayer(item['layer'])
	
	#c'est une image
	if 'path' in item:
		frame = createImage(posX, posY, width, height)
		loadImage(item['path'], frame)
		setScaleImageToFrame(True, True, frame)
		
	#c'est du texte
	else:
		frame = createText(posX, posY, width, height)
		print typo
		setText(item['text'], frame)
		setFont(typo, frame)
		if 'columns' in item:
			setColumns(item['columns'], frame)
		if 'size' in item:
			setFontSize(item['size'], frame)
		else:
			textSize(frame, 0)
	
	#rect = createRect(posX, posY, width, height)

	

def placeItem(item, maxPages, globalArea, neededArea, posX, posY, maxY, addedPage, output):
	global formats
	global currentPage
	global holes
	global layers
	
	maxIndex = len(formats)-1-item['limitFormat']
	
	#print "maxIndex "+str(maxIndex)
	
	neededArea = neededArea - formats[maxIndex]['width']*formats[maxIndex]['height']
	
	nb = getNumber()
	output = output + 'Koen said '+str(nb)+' for page '+str(currentPage)+': '+item['name']+' - color and format \n'
	
	item['layer'] = layers[nb%len(layers)]
	
	
	indexFormat = nb%(maxIndex+1)
	
	#print "index format" + str(indexFormat)
	
	validFormat = getValidFormat(indexFormat, globalArea, neededArea, maxIndex)
	
	#print "format de départ: "
	#print validFormat
	
	
	if validFormat['index'] == -1:
		return -1
	
	
	
	if posX + validFormat['width'] > 143:
		
		
		lostSpace = (maxY-posY)*(143-posX)
		
		if lostSpace > 0:
			holes.append({'posX':posX, 'posY':posY, 'height':(maxY-posY), 'width':143-posX, 'page':currentPage})
			
		
		posX = 5
		
		#print "lostSpace="+str(lostSpace)
		posY = maxY
		
		globalArea = globalArea - lostSpace
		
		validFormat = getValidFormat(indexFormat, globalArea, neededArea, maxIndex)
		if validFormat['index'] == -1:
			messageBox('message', 'format pas possible 1')
			return -1
		#print "nouveau format après passage à la ligne: "
		#print validFormat
	
	
	
	
	if posY + validFormat['height'] > 201:
		if addedPage < maxPages:
			#print "je passe à la page suivante "
			
			if(posY < 201):
				holes.append({'posX':posX, 'posY':posY, 'height':201-posY, 'width':143, 'page':currentPage})
				
			currentPage = currentPage +1
			addedPage = addedPage +1
			gotoPage(currentPage)
			globalArea = 138*196
			
			validFormat = getValidFormat(indexFormat, globalArea, neededArea, maxIndex)
			if validFormat['index'] == -1:
				messageBox('message', 'format pas possible 2')
				return -1
				
			maxY = 0
			posX = 5
			posY = 5 
			
			#print "nouveau format après passage à la page suivate: "
			#print validFormat
		else:
			validFormat = {'width':formats[maxIndex]['width'], 'height':formats[maxIndex]['height'], 'blocSize':formats[maxIndex]['height']*formats[maxIndex]['width']}
			
			holesCopy = list(holes)
			
			for hole in holesCopy:
				#messageBox('message', 'on cherche les trous')
				if hole['width'] >= validFormat['width'] and hole['height'] >= validFormat['height']:
					holes.remove(hole)
					gotoPage(hole['page'])
					insertItem(item, hole['posX'], hole['posY'], validFormat['width'], validFormat['height'])
					gotoPage(currentPage)
					return {'posX': posX, 'posY': posY, 'maxY':maxY, 'addedPage':addedPage, 'globalArea':globalArea, 'neededArea':neededArea, 'output':output}
			messageBox('message', 'erreur let start again')
			return -1
	
	
	
	insertItem(item, posX, posY, validFormat['width'], validFormat['height'])
	
	
	if posY + validFormat['height'] > maxY:
		maxY = posY + validFormat['height']
	
	
	result = {}
	
	if maxY > posY + validFormat['height']:
		result['posX'] = posX
		result['posY'] = posY+validFormat['height']
	else:
		result['posX'] = posX + validFormat['width']
		result['posY'] = posY
			
	
	
	
	result['output'] = output
	result['maxY'] = maxY
	result['addedPage'] = addedPage
	result['globalArea'] = globalArea - validFormat['blocSize']
	result['neededArea'] = neededArea
	
	
	return result
		
	
	

def buildPage(index, dblePage):
	global formats
	global currentPage
	global holes
	global output
	
	messageBox('message', 'page'+str(index))
	
	holes = []
	
	content = getContent(index)
	
	placeData = {'posX':5, 'posY':5, 'maxY':5}
	
	
	if dblePage:
		pages = str(currentPage+1)+', '+str(currentPage+2)
	else:
		pages = str(currentPage+1)
	
	nb = getNumber()
	
	placeData['output'] = 'Koen said '+str(nb)+' for page '+pages+': order \n'
	order = getOrder(content, nb)
	
	
	
	items = content.items()
	
	
	
	oldCurrentPage = currentPage
	
	
	if(index != 1):
		newPage(-1)
		currentPage = pageCount()
		gotoPage(currentPage)
	
	if(dblePage == True):
		newPage(-1)
		gotoPage(currentPage)
	
	
	
	
	
	placeData['globalArea'] = formats[0]['width']*formats[0]['height']
	
	
	if(dblePage == True):
		placeData['globalArea'] = placeData['globalArea'] * 2
		maxPages = 2
	else:
		maxPages = 1
	
	
	
	
	placeData['neededArea'] = 0
	placeData['addedPage'] = 1
	print items
	
	for item in items:
		if('subItem' in item[1]):
			 placeData['neededArea'] =  placeData['neededArea'] + formats[len(formats)-1-item[1]['subItem']['limitFormat']]['width'] * formats[len(formats)-1-item[1]['subItem']['limitFormat']]['height']
		placeData['neededArea'] = placeData['neededArea'] + formats[len(formats)-1-item[1]['limitFormat']]['width']*formats[len(formats)-1-item[1]['limitFormat']]['height']
		
	
	
	
	
	for i in order:
		placeData = placeItem(items[i][1], maxPages, **placeData)
		
		if(placeData == -1):
			messageBox('message', "error")
			nbPages = pageCount()
			currentPage = oldCurrentPage
			while(nbPages != oldCurrentPage):
				deletePage(nbPages)
				nbPages = nbPages -1
			
			buildPage(index, dblePage)
			return
		
				
		if 'subItem' in items[i][1]:
			print items[i][1]['subItem']
			placeData = placeItem(items[i][1]['subItem'], maxPages, **placeData)
			if(placeData == -1):
				messageBox('message', "error")
				nbPages = pageCount()
				currentPage = oldCurrentPage
				while(nbPages != oldCurrentPage):
					deletePage(nbPages)
					nbPages = nbPages -1
				
				buildPage(index, dblePage)
				return
	if 'output' in placeData:		
		output = output + placeData['output']
			
	


def buildLastPage():
	newPage(-1)
	insertItem({'text':output, 'layer':layers[0], 'columns':2, 'size':6}, 5, 5, formats[0]['width'], formats[0]['height'])	


if haveDoc():
	init()
	buildPage(1, False)
	buildPage(2, False)
	buildPage(3, False)
	
	for i in range(4, 28):
		buildPage(i, True)
	
	buildLastPage()
