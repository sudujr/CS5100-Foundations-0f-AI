#import necessary packages
import cv2
import imutils

# Read the Image
# obtain the height, width and no of channels of the image
# Display the Original Image
image = cv2.imread("lena.png")
(h,w,d)=image.shape
print(h,w,d)

cv2.imshow("LenaOriginal",image)
cv2.waitKey(0)

"Rotation of Image"
# Compute the Center value of Image
# Generate 2D rotation Matrix
# perform rotation operation using warpAffine function to rotate along the center
# Display the rotated Image
Center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(Center, 180,1.0)
rotated = cv2.warpAffine(image, M,(w,h))
cv2.imshow("RotatedImage",rotated)
cv2.waitKey(0)

"Smoothing an Image"
# Apply gaussian blur to smooth the image
# Display the smoothened Image
blurred = cv2.GaussianBlur(image,(51,51),0)
cv2.imshow("BlurredImage",blurred)
cv2.waitKey(0)


"Converting the image into grayscale"
image1 = cv2.imread("i.png")
cv2.imshow("originalImage",image1)
cv2.waitKey(0)
gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
cv2.imshow("GrayScaleImage",gray)
cv2.waitKey(0)

"Edge Detection"
edge = cv2.Canny(gray,30,150)
cv2.imshow("EdgeDetection",edge)
cv2.waitKey(0)

"Detecting and Drawing Contours"
thresh1 = cv2.threshold(gray,240,250,cv2.THRESH_BINARY_INV)[1]
cnts = cv2.findContours(thresh1.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image1.copy()
for c in cnts:
    cv2.drawContours(output,[c],-1,(240,0,159),3)
cv2.imshow("Contours", output)
cv2.waitKey(0)


"counting Objects"
text = "{} Objects".format(len(cnts))
cv2.putText(output,text,(10,25),cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.7,(0,0,200),2)
cv2.imshow("Contours", output)
cv2.waitKey(0)

