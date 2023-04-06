import altair as alt

def get_line_chart(data, x, y, measure_delta, cate = None, sorting = False):
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