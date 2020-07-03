import json

from django.http import JsonResponse

from rest_framework.response import Response

from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camelize, underscoreize


class CamelCaseMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.GET = underscoreize(
            request.GET,
            **api_settings.JSON_UNDERSCOREIZE
        )

        response = self.get_response(request)

        if isinstance(response, JsonResponse):
            content = response._container[0]
            data = json.loads(content)
            content = json.dumps(camelize(
                data,
                **api_settings.JSON_UNDERSCOREIZE
            )).encode('utf-8')
            response._container = [content]

            # It would be nice to build a
            # JsonResponse(data=data, status=response.status_code)
            # and then response.render()

        return response
