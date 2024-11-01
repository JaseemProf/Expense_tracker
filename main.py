from fasthtml.common import *


app, route = fast_app(live=True)


@route("/")
def get():
    entry_button = A(Button("Add entry"), href="/entry")
    return Titled("Expense tracker", entry_button)


@route("/entry")
def get():
    back_button = A(Button("Back"), href="/")
    return Titled("Add entry", back_button)


serve()
