from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:doit@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/blog")
def blog():
    id = request.args.get('id')
    if id:
        blog = db.session.query(Blog).filter(Blog.id == id).first()
        return render_template('blog_detail.html', blog=blog)
    else:
        return render_template('blog.html', blogs=get_blogs())

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if (not title) or (title.strip() == ""):
            return render_template('newpost.html', body=body, title_error='You must supply a title')
        if (not body) or (body.strip() == ""):
            return render_template('newpost.html', title=title, title_error='You must supply a body')

        newpost = Blog(title, body)
        db.session.add(newpost)
        db.session.commit()

        return render_template('blog_detail.html', blog=newpost)
    return render_template('newpost.html')

def get_blogs():
    return Blog.query.all()

if __name__ == "__main__":
    app.run()
