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
    global page_name, parameters, date_filter, source_filter
    global quart_filter, sorting, citations_to, citations_from
    global is_data, is_source, is_quart, is_cit

    if page_name != page:
        is_data = True
        is_source = True
        is_quart = True
        is_cit = True
        page_name = page
        sorting = "Title"
        parameters = [
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
        date_filter = [str(x) for x in range(2009, 2023)]
        source_filter = [
            "Conference Proceeding",
            "Journal",
            "Book Series",
            "Trade Journal",
            "Book",
        ]
        quart_filter = [1, 2, 3, 4, 100000]
        citations_from = 0
        citations_to = 100000


def sorting_check_with(new_sort):
    if new_sort not in parameters:
        return "Title"
    return new_sort


def sorting_check():
    if sorting not in parameters:
        return "Title"
    return sorting


def date_check_with(new_date_list):
    global is_data
    if "Publication Date" not in parameters:
        is_data = False
        return [str(x) for x in range(2009, 2023)]
    else:
        is_data = True
        return new_date_list


def date_check():
    global is_data
    if "Publication Date" not in parameters:
        is_data = False
        return [str(x) for x in range(2009, 2023)]
    else:
        is_data = True
        return date_filter


def source_check_with(new_source_list):
    global is_source
    if "Source Type" not in parameters:
        is_source = False
        return ["Conference Proceeding", "Journal", "Book Series", "Trade Journal", "Book"]
    else:
        is_source = True
        return new_source_list


def source_check():
    global is_source
    if "Source Type" not in parameters:
        is_source = False
        return ["Conference Proceeding", "Journal", "Book Series", "Trade Journal", "Book"]
    else:
        is_source = True
        return source_filter


def quart_check_with(new_quart_list):
    global is_quart
    if "Quartile" not in parameters:
        is_quart = False
        return [1, 2, 3, 4, 100000]
    else:
        is_quart = True
        return new_quart_list


def quart_check():
    global is_quart
    if "Quartile" not in parameters:
        is_quart = False
        return [1, 2, 3, 4, 100000]
    else:
        is_quart = True
        return quart_filter


def cit_check_with(cit_from, cit_to):
    global is_cit
    if "Citations" not in parameters:
        is_cit = False
        return 0, 100000
    else:
        is_cit = True
        return cit_from, cit_to


def cit_check():
    global is_cit
    if "Citations" not in parameters:
        is_cit = False
        return 0, 100000
    else:
        is_cit = True
        return citations_from, citations_to


def data_modification(papers_data):
    global date_filter, source_filter, quart_filter, citations_from, citations_to, sorting

    date_filter = date_check()
    if is_data:
        filt_1 = papers_data["Publication Date"].apply(lambda x: x[:4]).isin(date_filter)
        papers_data = papers_data.loc[filt_1]

    source_filter = source_check()
    if is_source:
        filt_2 = papers_data["Source Type"].isin(source_filter)
        papers_data = papers_data.loc[filt_2]

    quart_filter = quart_check()
    if is_quart:
        filt_4 = papers_data["Quartile"].isin(quart_filter)
        papers_data = papers_data.loc[filt_4]

    citations_from, citations_to = cit_check()
    if is_cit:
        filt_5 = (papers_data["Citations"] >= citations_from) & \
                 (papers_data["Citations"] <= citations_to)
        papers_data = papers_data.loc[filt_5]

    sorting = sorting_check()

    return papers_data[parameters].sort_values(by=sorting, ascending=order)

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
papers["source_quartile"] = papers["source_quartile"].apply(lambda x: 100000 if x == -1 else x)
papers["citations"] = papers["citations"].apply(dic_values_sum)
papers["publication_year"] = papers["publication_date"].apply(lambda x: x[:4])

source_type = "Source Type"
work_type = "Work Type"
authors_id = "Authors ID"
authors_names = "Authors Names"
public_date = "Publication Date"
affiliation = "Affiliation"
authors_affiliation = "Authors Affiliation"

sorting = ""
page_name = ""
order = True
is_data = True
is_source = True
is_quart = True
is_cit = True
date_filter = [str(x) for x in range(2009, 2023)]
source_filter = [
    "Conference Proceeding",
    "Journal",
    "Book Series",
]
quart_filter = [1, 2, 3, 4, 100000]
citations_from = 0
citations_to = 100000
parameters = [
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
        "id": "ID",
        "publication_year": "Publication Year",
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
        "ID",
        authors_id,
        authors_affiliation,
        "Publication Year",
    ]
)


# get statistics of IU
uni = University()
uni.num_researchers = authors.shape[0]
uni.num_publications = papers.shape[0]
uni.public_per_person = round(uni.num_publications / uni.num_researchers, 2)
uni.cit_per_person = round(authors["overall_citations"].sum() / uni.num_researchers, 2)


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

# fig, axes = plt.subplots(1, 1, figsize=(16, 12))
#
# axes.plot(x, y, "#004", lw=2)
# axes.grid(False)
# axes.bar(x, y, color="#036e8e", width=0.08)
# plt.ylim(ymin=0, ymax=2200)
# plt.rc("axes", labelsize=1000)

# fig.savefig("static/images/graphic.png")
# plt.close(fig)
#
# im = Image.open("static/images/graphic.png")
# width, height = im.size
# im1 = im.crop((150, 130, width - 150, height - 100))
# im1.save("static/images/graphic.png")

x = list(x)
y = list(y)

y_plot = pd.Series(y)

fig = plt.figure(figsize=(16, 12))
ax = y_plot.plot(kind="bar", color="#036e8e", width=0.08)
ax.set_xticklabels(x)

rects = ax.patches

for rect, label in zip(rects, y):
    height = rect.get_height()
    ax.text(
        rect.get_x() + rect.get_width() / 2,
        height + 5,
        label,
        ha="center",
        va="bottom",
        family="Open Sans, arial",
        size="x-large",
    )

ax.plot(x, y, "#004", lw=2)

fig.savefig("static/images/graphic.png")
plt.close(fig)

im = Image.open("static/images/graphic.png")
width, height = im.size
im1 = im.crop((150, 130, width - 150, height - 80))
im1.save("static/images/graphic.png")
