from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from api.settings import REQUEST_ID_RESPONSE_HEADER


def custom_exception_handler(exc, context):
    # TODO: handle 404 not found route
    response = exception_handler(exc, context)

    if response is not None:
        request_id = context["request"].id

        custom_response = Response(
            {
                "title": response.status_text,
                "status": response.status_code,
            },
            status=response.status_code,
            headers=response.headers,
        )

        if request_id:
            custom_response[REQUEST_ID_RESPONSE_HEADER] = request_id
            custom_response.data["id"] = request_id

        if isinstance(exc, ValidationError):
            custom_response.data["detail"] = "Validation Error"
            custom_response.data["errors"] = response.data

            return custom_response

        if isinstance(exc, APIException):
            custom_response.data.update(response.data)
            return custom_response

    return response
