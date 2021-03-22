import os
import inspect

from webob import Request, Response
from parse import parse
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader

class API:
    """
    WSGI Compatible dummy function.
    __call__ called when creating instances of this class.
    """

    def __init__(self, templates_dir="templates"):
        """
            Dictionary used to store paths as keys and handlers as values.
        """
        self.routes = {}
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        
        return wrapper
    
    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            if inspect.isclass(handler):
                handler_function = getattr(handler(), request.method.lower(), None)
                if handler_function is None:
                    raise AttributeError("Method not allowed", request.method)
                handler_function(request, response, **kwargs)
            else:
                handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        
        return None, None

    """
    Setting up a test client using WSGI Transport Adapter for Requests
    """
    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}
        
        return self.templates_env.get_template(template_name).render(**context)