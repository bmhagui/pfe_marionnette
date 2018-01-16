import numpy
import cv2
from numpy import linalg as linalg
import server


def getPinkRange():
  
  RANGE_MIN = numpy.array([150,100,100],numpy.uint8)
  RANGE_MAX = numpy.array([165,200,200],numpy.uint8)
  
  return RANGE_MIN, RANGE_MAX


def getRedRange():
  
  RANGE_MIN = numpy.array([170,200,100],numpy.uint8)
  RANGE_MAX = numpy.array([179,255,255],numpy.uint8)
  
  return RANGE_MIN, RANGE_MAX


def getOrangeRange():
  
  RANGE_MIN = numpy.array([5,100,100],numpy.uint8)
  RANGE_MAX = numpy.array([15,200,200],numpy.uint8)
  
  return RANGE_MIN, RANGE_MAX


def getBlueRange():
  
  RANGE_MIN = numpy.array([100,100,100],numpy.uint8)
  RANGE_MAX = numpy.array([120,255,255],numpy.uint8)
  
  return RANGE_MIN, RANGE_MAX


def getYellowRange():
  
  RANGE_MIN = numpy.array([20,100,100],numpy.uint8)
  RANGE_MAX = numpy.array([30,255,255],numpy.uint8)
  
  return RANGE_MIN, RANGE_MAX


def getHistogram(RANGE_MIN, RANGE_MAX, hsv_frame):
  
    # Set color range to track
    mask = cv2.inRange(hsv_frame, RANGE_MIN, RANGE_MAX)

    # Get histogram
    frame_histogram = cv2.calcHist([hsv_frame], [0], mask, [180], [0,180])
    cv2.normalize(frame_histogram,frame_histogram,0,255,cv2.NORM_MINMAX)

    return frame_histogram


def getRectangleGivenCenter(x, y, width, height):
  
    width,height = 100, 100
    x0 = x-width/2
    y0 = y-height/2
    
    return (x0,y0,width,height)
  

def handleUserInteraction(event, y, x, flags, param):
  
    global capture
    global frame_histogram
    global track_window
    
    if event == cv2.EVENT_LBUTTONDOWN :
      ret, frame = capture.read()
      print "[Tracking] Target center selected"
      
      track_window = getRectangleGivenCenter(x, y, 100, 100)
      
      
    if event == cv2.EVENT_RBUTTONDOWN :
      ret, frame = capture.read()
      print "[Tracking] Target color selected"
      
      hsv_frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      
      H, S, V = hsv_frame[x,y]
      print (hsv_frame[x,y])

      RANGE_MIN = numpy.array([H-5, S-50, V-50],numpy.uint8)
      RANGE_MAX = numpy.array([H+5, S+50, V+50],numpy.uint8)
      
      frame_histogram = getHistogram(RANGE_MIN, RANGE_MAX, hsv_frame)
      
      track_window = getRectangleGivenCenter(x, y, 100, 100)
      
    
    return


def drawROI(frame, x, y, width, height):
  
      # Draw it on image
      pts = ((x,y), (x+width,y), (x+width,y+height), (x,y+height)) # To get rectangle
      #pts = cv2.cv.BoxPoints(ret) # To get rotated box
      pts = numpy.int0(pts)
      
      # Draw track_window
      cv2.polylines(frame, [pts], True, (255,255,255), 2)
      
      # Store and draw tracking point (center of track_window)
      cv2.circle(frame, (x+width/2, y+height/2), 2, (0,0,255), -1)
      
      return frame


def init(frame):
	  
      # Setup initial location of window
      # Top left position
      x,y,width,height = 250, 400, 125, 90
      track_window = (x,y,width,height)

      # Set up the ROI for tracking
      hsv_frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # BGR to HSV
      
      # Set default color range to track
      RANGE_MIN, RANGE_MAX = getRedRange()  

      frame_histogram = getHistogram(RANGE_MIN, RANGE_MAX, hsv_frame)
      
      # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
      term_criteria = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
      
      return frame, term_criteria, track_window, frame_histogram


def main():
  
      global frame_histogram
      global track_window
      global capture
      
      # Capture camera device 0 (webcam)
      capture = cv2.VideoCapture(0) 
      # Capture first frame
      success, frame = capture.read()

      if(not success):
	print "[Tracking] Error in video first capture process."
	
      # Init server
      server_instance = server.server()
      
      # Init algo
      frame, term_criteria, track_window, frame_histogram = init(frame)
      
      while(True):
	
	  # Link mouse event to handleUserInteraction()
	  cv2.setMouseCallback('Make Baby Groot dance', handleUserInteraction)
	    
	  # Capture frame-by-frame
	  success, frame = capture.read()
	  
	  if(not success):
	    print "[Tracking] Error in video capture process."
	    break

	  # Transform image from BGR to HSV 
	  hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	  back_projection = cv2.calcBackProject([hsv_frame],[0],frame_histogram,[0,180],1)

	  # Apply meanshift to get the new location
	  ret, track_window = cv2.CamShift(back_projection, track_window, term_criteria)
	  x,y,width,height = track_window[0],track_window[1],track_window[2],track_window[3]
	    
	  if (width*height>1e-14):
	    
	      frame = drawROI(frame, x, y, width, height)
	      
	      # Call to server
	      ratio_x = float((x+width/2))/float(numpy.size(frame,0))
	      server_instance.sendPosition(str(ratio_x))
	    
	  else:
	    
	      #print "[Tracking] Nothing tracked. Reset track window."
	      x,y,width,height = 250, 400, 125, 90
	      track_window = (x,y,width,height)

	  key = cv2.waitKey(1) # Returns -1 if no key pressed 
	  if (key == ord('q')) or (key == 27): # Break if "q" or "esc" pressed 
	      break
	    
	  # Display the resulting frame
	  cv2.imshow('Make Baby Groot dance',frame)
	  cv2.imshow('Tracking',back_projection)
	  #cv2.imshow('HSV',hsv_frame)
	      
      # When everything done, release the capture
      capture.release()
      cv2.destroyAllWindows()
      
      return


if __name__ == "__main__":
	main()
