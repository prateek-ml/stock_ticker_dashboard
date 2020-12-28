from time import strftime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import pandas_datareader.data as web
from datetime import date, datetime
import os

os.environ["TIINGO_API_KEY"] = "ef3c2da7bd8ed93dcf7124f6cd1929638f61c50d"
app = dash.Dash()

nsdq = pd.read_csv('nasdaq_listed.csv', index_col=0)
nsdq_opts = []

for tick in nsdq.index:
    tick_dict = {}
    tick_dict['label'] = str(nsdq.loc[tick]['Company Name'] + ' ' + tick)
    tick_dict['value'] = tick
    nsdq_opts.append(tick_dict)


app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Enter a stock symbol: ', style = {'paddingRight' : '30px'}),
        dcc.Dropdown(
            id = 'stock_picker',
            options = nsdq_opts,
            value = ['GOOGL'],      #Sets a default value
            multi = True
        )], style = {'display' : 'inline-block', 
                    'verticalAlign' : 'top',
                    'width' : '30%'}
    ),

    html.Div([html.H3('Select a start and an end date'),
                dcc.DatePickerRange(
                    id = 'date_picker',
                    min_date_allowed = datetime(2000, 1, 1),
                    max_date_allowed = datetime(2020, 1, 1),
                    start_date = datetime(2020, 1, 1),
                    end_date = datetime.today()
        )], style = {'display' : 'inline-block'}
    ),

    html.Div([
        html.Button(
            id = 'submit_btn',
            n_clicks = 0,
            children = "Submit",
            style = {'fontSize' : 24,
                     'marginLeft' : '30px'}
        )
    ], style = {'display' : 'inline-block'}),

    dcc.Graph(
        id = 'stock_price_graph',
        figure = dict(
            data = [
                {'x' : [1,2], 'y' : [3, 1]}
            ], 
            layout = {'title' : 'Historical Stock Prices Data Graph'}
        )
    )
])

@app.callback(Output('stock_price_graph', 'figure'),
                [Input('submit_btn', 'n_clicks')],
                [State('stock_picker', 'value'),
                 State('date_picker', 'start_date'),
                 State('date_picker', 'end_date')])
def update_graph(n_clicks, stock_picker, start_date, end_date):
    start_date = datetime.strptime(start_date[:10], "%Y-%m-%d")
    end_date = datetime.strptime(end_date[:10], "%Y-%m-%d")

    traces = []
    for tick in stock_picker:
        df = web.get_data_tiingo(
            symbols = tick,
            start = start_date,
            end = end_date
        )

        df[['symbol', 'date']] = pd.DataFrame(df.index.tolist(), index = df.index)
        traces.append({
            'x' : df.date, 
            'y' : df.close, 
            'name' : tick})

    fig = dict(
        data = traces,
        layout = {'title' : "Stock Prices between "+
                    str(start_date.strftime('%b %d %Y'))+" and "+str(end_date.strftime('%b %d %Y'))}
    )

    return fig

if __name__ == "__main__":
    app.run_server()