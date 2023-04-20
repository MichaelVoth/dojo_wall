from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Post:

    DB = "dojo_wall"

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None


    @classmethod
    def get_all_posts(cls):
        query = """SELECT *
                    FROM posts
                    JOIN users ON posts.user_id = users.id
                    ORDER BY posts.created_at DESC;"""
        results = connectToMySQL(cls.DB).query_db(query)
        posts = []
        

        for post in results:
            post_obj = cls(post)
            user_data = {
                "id": post["user_id"],
                "first_name": post["first_name"],
                "last_name": post["last_name"],
                "email": post["email"],
                "password": post["password"],
                "created_at": post["users.created_at"],
                "updated_at": post["users.updated_at"]
            }
            post_obj.owner = User(user_data)
            posts.append(post_obj)
        return posts



    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    

    @staticmethod
    def validate_post(post):
        is_valid =True
        if not len(post['content']) >=1 :
            flash("Post content cannot be blank",'post')
            is_valid = False
        
        return is_valid
