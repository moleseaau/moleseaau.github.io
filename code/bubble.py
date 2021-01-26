import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Loading in the data, renaming columns, and generally making the data ready for plotting
df15 = pd.read_csv('2015.csv')
df16 = pd.read_csv('2016.csv')
df17 = pd.read_csv('2017.csv')
df18 = pd.read_csv('2018.csv')
df19 = pd.read_csv('2019.csv')

df15['Country'] = df15['Country'].replace({'Palestinian Territories': 'Palestine', 'Congo (Brazzaville)': 'Congo',
                                           'Somaliland region': 'Somalia', 'Congo (Kinshasa)': 'Congo Republic',
                                           'Central African Republic': 'Central Africa'})

df17 = df17.rename(columns={'Happiness.Score': 'Happiness Score', 'Economy..GDP.per.Capita.': 'Economy (GDP per Capita',
                            'Health..Life.Expectancy.': 'Health (Life Expectancy)', 'Happiness.Rank': 'Happiness Rank',
                            'Trust..Government.Corruption.': 'Trust (Government Corruption)'})
df18 = df18.rename(
    columns={'Country or region': 'Country', 'Score': 'Happiness Score', 'Overall rank': 'Happiness Rank',
             'GDP per capita': 'Economy (GDP per Capita', 'Social support': 'Family',
             'Healthy life expectancy': 'Health (Life Expectancy)', 'Freedom to make life choices': 'Freedom',
             'Perceptions of corruption': 'Trust (Goverment Corruption)'})
df19 = df19.rename(
    columns={'Country or region': 'Country', 'Score': 'Happiness Score', 'Overall rank': 'Happiness Rank',
             'GDP per capita': 'Economy (GDP per Capita', 'Social support': 'Family',
             'Healthy life expectancy': 'Health (Life Expectancy)', 'Freedom to make life choices': 'Freedom',
             'Perceptions of corruption': 'Trust (Goverment Corruption)'})

df15 = df15.set_index('Country', drop=False)
df16 = df16.set_index('Country', drop=False)
df17 = df17.set_index('Country', drop=False)
df18 = df18.set_index('Country', drop=False)
df19 = df19.set_index('Country', drop=False)

df17['Region'] = ''
df18['Region'] = ''
df19['Region'] = ''
df17['Region'] = df15['Region']
df18['Region'] = df15['Region']
df19['Region'] = df15['Region']

df15 = df15.set_index('Happiness Rank')
df16 = df16.set_index('Happiness Rank')
df17 = df17.set_index('Happiness Rank')
df18 = df18.set_index('Happiness Rank')
df19 = df19.set_index('Happiness Rank')

df15['Year'] = 2015
df16['Year'] = 2016
df17['Year'] = 2017
df18['Year'] = 2018
df19['Year'] = 2019

colors = {'Western Europe': 'Blue', 'Central and Eastern Europe': 'Magenta',
          'Australia and New Zealand': 'Purple', 'North America': 'Red',
          'Latin America and Caribbean': 'DarkOrange', 'Southern Asia': 'CornflowerBlue',
          'Southeastern Asia': 'Brown', 'Eastern Asia': 'LimeGreen',
          'Middle East and Northern Africa': 'Green', 'Sub-Saharan Africa': 'SlateGrey'}

df15_mean = df15.groupby(['Region']).mean()
df15_mean = df15_mean.drop(columns=['Happiness Score', 'Standard Error', 'Dystopia Residual', 'Year'])
df_new = df15_mean.transpose()
df_new = df_new[['Western Europe', 'North America', 'Australia and New Zealand',
                 'Middle East and Northern Africa', 'Latin America and Caribbean',
                 'Southeastern Asia', 'Central and Eastern Europe', 'Eastern Asia',
                 'Sub-Saharan Africa', 'Southern Asia']]

avg_happy_score15 = round((df15['Happiness Score'].sum(axis=0, skipna=True) / (len(df15.index))), 2)


