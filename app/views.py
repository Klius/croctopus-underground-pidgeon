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

def make_profile(profile):
    new_profile = {}
    new_profile['code'] = profile.code
    new_profile['name'] = profile.name
    new_profile['mail'] = profile.mail
    return new_profile


@app.route('/platinum/api/v1.0/profile/chuleter')
def get_all_profiles():
    profiles = models.Profile.query.all()
    cad = ""
    for p in profiles:
        cad += "Profile: %s, mail: %s </br>"%(p.code,p.mail)
    return cad


@app.route('/platinum/api/v1.0/profile/<string:code>/<string:mail>', methods = ['GET'])
#@auth.login_required
def get_profile(code,mail):
    profile = models.Profile.query.get(code)
    if profile == None or profile.mail != mail:
        abort(404)
    return jsonify( { 'profile': make_profile(profile) } )


##Recibe i crea el perfil
@app.route('/platinum/api/v1.0/profile', methods = ['POST'])
#@auth.login_required
def create_profile():
    if not request.json or not 'name' in request.json:
        abort(400)
    elif models.Profile.query.get(request.json['code']) == None :
        abort(400)
    profile = models.Profile.query.get(request.json['code'])
    #update name and mail
    profile.name = request.json['name']
    profile.mail = request.json['mail']

    db.session.commit()
    return jsonify( { 'profile': make_profile(profile) } ), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )