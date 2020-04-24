import os
import json
from flask import Flask, render_template, Response, send_from_directory
from pathlib import Path
from tts_read import read_tts_file
from build_tts_training_data import layers_to_array
import mimetypes

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

app = Flask(__name__)

tts_files = []

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
    tts = read_tts_file(Path("./prefabs/all/{0}.tts".format(name)))
    data = layers_to_array(tts)
    l = []
    for x in data:
        l.append(int(x))
    tts["data"] = l
    keys = tts.keys()
    r = {}
    for key in keys:
        o = tts[key]
        if isinstance(o, bytes):
            r[key] = o.hex()
        else:
            r[key] = o
    return json.dumps(r)

@app.route('/api/data/alltts')
def get_all_tts_files():
    return Response(json.dumps(tts_files), mimetype='application/json')

if __name__ == '__main__':
    print("caching tts file names")
    for subdir, dirs, files in os.walk("./prefabs/all"):
        for file in files:
            if file.endswith(".tts"):
                tts_files.append(file)
    app.run(debug=True)