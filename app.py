from flask import Flask, render_template, url_for

import data

app = Flask(__name__)


@app.route('/')
def main_page():
    main_logo = url_for('static', filename='images/dark_logo.png')
    main_title = url_for('static', filename='images/innopolis_title.png')
    arrow = url_for('static', filename='images/arrow_down.jpg')
    return render_template('base.html', title='Bibliogram',
                           main_logo=main_logo, main_title=main_title, arrow=arrow)


@app.route('/aboutIU')
def about_section():
    arrowUp = url_for('static', filename='images/arrow_up.jpg')
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


@app.route('/search')
def search_author():
    photos = [url_for('static', filename='images/author_photoholder.jpg'),
              url_for('static', filename='images/holder2.png'),
              url_for('static', filename='images/holder1.jpeg')]
    return render_template('search_page.html', title='Search for authors', photos=photos)


@app.route('/author_id:0')
def author():
    return render_template('author_page.html')


@app.route('/publications')
def publications():
    return render_template('publications_page.html')


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
