import re
list1 = []


def extract_features(list):
    features = {
        "Products": [],
        "Invoice Number": None,
        "Company Name": None,
        "GST": None,
        "Total Amount": None
    }
    # features["Company Name"] = list[1]

    for i in range(len(list)):
        if "For" in list[i]:
            # print("x", i)
            match = re.search(r"For\s*([A-Za-z\s]*)$", list[i])
            # print(list[i])
            # print(matchlist)
            # print('yes')
            if match:
                # print('yes')
                features["Company Name"] = match.group(1)

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


with open('output.txt', 'r+', encoding='utf-8') as file:
    for line in file:
        list1.append(line)
    # print(list1)
features = extract_features(list1)

for key, value in features.items():
    print(f"{key}: {value}")
