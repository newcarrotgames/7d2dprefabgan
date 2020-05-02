import os
import json
from flask import Flask, render_template, Response, send_from_directory, request
from pathlib import Path
from tts_read import read_tts_file
from resize_tts import resize_prefab
from build_tts_training_data import layers_to_array
import mimetypes
import numpy as np
from config import Config
from nim_utils import read_nim

conf = Config.getInstance()

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
    size = request.args.get('size')
    print(size.split(','))
    tts = read_tts_file(Path("./prefabs/all/{0}.tts".format(name)))
    sizes = size.split(',')
    new_size = (int(sizes[0]), int(sizes[1]), int(sizes[2]))
    print("new_size: {}", new_size)
    resized_tts = resize_prefab(tts, new_size)
    data = layers_to_array(resized_tts)
    l = []
    for x in data:
        l.append(int(x))
    resized_tts["data"] = l
    keys = resized_tts.keys()
    r = {}
    for key in keys:
        o = resized_tts[key]
        if isinstance(o, bytes):
            r[key] = o.hex()
        elif isinstance(o, np.ndarray):
            r[key] = o.tolist()
        else:
            r[key] = o
    return json.dumps(r)

@app.route('/api/nim/<name>')
def apinim(name):
    rootdir = conf.get("gamePrefabsFolder")
    filename = os.path.join(rootdir, "{}.blocks.nim".format(name))
    block_map = read_nim(filename)
    return json.dumps(block_map)

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