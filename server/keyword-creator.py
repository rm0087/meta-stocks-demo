from app import app
from models import db, Company, Keyword, CoKeyAssoc


keywords = [
    "Crohn's Disease",
    "sleep apnea",
    "breast cancer",
    "dermatitis",
    "rhinosinusitis",
    "rhinitis",
    "cardiovascular disease",
    "cancer",
    "osteoarthritis",
    "kidney health",
    "heart failure",
    "multiple sclerosis (MS)",
    "psoriasis",
    "hidradenitis suppurativa (HS)",
    "pain",
    "Parkinson's disease",
    "Gaucher disease",
    "dementia",
    "ulcerative colitis"
    "arthritis",
    "hearing loss",
    "steatohepatitis",
    "prostate cancer",
    "neurodegeneration",
    "cardiometabolic"
]

batch = []



with app.app_context():
    for k in keywords:
        k1 = Keyword(word=k)
        batch.append(k1)
    
    db.session.add_all(batch)
    db.session.commit()

