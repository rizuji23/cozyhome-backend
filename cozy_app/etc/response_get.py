from django.http import JsonResponse

RESPONSES = {
    200: {
        'status_code': 200,
        'status': True,
        'message': 'Request Success.',
        'data': None
    },
    201: {
        'status_code': 201,
        'status': True,
        'message': 'Request Created.'
    },
    400: {
        'status_code': 400,
        'status': False,
        'message': 'Validation Failed.',
        'detail_message': None,
        'data': None
    },
    401: {
        'status_code': 401,
        'status': False,
        'message': 'Unauthorized Request.',
        'detail_message': None,
        'data': None
    },
    403: {
        'status_code': 403,
        'status': False,
        'message': 'Forbidden Request.',
        'detail_message': None,
        'data': None
    },
    404: {
        'status_code': 404,
        'status': False,
        'message': 'Resource Not Found.',
        'detail_message': None,
        'data': None
    },
    422: {
        'status_code': 422,
        'status': False,
        'message': 'Unprocessable Entity',
        'detail_message': None,
        'data': None
    },
    500: {
        'status_code': 500,
        'status': False,
        'message': 'Internal Server Error.',
        'detail_message': None,
        'data': None
    }
}

def response(code=200, data=None, detail_message=None):
    response = {**RESPONSES[code], 'data': data, 'detail_message': detail_message}
    return JsonResponse(response, status=code, safe=False)

