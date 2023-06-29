from django.shortcuts import redirect


def auth_middleware(get_response):
    # one-time config and init
    def middleware(request):
        print(request.session.get('customer'))
        returnurl = request.META['PATH_INFO']
        print(request.META['PATH_INFO'])
        if not request.session.get('customer'):
            return redirect(f'login?return_url={returnurl}')

        response = get_response(request)
        return response

    return middleware

