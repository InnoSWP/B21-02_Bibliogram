from flask_sqlalchemy import SQLAlchemy

app.config['SQL_DATABASE_URI'] = 'sqlite:///publications.db'
db = SQLAlchemy(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    #authors_id: []
    #citations: {}