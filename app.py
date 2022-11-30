import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, redirect, render_template, request, send_file, url_for
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from pybliometrics.scopus import ScopusSearch

import data
user=os.environ['DB_USERNAME']
password=os.environ['DB_PASSWORD']
db_name=os.environ['DB_NAME']
db_adress=os.environ['DB_ADRESS']
db_port=os.environ['DB_PORT']

basedir = os.path.abspath(os.path.dirname(__file__))

# todo rename app to bibliometrics again
bibliometrics = Flask(__name__)
bibliometrics.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{db_adress}:{db_port}/{db_name}'
db = SQLAlchemy(bibliometrics)

matplotlib.use("Agg")


#todo move to separate file
class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    doc_type = db.Column(db.String(255))
    source_type = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    publication_date = db.Column(db.Date())
    quartile = db.Column(db.String(15))
    number_of_citations = db.Column(db.Integer)
    doi = db.Column(db.String(100))
    # updated_at = db.Column(db.Date())
    # affiliations
    # authors

    def __repr__(self):
        return f'<Publication "{self.title}">'


#todo move to separate file
class ScopusDataRetriever:
    scopus_fields_to_db_fields_mapping = {
        "title": "title",
        "doc_type": "subtypeDescription",
        "source_type": "aggregationType",
        "number_of_citations": "citedby_count",
        "doi": "doi"

    }

    def retrieve_data_from_scopus(self):
        search_results = ScopusSearch('( AF-ID ( "Innopolis University"   60105869 ) )', subscriber=False).results
        for result in search_results:
            values = {
                key: getattr(result, value) for key, value in self.scopus_fields_to_db_fields_mapping.items()
            }
            values["publication_date"] = datetime.strptime(getattr(result, "coverDate"), '%Y-%m-%d').date()
            publication = Publication(**values)
            db.create_all()
            db.session.add(publication)
        db.session.commit()


# @app.route('/testing_models')
# def test_view_function():
#     publications = Publication.query.all()
#     return render_template('test_index.html', publications=publications)


@bibliometrics.route('/refresh-data')
def refresh_data():
    scopus_data_retriever = ScopusDataRetriever()
    scopus_data_retriever.retrieve_data_from_scopus()
    return "Success"


@bibliometrics.route("/")
def main_page():
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")
    arrow = url_for("static", filename="images/arrow_up.jpg")
    number1 = url_for("static", filename="images/1.jpg")
    number2 = url_for("static", filename="images/2.jpg")
    number3 = url_for("static", filename="images/3.jpg")
    number4 = url_for("static", filename="images/4.jpg")
    return render_template(
        "base.html",
        title="Bibliogram",
        main_logo=main_logo,
        main_title=main_title,
        arrowUp=arrow,
        number1=number1,
        number2=number2,
        number3=number3,
        number4=number4,
        amount_of_publications=data.uni.num_publications,
        number_of_researches=data.uni.num_researchers,
        publications_per_person=data.uni.public_per_person,
        citations_per_person=data.uni.cit_per_person,
    )


@bibliometrics.route("/search", methods=["POST", "GET"])
def search_author():
    authors = data.authors.rename(columns=lambda x: x[0].upper() + x[1:])
    filt = authors["Institution"].str.contains("Innopolis University")
    authors = authors.loc[filt].sort_values(by="Overall_citations", ascending=False)
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")
    arrow = url_for("static", filename="images/arrow_up.jpg")

    def to_list(arg):
        return list(arg)

    if request.method == "POST":
        author_name = request.form["author"]
        filt = (
            authors["Name"].apply(lambda x: x.lower()).str.contains(author_name.lower())
        )
        authors = authors.loc[filt]

    return render_template(
        "search_page.html",
        title="Search for authors",
        authors=authors.set_index("Id"),
        list=list(authors["Id"].values),
        add_data=data.authors_add,
        photos=data.authors_photos,
        main_logo=main_logo,
        main_title=main_title,
        to_list=to_list,
        arrowUp=arrow,
    )


