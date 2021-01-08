from flask import Flask, url_for, redirect, render_template, make_response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("test")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Post(db.Model):
    uid = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    number = db.Column(db.Integer, unique=False, nullable=False)
    title = db.Column(db.String(32), unique=False, nullable=False)
    content = db.Column(db.String(512), unique=False, nullable=False)

    def __init__(self, post_title : str, post_content : str):
        posts = self.query.filter_by(title=post_title).all()
        post_count = len(posts)
        self.number = post_count
        self.title = post_title[:32]
        self.uid = f"{post_title[:32]}#{post_count}"[:64]
        self.content = post_content[:512]

@app.route("/error/<err>")
def error(err):
    return f"<h1>{err}</h1>"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        bad_matches = ["<", ">", "/"]
        bad_data_check = True

        for match in bad_matches:
            bad_data_check &= title.find(match) == -1 and content.find(match) == -1
            if bad_data_check == False:
                break

        if title and content and bad_data_check:
            post = Post(title, content)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("index"))
        return redirect(url_for("error", err="Invalid post"))
    else:
        return render_template("index.html", post_list=Post.query.all())

if __name__ == "__main__":
    db.create_all()
    app.run()