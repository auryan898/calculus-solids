# importing 3rd party packages
from flask import Flask
from flask import request,render_template,send_from_directory

# import dominate
# from dominate import tags as d
import webbrowser
import os

# calculus_solids package imports
from calculus_solids.plotting_math import *

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
 
@app.route("/")
def index():
    return render_template('home.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route("/create/")
def create():
    stype = request.args.get("solid_type")
    p_list = ["lower_limit","upper_limit","precision","wireframe","debug","invert"]
    if stype=='solid_revolution': 
        p_list.append('offset')
    params = ({k: eval(v) for k, v in request.args.items() if k in p_list})

    params.update({ k: eval( "lambda x : {}".format(v) ) for k, v in request.args.items() if k in ["lower_func","upper_func"] })

    print("Calculating Vertices and Faces...")
    data = None
    if stype == 'solid_revolution':
        data = solid_revolution(**params)
    elif stype == 'cross_semicircle':
        data = cross_semicircle(**params)
    elif stype == 'cross_triangle':
        data = cross_triangle(**params)
    elif stype == 'cross_square':
        data = cross_square(**params)
    v,e,f = data

    print("Generating Files...")
    name =  request.args.get('filename')
    name = name if name else 'generated_solid'
    context = []
    print(request.args.getlist("formats"))
    if 'stl' in request.args.getlist("formats"):
        context.append(('STL format',mesh_stl(v,f,name=name), 'Download this file and it can be opened in any 3D modelling software' ))
    if 'plot' in request.args.getlist("formats"):
        context.append(('3D Graphed Points',mesh_plotly(v,name=name), 'Click this link to open a 3D graph of the vertices of the solid' ))
    if 'jscad' in request.args.getlist("formats"):
        context.append(('OpenJsCAD',mesh_openjscad(v,f,name=name), 'Download this file and go to openjscad.org.  Drag the downloaded file to the website and click "autoreload" to get an automatically updating display of the solid' ))
    if 'scad' in request.args.getlist("formats"):
        context.append(('OpenSCAD',mesh_openscad(v,f,name=name), 'Download this file and you can open it in OpenSCAD' ))
    return render_template('results.html',filenames=context,os=os)

@app.route("/create/revolution/",methods=["GET"])
def revolution():
    params = ({k: eval(v) for k, v in request.args.items()})
    solid = solid_revolution(**params)
    return str(solid)

@app.route("/create/cross_section/",methods=["GET"])
def cross_section():
    params = ({k: eval(v) for k, v in request.args.items()})
    solid = solid_revolution(**params)
    return str(solid)

# http://localhost:5000/create/revolution/?lower_limit=-3.0&upper_limit=3.0&precision=0.1&offset=0&lower_func=lambda x: 0&

def debug():
    # run flask app
    # webbrowser.open_new_tab('http://localhost:5000/')
    app.run(host='0.0.0.0', port=5000, debug=True)
    # print("Hello")

def start():
    webbrowser.open_new_tab('http://localhost:5000/')
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__=='__main__':
    debug()