@bibliometrics.route("/author_id=<int:id>")
def author(id):
    mains_logo = url_for("static", filename="images/dark_logo.png")
    mains_title = url_for("static", filename="images/innopolis_title.png")
    authors_data = data.authors.set_index("id")
    authors_data = authors_data.loc[id]

    citations = authors_data["citations"]
    citations_max = int(citations[max(citations, key=citations.get)])
    papers_published = authors_data["papers_published"]
    papers_published_max = int(
        papers_published[max(papers_published, key=papers_published.get)]
    )

    myList2 = citations.items()
    myList2 = sorted(myList2)
    x2, y2 = zip(*myList2)

    x2 = list(x2)
    y2 = list(y2)

    y_plot = pd.Series(y2)

    fig = plt.figure(figsize=(16, 12))
    ax = y_plot.plot(kind="bar", color="#036e8e", width=0.08)
    ax.set_xticklabels(x2)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(20)

    rects = ax.patches

    for rect2, label in zip(rects, y2):
        height = rect2.get_height()
        ax.text(
            rect2.get_x() + rect2.get_width() / 2,
            height + citations_max / 80,
            label,
            ha="center",
            va="baseline",
            family="Arial",
            size=23.5,
        )

    ax.plot(x2, y2, "#004", lw=2)

    fig.savefig("static/images/graphic_author_citations.png")
    plt.close(fig)

    im = Image.open("static/images/graphic_author_citations.png")
    width, height = im.size
    im1 = im.crop((110, 130, width - 150, height - 30))
    im1.save("static/images/graphic_author_citations.png")

    myList = papers_published.items()
    myList = sorted(myList)
    x, y = zip(*myList)

    x = list(x)
    y = list(y)

    y_plot = pd.Series(y)

    fig = plt.figure(figsize=(16, 12))
    ax = y_plot.plot(kind="bar", color="#036e8e", width=0.08)
    ax.set_xticklabels(x)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(20)

    rects = ax.patches

    for rect, label in zip(rects, y):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            height + papers_published_max / 200,
            label,
            ha="center",
            va="bottom",
            family="Arial",
            size=23.5,
        )

    ax.plot(x, y, "#004", lw=2)

    fig.savefig("static/images/graphic_author_papers.png")
    plt.close(fig)

    im = Image.open("static/images/graphic_author_papers.png")
    width, height = im.size
    im1 = im.crop((110, 130, width - 150, height - 30))
    im1.save("static/images/graphic_author_papers.png")

    if authors_data["name"] in list(data.authors_add["name"].values):
        authors_add = data.authors_add.set_index("name")
        if_photo = True
        photo_link = authors_add.loc[authors_data["name"]]["photo_link"]
        if authors_add.loc[authors_data["name"]]["department"] != "No department":
            department = authors_add.loc[authors_data["name"]]["department"]
        else:
            department = ""
        disciplines = authors_add.loc[authors_data["name"]]["disciplines"]

    else:
        if_photo = False
        photo_link = ""
        department = ""
        disciplines = []

    return render_template(
        "author_page.html",
        author=authors_data,
        id=id,
        if_photo=if_photo,
        photo_link=photo_link,
        department=department,
        disciplines=disciplines,
        photos=data.authors_photos,
        main_logo=mains_logo,
        main_title=mains_title,
    )


@bibliometrics.route("/publications/page=<int:num>", methods=["POST", "GET"])
def publications(num):  # pragma: no cover
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")
    arrow_left = url_for("static", filename="images/arrow_left.jpg")
    arrow_right = url_for("static", filename="images/arrow_right.jpg")
    arrow = arrow = url_for("static", filename="images/arrow_up.jpg")

    # dataframe modification for further displaying
    data.page_check("general_publications")

    all_papers = data.data_modification(data.publications)

    if request.method == "POST":

        if "filtration" in request.form:
            # setting filters
            data.date_filter = data.date_check_with(request.form.getlist("date_filter"))
            data.source_filter = data.source_check_with(
                request.form.getlist("source_filter")
            )
            data.quart_filter = data.quart_check_with(
                list(map(int, request.form.getlist("quartile_filter")))
            )
            if request.form["citations_from"]:
                cit_from = int(request.form["citations_from"])
            else:
                cit_from = 0
            if request.form["citations_to"]:
                cit_to = int(request.form["citations_to"])
            else:
                cit_to = 100000
            data.citations_from, data.citations_to = data.cit_check_with(
                cit_from, cit_to
            )

            all_papers = data.data_modification(data.publications)

        elif "parameters" in request.form:
            data.parameters = sum(
                [["Authors Names"], ["Title"], request.form.getlist("show")], list()
            )
            all_papers = data.data_modification(data.publications)

        elif "sorting" in request.form:
            data.sorting = data.sorting_check_with(request.form["sort"])
            if request.form.get("order"):
                data.order = False
            else:
                data.order = True

            all_papers = data.data_modification(data.publications)

        elif "downloading" in request.form:
            file_type = request.form["download"]
            data.download_file(all_papers, file_type)
            return send_file(bibliometrics.root_path + "\\downloads\\download." + file_type)

        elif "page" in request.form:
            new_num = int(request.form["page"])
            print(new_num)
            if new_num > 0 and new_num * 20 - all_papers.shape[0] <= 20:
                return redirect("/publications/page=" + str(new_num))
            else:
                return redirect("/publications/page=" + str(num))

    return render_template(
        "publications_page.html",
        papers=all_papers,
        main_logo=main_logo,
        main_title=main_title,
        arrow_left=arrow_left,
        arrow_right=arrow_right,
        page_num=num,
        arrowUp=arrow,
    )


