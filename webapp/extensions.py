from flask import session
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_oauth import OAuth

from models import db, User

bcrypt = Bcrypt()
oid = OpenID()
oauth = OAuth()

@oid.after_login
def create_or_login(resp):
	from models import db, User
	username = resp.fullname or resp.fullname or resp.email
	if not username:
		flash('Invalid login. Please try again.', 'danger')
		return redirect(url_for('main.login'))

	user = User.query.filter_by(username=username).first()
	if user is None:
		user = User(username)
		db.session.add(user)
		db.session.commit()

	#redirect to home page
	return redirect(url_for('blog.home'))

facebook = oauth.remote_app(
	'facebook',
	base_url='https://graph.facebook.com/',
	request_token_url = None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key='',
	consumer_secret='',
	request_token_params={'scope':'email'}
)

@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('facebook_oauth_token')

twitter = oauth.remote_app(
	'twitter',
	base_url='https://api.twitter.com/1.1/',
	request_token_url='https://api.twitter.com/oauth/request_token',
	access_token_url='https://api.twitter.com/oauth/access_token',
	authorize_url='https://api.twitter.com/oauth/authenticate',
	consumer_key='',
    consumer_secret=''
)

@twitter.tokengetter
def get_twitter_oauth_token():
	return session.get('twitter_oauth_token')