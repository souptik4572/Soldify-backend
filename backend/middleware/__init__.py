from werkzeug.wrappers import Request, Response, ResponseStream

class AuthProtection():
    def __call__(self, environment, start_response):
        request = Request(environment)
        token = request.authorization
        print(token)
