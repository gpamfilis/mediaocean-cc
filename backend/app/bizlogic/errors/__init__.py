import logging
import traceback

from sqlalchemy.exc import IntegrityError

from app.api.responses import standard_response

logger = logging.getLogger(__name__)


class EnvironmentVariableError(Exception):
    pass


class NotFoundError(Exception):
    pass


class BadRequestError(Exception):
    pass


def init_errors(app):
    @app.errorhandler(409)
    def conflict_error(error):
        logger.error(error)
        traceback.print_exc()
        return standard_response(
            message="Conflict",
            error=True,
            status_code=409,
        )

    @app.errorhandler(NotFoundError)
    def resource_not_found_error(error):
        return standard_response(error=True, status_code=404, message=str(error))

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        msg = str(error)
        logger.error(error)
        return standard_response(
            message=msg,
            error=True,
            status_code=409,
        )

    @app.errorhandler(500)
    def server_error(error):
        logger.error(error)
        return standard_response(error=True, status_code=500, message=str(error))
