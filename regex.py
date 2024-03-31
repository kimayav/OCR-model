import re
a = 0
list1 = []


def extract_date(text):
    date_patterns = [
        r"\b(\d{2}-\d{2}-\d{4})\b",  # DD-MM-YYYY
        r"\b(\d{2}/\d{2}/\d{4})\b",  # DD/MM/YYYY
        r"\b(\d{4}-\d{2}-\d{2})\b",  # YYYY-MM-DD
        r"\b(\d{4}/\d{2}/\d{2})\b",  # YYYY/MM/DD
        # D-D-YY or DD-D-YY or D-DD-YY or DD-DD-YY
        r"\b(\d{1,2}-\d{1,2}-\d{2})\b"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def extract_features(list):
    features = {
        "Company Name": None,
        "Invoice Number": None,
        "Date": None,
        "GSTIN": None,
        "Products": [],
        "Total Amount": None
    }
    for i in range(len(list)):
        if "For" in list[i]:
            # print("x", i)
            match = re.search(r"For\s*([A-Za-z\s]*)$", list[i])
            if match:
                # print('yes')
                features["Company Name"] = match.group(1)
            # print(list[i])
            # print(matchlist)
            # print('yes')
            elif a == 0:
                for j in range(i, len(list)):
                    match = re.search(r"For\s*([A-Za-z\s]*)$", list[i])
                    if match:
                        # print('yes')
                        features["Company Name"] = match.group(
                            1).strip().replace(" ", "")
        # elif a == 0:
        #     match = re.search(
        #         r"(?:Invoice|Bill) No:?\s*([A-Za-z0-9]+)$", list[i])
        #     if match:
        #         features["Invoice Number"] = match.group(1)
        #     elif a == 0:
        #         for j in range(i, len(list)):
        #             re.match(
        #                 "(?:Invoice|Bill) No:?\s*([A-Za-z0-9]+/n)$", list[j])
        #             if match:
        #                 # print('yes')
        #                 features["Invoice Number"] = match.group(1)

        elif re.search(r"(?:Invoice|Bill) No:?\s*([A-Za-z0-9]+)$", list[i], re.MULTILINE):
            match = re.search(
                r'(Invoice| Bill)? \s*\n\s*\n(.+?)\s*\n', list[i], re.MULTILINE)
            if match:
                features["Invoice Number"] = match.group(1).strip()

        # elif "GSTIN/n" in list[i]:
        #     # print("x", i)
        #     # match = re.search(r"\d{2}[A-Z]{5}\d{3}[A-Z]{5}}\n", list[i+1])
        #     # if match:
        #     #     print("yes")
        #     features["GST"] = list[i+1]

        elif "GSTIN" in list[i]:
            match = re.search(
                r"(GSTIN|GST|GSTin)\s*:\s*([A-Za-z0-9]+)$", list[i])
            if match:
                features["GSTIN"] = match.group(2)
                # print(match)
                # break
            else:
                for j in range(i+1, len(list)):
                    match = re.findall(r"([A-Za-z0-9]{15})$", list[j])
                    if match and features["GSTIN"] == None:
                        features["GSTIN"] = match[0]
                        print(match)

        elif "TOTAL\n" in list[i]:
            match = re.search(r"\d+\.\d{2}", list[i+1])
            if match:
                features["Total Amount"] = list[i+1]

        elif re.search(r"\b[A-Z][A-Za-z\s]+\b", list[i], re.MULTILINE):
            match = re.search(r"\b[A-Z]+\b", list[i], re.MULTILINE)
            # features["Products"] = match.group()
            print(match)
        elif a == 0:
            extract_date(list[i])
    return features


with open('output.txt', 'r+', encoding='utf-8') as file:
    for line in file:
        list1.append(line)
    # print(list1)
features = extract_features(list1)

for key, value in features.items():
    print(f"{key}: {value}")
