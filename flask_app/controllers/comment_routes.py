from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.posts import Post
from flask_app.models.comments import Comment


@app.route('/add/comment', methods=['POST'])
def add_comment():
    #Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    #Validates the post.
    if not Comment.validate_comment(request.form):
        return redirect('/wall')
    #Saves the post.
    Comment.save(request.form)

    return redirect('/wall')