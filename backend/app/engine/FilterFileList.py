import re
file = "MCK-Q1-FY21-ECT.pdf"
# company_name = ["MCK"]
# year = ["FY23"]
# quarter = ["Q1"]
def filterFileList(query):

    promptNumber = query.find("You must return the name of the Source file and the page number for each information in the response. This information must be presented elegantly in the markdown format.")
    query = query[:promptNumber]
     
    MckessonNames = ["mckesson","mck ","mck-","mck,","mck?","mck."]
    CardinalNames = ["cardinal","cah ","cah-","cah,","cah?","cah."]
    CencoraNames = ["cencora","cor ","cor-","cor,","cor?","cor."]

    quarter_pattern = r"(?i)Q\s?[1-4]|Quarter\s?[1-4]"

    year_pattern = r"(?i)FY\s?\d{2}|Year\s?\d{2}"
    year_4_pattern = r"\b(1[0-9]{3}|2[0-9]{3})\b"
    year_4_match = re.findall(year_4_pattern,query)
    # query = "What is the revenue of Mckesson and Cardinal in Quarter 2 FY 20 and Q1 of year 21"

    # quarter = re.findall(quarter_pattern,query)
    # print(quarter)
    quarter = []
    quarter_match = re.findall(quarter_pattern, query)
    if quarter_match:
        for item in quarter_match:
            item2 = item.lower()
            item2 = item2.replace("quarter","Q")
            item2 = item2.upper()
            item2 = item2.replace(" ","")
            # print(item2)
            quarter.append(item2)
    else:
        quarter = ["Q1","Q2","Q3","Q4"]
    print("year:",year_4_match)
    # Extract year
    year = []
    year_match = re.findall(year_pattern, query)
    if year_match:
        for item in year_match:
            item2 = item.lower()
            item2 = item2.replace("year","FY")
            item2 = item2.upper()
            item2 = item2.replace(" ","")
            # print(item2)
            year.append(item2)
        # year = year_match
    elif year_4_match:
        for item in year_4_match:
            item2 = item[-2:]
            item2 = "FY" + str(item2)
            year.append(item2)
    else:
        year = ["FY24","FY23","FY22","FY21","FY20"]

    print(quarter)
    print(year)
    company_name = []
    for item in MckessonNames:
        if(query.lower().find(item) != -1):
            company_name.append("MCK")
    else:
        for item in CardinalNames:
            if(query.lower().find(item) != -1):
                company_name.append("CAH")
        else:
            for item in CencoraNames:
                if(query.lower().find(item) != -1):
                    company_name.append("CEN")

    if(len(company_name)==0):
        company_name.append("MCK")

    # print(company_name)
    # if (file[0:3] in company_name and file[4:6] in quarter and file[7:11] in year):
        # print(file)
    # print(quarter, year)
    # print(quarter_match)
    # if(query == "initial Query"):
    #     quarter = ["Q1"]
    #     year = ["FY24"]
    #     company_name = ["Mckesson"]
    return quarter,year,company_name

def getSourceDict(text):
    pattern = r'\(Source:\s([^\)]+),\sPage\sNumber:\s([\d, ]+)\)'
    matches = re.findall(pattern, text)

    source_dict = {}
    for match in matches:
        source, pages = match
        page_list = [int(page.strip()) for page in pages.split(',')]
        if source in source_dict:
            source_dict[source].extend(page_list)
        else:
            source_dict[source] = page_list

    for file in source_dict:
        pagenumberList = list(set(source_dict[file]))
        source_dict[file] = pagenumberList
    return source_dict