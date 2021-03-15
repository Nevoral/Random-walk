import dash_html_components as html
import dash
import dash_core_components as dcc
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Nevoral_semestralka_1'
app.layout = html.Div([
                html.Div([
                        html.Div([
                            html.P('Enter type of field and value of radius fields find function...'),
                        dcc.RadioItems(id = 'shape', options=[{'label': i, 'value': i} for i in ['Square space', 'Circle space']], labelStyle={'display': 'inline-block'}),
                        dcc.Input(id = 'field', placeholder='Enter size of area...', type='number',  debounce=True),
                        dcc.Input(id = 'iter', placeholder='Enter number of iteration...', type='number',  debounce=True),
                            html.P('Enter number of starting points...'),
                        dcc.Slider(id='number_start', min=1, max=100, step=1, value=20, marks={1: {'label': '1', 'style': {'color': '#77b0b1'}},
                                                                            10: {'label': '10'},
                                                                            20: {'label': '20'},
                                                                            30: {'label': '30'},
                                                                            40: {'label': '40'},
                                                                            50: {'label': '50'},
                                                                            60: {'label': '60'},
                                                                            70: {'label': '70'},
                                                                            80: {'label': '80'},
                                                                            90: {'label': '90'},
                                                                            100: {'label': '100', 'style': {'color': '#f50'}}})],
                                style={'width': '49%', 'display': 'inline-block'}),
                        html.Div([
                            html.P('Enter a value of radius array function...'),
                        dcc.RadioItems(id = 'metod', options=[{'label': i, 'value': i} for i in ['Random layout starting point', 'Custom layout starting point']], labelStyle={'display': 'inline-block'}),
                        dcc.Input(id = 'x1_value', placeholder='Enter value of x1...', type='number',  debounce=True),
                        dcc.Input(id = 'x2_value', placeholder='Enter value of x2...', type='number',  debounce=True),
                        dcc.Input(id = 'start_point_x1', placeholder='Enter start_point x1', type='number',  debounce=True),
                        dcc.Input(id = 'start_point_x2', placeholder='Enter start_point x2', type='number',  debounce=True),
                        html.P('Enter number of points in find field...'),
                        dcc.Slider(id='number_sol', min=0, max=300, step=10, value=50, marks={0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                                                            50: {'label': '50'},
                                                                            100: {'label': '100'},
                                                                            150: {'label': '150'},
                                                                            200: {'label': '200'},
                                                                            250: {'label': '250'},
                                                                            300: {'label': '300', 'style': {'color': '#f50'}}})],
                                style={'width': '49%', 'float': 'right', 'display': 'inline-block'})],
                            style={'borderBottom': 'thin lightgrey solid', 'backgroundColor': 'rgb(250, 250, 250)', 'padding': '30px 10px'}),
            dcc.Tabs(id="tab", value = 'tab-4', children=[
            dcc.Tab(label='Sphere function', value='tab-1'),
            dcc.Tab(label='Rastrigin function', value='tab-2'),
            dcc.Tab(label='Schwefel function', value='tab-3'),
            ]),
            html.Div(id='tabs-content')])

@app.callback(Output('tabs-content', 'children'),
              [
               Input('tab', 'value'),
               Input('shape', 'value'),
               Input('field', 'value'),
               Input('iter', 'value'),
               Input('number_start', 'value'),
               Input('metod', 'value'),
               Input('x1_value', 'value'),
               Input('x2_value', 'value'),
               Input('number_sol', 'value'),
               Input('start_point_x1', 'value'),
               Input('start_point_x2', 'value'),
               ])

