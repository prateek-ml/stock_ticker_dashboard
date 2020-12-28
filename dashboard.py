import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import os

os.environ["TIINGO_API_KEY"] = "ef3c2da7bd8ed93dcf7124f6cd1929638f61c50d"
app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.H3('Enter a stock symbol: '),
    dcc.Input(
        id = 'stock_picker',
        value = 'AAPL'
    ),
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
                [Input('stock_picker', 'value')])
def update_graph(stock_ticker):

    start_date = datetime(2017, 1, 1)
    end_date = datetime(2019, 4, 9)

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