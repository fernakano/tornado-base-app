#! /usr/bin/env python
# *-* coding: utf8 *-*
import yaml
import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.options
import tornado.autoreload
import tornado.httpclient
import tornado.websocket
from tornado.options import define, options

__config__ = 'app.yaml'

define('version', default=None, help='Version settings (default: production)')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class App(tornado.web.Application):
    def __init__(self, settings):
        handlers = [
            (r'/', MainHandler),
            (r'/websocket', SocketHandler),
        ]

        tornado.web.Application.__init__(
            self,
            handlers,
            **settings
        )


class BaseHandler(tornado.web.RequestHandler):
    pass


class MainHandler(BaseHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render('index.html', title="My title", items=items)


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        print(origin + " Opened connection")
        return True


class SocketHandler(BaseWebSocketHandler):
    def open(self):
        self.write_message("Websocket opened ")
        print("Websocket opened")

    def on_message(self, message):
        self.write_message(u"Thanks For Your Message: " + message)

    def on_close(self):
        print("Websocket closed")


if __name__ == '__main__':
    tornado.options.parse_command_line()

    # Try to load the Configuration File, If itis not Present Throw an Error.
    try:
        f = open(__config__, 'r')
        config = yaml.load(f)
        f.close()
    except IOError:
        print('Invalid or missing config file %s' % __config__)
    else:
        # if no settings is present in the file, we go away
        if 'settings' not in config:
            print('No default configuration found')
            sys.exit(1)

        # Check Environment option is setup.
        if options.version and options.version in config['extra_settings']:
            settings = dict(
                config['settings'],
                **config['extra_settings'][options.version]
            )
        else:
            settings = config['settings']

        # Set Base Path for configured directories
        for k, v in settings.items():
            if k.endswith('_path'):
                settings[k] = settings[k].replace(
                    '__path__',
                    os.path.dirname(__file__)
                )

        http_server = tornado.httpserver.HTTPServer(App(settings))
        http_server.listen(config['port'])

        # Set Debug mode ON.
        if 'debug' in settings and settings['debug'] is True:
            tornado.autoreload.start()
        tornado.ioloop.IOLoop.instance().start()
