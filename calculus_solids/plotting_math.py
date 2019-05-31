import math
import pkgutil

def cross_semicircle(lower_limit,upper_limit,precision,lower_func,upper_func,wireframe=False,debug=False,invert=False):
    a,b = lower_limit,upper_limit
    step = precision
    f1, f2 = upper_func, lower_func
    def l1(x):
        try:
            return f1(x)
        except:
            return None
    def l2(x):
        try:
            return f2(x)
        except:
            return None
    def l3(rad):
        def result(v):
            try:
                diameter = f1(v)-f2(v)
                radius = diameter/2.
                x = radius*math.cos(rad)
                y = radius*math.sin(rad) + f2(v) + radius
                return (x,y)
            except:
                return (0,0)
        return result
    
    # Create mesh
    r = range(int(a/step),int((b)/step)+1)
    r = [ x for x in r if l1(x*step) is not None and l2(x*step) is not None and l1(x*step)<=l2(x*step) ]

    radrange = range(-int(math.pi/2/0.1),int(math.pi/2/0.1)+1)
    verts,edges,faces = [],[],[]
    
    verts += [ (0,x*step,l1(x*step)) for x in r]
    verts += [ (0,x*step,l2(x*step)) for x in r]
    #if not debug:
    if True:
        for rad in radrange:
            g = l3(rad*0.1)
            verts += [ (abs(g(x*step)[0]),x*step,g(x*step)[1]) for x in r ]

    l = len(r)
    row_num = int(len(verts)/len(r))
    #row_num = 9
    if wireframe and not debug: 
        pairs = [ (i,i+1) for i in range(int(row_num-1))] + [(row_num-1,0)]
        for v,w in pairs:
            edges += [ (x+v*l,x+w*l) for x in range(l)]    
        #    pass
        pass
    elif not debug:
        pairs = [ (i,i+1) for i in range(int(row_num-1))] + [(row_num-1,0)]
        for v,w in pairs:
            faces += [ (x+v*l,x+1+v*l,x+1+w*l,x+w*l) for x in range(int(l-1)) ]
        
        faces += [ [ v*(l) for v in range(int(row_num))] ]
        faces += [ [ (l-1)+v*(l) for v in range(int(row_num))][::-1] ]
    if invert:
        faces = [ list(t)[::-1] for t in faces]
    return verts,edges,faces

def cross_square(lower_limit,upper_limit,precision,lower_func,upper_func,height_scale=1,wireframe=False,debug=False,invert=False):
    a,b = lower_limit,upper_limit
    step = precision
    def l1(x):
        try:
            return upper_func(x)
        except:
            return None
    def l2(x):
        try:
            return lower_func(x)
        except:
            return None
    def l3(x):
        try:
            return lower_func(x)-upper_func(x)
        except:
            return None
    
    # Create mesh
    r = range(int(a/step),int((b)/step)+1)
    r = [ x for x in r if l3(x*step) is not None and l3(x*step)<=0]
    
    verts = [ (0,x*step,l1(x*step)) for x in r]
    verts += [ (0,x*step,l2(x*step)) for x in r]
    
    if not debug:
        verts += [ (abs(l3(x*step)*height_scale),x*step,l1(x*step)) for x in r]
        verts += [ (abs(l3(x*step)*height_scale),x*step,l2(x*step)) for x in r]
    edges,faces = [],[]
    l = len(r)
    if wireframe and not debug: 
        for v,w in [(1,0),(0,2),(2,3),(3,1)]:
            edges += [ (x+v*l,x+w*l) for x in range(l)]    
    elif not debug:
        for v,w in [(1,0),(0,2),(2,3),(3,1)]:
            faces += [ (x+v*l,x+1+v*l,x+1+w*l,x+w*l) for x in range(int(l-1)) ]
        #faces += [ (x+0*l,x+1+0*l,x+1+2*l,x+2*l) for x in range(l-1) ]
        #faces += [ (x+0*l,x+1+0*l,x+1+2*l,x+2*l) for x in range(l-1) ]
        
        faces += [ [l-1,l-1+1*l,l-1+3*l,l-1+2*l][::-1] ]
        faces += [ [0,1*l,3*l,2*l][::-1] ]
    if invert:
        faces = [ list(t)[::-1] for t in faces]
    return verts,edges,faces

