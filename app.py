import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
from collections import defaultdict
import csv
import io

# Page settings
st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Monthly Expense Tracker")

# Session state
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------------- ADD EXPENSE ----------------

st.subheader("Add Expense")

expense_date = st.date_input("Select Date", date.today())

category = st.selectbox(
    "Select Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment"]
)

amount = st.number_input(
    "Enter Amount",
    min_value=0
)

note = st.text_input("Description")

# Add button
if st.button("Add Expense"):

    expense = {
        "Date": str(expense_date),
        "Month": expense_date.strftime("%B"),
        "Year": expense_date.strftime("%Y"),
        "Category": category,
        "Amount": amount,
        "Note": note
    }

    st.session_state.expenses.append(expense)

    st.success("Expense Added Successfully!")

# ---------------- DISPLAY EXPENSES ----------------

if st.session_state.expenses:

    st.subheader("Expense Records")

    # Month filter
    months = list(set(
        expense["Month"]
        for expense in st.session_state.expenses
    ))

    selected_month = st.selectbox(
        "Filter by Month",
        ["All"] + months
    )

    total = 0

    # Display expenses
    for i, expense in enumerate(st.session_state.expenses):

        if (
            selected_month == "All"
            or expense["Month"] == selected_month
        ):

            st.markdown("---")

            st.write(f"📅 Date: {expense['Date']}")
            st.write(f"📂 Category: {expense['Category']}")
            st.write(f"💵 Amount: ₹{expense['Amount']}")
            st.write(f"📝 Note: {expense['Note']}")

            total += expense["Amount"]

            # Delete button
            if st.button(f"Delete Expense {i}"):

                st.session_state.expenses.pop(i)

                st.rerun()

    # Total expense
    st.markdown("---")

    st.subheader(f"Total Expense: ₹{total}")

    # ---------------- PIE CHART ----------------

    st.subheader("Category Wise Expense Chart")

    category_total = defaultdict(int)

    for expense in st.session_state.expenses:

        if (
            selected_month == "All"
            or expense["Month"] == selected_month
        ):

            category_total[
                expense["Category"]
            ] += expense["Amount"]

    labels = list(category_total.keys())

    values = list(category_total.values())

    fig, ax = plt.subplots()

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    # ---------------- YEARLY ANALYSIS ----------------
    # ---------------- ANALYSIS FILTER ----------------

st.subheader("Analysis")

analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Monthly", "Yearly"]
)

# ---------------- MONTHLY ANALYSIS ----------------

if analysis_type == "Monthly":

    monthly_total = defaultdict(int)

    for expense in st.session_state.expenses:

        monthly_total[
            expense["Month"]
        ] += expense["Amount"]

    st.subheader("Monthly Expense Analysis")

    for month, amount in monthly_total.items():

        st.write(f"📅 {month} : ₹{amount}")

# ---------------- YEARLY ANALYSIS ----------------

elif analysis_type == "Yearly":

    yearly_total = defaultdict(int)

    for expense in st.session_state.expenses:

        yearly_total[
            expense["Year"]
        ] += expense["Amount"]

    st.subheader("Yearly Expense Analysis")

    for year, amount in yearly_total.items():

        st.write(f"📅 {year} : ₹{amount}")

    # ---------------- DOWNLOAD REPORT ----------------

    st.subheader("Download Report")

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(
        ["Date", "Month", "Year",
         "Category", "Amount", "Note"]
    )

    for expense in st.session_state.expenses:

        writer.writerow([
            expense["Date"],
            expense["Month"],
            expense["Year"],
            expense["Category"],
            expense["Amount"],
            expense["Note"]
        ])

    csv_data = output.getvalue()

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="expense_report.csv",
        mime="text/csv"
    )

else:

    st.info("No expenses added yet")