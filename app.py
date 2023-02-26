from chalice import Chalice, Response

app = Chalice(app_name='efs-sqlite')


@app.route('/')
def index():
    with open('chalicelib/index.html') as f:
        return Response(body=f.read(), status_code=200, headers={'Content-Type': 'text/html'})

def get_file(file_path):
    import os
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is None: # Not AWS Lambda - use /tmp
        return file_path.replace('/mnt/lambda/efs-sqlite', '/tmp')
    else: # AWS Lambda - use mount path
        return file_path

def jsonify(some_bytes):
    import base64
    return base64.b64encode(some_bytes).decode('utf8')

@app.route('/query', cors=True, methods=['POST'])
def do_query():
    import json
    print(app.current_request.json_body)
    statement = app.current_request.json_body['statement']
    file = app.current_request.json_body['file']
    token = app.current_request.json_body['token']
    result = query(statement, file, token)
    json_result = json.dumps(result, default=jsonify)
    return Response(json_result, headers={'Content-Type': 'application/json'}, status_code=200)

def query(statement, file, token):
    import sqlite3
    con = sqlite3.connect(get_file(file))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(statement)
    result = cur.fetchall()
    cur.close()
    con.close()
    return [dict(row) for row in result]

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
