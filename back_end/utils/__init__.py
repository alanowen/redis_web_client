from flask import jsonify


def success_json(text='', data=None):
    return jsonify(code=0, status='success', text=text, data=data)


def alert_json(status='success', text='', data=None):
    return jsonify(code=1, status=status, text=text, data=data)


def form_errors_json(text='', data=None):
    return jsonify(code=2, status='form errors', text=text, data=data)
