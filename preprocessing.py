import cv2

# Load the image
image = cv2.imread('C:\\kimdsyyaya\\NeoThermal\\dataset\\new.jpg')

# Define the coordinates of the region to crop
x1, y1 = 108, 142  # Top-left corner
x2, y2 = 476, 278  # Bottom-right corner

# Crop the region
cropped_image = image[y1:y2, x1:x2]

# Save the cropped image
cv2.imwrite('cropped_image.jpg', cropped_image)

# Display the cropped image (optional)
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
