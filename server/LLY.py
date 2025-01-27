from app import app
from models import db, Company, Keyword, CoKeyAssoc

with app.app_context():
    co = db.session.get(Company, 9)

    # CoKeyAssoc(company_id=co.id, keyword_id=, context="")
    ck1 = CoKeyAssoc(company_id=co.id, keyword_id=38, context=["Mirikizumab (drug candidate)"])
    ck2 = CoKeyAssoc(company_id=co.id, keyword_id=39, context=["Tirzepatide (drug candidate)"])
    ck3 = CoKeyAssoc(company_id=co.id, keyword_id=40, context=["Abemaciclib (drug candidate)", "Imlunestrant (drug candidate)"])
    ck6 = CoKeyAssoc(company_id=co.id, keyword_id=33, context=["Insulin Efsitora Alfa (drug candidate)", "Orforglipron (drug candidate)", "Retatrutide (drug candidate)", "Tirzepatide (drug candidate)"])
    ck7 = CoKeyAssoc(company_id=co.id, keyword_id=41, context=["Lebrikizumab (drug candidate)"])
    ck8 = CoKeyAssoc(company_id=co.id, keyword_id=42, context=["Lebrikizumab (drug candidate)"])
    ck9 = CoKeyAssoc(company_id=co.id, keyword_id=44, context=["Lepodisiran (drug candidate)"])
    ck10 = CoKeyAssoc(company_id=co.id, keyword_id=45, context=["Olomorasib (drug candidate)", "Pirtobrutinib (drug candidate)", "Selpercatinib (drug candidate)"])
    ck11 = CoKeyAssoc(company_id=co.id, keyword_id=34, context=["Orforglipron (drug candidate)", "Retatrutide (drug candidate)", "Tirzepatide (drug candidate)"])

    # ck14 = CoKeyAssoc(company_id=co.id, keyword_id=31, context=["Remternetug (drug candidate)"])
    ck17 = CoKeyAssoc(company_id=co.id, keyword_id=47, context=["Retatrutide (drug candidate)"])

    ck19 = CoKeyAssoc(company_id=co.id, keyword_id=48, context=["Tirzepatide (drug candidate)"])
    

    batch = [ck1,ck2,ck3,ck6,ck7,ck8,ck9,ck10,ck11,ck17,ck19]

    db.session.add_all(batch)
    db.session.commit()



