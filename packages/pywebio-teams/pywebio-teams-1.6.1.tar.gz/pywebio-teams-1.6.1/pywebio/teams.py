import base64
import json
import os

from tornado.web import decode_signed_value

from pywebio.output import *
from pywebio.output import Output
from pywebio.output import OutputPosition
from pywebio.utils import random_str

_serial = None
_config = {}


def config():
    return _config


def register(serial, config):
    """Register the teams version

    :param str serial: Register serial
    :param dict config: Capability configuration for teams version
     * footer: bool, whether to show the footer.
    :return: Return your brand name if register succeed, else ``None`` will be returned
    """
    global _serial, _config
    brand_name = biz_brand(serial)
    if brand_name:
        _serial = serial
        _config = config
        return brand_name


def biz_brand(serial=None):
    token = serial or os.environ.get('PYWEBIO_SERIAL')
    if not token:
        return False
    token = base64.b64decode(token)
    name = decode_signed_value("pywebio", "PYWEBIO", token, max_age_days=366)
    if not name:
        return False

    return name.decode('utf8')


try:
    from pandas import DataFrame
except ImportError:
    DataFrame = type('MockDataFrame', (), dict(__init__=None))


def put_datatable(tdata, header=None, scope=None, position=OutputPosition.BOTTOM, **extra_props) -> Output:
    """Output datatable

    The ``tdata`` and ``header`` arguments have the same meaning as for `pywebio.output.put_table()` except that
    the table cell can't be ``put_xxx()`` call.

    Also, the ``tdata`` can be a pandas DataFrame, if so, the ``header`` parameter will be ignored.

    :param extra_props: extra properties passed to the underlying
       `react data table component <https://github.com/jbetancur/react-data-table-component>`_ .
       See: https://react-data-table-component.netlify.app/?path=/docs/api-props--page
    """
    index = []
    if isinstance(tdata, DataFrame):
        data = tdata.to_dict('split')
        tdata, header, index = data['data'], data['columns'], data['index']

    if not tdata:
        return put_text('Empty datatable')

    # Change ``dict`` row table to list row table
    if isinstance(tdata[0], dict):
        if isinstance(header[0], (list, tuple)):
            header_ = [h[0] for h in header]
            order = [h[-1] for h in header]
        else:
            header_ = order = header

        tdata = [
            [row.get(k, '') for k in order]
            for row in tdata
        ]
        header = header_
    else:
        tdata = [list(i) for i in tdata]  # copy data

    if not header:
        header, tdata = tdata[0], tdata[1:]

    dom_id = random_str(10)
    html = """
    <div id="react-app-%s">⌛Loading datatable️</div>
    <script type="module">
        let header=%s, data=%s, extra_props=%s, index=%s, dom_id=%s;

        import React from "https://esm.sh/react";
        import ReactDOM from "https://esm.sh/react-dom";
        import DataTable from "https://esm.sh/react-data-table-component"

        data = data.map((value, idx) => {
            let row = {};
            for (let idx in header)
                row[header[idx]] = value[idx];
            if (index.length)
                row['__pd_index__'] = index[idx];
            return row;
        })
        let columns = header.map((value) => ({
            "name": value,
            "selector": (row) => row[value],
            "sortable": true,
            "reorder": true
        }))
        if(index.length){
            columns.splice(0, 0, {
                "name": '',
                "selector": (row) => row['__pd_index__'],
                "sortable": true,
            });
        }
        ReactDOM.render(React.createElement(DataTable, {
            "columns": columns,
            "data": data,
            "pagination": true,
            "dense":true,
            ...extra_props
        }), document.getElementById("react-app-"+dom_id));
    </script>
    """ % (dom_id, json.dumps(header), json.dumps(tdata), json.dumps(extra_props), json.dumps(index), repr(dom_id))

    return put_html(html, scope=scope, position=position)
