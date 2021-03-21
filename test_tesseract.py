import pytest

from api import API

def test_basic_routing_addition(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"

def test_tesseract_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT

def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"
    
    assert client.get("http://testserver/pankaj").text == "hey pankaj"
    assert client.get("http://testserver/kumar").text == "hey kumar"

def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")
    assert response.status_code == 404
    assert response.text == "Not found."

def test_class_based_handler_get(api, client):
    response_text = "this is a get request"

    @api.route("/book")
    class BooksResource:
        def get(self, req, resp):
            resp.text = response_text

    assert client.get("http://testserver/book").text == response_text

def test_class_based_handler_post(api, client):
    response_text = "this is a post request"

    @api.route("/book")
    class BooksResource:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post("http://testserver/book").text == response_text

def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/book")
    class BooksResource:
        def post(self, req, resp):
            resp.text = "yolo"

    with pytest.raises(AttributeError):
        client.get("http://testserver/book")