import config
from db import db
from models.organizations import Organizations


def add_org_demo_data():
    for org_name in config.organizations:

        new_org = db.session.query(Organizations).filter(Organizations.org_name == org_name).first()

        if new_org == None:
            org_name = org_name

            new_org = Organizations(org_name=org_name, active=True)

            db.session.add(new_org)

    db.session.commit()
