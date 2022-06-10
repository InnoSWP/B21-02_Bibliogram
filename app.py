from flask import Flask, render_template, url_for

import data_parser

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

@app.route('/reload')
def index():
    return "Reload Button"

@app.route('/aboutIU')
def about_section():
    return render_template('about_page.html', title='About IU',
                           amount_of_publications=data_parser.uni.num_publications,
                           number_of_researches=data_parser.uni.num_researchers,
                           pubications_per_person=data_parser.uni.public_per_person,
                           citations_per_person=data_parser.uni.cit_per_person)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')