from db import db


users_orgs_xref = db.Table(
    'UsersOrgsXref',
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('org_id', db.ForeignKey('Organizations.org_id'), primary_key=True)
)
