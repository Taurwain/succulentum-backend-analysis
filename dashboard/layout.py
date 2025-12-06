from io import StringIO
from dash import dcc, html

from .styles import SIDEBAR_STYLE, CONTENT_STYLE


def create_sidebar(all_genera, all_species, all_varieties):
    return html.Div([
        html.H2("Фильтры", className="sidebar-header"),

        html.Hr(),

        html.H5("Фильтр по названию:", className="filter-label"),
        dcc.Input(
            id='name-filter',
            type='text',
            placeholder='Название растения...',
            className='filter-input'
        ),

        html.H5("Фильтр по роду:", className="filter-label"),
        dcc.Dropdown(
            id='genus-filter',
            options=[{'label': g, 'value': g} for g in all_genera],
            placeholder='Выберите род...',
            multi=True,
            className='filter-dropdown',
            value=None
        ),

        html.H5("Фильтр по виду:", className="filter-label"),
        dcc.Dropdown(
            id='species-filter',
            options=[{'label': s, 'value': s} for s in all_species],
            placeholder='Выберите вид...',
            multi=True,
            className='filter-dropdown',
            value=None
        ),

        html.H5("Фильтр по сорту:", className="filter-label"),
        dcc.Dropdown(
            id='variety-filter',
            options=[{'label': v if v else '(без сорта)', 'value': v} for v in all_varieties],
            placeholder='Выберите сорт...',
            multi=True,
            className='filter-dropdown',
            value=None
        ),

        html.Hr(),

        html.Div([
            html.Button(
                'Сбросить фильтры',
                id='reset-filters',
                n_clicks=0,
                className='reset-button'
            )
        ], className='button-group'),

        html.Div(id='current-filters', className='current-filters'),

        html.Hr(),

        html.Div([
            html.H5("Быстрая статистика:", className="filter-label"),
            html.Div(id='quick-stats', className='quick-stats')
        ])

    ], style=SIDEBAR_STYLE)


def create_content(initial_data):
    import pandas as pd

    if initial_data:
        df = pd.read_json(StringIO(initial_data), orient='split')
        total = len(df)
        alive = (df['life_status'] == 'живое').sum()
        dead = (df['life_status'] == 'погибло').sum()

        stats_html = html.Div([
            html.Div([
                html.Div(total, className='stat-value'),
                html.Div("Всего растений", className='stat-label')
            ], className='stat-item'),

            html.Div([
                html.Div(alive, className='stat-value', style={'color': '#2ecc71'}),
                html.Div("Живых", className='stat-label')
            ], className='stat-item'),

            html.Div([
                html.Div(dead, className='stat-value', style={'color': '#e74c3c'}),
                html.Div("Погибших", className='stat-label')
            ], className='stat-item'),
        ], className='stats-summary')
    else:
        stats_html = html.Div("Загрузка данных...", className='stats-summary')

    return html.Div([
        html.H1("Аналитика коллекции растений", className="main-header"),

        html.Div(id='stats-summary', children=stats_html, className='stats-summary'),

        html.Div([
            html.Div([
                dcc.Graph(id='mortality-chart', className='chart')
            ], className='chart-container'),

            html.Div([
                dcc.Graph(id='seasonality-chart', className='chart')
            ], className='chart-container'),
        ], className='charts-row'),

        html.Div([
            html.Div([
                dcc.Graph(id='causes-chart', className='chart')
            ], className='chart-container'),

            html.Div([
                dcc.Graph(id='watering-chart', className='chart')
            ], className='chart-container'),
        ], className='charts-row'),

        html.Div([
            html.H3("Полезные подсказки"),
            html.Div(id='ai-tips', className='ai-tips-container'),
            html.Button(
                'Новая подсказка',
                id='new-tip-button',
                n_clicks=0,
                className='tip-button'
            )
        ], className='tips-section'),

        dcc.Store(id='filtered-data', data=initial_data),
        dcc.Store(id='current-genera', data=[]),
        dcc.Store(id='tip-genera', data=[])

    ], style=CONTENT_STYLE)


def create_layout(all_genera, all_species, all_varieties, initial_data=None):
    return html.Div([
        create_sidebar(all_genera, all_species, all_varieties),
        create_content(initial_data)
    ])
