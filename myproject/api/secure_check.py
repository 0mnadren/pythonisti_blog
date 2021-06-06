from myproject.models import User
from myproject.models import Blog
from flask_restful import Resource


def authenticate(username, password):
    # check if user exists
    # if so, return user
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)


class OneBlog(Resource):

    def get(self, blog_id):
        blog = Blog.query.filter_by(id=blog_id).first()
        if blog:
            return blog.json()
        return {'blog': None}, 404


class AllBlogs(Resource):

    def get(self):
        blogs = Blog.query.all()
        return [blog.json() for blog in blogs]



