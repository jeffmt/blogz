from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Blog, User

#app = Flask(__name__)
#app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:doit@localhost:3306/blogz'
#app.config['SQLALCHEMY_ECHO'] = True

#db = SQLAlchemy(app)

#class Blog(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(240))
#    body = db.Column(db.String(1000))
#    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#    create_date = db.Column(db.DateTime)
#
#    def __init__(self, title, body, owner, create_date):
#        self.title = title
#        self.body = body
#        self.owner = owner 
#        if create_date is None:
#            create_date = datetime.datetime.utcnow()
#        self.create_date = create_date
#
#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(240), unique=True)
#    password = db.Column(db.String(240))
#    blogs = db.relationship('Blog', backref='owner') 
#
#    def __init__(self, username, password):
#        self.username = username 
#        self.password = password 

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
#        session['user'] = user
        return redirect('/newpost')

    return render_template('signup.html')

#@app.route("/logout", methods=['POST'])
#def logout():
#	del session['username']
#	return redirect('/blog')

@app.route("/logout")
def logout():
    if 'username' in session:
        del session['username']
#    if 'user' in session:
#        del session['user']
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
#		if username.count(' ') > 0:
#			flash('Username cannot contain a space')
#			return redirect('/login')
#
#		if not username:
#			flash('Username cannot be left blank')
#			return redirect('/login')
#
#		if len(username) < 3 or len(username) > 20: 
#			flash('Username should be between 3 and 20 characters')
#			return redirect('/login')
#
#		if password.count(' ') > 0:
#			flash('Password cannot contain a space')
#			return redirect('/login')
#
#		if not password:
#			flash('Password cannot be left blank')
#			return redirect('/login')
#
#		if len(password) < 3 or len(password) > 20: 
#			flash('Password should be between 3 and 20 characters')
#			return redirect('/login')

        user = User.query.filter_by(username=username).first() 

        if not user:
            flash('Username does not exist in database', 'error')
            return redirect('/login')

        user = User.query.filter_by(username=username, password=password).first() 

        if not user:
            flash(username, 'username')
            flash('Password for user is incorrect', 'error')
            return redirect('/login')

        session['username'] = username
#        session['user'] = user
        return redirect('/newpost')
    return render_template('login.html')

@app.before_request
def require_login():
    public_paths = ['/login', '/',  '/signup', '/blog',]
    private = request.path not in public_paths
    logged_out = 'username' not in session
#    logged_out = 'user' not in session
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
