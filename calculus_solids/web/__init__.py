# importing 3rd party packages
from flask import Flask
from flask import request,render_template,send_from_directory,abort
from flask import Response, send_file
from werkzeug.wsgi import FileWrapper

# import dominate
# from dominate import tags as d
import webbrowser
import os
import json
from io import BytesIO,StringIO

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

    # Adding parameters to function
    stype = request.args.get("solid_type")
    p_list = ["lower_limit","upper_limit","precision","wireframe","debug","invert"]
    if stype=='solid_revolution': 
        p_list.append('offset')
        p_list.append('pie')
    print request.args.items()
    params = ({k: eval(v) for k, v in request.args.items() if k in p_list})

    params.update({ k: v for k, v in request.args.items() if k in ["lower_func","upper_func"] })

    if stype=='solid_revolution':
        params['offset'] = 0
    # extra options
    if 'wireframe' in request.args.getlist("extra_options"):
        params.update({'wireframe':True})
    if 'debug' in request.args.getlist("extra_options"):
        params.update({'debug':True})
    if 'invert' in request.args.getlist("extra_options"):
        params.update({'invert':True})
    if stype=='solid_revolution' and 'pie' in request.args.getlist("extra_options"):
        params.update({'pie':True})

    print("Calculating Vertices and Faces...")
    data = None
    title = ''
    if stype == 'solid_revolution':
        data = solid_revolution(**params)
        title = 'Solid of Revolution'
    elif stype == 'cross_semicircle':
        data = cross_semicircle(**params)
        title = 'Solid with Semicircle Cross Sections'
    elif stype == 'cross_triangle':
        data = cross_triangle(**params)
        title = 'Solid with Triangle Cross Sections'
    elif stype == 'cross_square':
        data = cross_square(**params)
        title = 'Solid with Square Cross Sections'
    v,e,f = data
    jscad_buffer = mesh_openjscad(v,f,buffer=True)
    jscad_content = jscad_buffer.read()
    mesh_data = json.dumps(data)
    # print(title)
    # # print(v,e,f)
    # print("Generating Files...")
    # name =  request.args.get('filename')
    # name = name if name else 'generated_solid' # Filename decision

    # # Generating Files
    # context = []
    # print(request.args.getlist("formats"))
    # isSTL = False
    # if 'stl' in request.args.getlist("formats"):
    #     context.append(('STL format','/uploads/'+mesh_stl(v,f,name=name), 'Download this file and it can be opened in any 3D modelling software' ))
    #     isSTL=True
    # if 'plot' in request.args.getlist("formats"):
    #     context.append(('3D Graphed Points','/uploads/'+mesh_plotly(v,name=name,title=title,altverts=e), 'Click this link to open a 3D graph of the vertices of the solid' ))
    # if 'jscad' in request.args.getlist("formats"):
    #     context.append(('OpenJsCAD','/uploads/'+mesh_openjscad(v,f,name=name), 'Download this file and go to openjscad.org.  Drag the downloaded file to the website and click "autoreload" to get an automatically updating display of the solid' ))
    # if 'scad' in request.args.getlist("formats"):
    #     context.append(('OpenSCAD','/uploads/'+mesh_openscad(v,f,name=name), 'Download this file and you can open it in OpenSCAD' ))
    # return render_template('results.html',filenames=context,os=os,isSTLformat=isSTL,the_filename="/uploads/"+name,mesh_data=mesh_data)
    file_info = []
    if 'stl' in request.args.getlist("formats"):
        file_info.append(('STL format','stl', 'Download this file and it can be opened in any 3D modelling software' ))
        isSTL=True
    if 'plot' in request.args.getlist("formats"):
        file_info.append(('3D Graphed Points','plot', 'Click this link to open a 3D graph of the vertices of the solid' ))
    if 'jscad' in request.args.getlist("formats"):
        file_info.append(('OpenJsCAD','jscad', 'Download this file and go to openjscad.org.  Drag the downloaded file to the website and click "autoreload" to get an automatically updating display of the solid' ))
    if 'scad' in request.args.getlist("formats"):
        file_info.append(('OpenSCAD','scad', 'Download this file and you can open it in OpenSCAD' ))
    return render_template('results.html',file_info=file_info,os=os,isSTL=isSTL,mesh_data=mesh_data,jscad_content=jscad_content)

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

# @app.route("/openjscad/",methods=["GET"])
# def openjscad_full_editor():
#     return render_template('viewer-minimal.html')

@app.route("/generate/",methods=["POST"])
def generate_jscad():
    mesh_data = request.form['mesh_data']
    v,e,f = json.loads(mesh_data)
    webpage=False
    isSTL=False
    if 'stl' in request.args.getlist("format"):
        b = mesh_stl(v,f,buffer=True)
        filename = 'generated_file.stl'
        isSTL=True
    elif 'plot' in request.args.getlist("format"):
        s = mesh_plotly(v,title='New Solid',altverts=e,buffer=True)
        filename = 'generated_file.html'
        webpage=True
    elif 'jscad' in request.args.getlist("format"):
        s = mesh_openjscad(v,f,buffer=True)
        filename = 'generated_file.jscad'
    elif 'scad' in request.args.getlist("format"):
        s = mesh_openscad(v,f,buffer=True)
        filename = 'generated_file.scad'
    else:
        abort(404)
    
    # s = StringIO(mesh_data.decode('utf-8'))
    if not isSTL:
        data = BytesIO()
        s.seek(0)
        data.write(s.getvalue().encode('utf-8'))
    else:
        data = b
    # data.seek(0)
    # response = Response(FileWrapper(data),mimetype='text/plain',direct_passthrough=True)
    data.seek(0)
    # data.name='generated_file.jscad'
    if webpage:
        return Response(FileWrapper(data),mimetype='text/html')
    else:
        return send_file(data,as_attachment=True,mimetype='text/plain',attachment_filename=filename)
    try:
        pass
    except Exception as e:
        abort(404) 


# http://localhost:5000/create/revolution/?lower_limit=-3.0&upper_limit=3.0&precision=0.1&offset=0&lower_func=0&

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