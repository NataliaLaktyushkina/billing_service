# gevent - чтобы сделать Flask асинхронным
from gevent import monkey

monkey.patch_all()  # заменяет все I/O-операции на асинхронные

from gevent.pywsgi import WSGIServer  # noqa: E402
import sys  # noqa: E402
import os  # noqa: E402g

sys.path.append(os.path.dirname(__file__) + '/..')
from main import app  # noqa: E402

http_server = WSGIServer(('', 5001), app)
http_server.serve_forever()
