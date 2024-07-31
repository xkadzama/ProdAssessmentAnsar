import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

from take_csv import parse_csv_data

# создаем Dash приложение
app = dash.Dash(__name__)

group_name = 'К.Хусейн'  # <-------- сменить файл преподавателя
data = parse_csv_data(f'MyGroups/{group_name}.csv')

# 1
# Достаем даты из парсера и кидаем в список days
days = list()
for dt_less in data:
    days.append(dt_less['data'])

# 2
# Парсим список с словарями и приводим в нужный вид (словарь) (без ключей с датами и имен) для отправки в датафрейм
result = {}
for entry in data:
    for key, value in entry.items():
        if key not in ['data', 'names']:
            if key not in result:
                result[key] = []
            result[key].extend(value)

# 3
df = pd.DataFrame(result)  # готовый фрейм

# создаем график
fig = go.Figure()

# 5
# Отображаем данные на графике
def add_student(name_df, name, group_days, color_s='white', dash_s='solid'):
    fig.add_trace(go.Scatter(
        x=group_days,
        y=name_df,
        mode='lines+markers',
        line=dict(color=color_s, width=2, dash=dash_s),  # solid прямая линия, dash черточки
        marker=dict(color=color_s, size=8),
        name=name
    ))

'''
Добавляем учеников через функцию add_student где: 
1: ДатаФрейм с баллами учеников
2: Имя (по дефолту - student
3: Дни учебы группы (по дефолу - пустой список)
4: Цвет ученика/линий (по дефолту - white)
5: Линия (по дефолту solid *прямая*, можно сменить на dash *черточки*)
'''
# 4
colors = ['green', 'red', 'blue', 'purple', 'orange', 'yellow', 'brown']
i = 0
for name in df:  # result
    add_student(df[name], name, days, colors[i])
    i += 1
# add_student(data['Xoce'], 'Xoce', 'green')

# Настройки диаграммы
fig.update_layout(
    plot_bgcolor='#09161C',
    paper_bgcolor='#09161C',
    font=dict(color='white'),
    xaxis=dict(
        tickmode='array',
        tickvals=days,
        range=[days[0], days[-1]],  # дни занятий от первого в списке до последнего
        showgrid=True,
        gridcolor='white',
        tickcolor='white',
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        range=[0, 7],  # шкала продуктивности
        showgrid=True,
        gridcolor='white',
        tickcolor='white',
        tickfont=dict(color='white')
    ),
    legend=dict(
        font=dict(color='white'),
        x=0,
        y=1
    ),
    title=f'{group_name}',
    xaxis_title='Дни',
    yaxis_title='Продуктивность'
)

# задаем стиль границ графика
fig.update_xaxes(showline=True, linewidth=0.5, linecolor='white', mirror=True)
fig.update_yaxes(showline=True, linewidth=0.5, linecolor='white', mirror=True)

# добавляем график в приложение и устанавливаем стиль для body
app.layout = html.Div(
    children=[
        html.Div(
            children=html.Img(src='assets/logo.png', style={'height': '60px'}),
            style={'textAlign': 'center', 'padding': '20px'}
        ),
        dcc.Graph(id='productivity-graph', figure=fig)
    ],
    style={'backgroundColor': '#09161C', 'height': '100vh', 'margin': '0px'}
)

if __name__ == '__main__':
    app.run_server(debug=True)
