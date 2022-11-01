from random import choice
from flask import Response
from flask import Flask

app = Flask(__name__)


@app.route('/execute_transaction', methods=['GET'])
def execute_transaction() -> Response:
    chosen = choice([True, False])  # noqa: S311
    if chosen:
        resp = Response('success!\n', mimetype='application/json')
    else:
        resp = Response('error!\n', status=404, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(port=5001)
