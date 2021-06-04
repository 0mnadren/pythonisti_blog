from flask import render_template, request, Blueprint
from myproject.models import Blog

cores_blueprint = Blueprint('core', __name__)


@cores_blueprint.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = Blog.query.order_by(Blog.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', blog_posts=blog_posts)


@cores_blueprint.route('/info')
def info():
    return render_template('info.html')
