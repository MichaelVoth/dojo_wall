from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.posts import Post
from flask_app.models.comments import Comment



@app.route('/wall')
def wall_page():
    #Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    #Gets user info by id in session.
    user = User.get_by_id({'id': session['user_id']})
    posts = Post.get_all_posts()
    comments = Comment.get_all_comments()

    return render_template('wall.html', user=user, posts=posts, comments = comments)

@app.route('/add/post', methods = ['POST'])
def add_post():
    #Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    #Validates the post.
    if not Post.validate_post(request.form):
        return redirect('/wall')
    #Saves the post.
    Post.save(request.form)

    return redirect('/wall')