from config import DevConfig
from flask import Flask

from models import db
from controllers.blog import blog_blueprint

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('blog.home'))

app.register_blueprint(blog_blueprint)

if __name__ == '__main__':
    app.run()