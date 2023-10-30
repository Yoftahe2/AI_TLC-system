import cv2 import time import sys
import RPi.GPIO as GPIO import numpy as np
import skimage.measure import structural_similarity as ssim import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)

# Assign constants for the traffic light GPIO pins red_led_A = 15
yellow_led_A = 7

green_led_A = 0


red_led_B = 24

yellow_led_B = 8

green_led_B = 1


red_led_C = 10

yellow_led_C = 23

green_led_C = 4


red_led_D = 9

yellow_led_D = 25

green_led_D = 14


# Configure the GPIO to BCM and set the pins to output mode GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led_A, GPIO.OUT)
 

GPIO.setup(yellow_led_A, GPIO.OUT) GPIO.setup(green_led_A, GPIO.OUT)

GPIO.setup(red_led_B, GPIO.OUT) GPIO.setup(yellow_led_B, GPIO.OUT) GPIO.setup(green_led_B, GPIO.OUT)

GPIO.setup(red_led_C, GPIO.OUT) GPIO.setup(yellow_led_C, GPIO.OUT) GPIO.setup(green_led_C, GPIO.OUT)

GPIO.setup(red_led_D, GPIO.OUT) GPIO.setup(yellow_led_D, GPIO.OUT) GPIO.setup(green_led_D, GPIO.OUT)

# Define function to control 1st traffic light def trafficState_A(red, yellow, green):
GPIO.output(red_led_A, red) GPIO.output(yellow_led_A, yellow) GPIO.output(green_led_A, green)

#Define function to control 2nd traffic light def trafficState_B(red, yellow, green):
GPIO.output(red_led_B, red) GPIO.output(yellow_led_B, yellow) GPIO.output(green_led_B, green)

#Define function to control 3rd traffic light def trafficState_C(red, yellow, green):
 

GPIO.output(red_led_C, red) GPIO.output(yellow_led_C, yellow) GPIO.output(green_led_C, green)

#Define function to control 4th traffic light def trafficState_D(red, yellow, green):
GPIO.output(red_led_D, red) GPIO.output(yellow_led_D, yellow) GPIO.output(green_led_D, green)

# for the motor rotating 90 degrees #{
def motor(): controlpin=[17,18,11,22] for pin in controlpin:
GPIO.setup(pin,GPIO.OUT) GPIO.output(pin,0)
seq=[[1,0,1,0],
[0,1,1,0],

[0,1,0,1],

[1,0,0,1]]

for step in range(3):

for fullstep in range(4): for pin in range(4):
GPIO.output(controlpin[pin],seq[fullstep][pin]) time.sleep(0.05)
#GPIO.cleanup()

#}

# for image capturing
 

#{

def image_capture(): motor() camera_port = 0
camera = cv2.VideoCapture(camera_port) def get_image():
retval, im = camera.read() return im
temp = get_image() print("Taking image...") camera_capture = get_image() file = "/home/pi/realtime.jpg"
cv2.imwrite(file, camera_capture) del(camera)

#}


# FOR IMAGE PROCESSING AND COMPARING #{
def mse(imageA, imageB):


err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2) err /= float(imageA.shape[0] * imageA.shape[1])*10000

return err

def compare_images(imageA, imageB):


m = mse(imageA, imageB)
 

print m


while true:	#General loop image_capture() time.sleep(3)
reference = cv2.imread("reference1.jpg") realtime = cv2.imread("realtime.jpg")

# convert the images to grayscale

reference1 = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY) realtime = cv2.cvtColor(realtime, cv2.COLOR_BGR2GRAY)

# compare the images compare_images(reference1, realtime)

#}

# density decision algorhtim #{
if(0<m<0.5):

time=5

else if (0.5<m<1): time=10
else if (1<m<1.5): time=15
else if (1.5<m<2): time=20
else if (2<m<3): time=25
else:
 

time=30

#}

#FOR LIGHT CONTROL #{





# A's Light Green for time seconds other light Lights Red trafficState_A(0,0,1)
trafficState_B(1,0,0) trafficState_C(1,0,0) trafficState_D(1,0,0) time.sleep(time)
# A's Light Yellow for 3 seconds other Lights Red trafficState_A(0,1,0)
trafficState_B(1,0,0) trafficState_C(1,0,0) trafficState_D(1,0,0)



#}

# for lane 2 image_capture() time.sleep(3)
reference = cv2.imread("reference2.jpg") realtime = cv2.imread("realtime.jpg")

# convert the images to grayscale

reference2 = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
 

realtime = cv2.cvtColor(realtime, cv2.COLOR_BGR2GRAY)


# compare the images compare_images(reference2, realtime)

#}

# density decision algorhtim #{
if(0<m<0.5):

time=5

else if (0.5<m<1): time=10
else if (1<m<1.5): time=15
else if (1.5<m<2): time=20
else if (2<m<3): time=25
else:

time=30

#}

#FOR LIGHT CONTROL #{

# B's Light Red for 10 seconds other Lights Green trafficState_A(1,0,0)
trafficState_B(0,0,1) trafficState_C(1,0,0) trafficState_D(1,0,0)
 

time.sleep(time)

# B's Light Yellow for 3 seconds other Lights Red trafficState_A(1,0,0)
trafficState_B(0,1,0) trafficState_C(1,0,0) trafficState_D(1,0,0)
#}

# for lane 3 image_capture() time.sleep(3)
reference = cv2.imread("reference3.jpg") realtime = cv2.imread("realtime.jpg")

# convert the images to grayscale

reference3 = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY) realtime = cv2.cvtColor(realtime, cv2.COLOR_BGR2GRAY)

# compare the images compare_images(reference3, realtime)

#}

# density decision algorhtim #{
if(0<m<0.5):

time=5

else if (0.5<m<1): time=10
else if (1<m<1.5): time=15
 

else if (1.5<m<2): time=20
else if (2<m<3): time=25
else:

time=30

#}

#FOR LIGHT CONTROL #{

# C's Light Red for 10 seconds other Lights Green trafficState_A(1,0,0)
trafficState_B(1,0,0) trafficState_C(0,0,1) trafficState_D(1,0,0) time.sleep(time)
# C's Light Yellow for 3 seconds other Lights Red trafficState_A(1,0,0)
trafficState_B(1,0,0) trafficState_C(0,1,0) trafficState_D(1,0,0)

#}

# for lane 3 image_capture() time.sleep(3)
reference = cv2.imread("reference4.jpg") realtime = cv2.imread("realtime.jpg")
 

# convert the images to grayscale

reference4 = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY) realtime = cv2.cvtColor(realtime, cv2.COLOR_BGR2GRAY)

# compare the images compare_images(reference4, realtime)

#}

# density decision algorhtim #{
if(0<m<0.5):

time=5

else if (0.5<m<1): time=10
else if (1<m<1.5): time=15
else if (1.5<m<2): time=20
else if (2<m<3): time=25
else:

time=30

#}

#FOR LIGHT CONTROL #{
# D's Light Red for 10 seconds other Lights Green trafficState_A(1,0,0)
trafficState_B(1,0,0) trafficState_C(1,0,0)
 

trafficState_D(0,0,1) time.sleep(time)
# B's Light Yellow for 3 seconds other Lights Red trafficState_A(1,0,0)
trafficState_B(1,0,0) trafficState_C(1,0,0) trafficState_D(0,1,0)

#}

GPIO.cleanup()
