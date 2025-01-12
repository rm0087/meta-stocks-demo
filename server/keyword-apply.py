from app import app
from models import db, Company, Keyword, CoKeyAssoc
from k_lists.alzheimers import keyword as kw, companies as cos




with app.app_context():
    db.session.query(CoKeyAssoc).delete()
    db.session.commit()
    
    kw_id = kw['id']
    k1 = Keyword.query.filter(Keyword.id == kw_id).first()

    batch = []
    exceptions = []
    for co in cos:
        try:
            company = Company.query.filter(Company.ticker==co[0]).first()
            assoc = CoKeyAssoc(company_id=company.id, keyword_id=k1.id, context=co[1])
            print(company.id, k1.id, co[1], company.name)
            batch.append(assoc)
        except AttributeError as e:
            ex = (co, e)
            exceptions.append(ex)
    
    db.session.add_all(batch)
    db.session.commit()
    print()
    print("THE FOLLOWING WERE NOT ENTERED INTO THE DATABASE:")
    for ex in exceptions:
        print(ex)
        
        





