import re
a = 0
list1 = []


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

        elif re.search(r"Invoice\s*|\s*Bill\s*No\s*:?\s*", list[i]):
            match = re.search(
                r"(?:Invoice|Bill)?\s*No\s*:?[\s:]*([A-Za-z]{2}[A-Za-z0-9/-]+)", "\n".join(list[i:len(list)]))
            if match:
                features["Invoice Number"] = match.group(1)
            elif re.search(r"Invoice\s*|\s*Bill\s*No_\s*:?\s*", list[i]):
                match = re.search(
                    r"(?:Invoice|Bill)?\s*No_\s*:?[\s:]*([A-Za-z]{2}[A-Za-z0-9/-]+)", "\n".join(list[i:len(list)]))
            if match:
                features["Invoice Number"] = match.group(1)

        # elif features["Invoice Number"] == None:
        #     for j in range(i, len(list)):
        #             if
        #             match = re.findall(r"([A-Za-z0-9])$", list[j])
        #             if match and features["Invoice Number"] == None:
        #                 features["Invoice Number"] = match[0]

        # elif "Invoice" in list[i] or "Bill" in list[i]:
        #     print(list[i])
        #     parts = list[i].split()
        #     print(parts)
        #     for part in parts:
        #         re.match("\s*([A-Za-z0-9]+/n)$", part)
        #         if match:
        #             # print('yes')
        #             features["Date"] = part

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
                        # print(match)

        elif "TOTAL\n" in list[i]:
            match = re.search(r"\d+\.\d{2}", list[i+1])
            if match:
                features["Total Amount"] = list[i+1]

        elif a == 0:
            match = re.search(
                r"(?:Date|\bBill Date\b|\bInvoice Date\b)?\s*\b(\d{1,2}\s*[-/]\s*\d{1,2}\s*[-/]\s*\d{2,4})\b", " ".join(list[i:len(list)]))
            if match:
                features["Date"] = match.group(1)

            # match = re.search(
            #     r"(?:Date|\bBill Date\b|\bInvoice Date\b)?\s*\b(\d{1,2}\s*[-/]\s*\d{1,2}\s*[-/]\s*\d{2,4})\b", "\n".join(list[i:len(list)]))
            # features["Date"] = match.group(0)

    return features


with open('output.txt', 'r+', encoding='utf-8') as file:
    for line in file:
        list1.append(line)
    # print(list1)
features = extract_features(list1)

for key, value in features.items():
    print(f"{key}: {value}")
