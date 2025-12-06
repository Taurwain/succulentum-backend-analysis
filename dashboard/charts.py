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
        genus_data = filtered_df[filtered_df['genus'].isin(genera_filter)]
        if genus_data.empty:
            return go.Figure()

        fig = go.Figure()

        for genus in genera_filter:
            genus_specific = genus_data[genus_data['genus'] == genus]

            alive_watering = genus_specific[genus_specific['life_status'] == 'живое']['watering_interval'].dropna()
            dead_watering = genus_specific[genus_specific['life_status'] == 'погибло']['watering_interval'].dropna()

            if not alive_watering.empty:
                fig.add_trace(go.Box(
                    y=alive_watering,
                    name=f'{genus} - Живые',
                    marker=dict(color='#2ecc71'),
                    boxmean=True,
                    legendgroup=genus,
                    showlegend=True
                ))

            if not dead_watering.empty:
                fig.add_trace(go.Box(
                    y=dead_watering,
                    name=f'{genus} - Погибшие',
                    marker=dict(color='#e74c3c'),
                    boxmean=True,
                    legendgroup=genus,
                    showlegend=True
                ))

        if genera_filter and len(genera_filter) == 1:
            title = f'Интервалы полива: {genera_filter[0]}'
        else:
            title = f'Интервалы полива: {len(genera_filter)} родов'

    else:
        genus_counts = filtered_df['genus'].value_counts()
        if genus_counts.empty:
            return go.Figure()

        top_genera = genus_counts.head(3).index.tolist()
        genus_data = filtered_df[filtered_df['genus'].isin(top_genera)]

        fig = go.Figure()

        for genus in top_genera:
            genus_specific = genus_data[genus_data['genus'] == genus]

            alive_watering = genus_specific[genus_specific['life_status'] == 'живое']['watering_interval'].dropna()
            dead_watering = genus_specific[genus_specific['life_status'] == 'погибло']['watering_interval'].dropna()

            if not alive_watering.empty:
                fig.add_trace(go.Box(
                    y=alive_watering,
                    name=f'{genus} - Живые',
                    marker=dict(color='#2ecc71'),
                    boxmean=True,
                    legendgroup=genus,
                    showlegend=True
                ))

            if not dead_watering.empty:
                fig.add_trace(go.Box(
                    y=dead_watering,
                    name=f'{genus} - Погибшие',
                    marker=dict(color='#e74c3c'),
                    boxmean=True,
                    legendgroup=genus,
                    showlegend=True
                ))

        title = 'Интервалы полива: Топ-3 рода'

    fig.update_layout(
        title=title,
        yaxis_title='Дней между поливами',
        height=400,
        showlegend=True,
        boxmode='group'
    )

    return fig