def bars():
    fig = make_subplots(rows=2, cols=1, subplot_titles=['', ''])

    for i in df15['Region'].unique():
        dfn = df15[df15['Region'] == i]
        fig.add_trace(trace=go.Bar(x=dfn['Country'],
                                   y=dfn['Happiness Score'],
                                   # error_y=dict(type='data', array=df15['Standard Error'],
                                   #              thickness=2, width=2),
                                   name=i,
                                   marker_color=colors[i],
                                   hovertemplate='<b>Region</b> : ' + dfn['Region'] +
                                                 '<br><b>Country</b> : %{x}' +
                                                 '<br><b>Happiness Score</b> : %{y:.2f}<extra></extra>',
                                   legendgroup=i),
                      row=1, col=1)

    average_line = [dict(type="line",
                         xref="paper", yref="y",
                         x0=0, y0=avg_happy_score15,
                         x1=1, y1=avg_happy_score15,
                         line=dict(color="Black", dash='dot'), opacity=0.5)]

    annotation = [dict(x=130, y=avg_happy_score15 + 0.3,
                       text="Average Happiness Score: 5.38",
                       showarrow=True, arrowhead=1)]

    for i in df_new.columns.unique():
        fig.add_trace(trace=go.Bar(x=df_new.index,
                                   y=df_new[i],
                                   name=i,
                                   marker_color=colors[i],
                                   hovertemplate='<b>Average Regional Value</b> : %{y:.2f}<extra></extra>',
                                   legendgroup=i,
                                   showlegend=False),
                      row=2, col=1)

    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                active=0,
                x=0.81,
                y=1.12,
                buttons=[
                    dict(label="Hide Average Happiness Score",
                         method="relayout",
                         args=[{"shapes": [], "annotations": []}]
                         ),
                    dict(label="Show Average Happiness Score",
                         method="relayout",
                         args=[{"shapes": average_line, "annotations": annotation}]
                         ),
                ],
            ),
            dict(
                type="dropdown",
                direction="down",
                active=0,
                x=1,
                y=1.12,
                buttons=[
                    dict(label="Sort in Regions",
                         method="relayout",
                         args=[{'xaxis.categoryorder': []}]
                         ),
                    dict(label="Sort by Happiness Score",
                         method="relayout",
                         args=[{'xaxis.categoryorder': 'total descending'}]
                         )
                ]
            )
        ]
    )

    fig.update_layout(barmode='group', legend_title='<b>Different Regions<b>',
                      title='Bar Plots of World Happiness Report',
                      legend=dict(bordercolor="Black", borderwidth=2))

    fig.update_yaxes(showspikes=True,
                     spikemode='across',
                     spikethickness=1,
                     spikecolor='Black',
                     showline=True,
                     showgrid=True,
                     row=1,
                     col=1
                     )

    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_xaxes(title_text="Explanatory Variables", row=2, col=1)

    fig.update_yaxes(title_text="Happiness Score", row=1, col=1)
    fig.update_yaxes(title_text="Average Regional Value", row=2, col=1)

    fig.write_html("C:/Users/magnu/Documents/GitHub/moleseaau.github.io/docs/bars.html")
    fig.show()


bars()


def bubble():
    fig = go.Figure()

    for i in df15['Region'].unique():
        dfn = df15[df15['Region'] == i]
        size = dfn['Happiness Score']
        fig.add_trace(go.Scatter(x=dfn['Economy (GDP per Capita)'],
                                 y=dfn['Health (Life Expectancy)'],
                                 customdata=dfn['Country'],
                                 hovertemplate='<b>Region</b> : ' + dfn['Region'] +
                                               '<br><b>Country</b> : %{customdata}' +
                                               '<br><b>Happiness Score</b> : %{marker.size:.2f}<br>' +
                                               'X & Y values : %{x:.2f} , %{y:.2f}<extra></extra>',
                                 mode='markers',
                                 name=i,
                                 marker=dict(
                                     size=size,
                                     sizeref=2. * max(size) / (6. ** 2),
                                     opacity=0.8)
                                 ))

    fig.update_layout(
        title='Bubble Chart of World Happiness Report',
        xaxis_title='Country GDP',
        yaxis_title='Life Expectancy',
        legend_title='<b>Different Regions<b>',

        legend=dict({'itemsizing': 'constant'}, bordercolor="Black", borderwidth=2),

        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=0.1
        ),

        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        )
    )

    fig.add_annotation(dict(x=0.8,
                            y=1.1,
                            showarrow=False,
                            text='Size of Bubbles Corresponds to Happiness Score of the Country',
                            xref="x",
                            yref="paper"
                            ))

    #fig.write_html("C:/Users/magnu/Documents/GitHub/moleseaau.github.io/docs/bubble.html")
    fig.show()


#bubble()


def spatial():
    fig = go.Figure()

    fig.add_trace(go.Choropleth(
        customdata=df15.index,
        locations=df15['Country'],
        z=df15['Happiness Score'].astype(float),
        locationmode='country names',
        hovertemplate='<b>Country</b> : ' + df15['Country'] +
                      '<br><b>Happiness Rank</b> : %{customdata}' +
                      '<br><b>Happiness Score</b> : %{z:.2f}<extra></extra>',
        colorscale='Greens',
        zauto=True,
        zmid=avg_happy_score15,
        colorbar=dict(title='Happiness<br>Score',
                      x=0.89),
    ))

    fig.update_layout(
        title_text='Spatial Map of World Happiness Report'
    )

    fig.write_html("C:/Users/magnu/Documents/GitHub/moleseaau.github.io/docs/spatial.html")
    fig.show()


#spatial()
