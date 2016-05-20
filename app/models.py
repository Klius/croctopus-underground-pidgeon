from app import db

class Profile(db.Model):
	code = db.Column(db.String(10), primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	mail = db.Column(db.String(120), index=True, unique=True)

	def __repr__(self):
		return '<Profile %r>' % (self.name)