def cross_triangle(lower_limit,upper_limit,precision,lower_func,upper_func,wireframe=False,debug=False,invert=False):
    a,b = lower_limit,upper_limit
    step = precision
    def l1(x):
        try:
            return upper_func(x)
        except:
            return None
    def l2(x):
        try:
            return lower_func(x)
        except:
            return None
    def l3(x):
        try:
            return upper_func(x)-lower_func(x)
        except:
            return 0
    
    # Create mesh
    r = range(int(a/step),int((b)/step)+1)
    r = [ x for x in r if l1(x*step) is not None and l2(x*step) is not None and l1(x*step)>=l2(x*step) ]
    
    verts = [ (0,x*step,l1(x*step)) for x in r]
    verts += [ (0,x*step,l2(x*step)) for x in r]
    if not debug:
        verts += [ (abs(l3(x*step)*math.sqrt(3)/2),x*step,l3(x*step)/2+l2(x*step)) for x in r]
    edges,faces = [],[]
    l = len(r)
    if wireframe and not debug: 
        for v,w in [(1,0),(0,2),(2,1)]:
            edges += [ (x+v*l,x+w*l) for x in range(l)]
    elif not debug:
        for v,w in [(1,0),(0,2),(2,1)]:
            faces += [ (x+v*l,x+1+v*l,x+1+w*l,x+w*l) for x in range(int(l-1)) ]
        
        faces += [ (l-1,l-1+1*l,l-1+2*l) ]
        faces += [ (0,1*l,2*l) ]
    if invert:
        faces = [ list(t)[::-1] for t in faces]
    return verts,edges,faces

