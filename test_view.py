
import dash
from dash.development.base_component import ComponentRegistry
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input,Output
import pandas as pd
import datetime

from database import db_session
from models import Data_D
from models import Data_L

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

now = datetime.datetime.today()
now_start_1 = now - datetime.timedelta(hours=3)

day1 = (datetime.datetime.today() - datetime.timedelta(days=1))
day2 = (datetime.datetime.today() - datetime.timedelta(days=2))
day3 = (datetime.datetime.today() - datetime.timedelta(days=3))
day4 = (datetime.datetime.today() - datetime.timedelta(days=4))
day5 = (datetime.datetime.today() - datetime.timedelta(days=5))
day6 = (datetime.datetime.today() - datetime.timedelta(days=6))
day7 = (datetime.datetime.today() - datetime.timedelta(days=7))

# fig1の値のlistを作成
data_D = db_session.query(Data_D.date_detection,Data_D.detection).all()
dates_D = []
detection = []

for datum in data_D:
    dates_D.append(datum.date_detection)
    detection.append(datum.detection)

df_fig1 = pd.DataFrame()
df_fig1["date"] =  dates_D
df_fig1["detection"] =  detection

# fig2の値のlistを作成
df_fig2 = df_fig1.groupby(pd.Grouper(key='date',freq='1H')).sum().reset_index()

# fig3の値のlistを作成
data_L = db_session.query(Data_L.date_luminance,Data_L.luminance).all()
dates_L = []
luminance = []

for datum in data_L:
    dates_L.append(datum.date_luminance)
    luminance.append(datum.luminance)

df_fig3 = pd.DataFrame()
df_fig3["date"] =  dates_L
df_fig3["luminance"] =  luminance

# fig4の値のlistを作成
df_fig4 = df_fig3.groupby(pd.Grouper(key='date',freq='1H')).mean().reset_index()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout=html.Div(children=[
    html.H3(style={'font-size':20},children='見守りシステム(人感センサー／輝度センサーの値表示）'),
    html.Div(children=[
        dcc.Graph(
            id='detection_graph',
            figure={
                'data':[
                    go.Bar(
                        x=df_fig1['date'],
                        y=df_fig1['detection'],
                        name='3時間以内の人感センサーの検知回数',
                        yaxis='y1',
                        width=450000
                    )
                ],
                'layout': go.Layout(
                    title='3時間以内の人感センサーのデーター',
                    xaxis=dict(title='date',range=[now_start_1,now]),
                    yaxis=dict(title='検知回数',side='right',overlaying='y',showgrid=False,range=[0,df_fig1['detection'].max()]),
                    margin=dict(l=50, r=100, b=80, t=100)
                )
            }
        )
    ]),
    html.P(style={"font-size":12,"margin-bottom":50,"margin-right":100,"text-align":"right"},children="※センサーの検知回数は1秒間に1回。\
        上記グラフは10分単位の検知回数の合計を表示しているため、60秒×10分＝600回が最大の検知回数"
    ),
    html.Div(children=[
        dcc.Graph(
            id='detection_graph2'
        )
    ]),
    html.P(style={"font-size":12,"margin-bottom":50,"margin-right":100,"text-align":"right"},children="※センサーの検知回数は1秒間に1回。\
        上記グラフは1時間単位の検知回数の合計を表示しているため、60秒×60分＝3600回が最大の検知回数"
    ),
    html.Label('表示させるグラフの日付を選択'),
        dcc.Dropdown(id='input-date',
        options=[
            {'label': '本日','value':day1},
            {'label': '1日前','value':day2},
            {'label': '2日前','value':day3},
            {'label': '3日前','value':day4},
            {'label': '4日前','value':day5},
            {'label': '5日前','value':day6},
            {'label': '6日前','value':day7}
        ],
        value=day1
    ),
    html.Div(style={"margin-bottom":100},id='output-div'
    ),
    html.Div(children=[
        dcc.Graph(
            id='luminance_graph',
            figure={
                'data':[
                    go.Scatter(
                        x=df_fig3['date'],
                        y=df_fig3['luminance'],
                        name='3時間以内の輝度センサーの検知回数',
                        yaxis='y1',
                        mode='lines+markers',
                        opacity=0.7,
                        marker={
                            'size':9
                        }
                    )
                ],
                'layout': go.Layout(
                    title='3時間以内の輝度センサーのデーター',
                    xaxis=dict(title='date',range=[now_start_1,now]),
                    yaxis=dict(title='輝度',side='right',overlaying='y',showgrid=False,range=[0,110]),
                    margin=dict(l=50, r=100, b=80, t=100)
                )
            }
        )
    ]),
    html.P(style={"font-size":12,"margin-bottom":50,"margin-right":100,"text-align":"right"},children="※輝度の最大値は100。\
        センサーの検知回数は1秒間に1回。上記グラフは10分単位の検知回数の平均を表示。"
    ),
    html.Div(children=[
        dcc.Graph(
            id='luminance_graph2'
        )
    ]),
    html.P(style={"font-size":12,"margin-bottom":50,"margin-right":100,"text-align":"right"},children="※輝度の最大値は100。\
        センサーの検知回数は1秒間に1回。上記グラフは1時間単位の検知回数の平均を表示。"
    ),
    html.Label('表示させるグラフの日付を選択'),
        dcc.Dropdown(id='input-date2',
        options=[
            {'label': '本日','value':day1},
            {'label': '1日前','value':day2},
            {'label': '2日前','value':day3},
            {'label': '3日前','value':day4},
            {'label': '4日前','value':day5},
            {'label': '5日前','value':day6},
            {'label': '6日前','value':day7}
        ],
        value=day1
    ),
    html.Div(style={"margin-bottom":100},id='output-div2'
    )
],
style={
    'textAlgin': 'center',
    'width':"1600px",
    'margin':'0 auto'
    }
)

