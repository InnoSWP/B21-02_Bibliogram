import data
from flask import Flask, render_template, url_for, request


app = Flask(__name__)


@app.route('/')
def main_page():
    main_logo = url_for('static', filename='images/dark_logo.png')
    main_title = url_for('static', filename='images/innopolis_title.png')
    arrow = url_for('static', filename='images/arrow_up.jpg')
    number1 = url_for('static', filename='images/1.jpg')
    number2 = url_for('static', filename='images/2.jpg')
    number3 = url_for('static', filename='images/3.jpg')
    number4 = url_for('static', filename='images/4.jpg')
    return render_template('base.html', title='Bibliogram',
                           main_logo=main_logo, main_title=main_title, arrowUp=arrow, number1=number1,
                           number2=number2,
                           number3=number3,
                           number4=number4,
                           amount_of_publications=data.uni.num_publications,
                           number_of_researches=data.uni.num_researchers,
                           pubications_per_person=data.uni.public_per_person,
                           citations_per_person=data.uni.cit_per_person)


@app.route('/aboutIU')
def about_section():
    arrowUp = url_for('static', filename='images/arrow_down.jpg')
    return render_template('about_page.html', title='About IU',
                           amount_of_publications=data.uni.num_publications,
                           number_of_researches=data.uni.num_researchers,
                           pubications_per_person=data.uni.public_per_person,
                           citations_per_person=data.uni.cit_per_person,
                           arrowUp=arrowUp)


@app.route('/features')
def features_section():
    number1 = url_for('static', filename='images/1.jpg')
    number2 = url_for('static', filename='images/2.jpg')
    number3 = url_for('static', filename='images/3.jpg')
    number4 = url_for('static', filename='images/4.jpg')
    arrow_up = url_for('static', filename='images/arrow_up.jpg')
    arrow_down = url_for('static', filename='images/arrow_down.jpg')
    return render_template('features_page.html', title='What to see here?',
                           number1=number1,
                           number2=number2,
                           number3=number3,
                           number4=number4, arrowUp=arrow_up, arrowDown=arrow_down)


@app.route('/search', methods=['POST', 'GET'])
def search_author():

    authors = data.authors.rename(columns=lambda x: x[0].upper()+x[1:])

    if request.method == 'POST':
        author_name = request.form['author']
        filt = authors["Name"].apply(lambda x: x.lower()).str.contains(author_name.lower())
        authors = authors.loc[filt]

    return render_template('search_page.html', title='Search for authors', authors=authors)


@app.route('/author_id=<int:id>')
def author(id):

    author_data = data.authors.set_index("id")
    author_data = author_data.loc[id]
    return render_template('author_page.html', author=author_data, id=id)


@app.route('/publications')
def publications():

    # dataframe modification for further displaying
    papers = data.papers.rename(columns=lambda x: x[0].upper()+x[1:])
    papers.rename(columns={"Publication_date": "Publication Date",
                           "Doi": "DOI",
                           "Source_type": "Source Type",
                           "Work_type": "Work Type",
                           "Source_quartile": "Quartile",
                           "Authors_affils": "Authors Affiliation"}, inplace=True)
    papers["Authors"] = papers["Authors Affiliation"].apply(lambda x: eval(x).keys())
    papers["Authors"] = papers["Authors"].apply(lambda x: ",\n".join(x))
    papers["Affiliation"] = papers["Authors Affiliation"].apply(lambda x: eval(x).values())
    papers["Affiliation"] = papers["Affiliation"].apply(lambda x: set(sum(x, list())))
    papers["Affiliation"] = papers["Affiliation"].apply(lambda x: ", ".join(x))
    papers.drop(columns="Authors Affiliation", inplace=True)
    papers = papers.reindex(columns=["Title", "Source Type", "Work Type", "Publisher", "Publication Date",
                            "Authors", "Affiliation", "Quartile", "Citations", "DOI"])

    return render_template('publications_page.html', papers=papers)


@app.route('/co-author=<int:id>')
def co_authors(id):

    author_data = data.authors.set_index("id")
    author_data = author_data.loc[id]

    return render_template('co-author.html', author=author_data, id=id, papers=data.papers)


@app.route('/author_publications=<int:id>')
def author_publications(id):

    author_data = data.authors.set_index("id")
    author_data = author_data.loc[id]

    return render_template('author_publications.html', author=author_data, id=id, papers=data.papers)


@app.route('/test_public')
def test_public():
    main_logo = url_for('static', filename='images/dark_logo.png')
    main_title = url_for('static', filename='images/innopolis_title.png')
    return render_template('test_public.html', title='Bibliogram',
                           main_logo=main_logo, main_title=main_title)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
