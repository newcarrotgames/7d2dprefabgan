import os
import json
from flask import Flask, render_template, send_from_directory
from pathlib import Path
from tts_read import read_tts_file
from build_tts_training_data import layers_to_array
import mimetypes

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

app = Flask(__name__)

# these method are not safe to use outside of your dev environment
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(Path('web/js'), path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(Path('web/css'), path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(Path('web/img'), path)

@app.route('/')
def index():
    return render_template('index.html'.format(os.path.sep))

@app.route('/view')
def view():
    return render_template('view.html'.format(os.path.sep))

@app.route('/api/tts/<name>')
def apitts(name):
    tts = read_tts_file(Path("./prefabs/{0}/{0}.tts".format(name)))
    data = layers_to_array(tts)
    l = []
    for x in data:
        l.append(int(x))
    tts["data"] = l
    keys = tts.keys()
    r = {}
    for key in keys:
        o = tts[key]
        print(type(o))
        if isinstance(o, bytes):
            r[key] = o.hex()
        else:
            r[key] = o
    return json.dumps(r)

if __name__ == '__main__':
    app.run(debug=True)