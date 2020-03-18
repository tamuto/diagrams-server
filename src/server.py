import urllib
import ast
import uuid
import mimetypes
from yapf.yapflib.yapf_api import FormatCode
from flask import Flask, request, send_file

from diagrams import Diagram

from diagrams.onprem.analytics import *
from diagrams.onprem.ci import *
from diagrams.onprem.client import *
from diagrams.onprem.compute import *
from diagrams.onprem.container import *
from diagrams.onprem.database import *
from diagrams.onprem.gitops import *
from diagrams.onprem.inmemory import *
from diagrams.onprem.logging import *
from diagrams.onprem.monitoring import *
from diagrams.onprem.network import *
from diagrams.onprem.queue import *
from diagrams.onprem.search import *
from diagrams.onprem.security import *
from diagrams.onprem.workflow import *

from diagrams.aws.analytics import *
from diagrams.aws.compute import *
from diagrams.aws.database import *
from diagrams.aws.devtools import *
from diagrams.aws.engagement import *
from diagrams.aws.integration import *
from diagrams.aws.iot import *
from diagrams.aws.management import *
from diagrams.aws.migration import *
from diagrams.aws.ml import *
from diagrams.aws.network import *
from diagrams.aws.security import *
from diagrams.aws.storage import *


app = Flask(__name__)


class DiagramTransformer(ast.NodeTransformer):
    def __init__(self, fmt, filename):
        self.fmt = fmt
        self.filename = filename

    def visit_Call(self, node):
        if node.func.id == 'Diagram':
            fmtFlag = False
            fnameFlag = False
            print(ast.dump(node))
            for k in node.keywords:
                if k.arg == 'outformat':
                    k.value.value = self.fmt
                    fmtFlag = True
                if k.arg == 'filename':
                    k.value.value = self.filename
                    fnameFlag = True
            
            if fmtFlag == False:
                node.keywords.append(ast.keyword(arg='outformat', value=ast.Constant(value=self.fmt, kind=None)))
            
            if fnameFlag == False:
                node.keywords.append(ast.keyword(arg='filename', value=ast.Constant(value=self.filename, kind=None)))
            
        return node


@app.route('/')
def root():
    return to_image('svg')


@app.route('/<fmt>')
def to_image(fmt='svg'):
    filename = '../work/' + str(uuid.uuid4())
    source = FormatCode(urllib.parse.unquote(request.query_string.decode()))
    code = ast.fix_missing_locations(DiagramTransformer(fmt, filename).visit(ast.parse(source[0])))
    exec(compile(code, '<string>', mode='exec', flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT))

    return send_file('{fname}.{ext}'.format(fname=filename, ext=fmt), mimetype=mimetypes.guess_extension(fmt))


@app.route('/usr/local/lib/python3.8/site-packages/resources/<path:filename>')
def resources(filename):
    return send_file('/usr/local/lib/python3.8/site-packages/resources/' + filename)


app.run(host='0.0.0.0', port=80)
