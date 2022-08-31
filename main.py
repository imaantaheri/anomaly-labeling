from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash import ctx
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timezone

app = Dash(__name__)
server = app.server

df1 = pd.read_csv('Task1.csv')
df2 = pd.read_csv('Task2.csv')


loc_keys = {'df1': 'L1_list' , 'df2': 'L2_list'}
task_keys = {'df1': 'Task1' , 'df2': 'Task2'}

T_list = u = [datetime.fromtimestamp(d, tz=timezone.utc).strftime('%H:%M:%S') for d in range(60*60*6, 60*60*(24), 15*60)]*3
L1_list = list(np.repeat(['CB-5-S', 'CB-9-N', 'CB-10-S'],72))
L2_list = list(np.repeat(['CB-13-E', 'CB-13-S', 'CB-14-E'],72))


L = []

dff = df1[(df1['Time'].isin([T_list[0]])) & (df1['Location'].isin([L1_list[0]]))]
dfg = df1[(df1['Time'].isin([T_list[1]])) & (df1['Location'].isin([L1_list[1]]))]
scale = df1[df1['Location'].isin([L1_list[0]])]


f1 = go.Figure([go.Scatter(x=dff['Density'], y=dff['Volume'], mode='markers')])
f1.data[0]['marker']['color'] = ['blue'] * len(dff)
f1.data[0]['marker']['line']['width'] = 0
f1.data[0]['marker']['size'] = [7] * len(df1)
f1.update_layout(width=510,height=300,clickmode='event', paper_bgcolor='#E1E1E1', plot_bgcolor='white', xaxis= go.layout.XAxis(title= 'Density (Veh/Km)',
                range=[-2,np.max(scale['Density'])+10],linecolor = 'black',linewidth = 1,gridcolor= '#e6e5e3',fixedrange=True, mirror = True),
                yaxis= go.layout.YAxis(title = 'Volume (Veh/hr)', range=[-10,np.max(scale['Volume'])+50], linecolor = 'black', linewidth = 1,
                gridcolor= '#e6e5e3',fixedrange=True, mirror = True),margin=go.layout.Margin(l=75, r=10,b=50,t=20,pad = 4))

f2 = go.Figure([go.Scatter(x=dfg['Density'], y=dfg['Volume'], mode='markers')])
f2.data[0]['marker']['color'] = ['blue'] * len(dff)
f2.data[0]['marker']['line']['width'] = 0
f2.data[0]['marker']['size'] = [7] * len(df1)
f2.update_layout(width=510,height=300,clickmode='event', paper_bgcolor='#E1E1E1',plot_bgcolor='white', xaxis= go.layout.XAxis(title= 'Density (Veh/Km)',
                range=[-2,np.max(scale['Density'])+10],linecolor = 'black',linewidth = 1,gridcolor= '#e6e5e3',fixedrange=True, mirror = True),
                yaxis= go.layout.YAxis(title = 'Volume (Veh/hr)', range=[-10,np.max(scale['Volume'])+50],linecolor = 'black', linewidth = 1,
                gridcolor= '#e6e5e3', fixedrange=True, mirror = True),margin=go.layout.Margin(l=75, r=10,b=50,t=20,pad = 4))

