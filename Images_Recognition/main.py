#Python3


##--------------------------------Main file------------------------------------
##
## Copyright (C) 2020 by Belinda Brown Ramírez (belindabrownr04@gmail.com)
##	Image recognition system for diagnosis of a network switch
##
##-----------------------------------------------------------------------------



##########  			IMPORTING PACKAGES   			##########

import cv2
import numpy as np
import glob
import os
from collections import OrderedDict

##########  			DEFINITIONS OF NECESSARY FUNCTIONS   			##########

######					 FILTERING NOISE / MAKING THE IMAGE SHARP
# def denoising_sharpening(input):
#     without_noise= cv2.fastNlMeansDenoisingColored(input, None,15,15,7,15)
#     kernel=np.array([[-1,-1,-1,-1,-1],
#                       [-1,2,2,2,-1],
#                       [-1,2,8,2,-1],
#                       [-2,2,2,2,-1],
#                       [-1,-1,-1,-1,-1]])/8.0
#     without_noise = cv2.filter2D(without_noise,-1,kernel)
#     return without_noise


######	Read the template
template_green = cv2.imread('',0)
template_orange = cv2.imread('',0)
template_dark_orange = cv2.imread('',0)

######	Store the width (w) and height (h) of the template
w_green, h_green = template_green.shape[::-1]
w_orange, h_orange = template_orange.shape[::-1]
w_dark_orange, h_dark_orange = template_dark_orange.shape[::-1]

