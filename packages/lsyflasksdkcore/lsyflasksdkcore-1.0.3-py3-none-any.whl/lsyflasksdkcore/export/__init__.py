from .cvs import CvsResponse
from .xls import XlsResponse

cvs = CvsResponse()
xls = XlsResponse()


def init_excel(app):
    cvs.init_app(app)
    xls.init_app(app)
