import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from pandas.io.formats import style
import pandas_datareader.data as web
from datetime import date, datetime
import os

os.environ["TIINGO_API_KEY"] = "ef3c2da7bd8ed93dcf7124f6cd1929638f61c50d"
app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Enter a stock symbol: ', style = {'paddingRight' : '30px'}),
        dcc.Input(
            id = 'stock_picker',
            value = 'AAPL',
            style = {'fontSize' : 24, 'width' : 75}      #Sets a default value
        )], style = {'display' : 'inline-block', 
                    'verticalAlign' : 'top'}
    ),

    html.Div([html.H3('Select a start and an end date'),
                dcc.DatePickerRange(
                    id = 'date_picker',
                    min_date_allowed = datetime(2000, 1, 1),
                    max_date_allowed = datetime.today(),
                    start_date = datetime(2018, 1, 1),
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
            layout = {'title' : 'Default Title'}
        )
    )
])

@app.callback(Output('stock_price_graph', 'figure'),
                [Input('submit_btn', 'n_clicks')],
                [State('stock_picker', 'value'),
                 State('date_picker', 'start_date'),
                 State('date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):

    start_date = datetime.strptime(start_date[:10], "%Y-%m-%d")
    end_date = datetime.strptime(end_date[:10], "%Y-%m-%d")

    df = web.get_data_tiingo(
        symbols = stock_ticker,
        start = start_date,
        end = end_date,
        freq = "day"
    )

    df[['symbol', 'date']] = pd.DataFrame(df.index.tolist(), index = df.index)

    fig = dict(
        data = [{'x' : df.date, 'y' : df.close}],
        layout = {'title' : stock_ticker}
    )

    return fig

if __name__ == "__main__":
    app.run_server()