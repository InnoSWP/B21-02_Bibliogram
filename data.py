import json
from datetime import datetime
from random import randint

import pandas as pd
import requests

# password for user update
password = "IU"


# authors from IU
# class Author:
#     id: int
#     name: str
#     photo_link: str
#     overall_citation: int
#     citations: {}
#     papers_published: {}
#     institution: str
#     department: str
#     hirsch_ind: int
#     disciplines: []
#     papers_id: []
#
#     def __init__(self, author):
#         self.id = author.id
#         self.name = author.name
#         self.photo_link = author.photo_link
#         self.overall_citation = author.overall_citation
#         self.citations = author.citations
#         self.papers_published = author.papers_published
#         self.institution = author.institution
#         self.department = author.department
#         self.hirsch_ind = author.hirsch_ind
#         self.disciplines = author.disciplines
#         self.papers_id = author.paper_id  # name of class object differs from name of JSON object
#
#
# # papers published in IU
# class Paper:
#     id: int
#     title: str
#     publication_year: int
#     authors_id: []
#     citations: {}
#
#     def __init__(self, paper):
#         self.id = paper.id
#         self.title = paper.title
#         self.publication_year = paper.publication_year
#         self.authors_id = paper.authors  # name of class object differs from name of JSON object
#         self.citations = paper.citations


# general statistics of IU
class University:
    num_publications: int
    num_researchers: int
    public_per_person: float
    cit_per_person: float

    def __init__(self):
        self.cit_per_person = 0


# write JSON file
def write(dt, filename):
    dt = json.dumps(dt)
    dt = json.loads(str(dt))
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dt, file, indent=3)


# automatic refresh of the remote DB
def refresh():
    hours = datetime.now().timetuple().tm_hour
    minutes = datetime.now().timetuple().tm_min
    seconds = datetime.now().timetuple().tm_sec
    weekday = datetime.today().isoweekday()
    status = "denied"
    if weekday == 4 and hours == 3 and minutes == 0 and seconds == 0:
        status = requests.get(
            "https://2f163d15-91eb-4a19-bb02-eee0c23503a5.mock.pstmn.io/update"
        ).json()["state"]
    return status


# update remote DB by user
def update(input):
    status = "denied"
    if password == input:
        status = requests.get(
            "https://2f163d15-91eb-4a19-bb02-eee0c23503a5.mock.pstmn.io/update"
        ).json()["state"]
    return status


# convert String to Integer
def str_to_int(string_word):
    return int(string_word)


# convert String keys to Integer keys in dictionary
def dic_to_int(dictionary):
    for key in dictionary.keys():
        dictionary[key] = int(dictionary.get(key))
    return dictionary


# convert String elements to Integer elements in list
def list_to_int(list):
    return map(int, list)


# count sum of all dictionary values
def dic_values_sum(dictionary):
    df = eval(dictionary)
    return sum(map(int, df.values()))


def ind_to_name(data_authors, authors_names):

    name = ["Michael", "Laura", "Jack", "Daniel", "Robbin", "Bruce", "Stephen"]
    surname = ["Johns", "Black", "Jordan", "White", "Oscar", "Lee", "Castle"]
    # temp_array = []

    for i in range(len(authors_names)):
        if authors_names[i] in list(data_authors["id"].values):
            authors_names[i] = data_authors.set_index("id").loc[
                authors_names[i], "name"
            ]
        else:
            authors_names[i] = name[randint(0, 6)] + " " + surname[randint(0, 6)]
    return authors_names


def page_check(page):
    global page_name
    global filters
    global sorting
    if page_name != page:
        page_name = page
        sorting = "Title"
        filters = [
            "Title",
            "Source Type",
            "Work Type",
            "Publisher",
            "Publication Date",
            "Authors Names",
            "Affiliation",
            "Quartile",
            "Citations",
            "DOI",
        ]


def sorting_check_with(new_sort):
    if sorting not in filters:
        return "Title"
    return new_sort


def sorting_check():
    if sorting not in filters:
        return "Title"
    return sorting


# download data
data = requests.get(
    "https://84c72655-369d-40ae-ae04-8880a8b56f27.mock.pstmn.io/data"
).json()

# authors = pd.DataFrame(data["authors"])
authors = pd.read_json("authors_info.json")
authors_add = pd.read_json("authors_4_0.json")
papers = pd.read_csv("papers_v1.csv", index_col="id")

# dataframes modification
authors["citations"] = authors["citations"].apply(dic_to_int)
authors["hirsch_ind"] = authors["hirsch_ind"].apply(str_to_int)
authors["overall_citation"] = authors["citations"].apply(lambda x: sum(x.values()))

authors["papers_published"] = authors["papers_published"].apply(dic_to_int)
# authors["paper_id"] = authors["paper_id"].apply(list_to_int)
authors["papers_number"] = authors["papers_published"].apply(lambda x: sum(x.values()))
authors["start_date"] = authors["papers_published"].apply(
    lambda x: min([y for y in x.keys() if x[y] != 0])
)

papers["source_quartile"] = papers["source_quartile"].apply(
    lambda x: abs(str_to_int(x))
)
papers["citations"] = papers["citations"].apply(dic_values_sum)

source_type = "Source Type"
work_type = "Work Type"
authors_id = "Authors"
authors_names = "Authors Names"
public_date = "Publication Date"
affiliation = "Affiliation"
authors_affiliation = "Authors Affiliation"
sorting = ""
filters = [
    "Title",
    "Publisher",
    "Quartile",
    "Citations",
    "DOI",
    source_type,
    work_type,
    authors_names,
    affiliation,
    public_date,
]
page_name = ""
publications = papers
publications = publications.rename(columns=lambda x: x[0].upper() + x[1:])
publications.rename(
    columns={
        "Publication_date": public_date,
        "Doi": "DOI",
        "Source_type": source_type,
        "Work_type": work_type,
        "Source_quartile": "Quartile",
        "Authors_affils": authors_affiliation,
    },
    inplace=True,
)
publications[authors_id] = publications[authors_affiliation].apply(lambda x: list(eval(x).keys()))

publications[affiliation] = publications[authors_affiliation].apply(lambda x: eval(x).values())
publications[affiliation] = publications[affiliation].apply(
    lambda x: set(sum(x, list()))
)
publications[affiliation] = publications[affiliation].apply(lambda x: ", ".join(x))
publications.drop(columns=authors_affiliation, inplace=True)
publications = publications.reindex(
    columns=[
        "Title",
        source_type,
        work_type,
        "Publisher",
        public_date,
        authors_id,
        affiliation,
        "Quartile",
        "Citations",
        "DOI",
    ]
)

author_data = authors
publications[authors_names] = publications[authors_id]
publications[authors_names] = publications[authors_names].apply(
    lambda x: ind_to_name(author_data, x)
)
publications[authors_names] = publications[authors_names].apply(
    lambda x: ",\n".join(x)
)
publications[authors_id] = publications[authors_id].apply(lambda x: ",\n".join(x))


# get statistics of IU
uni = University()
uni.num_researchers = authors.shape[0]
uni.num_publications = papers.shape[0]
uni.public_per_person = uni.num_publications / uni.num_researchers
uni.cit_per_person = authors["overall_citation"].sum() / uni.num_researchers

# write(data, "data_output.json")
