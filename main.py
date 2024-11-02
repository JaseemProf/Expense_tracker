from fasthtml.common import *
from datetime import datetime


app, route, expenses, Expense = fast_app(
    "data/expenses.db",
    category=str,
    amount=float,
    date=datetime,
    id=int,
    pk="id",
    live=True,
)


@route("/")
def get():
    entry_button = A(Button("Add entry"), href="/entry")
    return Titled("Expense tracker", entry_button)


@route("/entry")
def get():
    category_input = Select(
        Option("Grocery", value="grocery"),
        Option("Food", value="food"),
        Option("Others", value="others"),
        id="category",
    )

    amount_input = Input(
        placeholder="Amount", name="amount", type="number", required=True
    )

    # Date input field with current date as the default value
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_input = Input(placeholder="Date", name="date", type="date", value=current_date)

    submit_button = A(Button("Submit", cls="outline"))

    form = Form(
        category_input,
        amount_input,
        date_input,
        submit_button,
        method="POST",
        action="/add_entry",
    )
    return Titled(
        "Add Entry",
        form,
    )


@route("/add_entry")
def post(expense: Expense):  # type: ignore
    expenses.insert(expense)
    return P("Sucessfully added entry"), Meta(http_equiv="refresh", content="2; url=/")


serve()
