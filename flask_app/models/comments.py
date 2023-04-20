from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.posts import Post
from flask import flash

class Comment:

    DB = "dojo_wall"

    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.post_id = data['post_id']
        self.user_id = data['user_id']
        self.post = None
        self.author = None

    @classmethod
    def get_all_comments(cls):
        query = """
            SELECT *
            FROM comments
            JOIN posts ON posts.id = comments.post_id
            JOIN users ON users.id = comments.author_id
            ORDER BY comments.created_at;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        comments = []

        for comment in results:
            user_data = {
                "id": comment["user_id"],
                "first_name": comment["first_name"],
                "last_name": comment["last_name"],
                "email": comment["email"],
                "password": comment["password"],
                "created_at": comment["created_at"],
                "updated_at": comment["updated_at"]
            }
            post_data = {
                'id': comment['post_id'],
                'content': comment['content'],
                'created_at': comment['created_at'],
                'updated_at': comment['updated_at'],
                'user_id': comment['user_id']
            }
            comment_obj = cls(comment)
            comment_obj.author = User(user_data)
            comment_obj.post = Post(post_data)
            comments.append(comment_obj)

        return comments

    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO comments (comment, post_id, author_id)
                VALUES (%(comment)s, %(post_id)s, %(author_id)s)"""
        return connectToMySQL(cls.DB).query_db(query, data)

    
    @staticmethod
    def validate_comment(data):
        is_valid = True
        if not len(data['comment']) >= 1:
            flash('* Comment cannot be blank', f'comment-{data["post_id"]}')
            is_valid = False
        return is_valid