app.layout = html.Div([

    html.H1('Anomaly Detection in Urban Traffic Data: Labeling Survey',
            style={
                'textAlign': 'center',
                'color': 'white',
                'backgroundColor': 'rgb(25,81,144)',
                'font-family':'Calibri',
            }
            ),

    html.Div('Select abnormal points among the BLUE points in each plot and then click NEXT.', style={
        'textAlign': 'center', 'font-size': '20px', 'font-family':'Calibri'
    }),
    html.Div('All that matters is your opinion!', style={
        'textAlign': 'center', 'font-size': '20px', 'font-family':'Calibri'
    }),

    html.Div('Please make sure that the correct task is selected before you start (each task needs around 20 min to be completed):', style={
        'textAlign': 'center', 'margin-top': '20px','font-size': '20px', 'color': 'black', "fontWeight": "bold", 'font-family':'Calibri',
    }),

    dcc.RadioItems(
        options = [{'label': 'Task 1', 'value': 'df1'},
                   {'label': 'Task 2', 'value': 'df2'}],
        value = 'df1',
        id = 'task',
        style={
            'textAlign': 'center',
            'margin-top': '15px',
            'font-size': '18px',
            'color': 'black',
            'font-family':'Calibri',
        }
    ),

    html.Div(id='time',
             style={
                'textAlign': 'center',
                'margin-top': '30px',
                'font-size': '25px',
                'color': 'rgb(25,81,144)',
                "fontWeight": "bold", 'font-family':'Calibri',

             }
    ),

    html.Div(children=[
        dcc.Graph(figure=f1 ,id="basic-interactions", style={'display': 'inline-block'}),
        dcc.Graph(figure=f2 ,id="basic-interactions1", style={'display': 'inline-block'}),
    ], style={'text-align': 'center'}),

    html.Div([
        html.Button(id='next_button', n_clicks=0, children='Next', style= {
            'background-color': 'rgb(25,81,144)','color': 'white','height': '50px',
            'width': '100px','margin-top': '20px'})
    ], style={'text-align': 'center'}),

    html.Div(id='page_count', style={
        'textAlign': 'center',
        'margin-top': '30px',
        'font-size': '18px',
        'color': 'rgb(25,81,144)'
    }),

    html.Div(id ='final-message' ,style={
        'textAlign': 'center',
        'border':'rgb(25,81,144)',
        'margin-top': '30px',
        'font-size': '25px',
        'color': 'rgb(25,81,144)'
    }),

    dcc.Store(id='L1', data=[], storage_type='memory'),
    dcc.Store(id='L2', data=[], storage_type='memory'),
    dcc.Download(id = 'result'),
    ])

@app.callback(
    [Output('final-message', 'children'),
     Output('result', 'data')],
    Input('next_button', 'n_clicks'),
    [State('L1', 'data'),
     State('L2', 'data'),
     State('task', 'value')])
def download(n_clicks, l1, l2, value):
    if n_clicks*2 < len(T_list):
        raise PreventUpdate
    else:
        F = l1 +l2
        final = pd.DataFrame()
        final['Ind'] = F
        name = task_keys[value]
        return 'Thank you for your participation! A file will be automatically downloaded. Please send it to us.', \
               dcc.send_data_frame(final.to_csv, name + '_' + "myresult.csv", index = False)


@app.callback(
    Output('time', 'children'),
    [Input('next_button', 'n_clicks'),
     Input('task', 'value')])
def time_update(n_clicks ,value):
    if n_clicks*2 >= len(T_list):
        raise PreventUpdate
    else:
        cur_L = globals()[loc_keys[value]]
        return cur_L[n_clicks*2] + '______' + T_list[n_clicks*2] + '  and  ' +  T_list[n_clicks*2+1]


@app.callback(
    [Output('basic-interactions', 'figure'),
     Output('page_count', 'children'),
     Output('L1', 'data')],
    [Input('basic-interactions', 'clickData'),
     Input('next_button', 'n_clicks'),
     Input('task', 'value')],
    [State('basic-interactions', 'figure'),
     State('L1', 'data')], prevent_initial_call=True)
