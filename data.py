import json
import requests
from datetime import datetime
import pandas as pd


# authors from IU
class Author:
    id: int
    name: str
    photo_link: str
    overall_citation: int
    citations: {}
    papers_published: {}
    institution: str
    department: str
    hirsch_ind: int
    disciplines: []
    papers_id: []

    def __init__(self, author):
        self.id = author.id
        self.name = author.name
        self.photo_link = author.photo_link
        self.overall_citation = author.overall_citation
        self.citations = author.citations
        self.papers_published = author.papers_published
        self.institution = author.institution
        self.department = author.department
        self.hirsch_ind = author.hirsch_ind
        self.disciplines = author.disciplines
        self.papers_id = author.paper_id  # name of class object differs from name of JSON object


# papers published in IU
class Paper:
    id: int
    title: str
    publication_year: int
    authors_id: []
    citations: {}

    def __init__(self, paper):
        self.id = paper.id
        self.title = paper.title
        self.publication_year = paper.publication_year
        self.authors_id = paper.authors  # name of class object differs from name of JSON object
        self.citations = paper.citations


# general statistics of IU
class University:
    num_publications: int
    num_researchers: int
    public_per_person: int
    cit_per_person: int

    def __init__(self):
        self.cit_per_person = 0


# write JSON file
def write(dt, filename):
    dt = json.dumps(dt)
    dt = json.loads(str(dt))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dt, file, indent=3)


# automatic refresh of the remote DB
def refresh():
    hours = datetime.now().timetuple().tm_hour
    minutes = datetime.now().timetuple().tm_min
    seconds = datetime.now().timetuple().tm_sec
    weekday = datetime.today().isoweekday()
    status = "denied"
    if weekday == 4 and hours == 3 and minutes == 0 and seconds == 0:
        status = requests.get("https://2f163d15-91eb-4a19-bb02-eee0c23503a5.mock.pstmn.io/update").json()['state']
    return status


# convert String to Integer
def strToInt(string):
    return int(string)


# convert String keys to Integer keys in dictionary
def dicToInt(dictionary):
    for key in dictionary.keys():
        dictionary[key] = int(dictionary.get(key))
    return dictionary


# convert String elements to Integer elements in list
def listToInt(list):
    return map(int, list)


# count sum of all dictionary values
def dicValuesSum(dictionary):
    df = eval(dictionary)
    return sum(map(int, df.values()))


# download data
data = requests.get("https://84c72655-369d-40ae-ae04-8880a8b56f27.mock.pstmn.io/data").json()
authors = pd.DataFrame(data["authors"])
authors.set_index("id")
papers = pd.read_csv("papers_full.csv", index_col="id")

# dataframes modification
authors["overall_citation"] = authors["overall_citation"].apply(strToInt)
authors["hirsch_ind"] = authors["hirsch_ind"].apply(strToInt)
authors["citations"] = authors["citations"].apply(dicToInt)
authors["papers_published"] = authors["papers_published"].apply(dicToInt)
authors["paper_id"] = authors["paper_id"].apply(listToInt)

papers["source_quartile"] = papers["source_quartile"].apply(strToInt)
papers["citations"] = papers["citations"].apply(dicValuesSum)


# get statistics of IU
uni = University()
uni.num_researchers = len(authors)
uni.num_publications = len(papers)
uni.public_per_person = uni.num_publications / uni.num_researchers
uni.cit_per_person = authors['overall_citation'].sum() / uni.num_researchers


# write(data, 'data_output.json')
