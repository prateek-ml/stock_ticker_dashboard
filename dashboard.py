import dash
import dash_core_components as dcc
import dash_html_components as html

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
            ]
        )
    )
])

if __name__ == "__main__":
    app.run_server()