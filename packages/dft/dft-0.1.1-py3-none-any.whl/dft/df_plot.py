"""
Why only static method?

Why global state?

"""
df_chart_config = []

"""
Reset should be called primarily in the context of unittest to avoid race condition
 as chart_config is a global variable for this class.
"""


def reset():
    global df_chart_config
    df_chart_config = []


def bar_chart(name, x, y, data):
    df_chart_config.append({
        'kind': 'bar',
        'name': name,
        'options': {
            'x': x,
            'y': y,
            'data': data
        }
    })


def scatter_chart(name, x, y, data):
    df_chart_config.append({
        'kind': 'scatter',
        'name': name,
        'options': {
            'x': x,
            'y': y,
            'data': data
        }
    })


def pie_chart(name, legends, y, data):
    df_chart_config.append({
        'kind': 'pie',
        'name': name,
        'options': {
            'y': y,
            'legends': legends,
            'data': data
        }
    })


def line_chart(name, x, y, data):
    df_chart_config.append({
        'kind': 'line',
        'name': name,
        'options': {
            'x': x,
            'y': y,
            'data': data
        }
    })


def single_value(name, value, variation=None):
    df_chart_config.append({
        'kind': 'single_value',
        'name': name,
        'options': {
            'value': value,
            'variation': variation
        }
    })


def segment_line_chart(name, x, y, segments, data):
    df_chart_config.append({
        'kind': 'segment',
        'name': name,
        'options': {
            'x': x,
            'y': y,
            'segments': segments,
            'data': data
        }
    })


def time_series_forecast(name, forecasted_rows, data):
    df_chart_config.append({
        'kind': 'time_series',
        'name': name,
        'options': {
            'forecasted_rows': forecasted_rows,
            'data': data
        }
    })
