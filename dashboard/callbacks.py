from dash import Input, Output, State, html
import pandas as pd
from io import StringIO
import dash
from plotly import graph_objs as go

from .charts import create_mortality_chart
from .charts import create_seasonality_chart
from .charts import create_causes_chart
from .charts import create_watering_interval_chart
from .smart_tips import get_smart_tip


def register_callbacks(app, plants_df, initial_data=None):
    """
    Registers callbacks for the Dash application.

    Parameters
    ----------
    app : dash.Dash
        Dash application instance
    plants_df : pandas.DataFrame
        Main DataFrame containing plant data
    initial_data : any, optional
        Initial data for the application (default: None)

    Returns
    -------
    None
        Function registers callbacks directly to the app
    """
    @app.callback(
        Output('name-filter', 'value'),
        [Input('reset-filters', 'n_clicks')]
    )
    def reset_name_filter(reset_clicks):
        """
        Reset the name filter input to empty string.

        Parameters
        ----------
        reset_clicks : int
            Number of clicks on the reset button

        Returns
        -------
        str
            Empty string when reset is clicked, dash.no_update otherwise
        """
        if reset_clicks and reset_clicks > 0:
            return ''
        return dash.no_update

    @app.callback(
        [Output('genus-filter', 'options'),
         Output('genus-filter', 'value')],
        [Input('name-filter', 'value'),
         Input('reset-filters', 'n_clicks')]
    )
    def update_genus_options(name_filter, reset_clicks):
        """
        Update available genus options based on name filter.

        Parameters
        ----------
        name_filter : str
            Current value of name filter input
        reset_clicks : int
            Number of clicks on the reset button

        Returns
        -------
        tuple
            First element: List of dicts with genus options
            Second element: Selected genus value(s) or None on reset
        """
        ctx = dash.callback_context

        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if trigger_id == 'reset-filters':
                all_genera = sorted(plants_df['genus'].dropna().unique())
                return [{'label': g, 'value': g} for g in all_genera], None

        if name_filter:
            filtered_df = plants_df[plants_df['name'].str.contains(
                name_filter, case=False, na=False
            )]
            genera = sorted(filtered_df['genus'].dropna().unique())
        else:
            genera = sorted(plants_df['genus'].dropna().unique())

        return [{'label': g, 'value': g} for g in genera], dash.no_update

    @app.callback(
        [Output('species-filter', 'options'),
         Output('species-filter', 'value')],
        [Input('name-filter', 'value'),
         Input('genus-filter', 'value'),
         Input('reset-filters', 'n_clicks')]
    )
    def update_species_options(name_filter, selected_genera, reset_clicks):
        """
        Update available species options based on name and genus filters.

        Parameters
        ----------
        name_filter : str
            Current value of name filter input
        selected_genera : list
            Currently selected genus values
        reset_clicks : int
            Number of clicks on the reset button

        Returns
        -------
        tuple
            First element: List of dicts with species options
            Second element: Selected species value(s) or None on reset
        """
        ctx = dash.callback_context

        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if trigger_id == 'reset-filters':
                all_species = sorted(plants_df['species'].dropna().unique())
                return [{'label': s, 'value': s} for s in all_species], None

        if name_filter:
            filtered_df = plants_df[plants_df['name'].str.contains(
                name_filter, case=False, na=False
            )]
        else:
            filtered_df = plants_df.copy()

        if selected_genera:
            filtered_df = filtered_df[filtered_df['genus'].isin(selected_genera)]

        species = sorted(filtered_df['species'].dropna().unique())
        return [{'label': s, 'value': s} for s in species], dash.no_update

    @app.callback(
        [Output('variety-filter', 'options'),
         Output('variety-filter', 'value')],
        [Input('name-filter', 'value'),
         Input('genus-filter', 'value'),
         Input('species-filter', 'value'),
         Input('reset-filters', 'n_clicks')]
    )
    def update_variety_options(name_filter, selected_genera, selected_species, reset_clicks):
        """
        Update available variety options based on name, genus, and species filters.

        Parameters
        ----------
        name_filter : str
            Current value of name filter input
        selected_genera : list
            Currently selected genus values
        selected_species : list
            Currently selected species values
        reset_clicks : int
            Number of clicks on the reset button

        Returns
        -------
        tuple
            First element: List of dicts with variety options
            Second element: Selected variety value(s) or None on reset
        """
        ctx = dash.callback_context

        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if trigger_id == 'reset-filters':
                all_varieties = sorted(plants_df['variety'].dropna().unique())
                return [{'label': v if v else '(без сорта)', 'value': v} for v in all_varieties], None

        if name_filter:
            filtered_df = plants_df[plants_df['name'].str.contains(
                name_filter, case=False, na=False
            )]
        else:
            filtered_df = plants_df.copy()

        if selected_genera:
            filtered_df = filtered_df[filtered_df['genus'].isin(selected_genera)]

        if selected_species:
            filtered_df = filtered_df[filtered_df['species'].isin(selected_species)]

        varieties = sorted(filtered_df['variety'].dropna().unique())
        return [{'label': v if v else '(без сорта)', 'value': v} for v in varieties], dash.no_update

    @app.callback(
        [Output('filtered-data', 'data'),
         Output('current-genera', 'data'),
         Output('current-filters', 'children'),
         Output('quick-stats', 'children'),
         Output('stats-summary', 'children')],
        [Input('name-filter', 'value'),
         Input('genus-filter', 'value'),
         Input('species-filter', 'value'),
         Input('variety-filter', 'value'),
         Input('reset-filters', 'n_clicks')],
        [State('filtered-data', 'data')]
    )
    def update_data_and_stats(name_filter, genus_filter, species_filter, variety_filter,
                              reset_clicks, current_data):
        """
        Filter plant data and update statistics based on filter inputs.

        Parameters
        ----------
        name_filter : str
            Current value of name filter input
        genus_filter : list
            Currently selected genus values
        species_filter : list
            Currently selected species values
        variety_filter : list
            Currently selected variety values
        reset_clicks : int
            Number of clicks on the reset button
        current_data : str
            Current JSON data stored in the filtered-data component

        Returns
        -------
        tuple
            First element: Filtered DataFrame as JSON string
            Second element: List of currently selected genera
            Third element: HTML component showing active filters
            Fourth element: HTML component with quick statistics
            Fifth element: HTML component with detailed statistics summary
        """
        ctx = dash.callback_context

        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if trigger_id == 'reset-filters':
                filtered_df = plants_df.copy()
                active_filters = html.Div("Нет активных фильтров")
                current_genera = []

                total = len(filtered_df)
                alive = (filtered_df['life_status'] == 'живое').sum()
                dead = (filtered_df['life_status'] == 'погибло').sum()

                quick_stats = html.Div([
                    html.Div(f"Растений: {total}"),
                    html.Div(f"Живых: {alive}", style={'color': '#2ecc71'}),
                    html.Div(f"Погибших: {dead}", style={'color': '#e74c3c'})
                ])

                stats_summary = create_stats_summary(filtered_df)

                return (filtered_df.to_json(date_format='iso', orient='split'),
                        current_genera,
                        active_filters,
                        quick_stats,
                        stats_summary)

        filtered_df = plants_df.copy()
        active_filters = []
        current_genera = genus_filter or []

        if name_filter:
            filtered_df = filtered_df[filtered_df['name'].str.contains(
                name_filter, case=False, na=False
            )]
            active_filters.append(html.Span(f"Название: {name_filter}", className='filter-tag'))

        if genus_filter:
            filtered_df = filtered_df[filtered_df['genus'].isin(genus_filter)]
            genera_text = ", ".join(genus_filter[:3])
            if len(genus_filter) > 3:
                genera_text += f" (+{len(genus_filter) - 3})"
            active_filters.append(html.Span(f"Роды: {genera_text}", className='filter-tag'))

        if species_filter:
            filtered_df = filtered_df[filtered_df['species'].isin(species_filter)]
            species_text = ", ".join(species_filter[:3])
            if len(species_filter) > 3:
                species_text += f" (+{len(species_filter) - 3})"
            active_filters.append(html.Span(f"Виды: {species_text}", className='filter-tag'))

        if variety_filter:
            filtered_df = filtered_df[filtered_df['variety'].isin(variety_filter)]
            variety_text = ", ".join([v if v else '(без сорта)' for v in variety_filter[:3]])
            if len(variety_filter) > 3:
                variety_text += f" (+{len(variety_filter) - 3})"
            active_filters.append(html.Span(f"Сорта: {variety_text}", className='filter-tag'))

        if not active_filters:
            active_filters = html.Div("Нет активных фильтров")
        else:
            active_filters = html.Div(active_filters)

        total = len(filtered_df)
        alive = (filtered_df['life_status'] == 'живое').sum()
        dead = (filtered_df['life_status'] == 'погибло').sum()

        quick_stats = html.Div([
            html.Div(f"Растений: {total}"),
            html.Div(f"Живых: {alive}", style={'color': '#2ecc71'}),
            html.Div(f"Погибших: {dead}", style={'color': '#e74c3c'})
        ])

        stats_summary = create_stats_summary(filtered_df)

        return (filtered_df.to_json(date_format='iso', orient='split'),
                current_genera,
                active_filters,
                quick_stats,
                stats_summary)

    @app.callback(
        [Output('mortality-chart', 'figure'),
         Output('seasonality-chart', 'figure'),
         Output('causes-chart', 'figure'),
         Output('watering-chart', 'figure')],
        [Input('filtered-data', 'data'),
         Input('current-genera', 'data')]
    )
    def update_charts(json_data, genera_filter):
        """
        Update all charts with filtered data.

        Parameters
        ----------
        json_data : str
            JSON string of filtered DataFrame
        genera_filter : list
            Currently selected genus values for filtering

        Returns
        -------
        tuple
            Four plotly.graph_objs.Figure objects for:
            1. Mortality chart
            2. Seasonality chart
            3. Causes chart
            4. Watering interval chart
        """
        if json_data is None:
            return go.Figure(), go.Figure(), go.Figure(), go.Figure()

        df = pd.read_json(StringIO(json_data), orient='split')

        mortality_fig = create_mortality_chart(df)
        seasonality_fig = create_seasonality_chart(df)
        causes_fig = create_causes_chart(df)
        watering_fig = create_watering_interval_chart(df, genera_filter)

        return mortality_fig, seasonality_fig, causes_fig, watering_fig

    @app.callback(
        [Output('ai-tips', 'children'),
         Output('tip-genera', 'data')],
        [Input('new-tip-button', 'n_clicks'),
         Input('current-genera', 'data'),
         Input('filtered-data', 'data')],
        [State('tip-genera', 'data'),
         State('species-filter', 'value')]
    )
    def update_tips(n_clicks, current_genera, json_data, stored_genera, selected_species):
        """
        Generate tips for plant care.

        Parameters
        ----------
        n_clicks : int
            Number of clicks on the new tip button
        current_genera : list
            Currently selected genus values
        json_data : str
            JSON string of filtered DataFrame
        stored_genera : list
            Previously stored genus values for comparison
        selected_species : list
            Currently selected species values

        Returns
        -------
        tuple
            First element: HTML component with AI tip
            Second element: Updated list of current genera for state management
        """
        ctx = dash.callback_context

        if json_data:
            df = pd.read_json(StringIO(json_data), orient='split')
        else:
            df = plants_df.copy()

        tip = get_smart_tip(df, current_genera, selected_species)
        if not tip:
            return dash.no_update, current_genera

        return tip, current_genera


