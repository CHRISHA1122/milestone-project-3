import os
from camo_code import app, db, routes, login_manager

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG")
    )
