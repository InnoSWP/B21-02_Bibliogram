from flask_sqlalchemy import SQLAlchemy
from app import app
import requests


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///publications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PaperCitations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    citation = db.Column(db.Integer, nullable=False)


class AuthorCitations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    citation = db.Column(db.Integer, nullable=False)


class PapersOfAuthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    paper_id = db.Column(db.Integer, nullable=False)


class AuthorsOfPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)


class AuthorDisciplines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    discipline_name = db.Column(db.String(100), nullable=False)


class AuthorPublications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    num_of_publications = db.Column(db.Integer, nullable=False)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    photo_link = db.Column(db.String(100), nullable=False)
    overall_citation = db.Column(db.Integer, nullable=False)
    citations = AuthorCitations
    papers = AuthorPublications
    institution = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    hirsch_ind = db.Column(db.Integer, nullable=False)
    disciplines = AuthorDisciplines
    papers_id = PapersOfAuthor


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    publication_year = db.Column(db.Integer, nullable=False)
    authors_id = AuthorsOfPaper
    citations = PaperCitations
