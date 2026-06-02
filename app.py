import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Tours & Travels Dashboard",
    page_icon="🚖",
    layout="wide"
)

df = pd.read_excel("Tours_Travels_Sample_Dataset.xlsx")

df["Total Cost"] = df["Fuel Cost"] + df["Toll"] + df["Driver Payment"] + df["Other Cost"]
df["Profit"] = df["Revenue"] - df["Total Cost"]

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Booking", "Trip Cost Estimator"]
)

if menu == "Dashboard":

    st.title("🚖 Smart Tours & Travels Analytics Dashboard")
    st.write("Business dashboard for revenue, expenses, profit, vehicles, routes and trip estimation.")

    st.sidebar.header("🔍 Filters")

    vehicles = st.sidebar.multiselect(
        "Select Vehicle",
        options=df["Vehicle"].unique(),
        default=df["Vehicle"].unique()
    )

    clients = st.sidebar.multiselect(
        "Select Client",
        options=df["Client"].unique(),
        default=df["Client"].unique()
    )

    filtered_df = df[
        (df["Vehicle"].isin(vehicles)) &
        (df["Client"].isin(clients))
    ]

    total_bookings = len(filtered_df)
    total_revenue = filtered_df["Revenue"].sum()
    total_expense = filtered_df["Total Cost"].sum()
    total_profit = filtered_df["Profit"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Bookings", total_bookings)
    col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col3.metric("Total Expense", f"₹{total_expense:,.0f}")
    col4.metric("Net Profit", f"₹{total_profit:,.0f}")

    st.divider()

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("🚗 Vehicle Usage")
        vehicle_count = filtered_df["Vehicle"].value_counts().reset_index()
        vehicle_count.columns = ["Vehicle", "Trips"]

        fig_vehicle = px.bar(
            vehicle_count,
            x="Vehicle",
            y="Trips",
            text="Trips",
            title="Most Rented Vehicles"
        )
        st.plotly_chart(fig_vehicle, use_container_width=True)

    with col6:
        st.subheader("💰 Revenue by Vehicle")
        vehicle_revenue = filtered_df.groupby("Vehicle")["Revenue"].sum().reset_index()

        fig_revenue = px.pie(
            vehicle_revenue,
            names="Vehicle",
            values="Revenue",
            title="Vehicle Revenue Share"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

    st.divider()

    col7, col8 = st.columns(2)

    with col7:
        st.subheader("🛣️ Route Profit Analysis")
        route_profit = (
            filtered_df.groupby("Route")["Profit"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig_route = px.bar(
            route_profit,
            x="Route",
            y="Profit",
            text="Profit",
            title="Most Profitable Routes"
        )
        st.plotly_chart(fig_route, use_container_width=True)

    with col8:
        st.subheader("👤 Top Clients")
        client_revenue = (
            filtered_df.groupby("Client")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig_client = px.bar(
            client_revenue,
            x="Client",
            y="Revenue",
            text="Revenue",
            title="Revenue by Client"
        )
        st.plotly_chart(fig_client, use_container_width=True)

    st.divider()

    st.subheader("📋 Booking Data")
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Booking Data as CSV",
        data=csv,
        file_name="travel_booking_data.csv",
        mime="text/csv"
    )


elif menu == "Add Booking":

    st.title("➕ Add New Booking")

    date = st.date_input("Date")
    client = st.text_input("Client Name")

    vehicle = st.selectbox(
        "Vehicle",
        ["Dzire", "Ertiga", "Crysta", "Traveller"]
    )

    route = st.text_input("Route")

    trip_type = st.selectbox(
        "Trip Type",
        ["Airport", "Full Day", "Outstation"]
    )

    distance = st.number_input("Distance", min_value=0)
    revenue = st.number_input("Revenue", min_value=0)
    fuel_cost = st.number_input("Fuel Cost", min_value=0)
    toll = st.number_input("Toll", min_value=0)
    driver_payment = st.number_input("Driver Payment", min_value=0)
    other_cost = st.number_input("Other Cost", min_value=0)

    if st.button("Save Booking"):

        new_row = {
            "Date": date.strftime("%d-%m-%Y"),
            "Client": client,
            "Vehicle": vehicle,
            "Route": route,
            "Trip Type": trip_type,
            "Distance": distance,
            "Revenue": revenue,
            "Fuel Cost": fuel_cost,
            "Toll": toll,
            "Driver Payment": driver_payment,
            "Other Cost": other_cost
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.to_excel("Tours_Travels_Sample_Dataset.xlsx", index=False)

        st.success("Booking Saved Successfully ✅")
        st.info("Go to Dashboard to see updated data.")


elif menu == "Trip Cost Estimator":

    st.title("🧮 Trip Cost Estimator")

    c1, c2, c3 = st.columns(3)

    with c1:
        distance = st.number_input("Distance in KM", min_value=1, value=100)
        mileage = st.number_input("Vehicle Mileage KM/L", min_value=1, value=14)
        fuel_price = st.number_input("Fuel Price per Litre", min_value=1, value=105)

    with c2:
        toll = st.number_input("Toll Cost", min_value=0, value=150)
        driver_payment = st.number_input("Driver Payment", min_value=0, value=500)
        other_cost = st.number_input("Other Cost", min_value=0, value=200)

    with c3:
        profit_margin = st.number_input("Profit Margin %", min_value=0, value=25)

    fuel_cost = (distance / mileage) * fuel_price
    total_trip_cost = fuel_cost + toll + driver_payment + other_cost
    suggested_price = total_trip_cost + (total_trip_cost * profit_margin / 100)

    e1, e2, e3 = st.columns(3)

    e1.metric("Fuel Cost", f"₹{fuel_cost:,.0f}")
    e2.metric("Total Trip Cost", f"₹{total_trip_cost:,.0f}")
    e3.metric("Suggested Customer Price", f"₹{suggested_price:,.0f}")