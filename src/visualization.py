import plotly.graph_objects as go

COLOR_PALETTES = ['#2AF598', '#22E4AC', '#1BD7BB', '#14C9CB', '#0FBED8']

layout = go.Layout(
    font={'family': 'Roboto',
          'size': 16,
          'color': 'whitesmoke'},
    template='seaborn',
    xaxis={'showline': True,
           'zeroline': False,
           'showgrid': False,
           'showticklabels': True,
           'color': '#a3a7b0'},
    yaxis={
        'fixedrange': True,
        'showline': False,
        'zeroline': False,
        'showgrid': False,
        'showticklabels': True,
        'ticks': 'inside',
        'color': '#a3a7b0'},
    plot_bgcolor='#23272c',
    paper_bgcolor='#23272c'
)


def line_chart_with_moving_average(series_main, series_ma, custom_ma_name, type, save_as):
    fig = go.Figure(layout=layout)
    fig.add_trace(
        go.Scatter(
            x=series_main.index,
            y=series_main.values,
            name='Total',
        ))

    if series_ma is not None:
        fig.add_trace(
            go.Scatter(
                x=series_ma[0].index,
                y=series_ma[0].values,
                name=custom_ma_name[0],

            ))

        fig.add_trace(
            go.Scatter(
                x=series_ma[1].index,
                y=series_ma[1].values,
                name=custom_ma_name[1],
            ))

    if type == 'overall_freq':
        fig.update_layout(
            title={'text': 'Messages throughout the year'},
            width=700*2.22,
            height=700
        )
    else:
        fig.update_layout(
            title={'text': 'Messages throughout the day'},
            xaxis={
                    'dtick': 1000*60*30,  # in ms
                    'tickformat': '%H:%M'},
            xaxis_tickangle=-45,
            width=700*2.22,
            height=700
        )

    fig.write_image(save_as)


def horizontal_bar_chart(dict, title, suffix, side, save_as):
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Bar(
        x=list(dict.values()),
        y=list(dict.keys()),
        text=[str(v) + suffix for v in dict.values()],
        # insidetextanchor='middle',
        width=0.7,
        orientation='h',
        textposition='inside',
        marker={'line': {'width': 2},
                'color': COLOR_PALETTES}
    ))

    n = 450

    fig.update_layout(
        title={'text': title},
        xaxis={'showline': False,
               'showticklabels': False},
        yaxis={'ticks': ""},
        font={'size': 18},
        width=n,
        height=n
    )

    if side != 'left':
        fig.update_layout(
            xaxis={'autorange': 'reversed'},
            yaxis={'mirror': 'allticks',
                   'side': 'right',
                   })

    fig.write_image(save_as)