def solid_revolution(lower_limit,upper_limit,precision,offset,lower_func,upper_func,wireframe=False,pie=False, debug=False,x_axis=False,invert=False):
    def f(x):
        try:
            return lower_func(x)-offset
        except:
            return 0
    def g(x):
        try:
            return upper_func(x)-offset
        except:
            return 0
    def axis(x):
        return offset

    a,b,step = lower_limit,upper_limit,precision
    r = range(int(a/step),int((b)/step)+1)
    r = [ x for x in r if f(x*step) is not None and g(x*step) is not None and f(x*step)<=g(x*step) ]
    verts,altverts,faces = [],[],[]

    verts = [ (0,x*step,f(x*step)) for x in r ] + [ (0,x*step,g(x*step)) for x in r ]
    altverts = [ (0,x*step,f(x*step)) for x in r ] + [ (0,x*step,g(x*step)) for x in r ]
    if len(verts)<=0:
        raise ValueError("solid not possible. try switching top and bottom functions")

    l = int(len(verts)/2)

    # Existing Lines' vertices have been formed, now generate revolution vertices:
    start_angle = math.pi*1/2
    angle = math.pi*2 if not pie else math.pi*3/2
    angle_precision = 0.1
    radrange = range(1,int(angle/angle_precision)+2)
    verts += [ [z*math.cos(rad*angle_precision+start_angle),y,z*math.sin(rad*angle_precision+start_angle)] for rad in radrange for x,y,z in verts ]

    row_num = int(len(verts)/l)
    # Now to generate all faces (unless 'wireframe') "Think clockwise"
    faces = [ ( ((i)%2*2+i)*l+x,((i)%2*2+i)*l+x+1,((i+1)%2*2+i)*l+x+1,((i+1)%2*2+i)*l+x ) for i in range((row_num-2)) for x in range(int(l-1))]

    # Generate the sides of the solid
    faces += [ (  l*(2*x+3)+l-1, l*(2*x+2)+l-1,l*(2*x+0)+l-1,l*(2*x+1)+l-1  ) for x in range(row_num//2-1) ]
    faces += [ [  l*(2*x+1), l*(2*x+0),l*(2*x+2),l*(2*x+3)  ] for x in range(row_num//2-1) ]

    # Generate extra faces for the ends in case of "pie"
    if pie:
        faces.append([ x for x in range(l) ][::-1]+[ x+l for x in range(l)[::1] ])
        faces.append([ x+(row_num-1)*l for x in range(l) ][::-1]+[ x+(row_num-2)*l for x in range(l)[::1] ])

    if invert:
        faces = [ list(t)[::-1] for t in faces]

    return verts,altverts,faces

def mesh_stl(verts,faces,name="new_mesh"):
    import numpy as np
    from stl import mesh
    verts = [list((round(x,2),round(y,2),round(z,2))) for x,y,z in verts ]
    faces0 = [ [t[0], t[i], t[i+1]][::-1] for t in faces for i in range(1,len(t)-1)]

    # Define the 8 vertices of the cube
    vertices = np.array(verts)
    # Define the 12 triangles composing the cube
    faces0 = np.array(faces0)

    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces0.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces0):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    cube.save(name+'.stl')
    return name+'.stl'

def mesh_openscad(verts,faces,name="new_mesh"):
    
    verts = [list((round(x,2),round(y,2),round(z,2))) for x,y,z in verts ]
    faces = [list((t[0], t[i], t[i+1])) for t in faces for i in range(1,len(t)-1)]
    
    with open(name+".scad","w") as f:
        text = "polyhedron(points=%s,faces=%s);" % (str(verts),str(faces))
        f.write(text)
    return name+".scad"

def mesh_openjscad(verts,faces,name="new_mesh"):
    verts = [list((round(x,2),round(y,2),round(z,2))) for x,y,z in verts ]
    faces = [list((t[0], t[i], t[i+1])) for t in faces for i in range(1,len(t)-1)]
    # faces = [list(t) for t in faces]
    with open(name+".jscad","w") as f:
        text = """
// title      : Calculus Solids
// author     : Ryan B. Au
// license    : MIT License
// revision   : 1.00
// tags       : Calculus BC, Calculus AB,Vertices, Polyhedron
// file       : poly.jscad

function main () {
    return create_solid();
}
function create_solid(){
    let verts = %s;
    let faces = %s;
    return polyhedron({points:verts,triangles:faces});
}
        """ % (str(verts),str(faces))
        f.write(text)
    return name+".jscad"

def mesh_plotly(verts,name="new_mesh",title="New Mesh",altverts=None):
    # import plotly.offline as py
    # import plotly.graph_objs as go
    verts = [list((round(x,2),round(y,2),round(z,2))) for x,y,z in verts ]
    x,y,z = zip(*verts)
    # traces = []
    # print(altverts)
    # traces.append(go.Scatter3d(x=x,y=y,z=z,mode='markers',marker=dict(size=5,line=dict(color='rgba(217,217,217,0.14)',width=0.5),opacity=0.8)))
    # if altverts is not None:
    #     x1,y1,z1=zip(*altverts)
        
    #     # traces.append(go.Mesh3d(x=x1,y=y1,z=z1,color='#FFB6C1',opacity=0.50))
    #     traces.append(go.Scatter3d(x=x1,y=y1,z=z1,mode='markers',marker=dict(size=5,line=dict(color='rgba(217,0,0,0.14)',width=0.5),opacity=1)))

    
    # py.plot(traces,filename=name+".html",auto_open=False)


    # Quick Main Method
    src = pkgutil.get_data( __name__ , 'plotly_template.html')
    src = src.replace('{{x}}',str(list(x)))
    src = src.replace('{{y}}',str(list(y)))
    src = src.replace('{{z}}',str(list(z)))
    src = src.replace('{{title}}',str(title))
    with open(name+'.html','w') as f:
        f.write(src)
    return name+'.html'

if __name__=='__main__':
    # import subprocess
    # import os
    # v,e,f = cross_triangle(0,3,0.1,lambda x : x*1./5, lambda x : x)
    # v,e,f = cross_semicircle(1,3,0.1,lambda x : x*1./5, lambda x : x)
    v,e,f = solid_revolution(-3,3,0.1,4,lambda x : math.sqrt(9-x**2), lambda x : 0,invert=False)
    # v,e,f = cross_square(-3,3,0.1,lambda x :-math.sqrt(9-x**2), lambda x : math.sqrt(9-x**2))
    mesh_stl(v,f,name="sample")
    # mesh_openscad(v,f,name="sample")
    mesh_openjscad(v,f,name="sample")
    mesh_plotly(v,name='plotted_solid')
    # filename = os.getcwd()+'\sample.stl'
    # print(filename)
    # subprocess.check_call(['start', 'sample.stl']) 