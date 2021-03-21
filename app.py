from api import API

"""
Entrypoint for gunicorn
"""
app = API()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME Page"

@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT Page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello ,{name}"

@app.route("/tell/{age:d}")
def age(request, response, age):
    response.text = f"Age is {age}"

@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, response, num_1, num_2):
    total = int(num_1) + int(num_2)
    response.text = f"{num_1} + {num_2} = {total}"

@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    def put(self, req, resp):
        resp.text = "Update request

    def delete(self, req, resp):
        resp.text = "Delete request"