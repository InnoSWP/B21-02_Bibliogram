import data
from flask import Flask, render_template, request, send_file, url_for

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


@app.route("/aboutIU")
def about_section():
    arrow_up = url_for("static", filename="images/arrow_down.jpg")
    return render_template(
        "about_page.html",
        title="About IU",
        amount_of_publications=data.uni.num_publications,
        number_of_researches=data.uni.num_researchers,
        pubications_per_person=data.uni.public_per_person,
        citations_per_person=data.uni.cit_per_person,
        arrowUp=arrow_up,
    )


@app.route("/features")
def features_section():
    number1 = url_for("static", filename="images/1.jpg")
    number2 = url_for("static", filename="images/2.jpg")
    number3 = url_for("static", filename="images/3.jpg")
    number4 = url_for("static", filename="images/4.jpg")
    arrow_up = url_for("static", filename="images/arrow_up.jpg")
    arrow_down = url_for("static", filename="images/arrow_down.jpg")
    return render_template(
        "features_page.html",
        title="What to see here?",
        number1=number1,
        number2=number2,
        number3=number3,
        number4=number4,
        arrowUp=arrow_up,
        arrowDown=arrow_down,
    )


@app.route("/search", methods=["POST", "GET"])
def search_author():
    authors = data.authors.rename(columns=lambda x: x[0].upper() + x[1:])
    add_data = data.authors_add.set_index("name")

    if request.method == "POST":
        author_name = request.form["author"]
        filt = (
            authors["Name"].apply(lambda x: x.lower()).str.contains(author_name.lower())
        )
        authors = authors.loc[filt]

    return render_template(
        "search_page.html",
        title="Search for authors",
        authors=authors,
        add_data=add_data,
    )


@app.route("/author_id=<int:id>")
def author(id):
    author_data = data.authors.set_index("id")
    author_data = author_data.loc[id]
    author_add_data = data.authors_add.set_index("name")
    author_add_data = author_add_data.loc[author_data["name"]]

    return render_template(
        "author_page.html", author=author_data, id=id, add_data=author_add_data
    )


@app.route("/publications", methods=["POST", "GET"])
def publications():
    # dataframe modification for further displaying
    if data.page_name != "general_publications":
        data.page_name = "general_publications"
        data.sorting = "Title"

        data.filters = [
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

    papers = data.publications[data.filters].sort_values(by=data.sorting)

    if request.method == "POST":
        if "filtration" in request.form:
            data.filters = sum(
                [["Title"], ["Authors Names"], request.form.getlist("show")], list()
            )

            if data.sorting not in data.filters:
                data.sorting = "Title"

            papers = data.publications[data.filters].sort_values(by=data.sorting)

        elif "sorting" in request.form:
            data.sorting = request.form["sort"]

            if data.sorting not in data.filters:
                data.sorting = "Title"

            papers = data.publications[data.filters].sort_values(by=data.sorting)

        elif "downloading" in request.form:
            file_type = request.form["download"]

            if file_type == "tsv":
                papers.to_csv("downloads/download.tsv", sep="\t")
            elif file_type == "csv":
                papers.to_csv("downloads/download.csv")
            elif file_type == "json":
                papers.to_csv("downloads/download.json")
            elif file_type == "xlsx":
                papers.to_excel("downloads/download.xlsx")

            return send_file(app.root_path + "\\downloads\\download." + file_type)

    return render_template("publications_page.html", papers=papers)


@app.route("/co-author=<int:id>")
def co_authors(id):
    author_data = data.authors.set_index("id")
    author_data = author_data.loc[id]
    author_add_data = data.authors_add.set_index("name")
    author_add_data = author_add_data.loc[author_data["name"]]

    return render_template(
        "co-author.html",
        author=author_data,
        id=id,
        add_data=author_add_data,
        papers=data.papers,
    )


@app.route("/author_publications=<int:id>", methods=["POST", "GET"])
def author_publications(id):
    author_data = data.authors.set_index("id")
    author_data = author_data.loc[id]

    # dataframe modification for further displaying
    if data.page_name != author_data["name"]:
        data.page_name = author_data["name"]
        data.sorting = "Title"
        data.filters = [
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

    # filt = data.publications["Authors"].str.contains(id)

    papers = data.publications[data.filters].sort_values(by=data.sorting)

    if request.method == "POST":

        if "downloading" in request.form:
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

        elif "filtration" in request.form:
            data.filters = sum(
                [["Title"], ["Authors Names"], request.form.getlist("show")], list()
            )

            if data.sorting not in data.filters:
                data.sorting = "Title"

            papers = data.publications[data.filters].sort_values(by=data.sorting)

        elif "sorting" in request.form:
            data.sorting = request.form["sort"]

            if data.sorting not in data.filters:
                data.sorting = "Title"

            papers = data.publications[data.filters].sort_values(by=data.sorting)


    return render_template(
        "author_publications.html", author=author_data, id=id, papers=papers
    )


@app.route("/test_public")
def test_public():
    main_logo = url_for("static", filename="images/dark_logo.png")
    main_title = url_for("static", filename="images/innopolis_title.png")
    return render_template(
        "test_public.html",
        title="Bibliogram",
        main_logo=main_logo,
        main_title=main_title,
    )


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