# 人感センサーのcallback関数

@app.callback([
    Output(component_id='output-div',component_property='children'),
    Output(component_id='detection_graph2',component_property='figure')],
    [Input(component_id='input-date',component_property='value')]
)

def update(input_value):
    callback_date1 = input_value.split("T")
    callback_date2 = callback_date1[1].split(":")
    callback_date2 = str(int(callback_date2[0]) + 1)
    callback_date3 = datetime.datetime.strptime(input_value,'%Y-%m-%dT%H:%M:%S.%f')
    callback_date4 = callback_date3 + datetime.timedelta(days=1)
    figure={
        'data':[
            go.Bar(
                x=df_fig2['date'],
                y=df_fig2['detection'],
                name='選択した日付の人感センサーの検知回数',
                yaxis='y1',
                width=2700000
            )
        ],
        'layout': go.Layout(
            title='選択した日付の人感センサーのデーター',
            xaxis=dict(title='date',range=[callback_date3,callback_date4]),
            yaxis=dict(title='検知回数',side='right',overlaying='y',showgrid=False,range=[0,df_fig2['detection'].max()]),
            margin=dict(l=50, r=100, b=80, t=100)
        )
    }

    return [
        '{}時より1日分のグラフを表示'.format(callback_date1[0] + " " + callback_date2),
        figure
    ]

# 輝度センサーのcallback関数

@app.callback([
    Output(component_id='output-div2',component_property='children'),
    Output(component_id='luminance_graph2',component_property='figure')],
    [Input(component_id='input-date2',component_property='value')]
)

def update2(input_value):
    callback_date1 = input_value.split("T")
    callback_date2 = callback_date1[1].split(":")
    callback_date2 = str(int(callback_date2[0]) + 1)
    callback_date3 = datetime.datetime.strptime(input_value,'%Y-%m-%dT%H:%M:%S.%f')
    callback_date4 = callback_date3 + datetime.timedelta(days=1)
    figure={
        'data':[
            go.Scatter(
                x=df_fig4['date'],
                y=df_fig4['luminance'],
                name='選択した日付の輝度センサーの値',
                yaxis='y1',
                        mode='lines+markers',
                        opacity=0.7,
                        marker={
                            'size':9
                        }
            )
        ],
        'layout': go.Layout(
            title='選択した日付の輝度センサーのデーター',
            xaxis=dict(title='date',range=[callback_date3,callback_date4]),
            yaxis=dict(title='輝度',side='right',overlaying='y',showgrid=False,range=[0,110]),
            margin=dict(l=50, r=100, b=80, t=100)
        )
    }

    return [
        '{}時より1日分のグラフを表示'.format(callback_date1[0] + " " + callback_date2),
        figure
    ]

if __name__=='__main__':
    app.run_server(debug=True)
