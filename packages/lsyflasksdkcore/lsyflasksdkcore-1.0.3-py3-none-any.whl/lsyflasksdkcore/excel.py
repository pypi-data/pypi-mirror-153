# -*- coding: utf-8 -*-

import copy
import datetime
import functools
import io
import json
import os
from typing import Callable, Type

import xlrd as xlrd
import xlwt
from flask import current_app, make_response, request
from werkzeug.exceptions import InternalServerError
from xlutils.copy import copy

from .exceptions import ExcelExportError
from .schema import Schema


def _get_content_style():
    style = xlwt.easyxf(
        'font: bold 0, colour_index 0; align: wrap on, vert center, horz general; border: left thin,'
        ' right thin, top thin, bottom thin')
    return style


def _get_title_style():
    style = xlwt.easyxf(
        'font: bold 1, colour_index 0, height 350; align: wrap on, vert center, horz center')
    return style


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


def export_temp_xls(out_filename, temp_filename, data, start_row=2, start_col=0, sheet_index=0):
    """
    根据模板导入到xls
    :param out_filename: 输出文件
    :param temp_filename: 模板文件
    :param data:数据
    :param start_row: 开始行从0开始
    :param start_col: 开始列从0开始
    :param sheet_index: 开始sheet
    :return:
    """
    try:
        config = current_app.config
        excel_template_path = config.get('EXCEL_TEMPLATE_PATH')

        path = os.path.join(excel_template_path, temp_filename).replace('\\', '/').replace('//', '/')
        rb = xlrd.open_workbook(path, formatting_info=True)
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


def excelresponse(schema_class: Type[Schema], to_excel: Callable):
    """
    return result excelResponse.
    """

    def _excelresponse(fn):
        @functools.wraps(fn)
        def __excelresponse(*args, **kwargs):
            response = fn(*args, **kwargs)
            if request.content_type == 'application/excel':
                try:
                    lst = response.json.get('data', None)
                    schema: Schema = schema_class()
                    fields = schema.fields

                    columns = [(name, field.metadata.get("excel_colx", None),) for name, field in fields.items() if
                               field.metadata.get("excel_colx", None) is not None]
                    columns.sort(key=lambda x: int(x[1]))
                    rows = [[item.get(col[0], None) for col in columns] for item in lst]
                    return to_excel(rows)
                except Exception as ex:
                    raise InternalServerError()
            return response

        return __excelresponse

    return _excelresponse


def cvsresponse(output_filename):
    def _cvsresponse(fn):
        def __cvsresponse(*args, **kwargs):
            response = fn(*args, **kwargs)
            if request.content_type == 'application/excel':
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
                    row = [item[key] for key in keys]
                    rows.append(row)
                return export_xls(output_filename, headers, rows)

            return response

        return __cvsresponse

    return _cvsresponse
