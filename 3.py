import easyocr as Reader
import easyocr
import argparse
import cv2
import re


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def extract_features(list):
    features = {
        "Products": [],
        "Invoice Number": None,
        "Company Name": None,
        "GST": None,
        "Total Amount": None
    }
    features["Company Name"] = list[1]

    for i in range(len(list)):
        if "Invoice No:\n" in list[i]:
            # print("x", i)
            match = re.search(r"[A-Z]{2}\d{5}\n", list[i+1])
            # print('yes')
            if match:
                # print('yes')
                features["Invoice Number"] = list[i+1]
        elif "GSTIN\n" in list[i]:
            # print("x", i)
            # match = re.search(r"\d{2}[A-Z]{5}\d{3}[A-Z]{5}}\n", list[i+1])
            # if match:
            #     print("yes")
            features["GST"] = list[i+1]
        elif "TOTAL\n" in list[i]:
            match = re.search(r"\d+\.\d{2}", list[i+1])
            if match:
                features["Total Amount"] = list[i+1]
        elif "Product\n" in list[i]:
            # if multiple or elif
            features["Products"] = str(list[i+9])

    return features


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-l", "--langs", type=str, default="en",
                help="comma separated list of languages to OCR")
ap.add_argument("-g", "--gpu", type=int, default=-1,
                help="whether or not GPU should be used")
args = vars(ap.parse_args())
# break the input languages into a comma separated list
langs = args["langs"].split(",")
print("[INFO] OCR'ing with the following languages: {}".format(langs))
# load the input image from disk
image = cv2.imread(args["image"])

reader = easyocr.Reader(langs, gpu=args["gpu"] > 0)
results = reader.readtext(image)
print("[INFO] OCR'ing input image...")
# results = list(results)
# print(results)


# loop over the results
for (bbox, text, prob) in results:
    with open('output.txt', 'a+', encoding='utf-8') as file:
        file.write(str(text))
        file.write('\n')
        # print(text)

    (tl, tr, br, bl) = bbox
    tl = (int(tl[0]), int(tl[1]))
    tr = (int(tr[0]), int(tr[1]))
    br = (int(br[0]), int(br[1]))
    bl = (int(bl[0]), int(bl[1]))

    text = cleanup_text(text)
    cv2.rectangle(image, tl, br, (0, 255, 0), 2)
    cv2.putText(image, text, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
list1 = list()

with open('output.txt', 'r+', encoding='utf-8') as file:
    for line in file:
        list1.append(line)
    # print(list1)
features = extract_features(list1)

# Print the extracted features
for key, value in features.items():
    print(f"{key}: {value}")

# # show the output image
# cv2.imwrite("output_image.jpg", image)
# cv2.waitKey(0)
