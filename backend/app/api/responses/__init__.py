def standard_response(
    data=None,
    status_code: int = 200,
    redirect_to_login: bool = False,
    excluded_keys=[
        "pagination",
        "meta",
        "rateLimit",
        "_links",
        "requestInfo",
        "debugInfo",
        "warnings",
        "locale",
        "timezone",
        "authToken",
    ],
    error=False,
    message="",
):
    if excluded_keys is None:
        excluded_keys = []

    response_template = {
        "message": message,
        "error": error,
        "redirect_to_login": redirect_to_login,
        "status_code": status_code,
        "data": data,
        "pagination": {
            "currentPage": None,
            "totalPages": None,
            "pageSize": None,
            "totalCount": None,
            "nextPage": None,
            "previousPage": None,
        },
        "meta": {"apiVersion": None, "responseTime": None, "fromCache": None},
        "rateLimit": {
            "limit": None,
            "remaining": None,
            "reset": None,
        },
        "warnings": [],
        "locale": None,
        "timezone": None,
        "authToken": None,
        "_links": {
            "self": None,
            "next": None,
            "previous": None,
        },
        "requestInfo": {},
        "debugInfo": {"stackTrace": None},
    }

    # Remove excluded keys
    for key in excluded_keys:
        response_template.pop(key, None)

    return response_template, status_code