@bibliometrics.route("/co-author=<int:id>", methods=["POST", "GET"])
def co_authors(id):
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")

    authors_data = data.authors
    author_data = authors_data.set_index("id").loc[id]
    filt = data.publications["Authors Names"].str.contains(author_data["name"])
    author_papers = data.publications.loc[filt]
    list_ind = list(author_papers.index)

    co_authors_list = []
    for ind in list_ind:
        co_authors_list.append(author_papers.loc[ind]["Authors ID"])
    co_authors_list = list(set(sum(co_authors_list, list())))
    co_authors_list.remove(id)

    co_au_names = "Co-Authors Names"
    authors_id = "ID"
    joint_pub = "Quantity of joint publications"
    affil = "Affiliation"

    co_authors_data = {authors_id: [], co_au_names: [], joint_pub: [], affil: []}

    for au_id in co_authors_list:
        com_papers = 0
        affiliation = []

        for ind in list_ind:
            if au_id in author_papers.loc[ind]["Authors ID"]:
                com_papers += 1
                affiliation.append(
                    eval(author_papers.loc[ind]["Authors Affiliation"])[str(au_id)]
                )
        affiliation = ", ".join(set(sum(affiliation, list())))

        if au_id in list(authors_data["id"].values):
            temp_list = co_authors_data.get(authors_id)
            temp_list.append(au_id)
            co_authors_data[authors_id] = temp_list

            temp_list = co_authors_data.get(co_au_names)
            temp_list.append(authors_data.set_index("id").loc[au_id]["name"])
            co_authors_data[co_au_names] = temp_list

            temp_list = co_authors_data.get(joint_pub)
            temp_list.append(com_papers)
            co_authors_data[joint_pub] = temp_list

            temp_list = co_authors_data.get(affil)
            temp_list.append(affiliation)
            co_authors_data[affil] = temp_list

    co_authors_data = (
        pd.DataFrame(co_authors_data)
        .set_index("ID")
        .sort_values(by=joint_pub, ascending=False)
    )

    if request.method == "POST":
        file_type = request.form["download"]
        data.download_file(co_authors_data, file_type)
        return send_file(bibliometrics.root_path + "\\downloads\\download." + file_type)

    return render_template(
        "co-author.html",
        author_name=author_data["name"],
        co_authors_id=list(co_authors_data.index),
        co_authors=co_authors_data,
        id=id,
        main_logo=main_logo,
        main_title=main_title,
    )


@bibliometrics.route("/author_publications=<int:id>", methods=["POST", "GET"])
def author_publications(id):  # pragma: no cover
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")
    author_data = data.authors.set_index("id")
    author_data = author_data.loc[id]

    # dataframe modification for further displaying
    data.page_check(author_data["name"])

    filt = data.publications["Authors Names"].str.contains(author_data["name"])

    papers = data.data_modification(data.publications.loc[filt])

    if request.method == "POST":

        if "filtration" in request.form:
            data.source_filter = data.source_check_with(
                request.form.getlist("source_filter")
            )
            data.date_filter = data.date_check_with(request.form.getlist("date_filter"))
            data.quart_filter = data.quart_check_with(
                list(map(int, request.form.getlist("quartile_filter")))
            )
            if request.form["citations_to"]:
                cit_to = int(request.form["citations_to"])
            else:
                cit_to = 100000
            if request.form["citations_from"]:
                cit_from = int(request.form["citations_from"])
            else:
                cit_from = 0
            data.citations_from, data.citations_to = data.cit_check_with(
                cit_from, cit_to
            )

            papers = data.data_modification(data.publications.loc[filt])

        elif "parameters" in request.form:
            data.parameters = sum(
                [["Authors Names"], ["Title"], request.form.getlist("show")], list()
            )
            papers = data.data_modification(data.publications.loc[filt])

        elif "sorting" in request.form:
            data.sorting = data.sorting_check_with(request.form["sort"])
            if request.form.get("order"):
                data.order = False
            else:
                data.order = True

            papers = data.data_modification(data.publications.loc[filt])

        elif "downloading" in request.form:
            file_type = request.form["download"]
            data.download_file(papers, file_type)
            return send_file(bibliometrics.root_path + "\\downloads\\download." + file_type)

    return render_template(
        "author_publications.html",
        author=author_data,
        id=id,
        papers=papers,
        main_logo=main_logo,
        main_title=main_title,
        arrowUp=url_for("static", filename="images/arrow_up.jpg"),
    )


