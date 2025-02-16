from app import app
from models import db, Company, Keyword, CoKeyAssoc

with app.app_context():
    assocs = CoKeyAssoc.query.all()
    batch = []
    i = 1
    for a in assocs:
        a.id = i
        i += 1
        batch.append(a)
    db.session.commit()





