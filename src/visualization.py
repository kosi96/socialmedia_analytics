import plotly.graph_objects as go

layout = go.Layout(
    font={'family': 'Roboto',
          'size': 14,
          'color': 'whitesmoke'},
    template='seaborn',
    margin={'t': 50, 'b': 70},
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

color_palettes = ['#2AF598', '#22E4AC', '#1BD7BB', '#14C9CB', '#0FBED8']


def line_chart_with_moving_average(series_main, series_ma=tuple(), custom_name=('', ''), type='year', save_as=None):
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
                name=custom_name[0],

            ))

        fig.add_trace(
            go.Scatter(
                x=series_ma[1].index,
                y=series_ma[1].values,
                name=custom_name[1],
            ))

    if type == 'year':
        fig.update_layout(
            title={'text': 'Messages throughout the year'},
            xaxis={
                'dtick': 'M1',
                'tickformat': '%b'},
            width=None,
            height=None
        )
    else:
        fig.update_layout(
            title={'text': 'Messages throughout the day'},
            # xaxis_tickformat='%H:%M',
            xaxis={
                    'dtick': 1000*60*30, # ms frequency
                    'tickformat': '%H:%M'},
            xaxis_tickangle=-45,
            width=None,
            height=None
        )

    if save_as != None:
        fig.write_image(save_as)
    else:
        fig.show()


def horizontal_bar_chart(dict, custom_name='', side='left', save_as=None):
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Bar(
        x=list(dict.values()),
        y=list(dict.keys()),
        text=[str(v) + '%' for v in dict.values()],
        width=0.7,
        orientation='h',
        textposition='inside',
        marker={'line': {'width': 2},
                'color': color_palettes}
    ))

    fig.update_layout(
        title={'text': f'Favored Emojis {custom_name}'},
        xaxis={'showline': False,
               'showticklabels': False},
        yaxis={'ticks': ""},
        font={'size': 18},
        width=None,
        height=None
    )

    if side != 'left':
        fig.update_layout(
            xaxis={'autorange': 'reversed'},
            yaxis={'mirror': 'allticks',
                   'side': 'right',
                   })

    if save_as != None:
        fig.write_image(save_as)
    else:
        fig.show()

#
# def linePlotWithMonthlyTrend(series):
#     fig = px.line(
#         x=series.index,
#         y=series.values,
#         template=base_template
#     )
#
#     trendline = px.scatter(
#         x=series.index,
#         y=series.values,
#         opacity=0,
#         template=base_template,
#         trendline="rolling",
#         trendline_options={'window': 30},
#         trendline_color_override='#FFA500'
#     )
#
#     fig.add_traces(
#         list(trendline.select_traces())
#     )
#
#     fig.update_yaxes(range=[0, max(series.values)])
#
#     fig.show()
#
#
# def horizontalBarChart(data, reverse=False):
#     fig = px.bar(
#         x=data.values(),
#         y=data.keys(),
#         orientation='h',
#         text=data.values(),
#         template=base_template
#     )
#
#     fig.update_layout(title={'text': 'Favourite Emojis'},
#                       xaxis={'title': '',
#                              'showline': False,
#                              'zeroline': False,
#                              'showgrid': False,
#                              'showticklabels': False
#                              },
#                       yaxis={'title': '',
#                              'ticks': ""},
#                       # textposition='inside',
#                       # marker={'line': {'width': 2},
#                       #         'color': ['#2AF598', '#22E4AC', '#1BD7BB', '#14C9CB', '#0FBED8']},
#                       font={'size': 14},
#                       width=300, height=300)
#     if reverse:
#         fig.update_layout(
#             xaxis={"autorange": "reversed"},
#             yaxis={"mirror": "allticks", 'side': 'right'}
#         )
#
#     fig.show()
#
#
# def linePlotWithDailyTrend(df):
#     fig = px.line(
#         x=df.index,
#         y=df[0],
#         template=base_template
#     )
#
#     trendline = px.scatter(
#         x=df.index,
#         y=df[0],
#         opacity=0,
#         template=base_template,
#         trendline="rolling",
#         trendline_options={'window': 60},
#         trendline_color_override='#FFA500'
#     )
#
#     # fig.add_traces(
#     #     list(trendline.select_traces())
#     # )
#
#     fig.update_yaxes(range=[0, max(df[0].values)])
#
#     fig.update_layout(title={'text': 'Messages throughout the day'},
#                       xaxis={
#                           'title': '',
#                           'dtick': 60
#                       },
#                       yaxis={
#                           'title': '',
#                           'ticks': "",
#                           'color': '#a3a7b0',
#                           'tick0': 0.5
#                       },
#                       xaxis_tickangle=-45,
#                       font={'size': 14}
#                       )
#
#     fig.show()
