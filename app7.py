#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort
from flask import url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "username": "123",
    "password": "456"
}


@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_tasks', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries1',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python2',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
    { 'id': 3,
    'title': u'Learn Python3',
    'description': u'Need to find a good Python tutorial on the web',
    'done': False
    },
]


@app.route('/')
def get_hello():
    return "this is hello workd get_hello()"

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
#@auth.login_required
def get_tasks():
    # return jsonify({'tasks': tasks})
    # replace id to uri
    return jsonify({'tasks': map(make_public_task, tasks)})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
#@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})



@app.route('/todo/api/v1.0/tasks', methods=['POST'])
#@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
#@auth.login_required
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
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': '404lalalal Not found'}), 404)


@auth.error_handler
def unauthorized():
   return make_response(jsonify({'error': '401Unauthorized access-password not correct'}), 401)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host = '127.0.0.1', port = 5001, debug = True)
