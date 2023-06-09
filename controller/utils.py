import altair as alt

def create_bar_chart(data, label_colors):
    # base = alt.Chart(data).encode(x=alt.X('main_cate:N'))
    # bar = base.mark_bar().encode(xOffset="main_cate:N", y=alt.Y('sum(sl_ban_cate):Q', axis=alt.Axis(grid=True, title=None, values=list(range(0, 300, 20))), stack='zero'),
    #                             color = alt.Color('main_cate:N'),
    #                             tooltip=[alt.Tooltip("tong_cate", title="Tong"),
    #                                     alt.Tooltip("percent_sl", title="Percent Sl"),
    #                                     alt.Tooltip("percent_tong", title="Percent Tong")
    #                                     ]).properties(width=alt.Step(45),
    #                             )
    
    # line =  base.mark_line(color='red').encode(
    #                             y = 'sl_ban' + ':Q'
    #                             )
    
    fig = alt.Chart(data).mark_bar(size=20).encode(x=alt.X('main_cate:N', title=None, sort=['KM', 'Not KM']), 
                                                    y=alt.Y('sum(sl_ban_cate):Q', axis=alt.Axis(grid=True, title=None, values=list(range(0, 300, 20))), stack='zero'),
                                                    column = 'ngay_filter:N',
                                                    color = alt.Color('main_cate:N'),
                                                    tooltip=[alt.Tooltip("tong_cate", title="Tong"),
                                                            alt.Tooltip("percent_sl", title="Percent Sl"),
                                                            alt.Tooltip("percent_tong", title="Percent Tong")
                                                            ]).properties(width=alt.Step(30))
    
    line =  alt.Chart(data).mark_line(color='red').encode( x = 'ngay_filter:N',
                                y = 'sl_ban' + ':Q'
                                )
    
    # fig = alt.Chart(data).mark_bar(size=30).encode(x=alt.X('main_cate:N', title=None, sort=['KM', 'Not KM']), 
    #                                                     y=alt.Y('sum(sl_ban_cate):Q', axis=alt.Axis(grid=True, title=None, values=list(range(0, 300, 20))), stack='zero'),
    #                                                     color = 'main_cate:N',
    #                                                     tooltip=[alt.Tooltip("tong_cate", title="Tong"),
    #                                                             alt.Tooltip("percent_sl", title="Percent Sl"),
    #                                                             alt.Tooltip("percent_tong", title="Percent Tong")
    #                                                             ]).properties(width=alt.Step(45))

    # text = alt.Chart(data).mark_text(opacity=0.5, color='white', align = 'center', baseline = 'bottom', dx = 0, dy=0).encode(
    #         x=alt.X('main_cate:N', sort=['KM', 'Not KM']),
    #         y=alt.Y('sl_ban_cate:Q', axis = alt.Axis(values=list(range(0, 300, 20)))),
    #         text=alt.Text('sum(sl_ban_cate):Q', format=',.0f')
    #     )
    
    # line = fig.mark_line(color='red').encode(
    #                     y = 'sl_ban' + ':Q')
    
    return fig, line

def create_line_chart(data, x, y, measure_delta, cate = None, sorting = False):
    hover = alt.selection_single(
        fields=[x],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    if cate != None:
        if sorting == False:
            lines = alt.Chart(data).mark_line().encode(
                        x = x + ':O',
                        y = y + ':Q',
                        color = cate + ':N',
                        strokeDash = cate + ':N')
        else:
            lines = alt.Chart(data).mark_line().encode(
                        x = alt.X(x + ':O', sort = data[x].tolist()),
                        y = y + ':Q',
                        color = cate + ':N',
                        strokeDash = cate + ':N')
        tooltip=[
                alt.Tooltip(y, title=y),
                alt.Tooltip(x, title="Cycle"),
                alt.Tooltip(cate, title=cate),
                alt.Tooltip(measure_delta[y], title="Thay đổi")
            ]
    else:
        if sorting == False:
            lines = alt.Chart(data).mark_line().encode(
                        x = x + ':O',
                        y = y + ':Q')
        else:
            lines = alt.Chart(data).mark_line().encode(
                        x = alt.X(x + ':O', sort = data[x].tolist()),
                        y = y + ':Q')
        tooltip=[
                alt.Tooltip(y, title=y),
                alt.Tooltip(x, title=x),
                alt.Tooltip(measure_delta[y], title="Thay đổi")
            ]
    points = lines.transform_filter(hover).mark_circle(size=65)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x = alt.X(x + ':O', sort = data[x].tolist()),
            y=y,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=tooltip
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

def add_percent_symbol(str):
    str = list(str)
    str[-1] = '%)'
    new_str = ''.join(str)
    return new_str

def makeup_percentage_change(df, makeup_cols):
    for el in makeup_cols:
        temp = []
        df[el] = df[el].astype(str)
        for val in df[el].values:
            if float(val) > 0:
                val = '🔼 ' + val + '%'
                temp.append(val)
            elif float(val) == 0:
                val = '🔷 ' + val + '%'
                temp.append(val)
            else:
                val = '🔻 ' + val + '%'
                temp.append(val)
        df[el] = temp
    return df