import data
from flask import Flask, render_template, request, send_file, url_for, redirect

app = Flask(__name__)


@app.route("/")
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


@app.route("/search", methods=["POST", "GET"])
def search_author():
    authors = data.authors.rename(columns=lambda x: x[0].upper() + x[1:])
    filt = authors["Institution"].str.contains("Innopolis University")
    authors = authors.loc[filt].sort_values(by="Overall_citations", ascending=False)
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")

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
    )


@app.route("/author_id=<int:id>")
def author(id):
    mains_logo = url_for("static", filename="images/dark_logo.png")
    mains_title = url_for("static", filename="images/innopolis_title.png")
    authors_data = data.authors.set_index("id")
    authors_data = authors_data.loc[id]

    if authors_data["name"] in list(data.authors_add["name"].values):
        authors_add = data.authors_add.set_index("name")
        if_photo = True
        photo_link = authors_add.loc[authors_data["name"]]["photo_link"]
        department = authors_add.loc[authors_data["name"]]["department"]
        disciplines = authors_add.loc[authors_data["name"]]["disciplines"]

    else:
        if_photo = False
        photo_link = ""
        department = "Computer Science"
        disciplines = [
            "Machine Learning",
            "Neural Networks and Artificial Intelligence",
            "Computer Vision",
        ]

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


@app.route("/publications/page=<int:num>", methods=["POST", "GET"])
def publications(num):  # pragma: no cover
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")
    arrow_left = url_for("static", filename="images/arrow_left.jpg")
    arrow_right = url_for("static", filename="images/arrow_right.jpg")

    # dataframe modification for further displaying
    data.page_check("general_publications")

    all_papers = data.data_modification(data.publications)

    if request.method == "POST":

        if "filtration" in request.form:
            data.date_filter = data.date_check_with(request.form.getlist("date_filter"))
            data.source_filter = data.source_check_with(request.form.getlist("source_filter"))
            data.quart_filter = data.quart_check_with(list(map(int, request.form.getlist("quartile_filter"))))
            if request.form["citations_from"]:
                cit_from = int(request.form["citations_from"])
            else:
                cit_from = 0
            if request.form["citations_to"]:
                cit_to = int(request.form["citations_to"])
            else:
                cit_to = 100000
            data.citations_from, data.citations_to = data.cit_check_with(cit_from, cit_to)

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

            if file_type == "csv":
                all_papers.to_csv("downloads/download.csv")
            elif file_type == "tsv":
                all_papers.to_csv("downloads/download.tsv", sep="\t")
            elif file_type == "json":
                all_papers.to_csv("downloads/download.json")
            elif file_type == "xlsx":
                all_papers.to_excel("downloads/download.xlsx")

            return send_file(app.root_path + "\\downloads\\download." + file_type)

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
    )


@app.route("/co-author=<int:id>")
def co_authors(id):
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")

    authors_data = data.authors
    author_data = authors_data.set_index("id").loc[id]
    filt = data.publications["Authors Names"].str.contains(author_data["name"])
    author_papers = data.publications.loc[filt]
    print(author_papers)
    list_ind = list(author_papers.index)
    print(list_ind)

    co_authors_list = []
    for ind in list_ind:
        co_authors_list.append(author_papers.loc[ind]["Authors ID"])
    co_authors_list = list(set(sum(co_authors_list, list())))
    co_authors_list.remove(id)

    co_authors_dic = {}
    for au_id in co_authors_list:
        temp_dic = {}
        com_papers = 0
        affiliation = []

        for ind in list_ind:
            if au_id in author_papers.loc[ind]["Authors ID"]:
                com_papers += 1
                affiliation.append(eval(author_papers.loc[ind]["Authors Affiliation"])[str(au_id)])
        affiliation = ", ".join(set(sum(affiliation, list())))

        if au_id in list(authors_data["id"].values):
            temp_dic["name"] = authors_data.set_index("id").loc[au_id]["name"]
            temp_dic["common_papers"] = com_papers
            temp_dic["affiliation"] = affiliation
            co_authors_dic[au_id] = temp_dic

    return render_template(
        "co-author.html",
        author_name=author_data["name"],
        co_authors=co_authors_dic.keys(),
        co_authors_data=co_authors_dic,
        id=id,
        main_logo=main_logo,
        main_title=main_title,
    )


@app.route("/author_publications=<int:id>", methods=["POST", "GET"])
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
            data.source_filter = data.source_check_with(request.form.getlist("source_filter"))
            data.date_filter = data.date_check_with(request.form.getlist("date_filter"))
            data.quart_filter = data.quart_check_with(list(map(int, request.form.getlist("quartile_filter"))))
            if request.form["citations_to"]:
                cit_to = int(request.form["citations_to"])
            else:
                cit_to = 100000
            if request.form["citations_from"]:
                cit_from = int(request.form["citations_from"])
            else:
                cit_from = 0
            data.citations_from, data.citations_to = data.cit_check_with(cit_from, cit_to)

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

            if file_type == "csv":
                papers.to_csv("downloads/download.csv")
            elif file_type == "tsv":
                papers.to_csv("downloads/download.tsv", sep="\t")
            elif file_type == "xlsx":
                papers.to_excel("downloads/download.xlsx")
            elif file_type == "json":
                papers.to_csv("downloads/download.json")

            return send_file(app.root_path + "\\downloads\\download." + file_type)

    return render_template(
        "author_publications.html",
        author=author_data,
        id=id,
        papers=papers,
        main_logo=main_logo,
        main_title=main_title,
    )


@app.route("/refresh")
def refresh():
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")

    return render_template(
        "refresh_page.html",
        main_logo=main_logo,
        main_title=main_title,
    )


@app.route("/general")
def general():
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")

    return render_template(
        "general.html",
        main_logo=main_logo,
        main_title=main_title,
    )


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
