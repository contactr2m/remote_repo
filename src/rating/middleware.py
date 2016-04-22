try:
    from hashlib import md5
except ImportError:
    from md5 import md5


class ratingMiddleware(object):
    def process_request(self, request):
        request.rating_token = self.generate_token(request)

    def generate_token(self, request):
        raise NotImplementedError


class ratingIpMiddleware(ratingMiddleware):
    def generate_token(self, request):
        return request.META['REMOTE_ADDR']


class ratingIpUseragentMiddleware(ratingMiddleware):
    def generate_token(self, request):
        s = ''.join((request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT']))
        return md5(s).hexdigest()
