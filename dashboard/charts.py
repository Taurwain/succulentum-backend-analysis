import plotly.graph_objs as go


def create_mortality_chart(filtered_df):
    if filtered_df.empty:
        return go.Figure()

    alive_count = (filtered_df['life_status'] == 'живое').sum()
    dead_count = (filtered_df['life_status'] == 'погибло').sum()
    total = alive_count + dead_count

    fig = go.Figure(data=[
        go.Pie(
            labels=['Живые', 'Погибшие'],
            values=[alive_count, dead_count],
            hole=.3,
            marker=dict(colors=['#2ecc71', '#e74c3c']),
            textinfo='percent+label+value'
        )
    ])

    fig.update_layout(
        title=f'Смертность растений: {dead_count}/{total} ({dead_count / total * 100:.1f}%)',
        title_x=0.5,
        height=400
    )

    return fig


def create_seasonality_chart(filtered_df):
    if filtered_df.empty:
        return go.Figure()

    dead_df = filtered_df[filtered_df['life_status'] == 'погибло']
    if dead_df.empty:
        return go.Figure()

    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
              'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

    death_counts = dead_df['death_month'].value_counts().sort_index()

    for month in range(1, 13):
        if month not in death_counts.index:
            death_counts[month] = 0

    death_counts = death_counts.sort_index()

    fig = go.Figure(data=[
        go.Bar(
            x=months,
            y=death_counts.values,
            marker=dict(color='#e74c3c'),
            text=death_counts.values,
            textposition='auto'
        )
    ])

    fig.update_layout(
        title='Сезонность смертности по месяцам',
        xaxis_title='Месяц',
        yaxis_title='Количество смертей',
        height=400
    )

    return fig


def create_causes_chart(filtered_df):
    if filtered_df.empty:
        return go.Figure()

    dead_df = filtered_df[filtered_df['life_status'] == 'погибло']
    if dead_df.empty:
        return go.Figure()

    causes = dead_df['death_cause'].value_counts()

    fig = go.Figure(data=[
        go.Bar(
            x=causes.index,
            y=causes.values,
            marker=dict(color='#3498db'),
            text=causes.values,
            textposition='auto'
        )
    ])

    fig.update_layout(
        title='Причины смерти растений',
        xaxis_title='Причина',
        yaxis_title='Количество',
        height=400
    )

    return fig


def create_watering_interval_chart(filtered_df, genera_filter=None):
    if filtered_df.empty:
        return go.Figure()

    if genera_filter and len(genera_filter) > 0:
        plot_df = filtered_df[filtered_df['genus'].isin(genera_filter)]
        if plot_df.empty:
            return go.Figure()
    else:
        plot_df = filtered_df

    plot_df = plot_df[plot_df['watering_interval'].notna()]

    if plot_df.empty:
        return go.Figure()

    alive_df = plot_df[plot_df['life_status'] == 'живое']
    dead_df = plot_df[plot_df['life_status'] == 'погибло']

    fig = go.Figure()

    if not alive_df.empty:
        fig.add_trace(go.Histogram(
            x=alive_df['watering_interval'],
            name='Живые растения',
            marker=dict(color='#2ecc71'),
            opacity=0.7,
            nbinsx=20,
            histnorm='percent',
            hovertemplate='Интервал: %{x:.1f} дней<br>Растений: %{y:.1f}%<extra></extra>'
        ))

    if not dead_df.empty:
        fig.add_trace(go.Histogram(
            x=dead_df['watering_interval'],
            name='Погибшие растения',
            marker=dict(color='#e74c3c'),
            opacity=0.7,
            nbinsx=20,
            histnorm='percent',
            hovertemplate='Интервал: %{x:.1f} дней<br>Растений: %{y:.1f}%<extra></extra>'
        ))

    if not alive_df.empty:
        alive_mean = alive_df['watering_interval'].mean()
        fig.add_vline(
            x=alive_mean,
            line_dash="dash",
            line_color="#27ae60",
            annotation_text=f"Среднее (живые): {alive_mean:.1f} дней",
            annotation_position="top right",
            annotation_font_size=10,
            annotation_font_color="#27ae60"
        )

    if not dead_df.empty:
        dead_mean = dead_df['watering_interval'].mean()
        fig.add_vline(
            x=dead_mean,
            line_dash="dash",
            line_color="#c0392b",
            annotation_text=f"Среднее (погибшие): {dead_mean:.1f} дней",
            annotation_position="top left",
            annotation_font_size=10,
            annotation_font_color="#c0392b"
        )

    fig.update_layout(
        title={
            'text': "Распределение интервалов полива",
            'font': {'size': 16}
        },
        xaxis_title='Дней между поливами',
        yaxis_title='Процент растений',
        height=400,
        showlegend=True,
        barmode='overlay',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified',
        margin=dict(t=50, b=50, l=50, r=50)
    )

    fig.update_xaxes(
        range=[0, plot_df['watering_interval'].max() * 1.1],
        gridcolor='lightgray',
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor='lightgray',
        zeroline=False
    )

    return fig
