import routes


def register_blueprints(app):
    app.register_blueprint(routes.users)
    # app.register_blueprint(routes.organizations)
    # app.register_blueprint(routes.roles)
    # app.register_blueprint(routes.auth)
    # app.register_blueprint(routes.quilts)
    # app.register_blueprint(routes.images)
