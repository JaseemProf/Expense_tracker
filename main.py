from fasthtml.common import *
from datetime import datetime
import plotly.express as px
import pandas as pd

app, route, expenses, Expense = fast_app(
    "data/expenses.db",
    category=str,
    amount=float,
    date=str,
    id=int,
    pk="id",
    live=True,
)

setup_toasts(app)


@route("/")
def get():
    entry_button = A(Button("Add entry"), href="/entry")
    report_button = A(Button("Report"), href="/report")
    return Titled("Expense tracker", entry_button, " ", report_button)


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
def post(expense: Expense, session):  # type: ignore
    expenses.insert(expense)
    add_toast(session, f"Added Sucessfully", "success")
    return RedirectResponse("/", status_code=303)


def filter_by_date(date: str):
    query = f"date = '{date}'"  # this single quotes are important in order to
    print("query", query)
    return list(expenses.rows_where(where=query))


def generate_piechart(data):
    df = pd.DataFrame(data).drop("id", axis=1).rename(columns=str.capitalize)
    fig = px.pie(
        df,
        values="Amount",
        names="Category",
        hole=0.2,
        color="Category",
        color_discrete_map={
            "food": "royalblue",
            "grocery": "cyan",
            "others": "darkblue",
        },
    )
    # To diplay the chart in the browser
    return NotStr(fig.to_html(full_html=False))


@route("/report")
def get():
    date = datetime.now().strftime("%Y-%m-%d")
    filtered_data = filter_by_date(date)
    home_button = A(
        Button("Home"),
        href="/",
        style="position:absolute; left:10px; bottom:10px;",
    )
    return Titled(
        "Report",
        Div(
            generate_piechart(filtered_data),
            id="report-container",
        ),
        home_button,
    )


serve()
