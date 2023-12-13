import config
from db import db
from models.quilts import Quilts
from models.users import Users


def add_quilt_demo_data():
    user = db.session.query(Users).filter(Users.first_name == 'Super').first()

    for pattern_name in config.quilts:
        new_quilt = db.session.query(Quilts).filter(Quilts.pattern_name == pattern_name).first()

        if new_quilt == None:
            pattern_name = pattern_name
            user_id = user.user_id
            fabric_line = 'Sweet Water'
            pattern_designer = 'April'

            new_quilt = Quilts(pattern_name=pattern_name, user_id=user_id, fabric_line=fabric_line, pattern_designer=pattern_designer)

            db.session.add(new_quilt)

    db.session.commit()