def display_click_data(clickData, n_clicks,value, figure, L1):
    if n_clicks*2 >= len(T_list):
        raise PreventUpdate
    else:
        cur_df = globals()[value]
        cur_L = globals()[loc_keys[value]]
        new_data = cur_df[(cur_df['Time'].isin([T_list[n_clicks*2]])) & (cur_df['Location'].isin([cur_L[n_clicks*2]]))]
        scale1 = cur_df[(cur_df['Location'].isin([cur_L[n_clicks*2]]))]
        scat = figure['data'][0]
        scat['x'] = new_data['Density']
        scat['y'] = new_data['Volume']
        if ctx.triggered_id == 'next_button':
            c = ['blue']*len(new_data)
            figure['layout']['xaxis']['range'] = [-2, np.max(scale1['Density']) + 10]
            figure['layout']['yaxis']['range'] = [-10, np.max(scale1['Volume']) + 50]
        elif ctx.triggered_id == 'task':
            c = ['blue'] * len(new_data)
            figure['layout']['xaxis']['range'] = [-2, np.max(scale1['Density']) + 10]
            figure['layout']['yaxis']['range'] = [-10, np.max(scale1['Volume']) + 50]
        else:
            c = list(scat['marker']['color'])
            if c[clickData['points'][0]['pointIndex']] == 'blue':
                c[clickData['points'][0]['pointIndex']] = 'red'
                real_ind = [new_data['Ind'].iloc[clickData['points'][0]['pointIndex']],cur_L[n_clicks*2]]
                L1.append(real_ind) if real_ind not in L1 else L1
            else:
                c[clickData['points'][0]['pointIndex']] = 'blue'
                real_ind = [new_data['Ind'].iloc[clickData['points'][0]['pointIndex']],cur_L[n_clicks*2]]
                L1.remove(real_ind)
        scat['marker']['color'] = c
        if n_clicks*2 > len(T_list):
            total = int(len(T_list) / 2) + 1
            current = len(T_list) + 1
        else:
            total = int(len(T_list)/2) +1
            current = n_clicks+1
    return figure, str(current) + ' of ' + str(total) + ' pages', L1


@app.callback(
    [Output('basic-interactions1', 'figure'),
     Output('L2', 'data')],
    [Input('basic-interactions1', 'clickData'),
     Input('next_button', 'n_clicks'),
     Input('task', 'value')],
    [State('basic-interactions1', 'figure'),
     State('L2', 'data')], prevent_initial_call=True)
def display_click_data(clickData, n_clicks,value, figure,L2):
    if n_clicks*2 >= len(T_list):
        raise PreventUpdate
    else:
        cur_df = globals()[value]
        cur_L = globals()[loc_keys[value]]
        new_data = cur_df[(cur_df['Time'].isin([T_list[n_clicks * 2 +1]])) & (cur_df['Location'].isin([cur_L[n_clicks*2+1]]))]
        scale2 = cur_df[(cur_df['Location'].isin([cur_L[n_clicks * 2+1]]))]
        scat = figure['data'][0]
        scat['x'] = new_data['Density']
        scat['y'] = new_data['Volume']
        if ctx.triggered_id == 'next_button':
            c = ['blue'] * len(new_data)
            figure['layout']['xaxis']['range'] = [-2, np.max(scale2['Density']) + 10]
            figure['layout']['yaxis']['range'] = [-10, np.max(scale2['Volume']) + 50]
        elif ctx.triggered_id == 'task':
            c = ['blue'] * len(new_data)
            figure['layout']['xaxis']['range'] = [-2, np.max(scale2['Density']) + 10]
            figure['layout']['yaxis']['range'] = [-10, np.max(scale2['Volume']) + 50]
        else:
            c = list(scat['marker']['color'])
            if c[clickData['points'][0]['pointIndex']] == 'blue':
                c[clickData['points'][0]['pointIndex']] = 'red'
                real_ind = [new_data['Ind'].iloc[clickData['points'][0]['pointIndex']],cur_L[n_clicks*2]]
                L2.append(real_ind) if real_ind not in L2 else L2
            else:
                c[clickData['points'][0]['pointIndex']] = 'blue'
                real_ind = [new_data['Ind'].iloc[clickData['points'][0]['pointIndex']],cur_L[n_clicks*2]]
                L2.remove(real_ind)
        scat['marker']['color'] = c
        return figure, L2

if __name__ == '__main__':
    app.run_server(debug=True)
