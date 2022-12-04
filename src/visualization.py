import plotly.graph_objects as go

COLOR_PALETTES = ['#2AF598', '#22E4AC', '#1BD7BB', '#14C9CB', '#0FBED8']

layout = go.Layout(
    font={'family': 'Roboto',
          'size': 16,
          'color': 'whitesmoke'},
    template='seaborn',
    # margin={'t': 50, 'b': 70},
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


def line_chart_with_moving_average(series_main, series_ma=(), custom_name=('', ''), type='year', save=False, save_as=None):
    fig = go.Figure(layout=layout)
    fig.add_trace(
        go.Scatter(
            x=series_main.index,
            y=series_main.values,
            name='Total',
        ))

    if len(series_ma) != 0:
        fig.add_trace(
            go.Scatter(
                x=series_ma[0].index,
                y=series_ma[0].values,
                name=custom_name[0],

            ))

        fig.add_trace(
            go.Scatter(
                x=series_ma[1].index,
                y=series_ma[1].values,
                name=custom_name[1],
            ))

    scale = 2.22
    n = 700

    if type == 'overall_freq':
        fig.update_layout(
            # title={'text': 'Messages throughout the year'},
            # xaxis={
            #     'dtick': 'M1',
            #     'tickformat': '%b'},
            width=n*scale,
            height=n
        )
    else:
        fig.update_layout(
            title={'text': 'Messages throughout the day'},
            # xaxis_tickformat='%H:%M',
            xaxis={
                    'dtick': 1000*60*30, # ms frequency
                    'tickformat': '%H:%M'},
            xaxis_tickangle=-45,
            width=n*scale,
            height=n
        )

    if save:
        fig.write_image(save_as)
    else:
        fig.show()


def horizontal_bar_chart(dict, title='', suffix='', side='left', save=False, save_as=None):
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

    if save:
        fig.write_image(save_as)
    else:
        fig.show()
