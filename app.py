from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)


# general statistics of IU
class University:
    num_publications: int
    num_researchers: int
    public_per_person: int
    cit_per_person: int

    def __init__(self):
        self.cit_per_person = 0


# data parsing
data = requests.get("https://2f163d15-91eb-4a19-bb02-eee0c23503a5.mock.pstmn.io/data").json()
authors = data['authors']
papers = data['papers']

# get statistics of IU
uni = University()
uni.num_researchers = len(authors)
uni.num_publications = len(papers)
uni.public_per_person = uni.num_publications / uni.num_researchers
for auth in authors:
    uni.cit_per_person += int(auth['overall_citation'])
uni.cit_per_person /= uni.num_researchers


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
    return render_template('about_page.html', title='About IU',
                           amount_of_publications=uni.num_publications,
                           number_of_researches=uni.num_researchers,
                           pubications_per_person=uni.public_per_person,
                           citations_per_person=uni.cit_per_person)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')