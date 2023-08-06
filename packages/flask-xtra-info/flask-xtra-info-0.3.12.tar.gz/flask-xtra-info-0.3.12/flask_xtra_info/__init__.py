# -*- coding: utf-8 -*-
#
#    ________________________________
#   /   ______________________   | \ \
#   |  /.--------------------.\  | | | 
#   |  ||                    ||  |_| |
#   |  ||  Xtra_info         ||  | | |
#   |  \'--------------------'|  | | |
#   |   \__<<__|__>>__|______/   |_/ |
#   |                          ____  |
#   |  """""""""""'''''      /'    `\|
#   \________________________\______//
#
#

from flask import request
from flask import g
from flask import current_app

import datetime
import logging
import time
import uuid
import sys

__version__ = '0.3.12'
__author__ = '@jthop'


DEFAULT_ACCESS_LOG = '{now} - {ip} - - "{method} {path}" {status_code}'


class XtraInfoExtension():
    """
    Simple Flask Extension to manage several tasks I was repeadidly 
    doing in every project.

    Request ID generation - Track your requests across multiple APIs
    Request ID parsing - Use request ids from other services (coming soon)
    Request timing - Log the total time spent processing the request
    Instance ID Generation - Identify different flask instances
    Insertion of these generated variables to logs - Comes with a log filter
    Automatic access Log style logging - Access log entry for each request
    More to come...
    """

    def __init__(self, app=None, instance_id=None, request_id_generator=None):
        """
        This is here for a traditional instantiation using:
        my_app = SwissArmyKnife(app)

        instance_id = String variable to identify this instance.  If none is
        provided we will generate one via a uuid4.

        request_id_generator = Callable to use for request id generation.
        If none is provided we will generate via uuid4.

        At this time we are not parsing request ids.

        :return: None
        """

        # Do basic initialization
        self._instance_id = instance_id
        if self._instance_id is None:
            self._instance_id = uuid.uuid4().hex[0:7]

        self._request_id_generator = request_id_generator
        if self._request_id_generator is None:
            self._request_id_generator = lambda: str(uuid.uuid4())

        self.app = app
        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        """
        This is here to support the app factory patterns.  Here there is 
        no self.app since multiple apps could be used and app context
        is never to be assumed.

        :return: None
        """

        # Setup the access-log
        self.access = logging.getLogger("access")
        self.access.propogate = False
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")
        ch.setFormatter(formatter)
        self.access.addHandler(ch)
        self.access.setLevel(logging.DEBUG)


        # Default configuration - probably doing this part wrong?
        app.config.setdefault('XTRA_GEN_REQUEST_ID', True)
        app.config.setdefault('XTRA_PARSE_REQUEST_ID', False)
        app.config.setdefault('XTRA_GEN_INSTANCE_ID', True)
        app.config.setdefault('XTRA_TIME_RESPONSE', True)
        app.config.setdefault('XTRA_CREATE_ACCESSLOG', True)
        app.config.setdefault('XTRA_INSERT_VERSION', True)

        app.config.setdefault('XTRA_ACCESSLOG_FMT', DEFAULT_ACCESS_LOG)
        app.config.setdefault('XTRA_REQUEST_ID_HEADER', 'X-Request-Id')
        app.config.setdefault('XTRA_INSTANCE_ID_HEADER', 'X-Instance-Id')
        app.config.setdefault('XTRA_RESPONSE_TIME_HEADER', 'X-Response-Time')
        app.config.setdefault('XTRA_VERSION_HEADER', 'X-App-Version')

        # Register before request callback
        @app.before_request
        def _before_req_callback():
            if current_app.config['XTRA_TIME_RESPONSE']:
                g.response_start_time = time.time() * 1000

            if current_app.config['XTRA_GEN_REQUEST_ID']:
                request_id = self._request_id_generator()
                g.request_id = request_id

            if current_app.config['XTRA_GEN_INSTANCE_ID']:
                g.instance_id = self._instance_id
                g.short_instance_id = self._instance_id[24:36]

        # Register after request logging
        @app.after_request
        def _after_req_callback(response):
            if current_app.config['XTRA_INSERT_VERSION']:
                _header = current_app.config['XTRA_VERSION_HEADER']
                response.headers[_header] = current_app.config.get('APP_VERSION', '1.0')

            if current_app.config['XTRA_GEN_REQUEST_ID']:
                _header = current_app.config['XTRA_REQUEST_ID_HEADER']
                response.headers[_header] = g.request_id

            if current_app.config['XTRA_GEN_INSTANCE_ID']:
                _header = current_app.config['XTRA_INSTANCE_ID_HEADER']
                response.headers[_header] = self._instance_id

            if current_app.config['XTRA_TIME_RESPONSE']:
                stop = time.time() * 1000
                t = round(stop - g.response_start_time, 1)
                g.response_time = f'{t} ms'
                _header = current_app.config['XTRA_RESPONSE_TIME_HEADER']
                response.headers[_header] = g.response_time

            # Auto access-log style logging
            if current_app.config['XTRA_CREATE_ACCESSLOG']:

                try:
                    l = current_app.config['XTRA_ACCESSLOG_FMT'].format(
                        now=datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'),
                        ip=request.remote_addr,
                        agent=request.user_agent.string,
                        method=request.method,
                        path=request.path,
                        status_code=response.status_code,
                        request_id=g.request_id,
                        instance_id=self._instance_id,
                        shorty=g.request_id[24:36]
                    )
                except KeyError as e:
                    app.logger.error(
                        f'access-log suspended.  unknown variable {e} in format')
                else:
                    self.access.info(l)

            return response


class XtraInfoLogFilter(logging.Filter):
    """
    Log all the attributes swiss army middleware is being used for.
    currently `log_record.response_time` and `log_record.request_id`
    and `log_record.instance_id`
    bonus is `log_record.shorty` This is a shorter version of the 
    request id if you want for stdout logs
    :return: modified log_record
    """

    def filter(self, log_record):
        default = '[null]'
        shorty = default
        if g.get('request_id'):
            shorty = g.request_id[24:36]
        log_record.response_time = g.get('response_time', default)
        log_record.request_id = g.get('request_id', default)
        log_record.shorty = shorty
        log_record.instance_id = g.get('instance_id', default)

        return log_record