def render_content(tab, shape, field, iter, number_start, metod, x1_value, x2_value, number_sol, start_point_x1, start_point_x2):
    button = True
    if button == True:
        poradi = 0
        if tab == 'tab-1':
            density = 0.1
            x1, x2 = vectors_graf(x1_value, x2_value, density)
            X1, X2 = np.meshgrid(x1, x2)
            poradi = new_txt()
            y = sphere(X1, X2)
            fig = make_subplots(rows=1, cols=2, specs=[[{"type": "surface"}, {}]],)
            fig.add_trace(go.Surface(x = X1, y = X2, z = y), row=1, col=1,)
            fig.update_traces(contours_z = dict(show = True, usecolormap = True, highlightcolor = "limegreen", project_z = True))
            fig.update_layout(width = 1800, height = 750, autosize = False, margin = dict(t = 0, b = 0, l = 0, r = 0), template = "plotly_white",)
            fig.update_scenes(aspectratio = dict(x = 1, y = 1, z = 0.7), aspectmode = "manual")
            fig.update_layout(annotations = [dict(text = "Sphere function", showarrow = False, x = 0, y = 1.085, yref = "paper", align = "left")])
            fig.add_trace(go.Contour(x = x1, y = x2, z = y), row=1, col=2,)
            j = 0
            ymin_abs = 1000
            while j != number_start:
                if metod == 'Custom layout starting point':
                    point, ymin = random_walk_sphere(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, start_point_x1, start_point_x2, j, poradi)
                    metod = 'Random layout starting point'
                    number_start = 1
                else:
                    point, ymin = random_walk_sphere(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, start_point_x1, start_point_x2, j, poradi)
                if ymin_abs > ymin:
                    ymin_abs = ymin
                fig.add_trace(go.Scatter3d(x=point[0:iter-1,0], y=point[0:iter-1,1], z=point[0:iter-1,2]), row=1, col=1,)
                fig.update_layout(title='The best Y minumum... ' + str(ymin_abs), autosize = False)
                fig.add_trace(go.Scatter(x=point[0:iter-1,0], y=point[0:iter-1,1], mode='lines+markers', marker_color='rgba(112, 255, 6, .8)'), row=1, col=2,)
                j += 1
            return html.Div([
                dcc.Graph(id='3Dsurface', figure = fig)], 
                         style={'width': '100%', 'height' : '50%', 'display': 'inline-block', 'padding': '0 0'}),
        elif tab == 'tab-2':
            density = 0.1
            x1, x2 = vectors_graf(x1_value, x2_value, density)
            X1, X2 = np.meshgrid(x1, x2)
            poradi = new_txt()
            y = rastrigin(X1, X2)
            fig = make_subplots(rows=1, cols=2, specs=[[{"type": "surface"}, {}]],)
            fig.add_trace(go.Surface(x = X1, y = X2, z = y), row=1, col=1,)
            fig.update_traces(contours_z = dict(show = True, usecolormap = True, highlightcolor = "limegreen", project_z = True))
            fig.update_layout(width = 1800, height = 750, autosize = False, margin = dict(t = 0, b = 0, l = 0, r = 0), template = "plotly_white",)
            fig.update_scenes(aspectratio = dict(x = 1, y = 1, z = 0.7), aspectmode = "manual")
            fig.update_layout(annotations = [dict(text = "Rastrigin function", showarrow = False, x = 0, y = 1.085, yref = "paper", align = "left")])
            fig.add_trace(go.Contour(x = x1, y = x2, z = y), row=1, col=2,)
            j = 0
            ymin_abs = 1000
            while j != number_start:
                if metod == 'Custom layout starting point':
                    point, ymin = random_walk_rastrigin(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, start_point_x1, start_point_x2, j, poradi)
                    metod = 'Random layout starting point'
                    number_start = 1
                else:
                    point, ymin = random_walk_rastrigin(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, start_point_x1, start_point_x2, j, poradi)
                if ymin_abs > ymin:
                    ymin_abs = ymin
                fig.add_trace(go.Scatter3d(x=point[0:iter-1,0], y=point[0:iter-1,1], z=point[0:iter-1,2]), row=1, col=1,)
                fig.update_layout(title='The best Y minumum... ' + str(ymin_abs), autosize = False)
                fig.add_trace(go.Scatter(x=point[0:iter-1,0], y=point[0:iter-1,1], mode='lines+markers', marker_color='rgba(112, 255, 6, .8)'), row=1, col=2,)
                j += 1
            return html.Div([
                dcc.Graph(id='3Dsurface', figure = fig)], 
                         style={'width': '100%', 'height' : '50%', 'display': 'inline-block', 'padding': '0 0'}),
        elif tab == 'tab-3':
            density = 1
            x1, x2 = vectors_graf(x1_value, x2_value, density)
            X1, X2 = np.meshgrid(x1, x2)
            poradi = new_txt()
            y = schwefel(X1, X2)
            fig = make_subplots(rows=1, cols=2, specs=[[{"type": "surface"}, {}]],)
            fig.add_trace(go.Surface(x = X1, y = X2, z = y), row=1, col=1,)
            fig.update_traces(contours_z = dict(show = True, usecolormap = True, highlightcolor = "limegreen", project_z = True))
            fig.update_layout(width = 1800, height = 750, autosize = False, margin = dict(t = 0, b = 0, l = 0, r = 0), template = "plotly_white",)
            fig.update_scenes(aspectratio = dict(x = 1, y = 1, z = 0.7), aspectmode = "manual")
            fig.update_layout(annotations = [dict(text = "Schwefel function", showarrow = False, x = 0, y = 1.085, yref = "paper", align = "left")])
            fig.add_trace(go.Contour(x = x1, y = x2, z = y), row=1, col=2,)
            j = 0
            ymin_abs = 1000
            while j != number_start:
                if metod == 'Custom layout starting point':
                    point, ymin = random_walk_schwefel(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, start_point_x1, start_point_x2, j, poradi)
                    metod = 'Random layout starting point'
                    number_start = 1
                else:
                    point, ymin = random_walk_schwefel(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, start_point_x1, start_point_x2, j, poradi)
                if ymin_abs > ymin:
                    ymin_abs = ymin
                fig.add_trace(go.Scatter3d(x=point[0:iter-1,0], y=point[0:iter-1,1], z=point[0:iter-1,2]), row=1, col=1,)
                fig.update_layout(title='The best Y minumum... ' + str(ymin_abs), autosize = False)
                fig.add_trace(go.Scatter(x=point[0:iter-1,0], y=point[0:iter-1,1], mode='lines+markers', marker_color='rgba(112, 255, 6, .8)'), row=1, col=2,)
                j += 1
            return html.Div([
                dcc.Graph(id='3Dsurface', figure = fig)], 
                         style={'width': '100%', 'height' : '50%', 'display': 'inline-block', 'padding': '0 0'}),

