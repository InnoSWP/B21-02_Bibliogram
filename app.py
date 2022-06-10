from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def main_page():
    main_logo = url_for('static', filename='images/dark_logo.png')
    main_title = url_for('static', filename='images/innopolis_title.png')
    return render_template('base.html', title='Bibliogram',
                           main_logo=main_logo, main_title=main_title)


@app.route('/index')
def index():
    return "Hello, world!"


@app.route('/aboutIU')
def about_section():
    amount_of_publications = 0
    number_of_researches = 0
    pubications_per_person = 0
    citations_per_person = 0
    return render_template('about_page.html', title='About IU',
                           amount_of_publications=amount_of_publications,
                           number_of_researches=number_of_researches,
                           pubications_per_person=pubications_per_person,
                           citations_per_person=citations_per_person)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')