from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Blog, User
from hashutils import password_matches_hash

@app.route("/blog")
def blog():
    id = request.args.get('id')
    user_id = request.args.get('user')
    if id:
        blog = db.session.query(Blog).filter(Blog.id == id).first()
        return render_template('blog_detail.html', blog=blog)

    if user_id:
        blogs = db.session.query(Blog).filter(Blog.owner_id == user_id).all()
        return render_template('blog.html', blogs=blogs)

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

        user = User.query.filter_by(username=session['username']).first()

        newpost = Blog(title, body, user.id, None)
        db.session.add(newpost)
        db.session.commit()

        return render_template('blog_detail.html', blog=newpost)
    return render_template('newpost.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify-password']

        if is_invalid(username):
            flash('invalid username', 'error')
            return redirect('/signup')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists', 'error')
            return redirect('/signup')

        if is_invalid(password):
            flash(username, 'username')
            flash('invalid password', 'error')
            return redirect('/signup')

        if is_invalid(verify_password):
            flash('invalid verify password', 'error')
            flash(username, 'username')
            return redirect('/signup')

        if password != verify_password:
            flash('passwords do not match', 'error')
            flash(username, 'username')
            return redirect('/signup')

        user = User(username, password)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        return redirect('/newpost')

    return render_template('signup.html')

@app.route("/logout")
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/blog')

@app.route("/")
def index():
    return render_template('index.html', users=get_users())

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_invalid(username):
            flash('invalid username', 'error')
            return redirect('/login')

        if is_invalid(password):
            flash(username, 'username')
            flash('invalid password', 'error')
            return redirect('/login')

        user = User.query.filter_by(username=username).first() 

        if not user:
            flash('Username does not exist in database', 'error')
            return redirect('/login')

        if not password_matches_hash(password, user.pw_hash):
            flash(username, 'username')
            flash('Password for user is incorrect', 'error')
            return redirect('/login')

        session['username'] = username
        return redirect('/newpost')
    return render_template('login.html')

@app.before_request
def require_login():
    public_paths = ['/login', '/',  '/signup', '/blog',]
    private = request.path not in public_paths
    logged_out = 'username' not in session
    if logged_out and private:
        return redirect('/login')

def is_invalid(field):
    if field.count(' ') > 0:
        return True

    if not field:
        return True

    if len(field) < 3: 
        return True

    return False

def get_blogs():
    return Blog.query.order_by(Blog.create_date.desc()).all()

def get_users():
    return User.query.order_by(User.username).all()

if __name__ == "__main__":
    app.run()
