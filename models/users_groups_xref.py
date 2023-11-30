from db import db


users_groups_xref = db.Table(
    'UsersGroupssXref',
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('org_id', db.ForeignKey('Groups.group_id'), primary_key=True)
)
