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


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')