######	Specifying (threshold)
threshold= 0.90
######	Directory with images verify
img_dir = ''
data_path = os.path.join(img_dir,'*.jpg')
files = glob.glob(data_path)
data = []
######	Analyzing all the images in the folder
for f1 in files:
					########   FOR GREEN     ######
	######	COMPARING  X
	Green_x = []
	X_Green_before_filtered = []
	######	COMPARING Y
	Green_y = []
	Y_Green_before_filtered = []
	######	THE FILTERED GREEN COORDINATES
	X_Green_Filtered =[]
	Y_Green_Filtered =[]
	########	TO JOIN THE TWO GREEN VECTORS
	Green_filtered_coordenates = []
	######	Number of LEDs in state # XXX
	Quantity_Leds_Green = 0
					#######    FOR YELLOW ORANGE    #####
	######	COMPARING  X
	YellowOrange_x = []
	X_YellowOrange_before_filtered = []
	######	COMPARING Y
	YellowOrange_y = []
	Y_YellowOrange_before_filtered = []
	######	THE FILTERED YELLOW ORANGE COORDINATES
	X_YellowOrange_Filtered =[]
	Y_YellowOrange_Filtered =[]
	###	TO JOIN THE TWO GREEN VECTORS
	YellowOrange_filtered_coordenates = []
	######	Number of LEDs in state # XXX
	Quantity_Leds_YellowOrange = 0
					#######    FOR ORANGE ORANGE     #####
	######	COMPARING  X
	OrangeOrange_x = []
	X_OrangeOrange_before_filtered = []
	######	COMPARING  Y
	OrangeOrange_y = []
	Y_OrangeOrange_before_filtered = []
	######	THE FILTERED YELLOW ORANGE COORDINATES
	X_OrangeOrange_Filtered =[]
	Y_OrangeOrange_Filtered =[]
	########	TO JOIN THE TWO GREEN VECTORS
	OrangeOrange_filtered_coordenates = []
	######	Number of LEDs in state # XXX
	Quantity_Leds_OrangeOrange = 0

	##### Read each image
	img = cv2.imread(f1)
	print("\n", f1) #picture name
	##### Store image data
	data.append(img)
	#####	uses a gray filter for easy recognition
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, 0)

	########		 COMPARING THE IMAGE USING TEMPLATE METHOD 			########
	res_matching_green = cv2.matchTemplate(img_gray,template_green,cv2.TM_CCOEFF_NORMED)
	res_matching_orange = cv2.matchTemplate(img_gray,template_orange,cv2.TM_CCOEFF_NORMED)
	res_matching_dark_orange = cv2.matchTemplate(img_gray,template_dark_orange,cv2.TM_CCOEFF_NORMED)

	##### If you use denoising image:
	#f1Filtrada = cv2.imread(f1)
	#img = denoising_sharpening(f1Filtrada)

	###### Announces every time an image is reviewed
	print("Image loaded, analyzing patterns ...")
	###### gets the position of matching
	location_green = np.where(res_matching_green >= threshold)
	location_orange = np.where(res_matching_orange >= threshold)
	location_dark_orange = np.where(res_matching_dark_orange >= threshold)

				########## IF THERE IS GREEN THEN ... ##########
	####### GREEN BEFORE FILTERING for Y - without repeats
	if len(location_green[0]) > 0:
		for itergreeny in sorted(location_green[0]):
			if itergreeny not in Green_y:
				Green_y.append(itergreeny)
		###### Compying the vector without repetitions to generate the second to compare
		Y_Green_before_filtered =  Green_y.copy()
		######	Obtaining the first coordinate
		yGreen0 = Green_y[0]
		###### Deleting the first coordinate
		Y_Green_before_filtered.pop(0)
		######	The deleted coordinate is added to the result
		Y_Green_Filtered.append(yGreen0)
		#####	Green before filtering for X - basically vector obtained minus repeated coordinates
		for itergreenx in sorted(location_green[1]):
			if itergreenx not in Green_x:
				Green_x.append(itergreenx)
		#####	Compying the vector to generate the second
		X_Green_before_filtered =  Green_x.copy()
		##### Gets the first coordinate obtained from the list of elements without repetitions
		xGreen0 = Green_x[0]
		#######	Deleting the first element to be able to subtract with the complete list
		X_Green_before_filtered.pop(0)
		######	The deleted coordinate is added to the result
		X_Green_Filtered.append(xGreen0)
			##########   GREEN COORDENATES FILTERS ONE FOR LOCATION								##########
		#For green Y
		for e, i in sorted(zip(Green_y, Y_Green_before_filtered)):
			#Difference between y coordinates
			Diff_Y_Green = i - e
			if h_green < abs(Diff_Y_Green):
				Y_Green_Filtered.append(i)
		Y_Green_Filtered = list(OrderedDict.fromkeys(Y_Green_Filtered))
		# Filter for the X
		for ee, ii in sorted(zip(Green_x, X_Green_before_filtered)):
			#Difference between x coordinates
			Diff_X_Green = ii - ee
			if w_green < abs(Diff_X_Green):
				X_Green_Filtered.append(ii)
		X_Green_Filtered = list(OrderedDict.fromkeys(X_Green_Filtered))
		#Counting the number of pixels each coordinate
		number_X_Green = len(X_Green_Filtered)
		number_Y_Green = len(Y_Green_Filtered)
		HowManyGreen = 0
		#Equalizing in order the number of pixels Y
		while HowManyGreen < number_X_Green-1:
			HowManyGreen = HowManyGreen +1
			if number_Y_Green != number_X_Green and number_Y_Green < number_X_Green:
				Y_Green_Filtered.append(yGreen0)
		######		Joining the two x, y coordinates
		Green_filtered_coordenates = sorted(zip(X_Green_Filtered, Y_Green_Filtered))
		###### 	Draw the rectangle and label in that case where it finds green
		for ptGreen in Green_filtered_coordenates:
			####	cv2.rectangle(image where draw, place , color BGR, thick line drawing)
			cv2.rectangle(img, ptGreen, (ptGreen[0] + w_green, ptGreen[1] + h_green), (0,255,255), 4)
			###	In this function the color goes BGR, what it does is put the text where it found the led
			cv2.putText(img, 'GREEN', ptGreen, cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 4)
			##### 	Count the number of LEDs you found in this state
			Quantity_Leds_Green = Quantity_Leds_Green +1
		print("The number of LEDs in Green Green status (on / on) found is:      ", Quantity_Leds_Green)

				########## IF THERE IS YELLOW ORANGE THEN ... ##########
	if len(location_orange[0]) > 0:
		##### for Y on yellow orange before filtered
		for iteryelloworangY in sorted(location_orange[0]):
			if iteryelloworangY not in YellowOrange_y:
				YellowOrange_y.append(iteryelloworangY)
			####	Compying the vector without repetitions to generate the second to compare
			Y_YellowOrange_before_filtered =  YellowOrange_y.copy()
			####	Obtaining the first coordinate
			yYellowOrang0 = YellowOrange_y[0]
			####	Deleting the first coordinate
			Y_YellowOrange_before_filtered.pop(0)
			#### 	The deleted coordinate is added to the result
			Y_YellowOrange_Filtered.append(yYellowOrang0)
			#####	yellow orange before filtering for X - basically vector obtained minus repeated coordinates
			for iteryelloworangX in sorted(location_orange[1]):
				if iteryelloworangX not in YellowOrange_x:
					YellowOrange_x.append(iteryelloworangX)
			####	Compying the vector to generate the second
			X_YellowOrange_before_filtered =  YellowOrange_x.copy()
			####	Gets the first coordinate obtained from the list of elements without repetitions
			xYellowOrang0 = YellowOrange_x[0]
			###		Deleting the first element to be able to subtract with the complete list
			X_YellowOrange_before_filtered.pop(0)
			###		The deleted coordinate is added to the result
			X_YellowOrange_Filtered.append(xYellowOrang0)
		#### Applying the same method for filter similar Y COORDENATES
		for eee,iii in sorted(zip(YellowOrange_y,Y_YellowOrange_before_filtered)):
			Diff_Y_YellowOrnge = iii - eee
			if h_orange < abs(Diff_Y_YellowOrnge):
				Y_YellowOrange_Filtered.append(iii)
		Y_YellowOrange_Filtered = list(OrderedDict.fromkeys(Y_YellowOrange_Filtered))
		#### Applying the same method for filter similar X COORDENATES
		for eeee,iiii in sorted(zip(YellowOrange_x,X_YellowOrange_before_filtered)):
			Diff_X_YellowOrnge = iiii - eeee
			if w_orange < abs(Diff_X_YellowOrnge):
				X_YellowOrange_Filtered.append(iiii)
		X_YellowOrange_Filtered = list(OrderedDict.fromkeys(X_YellowOrange_Filtered))
		#### counting the total of coordinates finally filtered
		number_X_YellowOrange = len(X_YellowOrange_Filtered)
		number_Y_YellowOrange = len(Y_YellowOrange_Filtered)
		HowManyYellowOrange = 0
		while HowManyYellowOrange < number_X_YellowOrange-1 :
			HowManyYellowOrange = HowManyYellowOrange +1
			if number_Y_YellowOrange != number_X_YellowOrange and number_Y_YellowOrange < number_X_YellowOrange:
				Y_YellowOrange_Filtered.append(yYellowOrang0)
		######		Joining the two x, y coordinates
		YellowOrange_filtered_coordenates = sorted(zip(X_YellowOrange_Filtered, Y_YellowOrange_Filtered ))
		###### 	Draw the rectangle and label in that case where it finds yellow orange
		for ptYellowOrange in YellowOrange_filtered_coordenates:
			#Draw a rectangle around the adapted region found in this case
			####	cv2.rectangle(image where draw, place , color BGR, thick line drawing)
			cv2.rectangle(img, ptYellowOrange, (ptYellowOrange[0] + w_orange, ptYellowOrange[1] + h_orange), (0,255,255), 4)
			###	In this function the color goes BGR, what it does is put the text where it found the led
			cv2.putText(img, 'ORANGE', ptYellowOrange, cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 4)
			##### 	Count the number of LEDs you found in this state
			Quantity_Leds_YellowOrange = Quantity_Leds_YellowOrange +1
		print("The number of LEDs in Yellow Orange state (on / problem) found is:      ", Quantity_Leds_YellowOrange)

				########## IF THERE IS ORANGE ORANGE OR DARK ORANGE (IS THE SAME) THEN  ... ##########
	if len(location_dark_orange[0]) > 0:
		#####	For Y on yellow orange before filtered
		for iterdarkorangY in sorted(location_dark_orange[0]):
			if iterdarkorangY not in OrangeOrange_y:
				OrangeOrange_y.append(iterdarkorangY)
		#### Compying the vector without repetitions to generate the second to compare
		Y_OrangeOrange_before_filtered =  OrangeOrange_y.copy()
		####	Obtaining the first coordinate
		yOrangOrang0 = OrangeOrange_y[0]
		####	Deleting the first coordinate
		Y_OrangeOrange_before_filtered.pop(0)
		#### 	The deleted coordinate is added to the result
		Y_OrangeOrange_Filtered.append(yOrangOrang0)
		#####	orange orange same dark orange before filtering for X - basically vector obtained minus repeated coordinates
		for iterdarkorangX in sorted(location_dark_orange[1]):
			if iterdarkorangX not in OrangeOrange_x:
				OrangeOrange_x.append(iterdarkorangX)
		####	Compying the vector to generate the second
		X_OrangeOrange_before_filtered =  OrangeOrange_x.copy()
		####	Gets the first coordinate obtained from the list of elements without repetitions
		xOrangOrang0 = OrangeOrange_x[0]
		###		Deleting the first element to be able to subtract with the complete list
		X_OrangeOrange_before_filtered.pop(0)
		###		The deleted coordinate is added to the result
		X_OrangeOrange_Filtered.append(xOrangOrang0)
		#### Applying the same method for filter similar Y COORDENATES
		for nne,nni in sorted(zip(OrangeOrange_y,Y_OrangeOrange_before_filtered)):
			Diff_Y_OrangOrang = nni - nne
			if h_dark_orange < abs(Diff_Y_OrangOrang):
				Y_OrangeOrange_Filtered.append(nni)
		Y_OrangeOrange_Filtered = list(OrderedDict.fromkeys(Y_OrangeOrange_Filtered))
		#### Applying the same method for filter similar X COORDENATES
		for nnee,nnii in sorted(zip(OrangeOrange_x,X_OrangeOrange_before_filtered)):
			Diff_X_OrangOrang = nnii - nnee
			if w_dark_orange < abs(Diff_X_OrangOrang):
				X_OrangeOrange_Filtered.append(nnii)
		X_OrangeOrange_Filtered = list(OrderedDict.fromkeys(X_OrangeOrange_Filtered))
		##### Counting the total of coordinates finally filtered
		number_X_OrangOrang = len(X_OrangeOrange_Filtered)
		number_Y_OrangOrang = len(Y_OrangeOrange_Filtered)
		HowManyDarkOrange = 0
		while HowManyDarkOrange < number_X_OrangOrang-1 :
			HowManyDarkOrange = HowManyDarkOrange +1
			if number_Y_OrangOrang != number_X_OrangOrang and number_Y_OrangOrang < number_X_OrangOrang:
				Y_OrangeOrange_Filtered.append(yOrangOrang0)
		######		Joining the two x, y coordinates
		OrangeOrange_filtered_coordenates = sorted(zip(X_OrangeOrange_Filtered, Y_OrangeOrange_Filtered))
		###### 	Draw the rectangle and label in that case where it finds orange orange
		for ptOrangOrang in OrangeOrange_filtered_coordenates:
			#Draw a rectangle around the adapted region found in this case
			####	cv2.rectangle(image where draw, place , color BGR, thick line drawing)
			cv2.rectangle(img, ptOrangOrang, (ptOrangOrang[0] + w_dark_orange, ptOrangOrang[1] + h_dark_orange), (0,255,255), 4)
			###	In this function the color goes BGR, what it does is put the text where it found the led
			cv2.putText(img, 'DARK ORANGE', ptOrangOrang, cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 4)
			##### 	Count the number of LEDs you found in this state
			Quantity_Leds_OrangeOrange = Quantity_Leds_OrangeOrange + 1
		print("The number of LEDs in Orange Orange status (problem / problem) found is:     ", Quantity_Leds_OrangeOrange)
	#### Shows me the figure already analyzed
	cv2.imshow("\nProcessed Image",img)
	### Since there are several, wait until you press a key and thus analyze the other image
	cv2.waitKey(0)
### Once finished remove all windows
cv2.destroyAllWindows()
