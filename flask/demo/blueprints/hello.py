#!/usr/bin/env python3

import json

from flask import current_app, Blueprint, request, jsonify

name = 'hello'
bp = Blueprint(name, __name__, url_prefix='/demo')


@bp.route('/{}'.format(name), methods=['POST'])
def hello():
    data = json.loads(request.get_data(as_text=True))
    current_app.logger.info("receive data: {}".format(data))

    name = data.get('name', '')
    return jsonify({
        'msg': "hello " + name
    })
