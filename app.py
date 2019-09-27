#!/usr/bin/env python3

# import connexion
#
# if __name__ == '__main__':
#     app = connexion.FlaskApp(__name__, port=8080, specification_dir='openapi/')
#     app.add_api('pychubby-api.yaml', arguments={'title': 'Pychubby Api'})
#     app.run()

import logging
import connexion
import os

logger = logging.getLogger('phchubby-api')

def healthz():
    logger.debug("healthz")
    return "OK"


app = connexion.FlaskApp(__name__,  port=8080, specification_dir='openapi/')
app.add_api('pychubby-api.yaml', arguments={'title': 'Pychubby Api'})

flask_app = app.app

# Add Basic health check
flask_app.add_url_rule('/', 'healthz', healthz)
flask_app.add_url_rule('/healthz', 'healthz', healthz)

if __name__ == '__main__':
    app.run(debug=True)

else:
    # Add Flask logs to gunicorn logs:
    # https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
    gunicorn_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers = gunicorn_logger.handlers
    flask_app.logger.setLevel(gunicorn_logger.level)

    # Add handlers for logger and format it:
    logger.handlers = gunicorn_logger.handlers
    formatter = logging.Formatter('%(asctime)s - %(name)14s - %(levelname)7s - %(threadName)-10s - %(message)s')

    for lh in logger.handlers:
        lh.setFormatter(formatter)

    logger.setLevel(gunicorn_logger.level)

    flask_app.logger.info("Run: connexion: {} flask_app: {} pid: {}".format(app, flask_app, os.getpid()))
    logger.info("Logger INFO message")
    logger.debug("Logger DEBUG message")