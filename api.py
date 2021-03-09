from flask import Flask, abort, request, jsonify
import spider

app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def post_app_id():
    if not request.json or 'id' not in request.json:
        abort(400)
    appid = {
        'id': request.json['id']
    }
    # tasks.append(task)
    print(appid['id'])
    return jsonify({'result': 'success'})


@app.route('/')
def home():
    abort(400)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
