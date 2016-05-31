from app import db

class Profile(db.Model):
	id = db.Column(db.String(10), primary_key=True)
	partner = db.Column(db.String(64), index=True, unique=False)
	empresa = db.Column(db.String(64), index=True, unique=False)
	contacto = db.Column(db.String(64), index=True, unique=False)
	telefono = db.Column(db.String(64), index=True, unique=False)
	movil = db.Column(db.String(64), index=True, unique=False)
	mail = db.Column(db.String(120), index=True, unique=False)
	servers = db.relationship('Server',backref='serv',lazy="dynamic")
	def __repr__(self):
		return '<Profile %r>' % (self.empresa)

class Server(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(15))
	ref = db.Column(db.String(64))
	profile_id = db.Column(db.String(10),db.ForeignKey('profile.id'))

	def __repr__(self):
		return '<Self %r>' % (self.ref)
