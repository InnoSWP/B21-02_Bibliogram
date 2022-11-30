from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

PublicationAffiliation = db.Table(
    'publication_affiliation',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('publication_id', db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE')),
    db.Column('affiliation_id', db.Integer, db.ForeignKey('affiliation.id', ondelete='CASCADE')),
    db.UniqueConstraint('publication_id', 'affiliation_id')
)

PublicationAuthor = db.Table(
    'publication_author',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('publication_id', db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id', ondelete='CASCADE')),
    db.UniqueConstraint('publication_id', 'author_id')
)


class Publication(db.Model):
    __tablename__ = 'publication'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    doc_type = db.Column(db.String(255))
    source_type = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    publication_date = db.Column(db.Date())
    quartile = db.Column(db.String(15))
    number_of_citations = db.Column(db.Integer)
    doi = db.Column(db.String(100))
    affiliations = db.relationship('Affiliation', secondary=PublicationAffiliation, backref='publication')
    authors = db.relationship('Author', secondary=PublicationAuthor, backref='publication')
    #updated_at

    def __repr__(self):
        return f'<Publication "{self.title}">'


class Affiliation(db.Model):
    __tablename__ = 'affiliation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False, unique=True)

    def __repr__(self):
        return f'<Affiliation "{self.name}">'


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(500), nullable=False)
    h_index = db.Column(db.Integer())
    # updated_at
