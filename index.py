from wsgi import app

from http import HTTPStatus

def handler(request, response):
    # Your code here
    response.status_code = HTTPStatus.OK
    response.text = "Hello, Vercel!"
