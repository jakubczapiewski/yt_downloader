from django.contrib.sessions.middleware import SessionMiddleware


class DisableSessionMiddleware(SessionMiddleware):

    def process_response(self, request, response):
        response = super(DisableSessionMiddleware, self).process_response(request, response)
        try:
            cookie = [x for x in response.cookies]
            for x in cookie:
                del response.cookies[x]
        except:
            pass
        return response
