import os
import argparse
import shutil

from jinja2 import Environment, PackageLoader, select_autoescape

import app
from app.util import minify

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dest',help='destination directory for html')
args = parser.parse_args()

if os.path.exists(args.dest):
    shutil.rmtree(args.dest)

# static parts
shutil.copytree(os.path.join('app', 'static'),
                os.path.join(args.dest, 'static'),
                symlinks=False)

# dynamic parts
env = Environment(loader=PackageLoader('app','templates'),
                  autoescape=select_autoescape(['html', 'xml']))

def save(path, ret):
    template = env.get_template(ret.template)
    html = template.render(*ret.args, **ret.kwargs)
    dirname = os.path.dirname(os.path.join(args.dest, path))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(os.path.join(args.dest, path), 'w') as f:
        f.write(minify(html))

for r in app.routes:
    if len(r) == 2:
        path, handler = r
        ret = handler()
        save(path, ret)
    elif len(r) == 3:
        path, handler, handler_args = r
        for a in handler_args:
            p = path.replace('*', a)
            ret = handler(a)
            save(p, ret)
