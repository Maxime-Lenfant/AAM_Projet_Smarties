# Source - https://stackoverflow.com/a/55509210
# Posted by HansHirse, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-22, License - CC BY-SA 4.0

import cv2

# Input image
input = cv2.imread('C:\Users\maxim\OneDrive\Cours\INSA\4A\microprocmms/image/test')

# Get input size
height, width = input.shape[:2]

# Desired "pixelated" size
w, h = (16, 16)

# Resize input to "pixelated" size
temp = cv2.resize(input, (w, h), interpolation=cv2.INTER_LINEAR)

# Initialize output image
output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

cv2.imshow('Input', input)
cv2.imshow('Output', output)

cv2.waitKey(0)
