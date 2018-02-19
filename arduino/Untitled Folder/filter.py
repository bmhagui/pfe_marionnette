if type(vectors) is list:
	    alpha = 0.1
            #this condition is just to test that the hand is in the range of the leapmotion
            
            #Treating the z axis values, starting at 150mm from the leapmtion to leave space for the hand to
            #move without getting out of range, after 400 its far enough and should be considered at max=>250
            if vectors[10][1] <= 150:
                itermediaireZ = 0
            elif vectors[10][1] >= 400:
                itermediaireZ = 250
            else:
                itermediaireZ = vectors[10][1]-150

            #if it is then we will manually map the x axis values on the 18 cm range the platform can move 
            if vectors[10][0] <= -200:
                outputVector[13] = 4
            elif vectors[10][0] > -200 and vectors[10][0] <= -150:
                outputVector[13] = 6
            elif vectors[10][0] > -150 and vectors[10][0] <= -100:
                outputVector[13] = 8
            elif vectors[10][0] > -100 and vectors[10][0] <= -50:
                outputVector[13] = 10
            elif vectors[10][0] > -50 and vectors[10][0] <= 0:
                outputVector[13] = 12
            elif vectors[10][0] > 0 and vectors[10][0] <= 50:
                outputVector[13] = 14
            elif vectors[10][0] > 50 and vectors[10][0] <= 100:
                outputVector[13] = 16
            elif vectors[10][0] > 100 and vectors[10][0] <= 150:
                outputVector[13] = 18
            elif vectors[10][0] > 150 and vectors[10][0] <= 200:
                outputVector[13] = 20
            elif vectors[10][0] > 200:
                outputVector[13] = 22


        for i in range(0,12):
            if outputVector[i] < 0:
                outputVector[i] = 0
            outputVector[i] = 255/116*outputVector[i]
            #adding an offset to compensate for lifting the robot
            outputVector[i] += (outputVector[12])
            if outputVector[i] > 250:
                outputVector[i] = 250
	outputVector[12] = lastvalueZ (1-alpha) + itermediaireZ * alpha
	lastvalueZ = outputVector[12]
	lastvalueX = outputVector[13]
	

        #print outputVector
        #Cable entre -19 et 115

        self.node.getObject('serial').findData('sentData').value = outputVector
