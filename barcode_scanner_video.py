#import necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argeparse
import datetime
import imutils
import time
import cv2


#construct argument parser and parse the arguments for taking command line input

ap = argparse.ArgumentParser()

ap.add_argument("-o","--output",type =str,default ="barcodes.csv", help = "path to csv files containing barcodes")

args = vars(ap.parse_args())


#initialiaze the video stream and alow the camera sensor to warm up
print("[INFO] starting video stream...")
#vs =  videoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#open the output CSV file for waiting and initialize the set of
#barcodes found thus far
csv = open(args["output"],"w")
found = set()

#loop over the frames from the video stream

while True:
    #grab the frame from the threaded video stream and resize it to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame,width=400)

    #find the barcodes in the frame and decode each of the barcodes

    barcodes = pyzbar.decode(frame)

#loop over the detected images

for barcode in barcodes:
        #extracting the bounding box lcoation of the barcode and draw the bounding box surrounding the barcode on the image
        (x,y,w,h) = barcode.rect
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        
        #the barcode data is a bytes object so if we want to draw it on
        #our output image we need to convert it to a string first
        barcodeData = barcode.data.decode('utf-8")
        barcodeType = barcode.type

        #draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData,barcodeType)
        cv2.putText(frame,text,(x,y-10),cv.Font_HERSEY_SIMPLEX,0.5,(0,0,255),2)


        #if the barcode text is currently not in our CSV file,write
        #the timestamp + barcode to disk and update the set
        if barcodeData not in found:
           csv.write("{} ({})".format(datetime.datatime.now(),barcodeData))
           csv.flush()
           found.add(barcodeData)


           #show the output frame
           cv2.imshow("Barcode Scanner",frame)
           key = cv2.waitKey(1) & 0xFF

           #if the "q" is pressed then break from the loop
           if key == ord("q"):
               break


print("[INFO] cleaning up....")
csv.close()
cv2.destroyAllWindows()
vs.stop()
           
                                      
                            
                                      
                                      

        
                                      


                

