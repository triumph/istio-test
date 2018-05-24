from flask import Flask, jsonify, g, request
import platform
import requests
import logging

app = Flask(__name__)


def getForwardHeaders(request):
    headers = {}
    incoming_headers = [
        'x-request-id',
        'x-b3-traceid',
        'x-b3-spanid',
        'x-b3-parentspanid',
        'x-b3-sampled',
        'x-b3-flags',
        'x-ot-span-context'
    ]

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val
            # print("incoming: "+ihdr+":"+val)

    return headers


@app.before_request
def before_request():
    g.forwardHeaders = getForwardHeaders(request)


@app.after_request
def after_request(response):
    for k, v in g.forwardHeaders.iteritems():
        response.headers.set(k, v)
    logging.debug(g.forwardHeaders)
    return response


@app.route("/env")
def env():
    resp = requests.get('http://' + 'service-go' + '/env')
    data = resp.json()
    return jsonify({
        "message": 'Python' + platform.python_version() + '----->' + data['message']
    })


@app.route("/status")
def status():
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