def sphere(x1, x2):
    return x1**2 + x2**2

def rastrigin(x1, x2):
    return 10 * 2 + ((x1**2 - 10 * np.cos(2 * np.pi * x1)) + (x2**2 - 10 * np.cos(2 * np.pi * x2)))

def schwefel(x1, x2):
    return 418.9829 * 2 - ((x1 * np.sin(np.sqrt(np.abs(x1)))) + (x2 * np.sin(np.sqrt(np.abs(x2)))))

def random_point(x1_value, point):
    limit_dol = point - x1_value
    limit_hor = point + x1_value
    start_point_x1 = np.random.uniform(limit_dol, limit_hor)
    return start_point_x1

def random_point_field(x1_value, point, field):
    limit_dol = point - field
    if limit_dol < -x1_value:
        limit_dol = -x1_value
    limit_hor = point + field
    if limit_hor > x1_value:
        limit_hor = x1_value
    start_point_x1 = np.random.uniform(limit_dol, limit_hor)
    return start_point_x1

def border(x1, x1_value):
     if x1 < -x1_value:
         x1 = -x1_value
     if x1 > x1_value:
         x1 = x1_value
     return x1

def new_txt():
    f = open("poradi.txt", "a+")
    f.write("end")
    f.close()
    f = open("poradi.txt", "r")
    x = f.readline()
    f.close()
    if x == "end":
        f = open("poradi.txt", "w")
        f.write(str(0) + "\n")
        f.close()
    f = open("poradi.txt", "r+")
    x = f.readline()
    x1 = int(x, 10)
    f.close()
    f = open("poradi.txt", "w")
    x1 += 1
    f.write(str(x1) + "\n")
    f.close()
    return x1 - 1

