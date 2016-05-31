from app import app, models , db
from flask import jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

#Description: Return the servers in list form.
def make_servers(servers):
	list_servers = []
	for server in servers:
		new_server = {}
		new_server['ip'] = server.ip
		new_server['ref'] = server.ref
		list_servers.append(new_server)
	return list_servers

#Description: Return the profile in a dictionary, this way we cant print it as JSON
def make_profile(profile):
	new_profile = {}
	new_profile['id'] = profile.id
	new_profile['partner'] = profile.partner
	new_profile['empresa'] = profile.empresa
	new_profile['contacto'] = profile.contacto
	new_profile['telefono'] = profile.telefono
	new_profile['movil'] = profile.movil
	new_profile['mail'] = profile.mail
	new_profile['servers'] = make_servers( profile.servers)
	return new_profile

#Erase it after debbugging
@app.route('/platinum/api/v1.0/profile/chuleter')
def get_all_profiles():
    profiles = models.Profile.query.all()
    cad = ""
    for p in profiles:
        cad += "Profile: %s, mail: %s </br>"%(p.id,p.partner)
    return cad


@app.route('/platinum/api/v1.0/profile/<string:id>/<string:partner>', methods = ['GET'])
#@auth.login_required
def get_profile(id,partner):
    profile = models.Profile.query.get(id)
    if profile == None or profile.partner != partner:
        abort(404)
    return jsonify( { 'profile': make_profile(profile) } )


##Recibe i crea el perfil
@app.route('/platinum/api/v1.0/profile', methods = ['POST'])
#@auth.login_required
def create_profile():
    print (request.json)
    if not request.json or not 'name' in request.json:
        abort(400)
    if models.Profile.query.get(request.json['code']) == None :
        abort(400)
    profile = models.Profile.query.get(request.json['code'])
    #update name and mail
    profile.name = request.json['name']
    profile.mail = request.json['mail']

    db.session.commit()
    return jsonify( { 'profile': make_profile(profile) } ), 201

####
#Description: Updates Profile info that we are willing to change
####
@app.route('/platinum/api/v1.0/profile/', methods = ['PUT'])
#@auth.login_required
def update_profile():
    if not request.json or not 'Profile' in request.json:
        abort(400)
    if models.Profile.query.get(request.json['Profile']['id']) == None:
        abort(404)
    if 'name' in request.json and type(request.json['Profile']['empresa']) != unicode:
       #print("name not unicode")
        abort(400) 
    if 'code' in request.json and type(request.json['Profile']['id']) != unicode:
        abort(400)
    
    profile = models.Profile.query.get(request.json['Profile']['id']) 
    profile.empresa = request.json['Profile']['empresa']
    db.session.commit()
   
    return jsonify( { 'profile': make_profile(profile) } ),201
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )
