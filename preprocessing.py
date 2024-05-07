# import numpy as np
# import cv2
# image = cv2.imread('C:\\kimdsyyaya\\NeoThermal\\dataset\\new.jpg')
# regions = [
#     {"name": "SANJAY FOOD", "coords": (115, 150, 266, 178)},
#     {"name": "SF024359", "coords": (839, 179, 975, 199)},
#     {"name": "24-03-202", "coords": (841, 201, 973, 219)},
#     {"name": "GSTIN: 27BUGPMI67DIZR", "coords": (111, 241, 303, 262)},
#     {"name": "1100.00", "coords": (209, 747, 265, 765)}
# ]
# offset = 8
# for region in regions:
#     name = region["name"]
#     x1, y1, x2, y2 = region["coords"]
#     x1, y1, x2, y2 = x1 - offset, y1 - offset, x2 + offset, y2 + offset
#     cropped_image = image[y1:y2, x1:x2]
#     cv2.imwrite(f'cropped_{name}.jpg', cropped_image)

# for region in regions:
#     name = region["name"]
#     cropped_image = cv2.imread(f'cropped_{name}.jpg', cv2.IMREAD_GRAYSCALE)
#     cv2.imshow(f'Cropped {name}', cropped_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