def text_out(x1, x2, y, poradi):
    f = open("result_" + str(poradi) + ".txt","a")
    f.write("(" + str(x1) + "; " + str(x2) + "; " + str(y) + ")\n")
    f.close() 

def text_out_headline(x1_value, x2_value, shape, field, number_start, number_sol, number_trace, type_function, poradi):
    f = open("result_" + str(poradi) + ".txt","a")
    if type_function == 1:
        f.write("--------------------------------------------------------- Sphere function -------------------------------------------------------------\n")
    elif type_function == 2:
        f.write("--------------------------------------------------------- Rastrigin function -------------------------------------------------------------\n")    
    elif type_function == 3:
        f.write("--------------------------------------------------------- Schwefel function -------------------------------------------------------------\n")
    f.write("Size X1: " + str(x1_value) + ",   Shape of searched field: " + str(shape) + ",   Numbers of starting points: " + str(number_start) + "\n")
    f.write("Size X2: " + str(x2_value) + ",   Size of searched field: " + str(field) + ",   Numbers of points in searched field: " + str(number_sol))
    f.write("\n------------------------------------------------------- " + str(number_trace) + " ---------------------------------------------------------\n")
    f.close() 

def text_out_finish(xmin, x2min, ymin, iter, poradi):
    f = open("result_" + str(poradi) + ".txt","a")
    f.write("----------------------------------------------------------------------------------------------------------------------\n")
    f.write("Min X1: " + str(xmin) + ",   Min X2: " + str(x2min) + ",   Min Y: " + str(ymin) + ",   Number of iteration: " + str(iter))
    f.write("\n----------------------------------------------------------------------------------------------------------------------\n")
    f.close() 

def random_point_gaus(x1_value, x2_value, start_point_x1, start_point_x2, radius):
     dist = 2 * radius * (np.random.normal(0, 0.1902, None) - 0.5)
     angle = np.random.uniform(0, 360)
     x1 = float(start_point_x1) + dist * np.cos(angle)
     x1 = border(x1, x1_value)
     x2 = float(start_point_x2) + dist * np.sin(angle)
     x2 = border(x2, x2_value)
     return x1, x2

def vectors_graf(x1, x2, density):
    limit_dol = 0 - x1
    limit_hor = 0 + x1 + density
    x1 = np.arange(limit_dol, limit_hor, density)
    limit_dol = 0 - x2
    limit_hor = 0 + x2 + density
    x2 = np.arange(limit_dol, limit_hor, density)
    return x1, x2

def random_walk_sphere(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, x1, x2, number_trace, poradi):
    text_out_headline(x1_value, x2_value, shape, field, number_start, number_sol, number_trace, 1, poradi) #1 znamena ktera funkce
    point = np.zeros((iter, 3))
    xov = 0
    yov = 1
    zov = 2
    if metod == 'Custom layout starting point':
        start_point_x1 = x1
        start_point_x2 = x2
    else:
        start_point_x1 = random_point(x1_value, 0)
        start_point_x2 = random_point(x2_value, 0)
    ymin = sphere(start_point_x1, start_point_x2)
    point[0,xov] = start_point_x1
    point[0,yov] = start_point_x2
    point[0,zov] = ymin
    text_out(point[0,xov], point[0,yov], point[0,zov], poradi)
    min_abs = [10000, 100000, 100000]
    if shape == 'Square space':
        i = 0
        radius = float(field)/2
        no_change = 0
        while i < iter - 1:
            if no_change == 25:
                radius /= 2
            count = 0
            while count != number_sol:
                x1 = random_point_field(x1_value, start_point_x1, radius)
                x2 = random_point_field(x2_value, start_point_x2, radius)
                y = sphere(x1, x2)
                if y < ymin:
                    ymin = y
                    x1_min = x1
                    x2_min = x2
                    no_change = 0
                count += 1
            i += 1
            no_change += 1
            point[i,xov] = x1_min
            point[i,yov] = x2_min
            point[i,zov] = ymin
            text_out(point[i,xov], point[i,yov], point[i,zov], poradi)
            if ymin < min_abs[2]:
                if np.abs((min_abs[2] - ymin)) < 0.0001:
                    min_abs[0] = x1_min
                    min_abs[1] = x2_min
                    min_abs[2] = ymin
                    break
                min_abs[0] = x1_min
                min_abs[1] = x2_min
                min_abs[2] = ymin
            start_point_x1 = x1_min
            start_point_x2 = x2_min
        text_out_finish(min_abs[0], min_abs[1], min_abs[2], i, poradi)
    else:
        i = 0
        radius = field/2
        no_change = 0
        while i < iter - 1:
            if no_change == 25:
                radius /= 2
            count = 0
            while count != number_sol:
                x1, x2 = random_point_gaus(x1_value, x2_value, start_point_x1, start_point_x2, radius)
                y = sphere(x1, x2)
                if y < ymin:
                    ymin = y
                    x1_min = x1
                    x2_min = x2
                    no_change = 0
                count += 1
            i += 1
            no_change += 1
            point[i,xov] = x1_min
            point[i,yov] = x2_min
            point[i,zov] = ymin
            text_out(point[i,xov], point[i,yov], point[i,zov], poradi)
            if ymin < min_abs[2]:
                if np.abs((min_abs[2] - ymin)) < 0.0001:
                    min_abs[0] = x1_min
                    min_abs[1] = x2_min
                    min_abs[2] = ymin
                    break
                min_abs[0] = x1_min
                min_abs[1] = x2_min
                min_abs[2] = ymin
            start_point_x1 = x1_min
            start_point_x2 = x2_min
        text_out_finish(min_abs[0], min_abs[1], min_abs[2], i, poradi)
    return point, min_abs[2]

def random_walk_rastrigin(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, x1, x2, number_trace, poradi):
    text_out_headline(x1_value, x2_value, shape, field, number_start, number_sol, number_trace, 2, poradi)
    point = np.zeros((iter, 3))
    xov = 0 
    yov = 1
    zov = 2
    if metod == 'Custom layout starting point':
        start_point_x1 = x1
        start_point_x2 = x2
    else:
        start_point_x1 = random_point(x1_value, 0)
        start_point_x2 = random_point(x2_value, 0)
    ymin = rastrigin(start_point_x1, start_point_x2)
    point[0,xov] = start_point_x1
    point[0,yov] = start_point_x2
    point[0,zov] = ymin
    text_out(point[0,xov], point[0,yov], point[0,zov], poradi)
    min_abs = [10000, 100000, 100000]
    if shape == 'Square space':
        i = 0
        radius = field/2
        no_change = 0
        while i < iter - 1:
            if no_change == 25:
                radius /= 2
            count = 0
            while count != number_sol:
                x1 = random_point_field(x1_value, start_point_x1, radius)
                x2 = random_point_field(x2_value, start_point_x2, radius)
                y = rastrigin(x1, x2)
                if y < ymin:
                    ymin = y
                    x1_min = x1
                    x2_min = x2
                    no_change = 0
                count += 1
            i += 1
            no_change += 1
            point[i,xov] = x1_min
            point[i,yov] = x2_min
            point[i,zov] = ymin
            text_out(point[i,xov], point[i,yov], point[i,zov], poradi)
            if ymin < min_abs[2]:
                if np.abs((min_abs[2] - ymin)) < 0.001:
                    min_abs[0] = x1_min
                    min_abs[1] = x2_min
                    min_abs[2] = ymin
                    break
                min_abs[0] = x1_min
                min_abs[1] = x2_min
                min_abs[2] = ymin
            start_point_x1 = x1_min
            start_point_x2 = x2_min
        text_out_finish(min_abs[0], min_abs[1], min_abs[2], i, poradi)
    else:
        i = 0
        radius = field/2
        no_change = 0
        while i < iter - 1:
            if no_change == 25:
                radius /= 2
            count = 0
            while count != number_sol:
                x1, x2 = random_point_gaus(x1_value, x2_value, start_point_x1, start_point_x2, radius)
                y = rastrigin(x1, x2)
                if y < ymin:
                    ymin = y
                    x1_min = x1
                    x2_min = x2
                    no_change = 0
                count += 1
            i += 1
            no_change += 1
            point[i,xov] = x1_min
            point[i,yov] = x2_min
            point[i,zov] = ymin
            text_out(point[i,xov], point[i,yov], point[i,zov], poradi)
            if ymin < min_abs[2]:
                if np.abs((min_abs[2] - ymin)) < 0.001:
                    min_abs[0] = x1_min
                    min_abs[1] = x2_min
                    min_abs[2] = ymin
                    break
                min_abs[0] = x1_min
                min_abs[1] = x2_min
                min_abs[2] = ymin
            start_point_x1 = x1_min
            start_point_x2 = x2_min
        text_out_finish(min_abs[0], min_abs[1], min_abs[2], i, poradi)
    return point, min_abs[2]

