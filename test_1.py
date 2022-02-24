from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML



if __name__ == "__main__":
    data = {
        1: {
            'size': 1,
            'type': 'balance',
            'ticket': '01',
            'open_time': '01-01-2020',
            'COMMENT': 'test test',
            'tradepl': 123
        },
        2: {
            'size': 2,
            'type': 'buy limit',
            'ticket': '02',
            'open_time': '01-01-2020',
            'size': 20,
            'item': 200,
            'open_price': 15,
            'sl': 10,
            'tp': 5,
            'COMMENT': 'test test'
        },
        3: {
            'size': 2,
            'type': 'buy',
            'ticket': '02',
            'open_time': '01-01-2020',
            'size': 20,
            'item': 200,
            'open_price': 15,
            'sl': 10,
            'tp': 5,
            'COMMENT': 'test test',
            'close_time': '02-01-2020',
            'close_price': 20,
            'commission': 10,
            'swap': 20,
            'tradepl': 100,
        },
    }
    env = Environment(loader=FileSystemLoader('.'), extensions=['jinja2.ext.do'])
    template = env.get_template("index.html")

    comm, swap, tradepl = 0.0, 0.0, 0.0
    for value in data.values():
        if value['type'] not in ["buy limit", "sell limit", "buy stop", "sell stop", "balance", "credit"]:
            comm += value['commission']
            swap += value['swap']
            tradepl += value['tradepl']

    template_vars = {
        "table" : data,
        "comm": comm,
        "swap": swap,
        "tradepl": tradepl,
        }

    # Render our file and create the PDF using our css style file
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf('test.pdf', stylesheets=["style.css"])
