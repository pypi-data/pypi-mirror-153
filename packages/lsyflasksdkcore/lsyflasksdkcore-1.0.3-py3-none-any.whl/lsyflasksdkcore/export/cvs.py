import io
import json
import typing

import xlwt
from flask import request, make_response
from werkzeug.exceptions import InternalServerError


def export_xls(output_file_name, head_cols, data_rows):
    """
    根据数据生成xls
    :param output_file_name: 输出文件名
    :param head_cols: 表头数组
    :param data_rows: 数据行
    :return:
    """
    encoding = 'utf-8'

    book = xlwt.Workbook(encoding=encoding)
    sheet = book.add_sheet(output_file_name)

    font1 = xlwt.Font()
    font1.colour_index = 2
    font1.bold = True

    bordesr = xlwt.Borders()
    bordesr.left = xlwt.Borders.THIN
    bordesr.top = xlwt.Borders.THIN
    bordesr.right = xlwt.Borders.THIN
    bordesr.bottom = xlwt.Borders.THIN
    bordesr.left_colour = 0x08
    bordesr.top_colour = 0x08
    bordesr.right_colour = 0x08
    bordesr.bottom_colour = 0x08

    style1 = xlwt.Style.default_style
    style1.borders = bordesr

    for col_index, col in enumerate(head_cols):
        sheet.write(0, col_index, col, style=style1)
        sheet.col(col_index).width = 5000

    for row_index, row in enumerate(data_rows):
        for col_index in range(len(row)):
            value = row[col_index]
            sheet.write(row_index + 1, col_index, value, style=style1)

    output = io.BytesIO()
    book.save(output)
    output.seek(0)

    resp = make_response(output.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=testing.xls"
    resp.headers['Content-Type'] = 'application/x-xls'
    return resp


class CvsResponse(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not self.app:
            self.app = app

    def response(self, output_filename: str, row_hander: typing.Callable = None):
        def _cvsresponse(fn):
            def __cvsresponse(*args, **kwargs):
                response = fn(*args, **kwargs)
                if request.content_type == 'application/excel':
                    try:
                        lst = response.json.get('data', None)
                        query = json.loads(request.data)
                        body = query.get("body", {})
                        columns = body.get('excelFields', None)

                        headers = []
                        keys = []
                        for item in columns:
                            headers.append(item['title'])
                            keys.append(item['key'])

                        rows = []
                        for item in lst:
                            if row_hander:
                                item = row_hander(item)
                            row = [item[key] for key in keys]
                            rows.append(row)
                        return export_xls(output_filename, headers, rows)
                    except Exception as ex:
                        raise InternalServerError()

                return response

            return __cvsresponse

        return _cvsresponse
