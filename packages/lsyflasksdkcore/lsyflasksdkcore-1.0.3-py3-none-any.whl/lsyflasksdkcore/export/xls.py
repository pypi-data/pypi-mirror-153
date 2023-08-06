import datetime
import functools
import io
import os
import typing

import xlrd
import xlwt
from flask import request, make_response
from werkzeug.exceptions import InternalServerError
from xlutils.copy import copy

from lsyflasksdkcore.exceptions import ExcelExportError
from lsyflasksdkcore.schema import Schema


def _get_content_style():
    style = xlwt.easyxf(
        'font: bold 0, colour_index 0; align: wrap on, vert center, horz general; border: left thin,'
        ' right thin, top thin, bottom thin')
    return style


def _get_title_style():
    style = xlwt.easyxf(
        'font: bold 1, colour_index 0, height 350; align: wrap on, vert center, horz center')
    return style


def export_temp_xls(out_filename, temp_filepath, data, start_row=2, start_col=0, sheet_index=0):
    """
    根据模板导入到xls
    :param out_filename: 输出文件
    :param temp_filepath: 模板文件
    :param data:数据
    :param start_row: 开始行从0开始
    :param start_col: 开始列从0开始
    :param sheet_index: 开始sheet
    :return:
    """
    try:
        rb = xlrd.open_workbook(temp_filepath, formatting_info=True)
        wb = copy(rb)

        w_sheet = wb.get_sheet(sheet_index)
        w_sheet.write(0, 0, out_filename, _get_title_style())
        w_sheet.name = out_filename

        style = _get_content_style()
        if data:
            for rowx, row in enumerate(data):
                for colx, value in enumerate(row):
                    if isinstance(value, datetime.datetime):
                        style.num_format_str = 'yyyy-mm-dd hh:mm:ss'
                    elif isinstance(value, datetime.date):
                        style.num_format_str = 'yyyy-mm-dd'
                    elif isinstance(value, datetime.time):
                        style.num_format_str = 'hh:mm:ss'
                    elif isinstance(value, float):
                        style.num_format_str = '#,##0.00'
                    elif isinstance(value, int):
                        style.num_format_str = '0'
                    else:
                        style.num_format_str = u'General'
                    w_sheet.write(start_row + rowx, start_col + colx, value, style)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=testing.xls"
        resp.headers['Content-Type'] = 'application/x-xls'
        return resp
    except Exception as ex:
        raise ExcelExportError(ex)


class XlsResponse(object):
    def __init__(self, app=None):
        self.app = app
        self.excel_template_path = ""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not self.app:
            self.app = app

        if not app.config.get("EXCEL_TEMPLATE_PATH", None):
            raise Exception("EXCEL_TEMPLATE_PATH NOT IN CONFIG")

        self.excel_template_path = app.config.get("EXCEL_TEMPLATE_PATH")

    def response(self, schema_class: typing.Type[Schema], output_filename: str,
                 temp_filename: str, row_hander: typing.Callable = None, start_row=2, start_col=0, sheet_index=0):
        def _excelresponse(fn):
            @functools.wraps(fn)
            def __excelresponse(*args, **kwargs):
                response = fn(*args, **kwargs)
                if request.content_type == 'application/excel':
                    try:
                        lst = response.json.get('data', None)
                        schema: Schema = schema_class()
                        fields = schema.fields

                        if row_hander:
                            pass

                        columns = [(name, field.metadata.get("excel_colx", None),) for name, field in fields.items() if
                                   field.metadata.get("excel_colx", None) is not None]
                        columns.sort(key=lambda x: int(x[1]))
                        rows = [[item.get(col[0], None) for col in columns] for item in lst]

                        temp_path = os.path.join(self.excel_template_path, temp_filename).replace('\\', '/'). \
                            replace('//', '/')
                        return export_temp_xls(output_filename, temp_path, rows,
                                               start_row, start_col, sheet_index)
                    except Exception as ex:
                        raise InternalServerError()
                return response

            return __excelresponse

        return _excelresponse
