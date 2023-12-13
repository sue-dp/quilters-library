from db import db


users_organizations_xref = db.Table(
    'UsersOrganizationssXref',
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('org_id', db.ForeignKey('Organizations.organization_id'), primary_key=True)
)
