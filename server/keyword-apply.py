from app import app
from models import db, Company, Keyword, CoKeyAssoc
from k_lists.alzheimers import keyword as kw, companies as cos
with app.app_context():
    kw_id = kw['id']
    k1 = Keyword.query.filter(Keyword.id == kw_id).first()

    batch = []
    for co in cos:
        
        company = Company.query.filter(Company.ticker==co[0]).first()
        print(company.id, k1.id, co[1])
        assoc = CoKeyAssoc(company_id=company.id, keyword_id=k1.id, context=co[1])
        batch.append(assoc)
    
    db.session.add_all(batch)
    db.session.commit()
        
        





