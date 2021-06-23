from myproject import app, api
from myproject.api.secure_check import OneBlog, AllBlogs


api.add_resource(OneBlog, '/api/blog/<int:blog_id>')
api.add_resource(AllBlogs, '/api/blogs')

if __name__ == '__main__':
    app.run(debug=False)
