from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy import func, Index
from datetime import datetime
from config import db


company_keyword_assoc = db.Table(
    'company_keyword_assoc', db.metadata,
    db.Column('company_id', db.Integer, db.ForeignKey('companies_table.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords_table.id')),
    db.Column('context', db.String)
)

class CoKeyAssoc(db.Model, SerializerMixin):
    __tablename__ = 'co_keyword_table'
    company_id = db.Column(db.Integer, db.ForeignKey('companies_table.id'), primary_key=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords_table.id'), primary_key=True)
    context = db.Column(db.JSON)
    
    company = db.relationship("Company", back_populates="keyword_associations")
    keyword = db.relationship("Keyword", back_populates="company_associations")

    serialize_rules = ('-company.keyword_associations', '-keyword.company_associations')


class Company(db.Model, SerializerMixin):
    __tablename__ = "companies_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ticker = db.Column(db.String, nullable=False)
    cik = db.Column(db.Integer, nullable=False)
    exchange = db.Column(db.String)
    cik_10 = db.Column(db.String)
    sic = db.Column(db.Integer)
    sic_description = db.Column(db.String)
    owner_org = db.Column(db.String)
    entity_type = db.Column(db.String)
    country = db.Column(db.String)
    notes = db.relationship('Note', back_populates='company')
    keyword_associations = db.relationship("CoKeyAssoc", back_populates="company")

    # balance_sheets = db.relationship('BalanceSheet', back_populates='company')
    # income_statements = db.relationship('IncomeStatement', back_populates='company')
    # cash_flows_statements = db.relationship('CashFlowsStatement', back_populates='company')

    serialize_rules = ('-balance_sheets.company', '-income_statements.company', '-cash_flows_statements.company', '-keyword_associations.company', '-keyword_associations.keyword_id', '-keyword_associations.company_id')

    ###################

    __table_args__ = (
        Index('idx_ticker', 'ticker'),
    )
    

class BalanceSheet(db.Model, SerializerMixin):
    __tablename__ = "bs_table"

    id = db.Column(db.Integer, primary_key=True)
    company_cik = db.Column(db.Integer, db.ForeignKey('companies_table.cik'), nullable=False)
    total_assets = db.Column(db.Integer)
    assets_current = db.Column(db.Integer)
    assets_noncurrent = db.Column(db.Integer)
    total_liabilities = db.Column(db.Integer)
    liabilities_current = db.Column(db.Integer)
    liabilities_noncurrent = db.Column(db.Integer)
    total_liabilities_and_stockholders_equity = db.Column(db.Integer)
    total_stockholders_equity = db.Column(db.Integer)
    total_stockholders_equity_nci = db.Column(db.Integer)
    cash = db.Column(db.Integer)
    cash_and_equiv = db.Column(db.Integer)
    cash_all = db.Column(db.Integer)
    goodwill = db.Column(db.Integer)
    intangible_assets = db.Column(db.Integer)
    accn = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    filed = db.Column(db.String)
    form = db.Column(db.String)
    fp = db.Column(db.String)
    frame = db.Column(db.String)
    fy = db.Column(db.Integer)

    # company = db.relationship('Company', back_populates='balance_sheets')

    # serialize_rules = ('-company.balance_sheets',)

    __table_args__ = (
        Index('idx_company_cik', 'company_cik'),
    )


class IncomeStatement(db.Model, SerializerMixin):
    __tablename__ = "inc_table"

    id = db.Column(db.Integer, primary_key=True)
    company_cik = db.Column(db.Integer, db.ForeignKey('companies_table.cik'), nullable=False)
    total_revenue = db.Column(db.Integer)
    rev_from_ceat = db.Column(db.Integer)
    rev_net_of_ie = db.Column(db.Integer)
    rev_from_ciat = db.Column(db.Integer)
    sales_rev_net = db.Column(db.Integer)
    sales_rev_goods_net = db.Column(db.Integer)
    sales_rev_serv_net = db.Column(db.Integer)
    interest_and_div_inc_op = db.Column(db.Integer)
    net_income = db.Column(db.Integer)
    ifrs_revenue = db.Column(db.Integer)
    accn = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    filed = db.Column(db.String)
    form = db.Column(db.String)
    fp = db.Column(db.String)
    frame = db.Column(db.String)
    fy = db.Column(db.Integer)
    currency = db.Column(db.Integer)
    accounting_standard = db.Column(db.String)
    key = db.Column(db.String)
    rev_key = db.Column(db.String)
    preferred_dividends = db.Column(db.Integer)
    eps = db.Column(db.Integer)

    # company = db.relationship('Company', back_populates='income_statements')
    # serialize_rules = ('-company.income_statements',)


class CashFlowsStatement(db.Model, SerializerMixin):
    __tablename__ = "cf_table"

    id = db.Column(db.Integer, primary_key=True)
    company_cik = db.Column(db.Integer, db.ForeignKey('companies_table.cik'), nullable=False)
    opr_cf = db.Column(db.Integer)
    inv_cf = db.Column(db.Integer)
    fin_cf = db.Column(db.Integer)
    net_cf = db.Column(db.Integer)
    accn = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    filed = db.Column(db.String)
    form = db.Column(db.String)
    fp = db.Column(db.String)
    frame = db.Column(db.String)
    fy = db.Column(db.Integer)
    op_cf_key = db.Column(db.String)
    inv_cf_key = db.Column(db.String)
    fin_cf_key = db.Column(db.String)

    # company = db.relationship('Company', backref='cash_flows_statements')
    # serialize_rules = ('-company.cash_flows_statements', '-company.cik', '-company.cik_10', '-company.country', '-company.entity_type', '-company.exchange', '-company.keywords', '-company.notes', '-company.owner_org', '-company.sic', '-company.sic_description')


class Keyword(db.Model, SerializerMixin):
    __tablename__ = "keywords_table"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    description = db.Column(db.String)
    co_assoc = db.Column(db.String)
    
    company_associations = db.relationship("CoKeyAssoc", back_populates="keyword")

    serialize_rules = ('-companies',)


class Note(db.Model, SerializerMixin):
    __tablename__ = "notes_table"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies_table.id'))
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    company = db.relationship('Company', back_populates="notes")

    serialize_rules = ('-company',)


class CommonShares(db.Model, SerializerMixin):
    __tablename__ = "common_shares_table"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies_table.id'), nullable=False)
    date = db.Column(db.String)
    historical_shares = db.Column(db.Integer)
    split_coefficient = db.Column(db.Integer)
    adjusted_shares = db.Column(db.Integer)
    historical_shares_diluted = db.Column(db.Integer)
    adjusted_shares_diluted = db.Column(db.Integer)




# # String types
# db.String(length)      # Variable-length string with max length
# db.Text               # Unlimited-length text
# db.Unicode(length)    # Variable-length Unicode string
# db.UnicodeText       # Unlimited-length Unicode text

# # Numeric types
# db.Integer           # Regular integer
# db.BigInteger        # Large integer
# db.Float            # Floating-point number
# db.Numeric(p, s)    # Decimal number with precision and scale
# db.Boolean          # True/False value

# # Date and Time types
# db.DateTime         # Date and time
# db.Date            # Date only
# db.Time            # Time only
# db.Interval        # Time interval

# # Binary types
# db.LargeBinary     # Binary blob
# db.Binary          # Fixed-length binary data

# # Specialized types
# db.Enum(*items)    # List of string values
# db.JSON            # JSON-encoded data
# db.PickleType      # Automatically pickled Python objects
# db.ARRAY(type)     # Array of another type