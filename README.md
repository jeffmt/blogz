# Blog web application

This is a blogging web application implemented in Python using the Flask web framework and the Jinja2 templating 
engine.  It uses SQLAlchemy as an ORM to access a MySQL database containing a user and a blog table.

This application builds upon build-a-blog to make the application a multi-user site.  Users must create an account 
and be logged in before creating blog posts.  Users can view blog posts by an individual 
user as well as by all users.  User passwords are hashed and salted before being stored in the database.

### Users Page

![Users](Users.png "Users")

### Blog Posts Page

![Posts](Posts.png "Posts")

### Blog Post Detail Page

![Post](Post.png "Post")

### Form to create a new blog post

![AddNewPost](AddNewPost.png "AddNewPost")


# Author
Jeff T
