from flusk_sqlalchemy import SQLAlchemy

app.config['SQL_DATABASE_URI'] = 'sqlite:///publications.db'
db = SQLAlchemy(app)