@bibliometrics.route("/refresh")
def refresh():
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")
    date = data.cur_date

    return render_template(
        "refresh_page.html",
        main_logo=main_logo,
        main_title=main_title,
        date=date,
    )


@bibliometrics.route("/general", methods=["POST", "GET"])
def general():
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")

    filt = data.publications["Affiliation"].str.contains("Innopolis University")
    papers = data.publications.loc[filt]

    indicators_names = [
        "Number of all publications",
        "Articles",  # 1
        "Books",
        "Book Chapters",
        "Conference Papers",
        "Reviews",
        "Short Surveys",
        "Others",  # 7
        "Scopus",
        "Q1 & Q2",
        "Number of citations",
        ">10",
        "5-9",
        "1-4",
        "0",
    ]
    info = pd.DataFrame(indicators_names, columns=["Indicators"])

    for year in range(2016, 2023):
        year_filt = papers["Publication Date"].apply(lambda x: x[:4]) == str(year)
        temp_papers = papers.loc[year_filt]
        info_param = [temp_papers.shape[0]]
        number = 0

        for type in indicators_names[1:7]:
            type = type[:-1]
            add_filt = temp_papers["Work Type"] == type
            info_param.append(temp_papers.loc[add_filt].shape[0])
            number += info_param[-1]
        info_param.append(temp_papers.shape[0] - number)

        info_param.append(temp_papers.shape[0])
        add_filt = (temp_papers["Quartile"] == 1) | (temp_papers["Quartile"] == 2)
        info_param.append(temp_papers.loc[add_filt].shape[0])
        info_param.append(sum(list(temp_papers["Citations"].values)))

        add_filt = temp_papers["Citations"] > 10
        info_param.append(temp_papers.loc[add_filt].shape[0])
        add_filt = (temp_papers["Citations"] > 4) & (temp_papers["Quartile"] < 10)
        info_param.append(temp_papers.loc[add_filt].shape[0])
        add_filt = (temp_papers["Citations"] > 0) & (temp_papers["Quartile"] < 5)
        info_param.append(temp_papers.loc[add_filt].shape[0])
        add_filt = temp_papers["Citations"] == 0
        info_param.append(temp_papers.loc[add_filt].shape[0])

        info[year] = info_param

    if request.method == "POST":
        file_type = request.form["download"]
        data.download_file(info, file_type)
        return send_file(bibliometrics.root_path + "\\downloads\\download." + file_type)

    add_filt_1 = info["Indicators"] == "Number of all publications"
    info_1 = info.loc[add_filt_1]

    types = [
        "Articles",
        "Books",
        "Book Chapters",
        "Conference Papers",
        "Reviews",
        "Short Surveys",
        "Others",
    ]
    add_filt_2 = info["Indicators"].isin(types)
    info_2 = info.loc[add_filt_2]

    scopus = [
        "Scopus",
        "Q1 & Q2",
        "Number of citations",
    ]
    add_filt_3 = info["Indicators"].isin(scopus)
    info_3 = info.loc[add_filt_3]

    citations = [
        ">10",
        "5-9",
        "1-4",
        "0",
    ]
    add_filt_4 = info["Indicators"].isin(citations)
    info_4 = info.loc[add_filt_4]

    return render_template(
        "general.html",
        main_logo=main_logo,
        main_title=main_title,
        info_1=info_1,
        info_2=info_2,
        info_3=info_3,
        info_4=info_4,
    )


if __name__ == "__main__":
    bibliometrics.run(port=8080, host="0.0.0.0")
