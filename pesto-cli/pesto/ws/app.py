import sys

from pesto.common.utils import get_logger
import logging

# override sanic logger
from sanic.log import LOGGING_CONFIG_DEFAULTS

logging.Logger.manager.loggerDict["sanic.root"] = get_logger()
logging.Logger.manager.loggerDict["sanic.access"] = get_logger()
logging.Logger.manager.loggerDict["sanic.error"] = get_logger()
from sanic.server import  HTTPResponse

def my_log_response(self, response):
    if self.access_log:
        extra = {"status": getattr(response, "status", 0)}

        if isinstance(response, HTTPResponse):
            extra["byte"] = len(response.body)
        else:
            extra["byte"] = -1

        extra["host"] = "UNKNOWN"
        if self.request is not None:
            if self.request.ip:
                extra["host"] = "{0}:{1}".format(
                    self.request.ip, self.request.port
                )

            extra["request"] = "{0} {1}".format(
                self.request.method, self.request.url
            )
        else:
            extra["request"] = "nil"
        msg = "(sanic.access) [{}]: {} {} {}".format(extra['host'], extra['request'], extra['status'], extra['byte'])
        logging.getLogger("sanic.access").info(msg)

PESTO_LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        }
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
)
#default stdout hanlder for pesto incase if there is no call to init_looger(..) like codip
logging.config.dictConfig(PESTO_LOGGING_CONFIG_DEFAULTS)

from sanic import Sanic
from sanic.server import HttpProtocol
HttpProtocol.log_response = my_log_response
from sanic_openapi import swagger_blueprint, openapi_blueprint
from pesto.ws.v1 import v1

# Declare Sanic application
# configure_logging must be False as we are using PESTO_LOGGING_CONFIG_DEFAULTS

app = Sanic(__name__, configure_logging=False)

# API Configuration
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)
app.blueprint(v1)

app.config.API_VERSION = '1.0.0'
app.config.API_TITLE = 'GeoProcessing SDK API'
app.config.API_DESCRIPTION = 'GeoProcessing SDK API'
app.config.API_TERMS_OF_SERVICE = 'Apache 2.0'
app.config.API_PRODUCES_CONTENT_TYPES = ['application/json', 'mimetypes/jpeg', 'mimetypes/tiff']
app.config.API_CONTACT_EMAIL = 'tbd@airbus.com'

app.config.KEEP_ALIVE = False

TIMEOUT = 1_000_000
app.config.REQUEST_TIMEOUT = TIMEOUT
app.config.RESPONSE_TIMEOUT = TIMEOUT
app.config.KEEP_ALIVE_TIMEOUT = TIMEOUT


def main():
    app.run(host="0.0.0.0", port=8080, debug=False)


if __name__ == '__main__':
    main()
