import json
from datetime import datetime
from random import randint
from photos import photos_dic

import matplotlib.pyplot as plt
import pandas as pd
import requests
from PIL import Image

# password for user update
password = "IU"


# general statistics of IU
class University:
    num_publications: int
    num_researchers: int
    public_per_person: float
    cit_per_person: float

    def __init__(self):
        self.cit_per_person = 0


# # automatic refresh of the remote DB
# def refresh():
#     hours = datetime.now().timetuple().tm_hour
#     minutes = datetime.now().timetuple().tm_min
#     seconds = datetime.now().timetuple().tm_sec
#     weekday = datetime.today().isoweekday()
#     status = "denied"
#     if weekday == 4 and hours == 3 and minutes == 0 and seconds == 0:
#         status = requests.get(
#             "https://2f163d15-91eb-4a19-bb02-eee0c23503a5.mock.pstmn.io/update"
#         ).json()["state"]
#     return status


# # update remote DB by user
# def update(input):
#     status = "denied"
#     if password == input:
#         status = requests.get(
#             "https://2f163d15-91eb-4a19-bb02-eee0c23503a5.mock.pstmn.io/update"
#         ).json()["state"]
#     return status


# convert String to Integer
def str_to_int(string_word):
    return int(string_word)


# convert String values to Integer values in dictionary
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


def ind_to_name(data_authors, author_id):
    temp_names = []
    list_id = list(data_authors["id"].values)
    data_authors = data_authors.set_index("id")

    for au_id in author_id:
        if au_id in list_id:
            temp_names.append(data_authors.loc[au_id]["name"])

    return temp_names


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
# data = requests.get(
#     "https://84c72655-369d-40ae-ae04-8880a8b56f27.mock.pstmn.io/data"
# ).json()

# authors = pd.DataFrame(data["authors"])
authors = pd.read_json("data/authors_info_new.json")
authors_add = pd.read_json("data/authors_add_info.json")
authors_photos = photos_dic
papers = pd.read_csv("data/papers_v1.csv", index_col="id")

# dataframes modification
authors["citations"] = authors["inno_affil_citations"].apply(dic_to_int)
authors["hirsch_ind"] = authors["hirsch_ind"].apply(str_to_int)
authors["overall_citations"] = authors["overall_citations"].apply(str_to_int)
# authors["overall_citation"] = authors["citations"].apply(lambda x: sum(x.values()))
authors["papers_published"] = authors["papers_published"].apply(dic_to_int)
authors["paper_id"] = authors["paper_id"].apply(list_to_int)
authors["papers_number"] = authors["papers_published"].apply(lambda x: sum(x.values()))
# authors["start_date"] = authors["papers_published"].apply(
#     lambda x: min([y for y in x.keys() if x[y] != 0])
# )
authors["institution"] = authors["institution"].apply(lambda x: ", ".join(x))

papers["source_quartile"] = papers["source_quartile"].apply(str_to_int)
papers["source_quartile"] = papers["source_quartile"].apply(lambda x: "-" if x == -1 else x)
papers["citations"] = papers["citations"].apply(dic_values_sum)

source_type = "Source Type"
work_type = "Work Type"
authors_id = "Authors ID"
authors_names = "Authors Names"
public_date = "Publication Date"
affiliation = "Affiliation"
authors_affiliation = "Authors Affiliation"

sorting = ""
page_name = ""
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
publications[authors_id] = publications[authors_affiliation].apply(
    lambda x: list(map(int, eval(x).keys()))
)

publications[affiliation] = publications[authors_affiliation].apply(
    lambda x: eval(x).values()
)
publications[affiliation] = publications[affiliation].apply(
    lambda x: set(sum(x, list()))
)
publications[affiliation] = publications[affiliation].apply(lambda x: ", ".join(x))
# publications.drop(columns=authors_affiliation, inplace=True)

publications[authors_names] = publications[authors_id].apply(
    lambda x: ind_to_name(authors, x)
)
publications[authors_names] = publications[authors_names].apply(lambda x: ",\n".join(x))

publications = publications.reindex(
    columns=[
        "Title",
        source_type,
        work_type,
        "Publisher",
        public_date,
        authors_names,
        affiliation,
        "Quartile",
        "Citations",
        "DOI",
    ]
)


# get statistics of IU
uni = University()
uni.num_researchers = authors.shape[0]
uni.num_publications = papers.shape[0]
uni.public_per_person = uni.num_publications / uni.num_researchers
uni.cit_per_person = authors["overall_citations"].sum() / uni.num_researchers


# creating a wordcloud
# create_wordcloud()
def date_citation():  # pragma: no cover
    dict = {}
    for ind in publications.index:
        if publications["Publication Date"][ind][0:4] not in dict:
            dict[publications["Publication Date"][ind][0:4]] = publications[
                "Citations"
            ][ind]
        else:
            dict[publications["Publication Date"][ind][0:4]] += publications[
                "Citations"
            ][ind]

    # return sorted(dict.items())
    return dict


tuple = date_citation()

# print(tuple)
myList = tuple.items()
myList = sorted(myList)
x, y = zip(*myList)

fig, axes = plt.subplots(1, 1, figsize=(16, 12))

axes.plot(x, y, "#004", lw=2)
axes.grid(False)
axes.bar(x, y, color="#036e8e", width=0.08)
plt.ylim(ymin=0, ymax=2200)
plt.rc("axes", labelsize=1000)

fig.savefig("static/images/graphic.png")
plt.close(fig)

im = Image.open("static/images/graphic.png")
width, height = im.size
im1 = im.crop((150, 130, width - 150, height - 100))
im1.save("static/images/graphic.png")