def create_stats_summary(df):
    """
    Create HTML summary component with plant statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing plant data

    Returns
    -------
    dash.html.Div
        HTML component with statistics displayed in a grid layout
    """
    total = len(df)
    alive = (df['life_status'] == 'живое').sum()
    dead = (df['life_status'] == 'погибло').sum()

    avg_lifespan = df[df['life_status'] == 'погибло']['lifespan_days'].mean()
    if pd.isna(avg_lifespan):
        avg_lifespan_text = "Нет данных"
    else:
        years = avg_lifespan // 365
        months = (avg_lifespan % 365) // 30
        if years > 0:
            avg_lifespan_text = f"{years}г {months}м"
        else:
            avg_lifespan_text = f"{months} месяцев"

    avg_watering = df['watering_interval'].mean()
    if pd.isna(avg_watering):
        avg_watering_text = "Нет данных"
    else:
        avg_watering_text = f"{avg_watering:.1f} дней"

    top_cause = "Нет данных"
    if dead > 0:
        causes = df[df['life_status'] == 'погибло']['death_cause'].value_counts()
        if not causes.empty:
            top_cause = causes.index[0]

    return html.Div([
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

        html.Div([
            html.Div(avg_lifespan_text, className='stat-value'),
            html.Div("Средняя продолжительность жизни", className='stat-label')
        ], className='stat-item'),

        html.Div([
            html.Div(avg_watering_text, className='stat-value'),
            html.Div("Средняя частота полива", className='stat-label')
        ], className='stat-item'),

        html.Div([
            html.Div(top_cause[:15] + "..." if len(top_cause) > 15 else top_cause,
                     className='stat-value', style={'font-size': '18px'}),
            html.Div("Частая причина", className='stat-label')
        ], className='stat-item')
    ], className='stats-summary')