def random_walk_schwefel(x1_value, x2_value, shape, field, number_start, number_sol, metod, iter, x1, x2, number_trace, poradi):
    text_out_headline(x1_value, x2_value, shape, field, number_start, number_sol, number_trace, 3, poradi)
    point = np.zeros((iter, 3))
    xov = 0
    yov = 1 
    zov = 2
    if metod == 'Custom layout starting point':
        start_point_x1 = x1
        start_point_x2 = x2
    else:
        start_point_x1 = random_point(x1_value, 0)
        start_point_x2 = random_point(x2_value, 0)
    ymin = schwefel(start_point_x1, start_point_x2)
    point[0,xov] = start_point_x1
    point[0,yov] = start_point_x2
    point[0,zov] = ymin
    text_out(point[0,xov], point[0,yov], point[0,zov], poradi)
    min_abs = [10000, 10000, 10000]
    if shape == 'Square space':
        i = 0
        radius = field/2
        no_change = 0
        while i < iter - 1:
            if no_change == 25:
                radius /= 2
            count = 0
            while count != number_sol:
                x1 = random_point_field(x1_value, start_point_x1, radius)
                x2 = random_point_field(x2_value, start_point_x2, radius)
                y = schwefel(x1, x2)
                if y < ymin:
                    ymin = y
                    x1_min = x1
                    x2_min = x2
                    no_change = 0
                count += 1
            i += 1
            no_change += 1
            point[i,xov] = x1_min
            point[i,yov] = x2_min
            point[i,zov] = ymin
            text_out(point[i,xov], point[i,yov], point[i,zov], poradi)
            if ymin < min_abs[2]:
                if np.abs((min_abs[2] - ymin)) < 0.01:
                    min_abs[0] = x1_min
                    min_abs[1] = x2_min
                    min_abs[2] = ymin
                    break
                min_abs[0] = x1_min
                min_abs[1] = x2_min
                min_abs[2] = ymin
            start_point_x1 = x1_min
            start_point_x2 = x2_min
        text_out_finish(min_abs[0], min_abs[1], min_abs[2], i, poradi)
    else:
        i = 0
        radius = field/2
        no_change = 0
        while i < iter - 1:
            if no_change == 25:
                radius /= 2
            count = 0
            while count != number_sol:
                x1, x2 = random_point_gaus(x1_value, x2_value, start_point_x1, start_point_x2, radius)
                y = schwefel(x1, x2)
                if y < ymin:
                    ymin = y
                    x1_min = x1
                    x2_min = x2
                    no_change = 0
                count += 1
            i += 1
            no_change += 1
            point[i,xov] = x1_min
            point[i,yov] = x2_min
            point[i,zov] = ymin
            text_out(point[i,xov], point[i,yov], point[i,zov], poradi)
            if ymin < min_abs[2]:
                if np.abs((min_abs[2] - ymin)) < 0.01:
                    min_abs[0] = x1_min
                    min_abs[1] = x2_min
                    min_abs[2] = ymin
                    break
                min_abs[0] = x1_min
                min_abs[1] = x2_min
                min_abs[2] = ymin
            start_point_x1 = x1_min
            start_point_x2 = x2_min
        text_out_finish(min_abs[0], min_abs[1], min_abs[2], i, poradi)
    return point, min_abs[2]

if __name__ == '__main__':
    app.run_server(debug=True)