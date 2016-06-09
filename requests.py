from flask import request, Response
import pymongo
from bson import json_util, ObjectId
import datetime


class Requests:

    def __init__(self, mongo=None):
        self.mongo = mongo

    # Fetch todos
    def todos_index(self):
        now = datetime.datetime.utcnow()
        if request.args.get('limit') is None:
            limit = 1000
        else:
            limit = int(request.args.get('limit'))
            if limit == 0:
                limit = 10000
        todos = self.mongo.db.todos.find().sort('createdAt', pymongo.DESCENDING).limit(limit)
        todos_data = []

        for todo in todos:
            todos_data.append({
                "title": todo['title'],
                "text": todo['text'],
                "__v": todo.get("__v", 0),
                "done": todo['done'],
                "updatedAt": str(todo.get("updatedAt", now)),
                "_id": str(todo['_id']),
                "createdAt": str(todo.get("createdAt", now)),
            })
        return Response(
            json_util.dumps({
                'data': todos_data,
                'count': todos.count(),
                'limit': 1000
            }),
            status=200,
            mimetype='application/json'
        )

    # Create todos
    def todos_create(self):
        errors = []
        if not request.form.get('title'):
            errors.append("Title is required")
        if not request.form.get('text'):
            errors.append("Text description is required")
        if not request.form.get('done'):
            errors.append("Done field is required")

        if errors:
            return Response(
                json_util.dumps(errors),
                status=422,
                mimetype='application/json')
        else:
            done = True
            if str(request.form.get('done').lower()) == 'false':
                done = False
            if str(request.form.get('done')) == '0':
                done = False
            now = datetime.datetime.utcnow()
            todo_id = self.mongo.db.todos.insert_one({
                "title" : request.form.get('title'),
                "text" : request.form.get('text'),
                "done" : done,
                "createdAt" : now,
                "updatedAt" : now
            }).inserted_id
            return Response(
                json_util.dumps({
                    "title": request.form.get('title'),
                    "text": request.form.get('text'),
                    "done": done,
                    "_id" : str(todo_id),
                    "createdAt": str(now),
                    "updatedAt": str(now)
                }),
                status=200,
                mimetype='application/json')

    # Show todos
    def todos_show(self, todo_id=None):
        todo = self.mongo.db.todos.find_one_or_404({'_id': ObjectId(todo_id)})
        return Response(
            json_util.dumps(todo),
            status=200,
            mimetype='application/json')

    # Update todos
    def todos_update(self, todo_id=None):
        self.mongo.db.todos.find_one_or_404({'_id': ObjectId(todo_id)})
        errors = []
        if not request.form.get('title'):
            errors.append("Title is required")
        if not request.form.get('text'):
            errors.append("Text description is required")
        if not request.form.get('done'):
            errors.append("Done field is required")

        if errors:
            return Response(
                json_util.dumps(errors),
                status=422,
                mimetype='application/json')
        else:
            done = True
            if str(request.form.get('done').lower()) == 'false':
                done = False
            if str(request.form.get('done')) == '0':
                done = False
            now = datetime.datetime.utcnow()
            self.mongo.db.todos.update_one({
                '_id': ObjectId(todo_id)
            }, {
                "$set": {
                    "title": request.form.get('title'),
                    "text": request.form.get('text'),
                    "done": done,
                    "updatedAt": now
                }
            }, False)
            return Response(
                json_util.dumps({
                    "title": request.form.get('title'),
                    "text": request.form.get('text'),
                    "done": done,
                    "_id": str(todo_id)
                }),
                status=200,
                mimetype='application/json')

    # Update todos
    def todos_delete(self, todo_id=None):
        self.mongo.db.todos.delete_one({'_id': ObjectId(todo_id)})
        return Response(
            json_util.dumps({
                "success": True,
            }),
            status=200,
            mimetype='application/json')

    def _str2bool(v):
      return v.lower() in ("yes", "true", "t", "1")
