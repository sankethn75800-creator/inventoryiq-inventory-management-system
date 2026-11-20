
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st


# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="InventoryIQ | Inventory Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv(
    "INVENTORY_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

PRIMARY = "#818CF8"
GREEN = "#34D399"
YELLOW = "#FBBF24"
RED = "#FB7185"
BLUE = "#38BDF8"
CARD = "#151E32"
BACKGROUND = "#0B1120"


# ==================================================
# PROFESSIONAL DARK THEME
# ==================================================

st.markdown("""
<style>
.stApp {
    background: #0B1120;
    color: #F1F5F9;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1550px;
}

[data-testid="stSidebar"] {
    background: #111A2C;
    border-right: 1px solid #26334B;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #E2E8F0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px;
    border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #202D46;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #26345C;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg, #19243B, #141D30
    );
    border: 1px solid #2B3852;
    padding: 19px 17px;
    border-radius: 15px;
    min-height: 128px;
}

[data-testid="stMetricLabel"] p {
    color: #A5B4CC !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-size: clamp(19px, 1.8vw, 30px) !important;
    font-weight: 750 !important;
    letter-spacing: -0.5px;
    overflow-wrap: anywhere;
}

h1, h2, h3 {
    color: #F8FAFC !important;
    letter-spacing: -0.6px;
}

h1 {
    font-weight: 800 !important;
}

div.stButton > button {
    border-radius: 9px;
    border: 1px solid #35445F;
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button[kind="primary"] {
    background: #6366F1;
    color: #FFFFFF;
    border: none;
}

div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button[kind="primary"]:hover {
    background: #4F46E5;
}

[data-testid="stDataFrame"] {
    border: 1px solid #2B3852;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stTabs"] button {
    color: #CBD5E1;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #A5B4FC;
}

.brand {
    font-size: 27px;
    font-weight: 850;
    color: #F8FAFC;
    padding: 16px 0 5px;
}

.brand span {
    color: #818CF8;
}

.brand-subtitle {
    color: #A5B4CC;
    font-size: 11px;
    letter-spacing: 1.5px;
    margin-bottom: 26px;
}

.subtitle {
    color: #A5B4CC;
    font-size: 15px;
    margin: -4px 0 24px;
}

.section-label {
    color: #A5B4CC;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1px;
    margin-top: 16px;
    margin-bottom: 8px;
}

.status-online {
    background: #12382F;
    border: 1px solid #236A54;
    color: #6EE7B7;
    padding: 12px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 650;
}

.status-offline {
    background: #42202B;
    color: #FDA4AF;
    padding: 12px;
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    margin-top: 50px;
    padding: 20px;
    border-top: 1px solid #26334B;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# API COMMUNICATION
# ==================================================

def api_request(method, endpoint, payload=None, params=None):
    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            json=payload,
            params=params,
            timeout=15
        )

        if not response.ok:
            try:
                detail = response.json().get(
                    "detail", response.text
                )
            except ValueError:
                detail = response.text

            if isinstance(detail, list):
                detail = "; ".join(
                    str(item.get("msg", item))
                    for item in detail
                )

            return None, str(detail)

        return (
            response.json() if response.content else {},
            None
        )

    except requests.exceptions.RequestException as exc:
        return None, f"Backend connection error: {exc}"

    except ValueError:
        return None, "Invalid JSON response from backend."


def perform_action(method, endpoint, payload=None):
    result, error = api_request(
        method, endpoint, payload
    )

    if error:
        st.error(error)
        return

    st.success("Operation completed successfully.")
    st.rerun()


def currency(value):
    return f"₹{float(value):,.2f}"


def compact_currency(value):
    value = float(value)

    if abs(value) >= 10000000:
        return f"₹{value / 10000000:,.2f}Cr"

    if abs(value) >= 100000:
        return f"₹{value / 100000:,.2f}L"

    if abs(value) >= 1000:
        return f"₹{value / 1000:,.1f}K"

    return f"₹{value:,.0f}"


def stock_status(product):
    quantity = product["quantity"]
    threshold = product["low_stock_threshold"]

    if quantity == 0:
        return "Out of Stock"

    if quantity <= threshold:
        return "Low Stock"

    return "Healthy"


def products_table(items):
    rows = []

    for item in items:
        rows.append({
            "ID": item["id"],
            "Product": item["name"],
            "Price": item["price"],
            "Stock": item["quantity"],
            "Threshold": item["low_stock_threshold"],
            "Status": stock_status(item)
        })

    return pd.DataFrame(
        rows,
        columns=[
            "ID", "Product", "Price",
            "Stock", "Threshold", "Status"
        ]
    )


def show_products(items):
    df = products_table(items)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Price": st.column_config.NumberColumn(
                "Price",
                format="₹%.2f"
            )
        }
    )


def style_chart(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color="#CBD5E1", size=12),
        height=height,
        margin=dict(l=20, r=20, t=30, b=25),
        legend=dict(
            orientation="h",
            y=-0.25,
            x=0
        ),
        coloraxis_showscale=False
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#35445F"
    )

    fig.update_yaxes(
        gridcolor="#283650",
        zerolinecolor="#35445F"
    )

    return fig


def page_header(title, description):
    st.title(title)
    st.markdown(
        f'<div class="subtitle">{description}</div>',
        unsafe_allow_html=True
    )


def metric_card(label, value, help_text=None):
    st.metric(
        label,
        value,
        help=help_text
    )


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">◈ Inventory<span>IQ</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'INVENTORY INTELLIGENCE PLATFORM'
        '</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "📊 Overview",
            "📦 Products",
            "🛒 Sales",
            "📈 Analytics",
            "🧠 AI Forecasting"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        '<div class="section-label">SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    health, health_error = api_request("GET", "/")

    if health_error:
        st.markdown(
            '<div class="status-offline">'
            '● Backend Offline'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-online">'
            '● API Connected'
            '</div>',
            unsafe_allow_html=True
        )

    st.write("")

    if st.button(
        "↻ Refresh Dashboard",
        use_container_width=True
    ):
        st.rerun()

    st.caption("InventoryIQ • v2.0")
    st.caption(f"Backend: {API_URL}")


# ==================================================
# FETCH LIVE DATA
# ==================================================

products, error = api_request("GET", "/products")

if error:
    st.error(error)
    st.info(
        "Start FastAPI using: "
        "python -m uvicorn main:app --reload"
    )
    st.stop()

summary, error = api_request("GET", "/dashboard")

if error:
    st.error(error)
    st.stop()

sales, error = api_request("GET", "/sales")

if error:
    st.error(error)
    st.stop()

product_map = {
    product["id"]: product
    for product in products
}

low_stock = [
    product for product in products
    if product["quantity"] <=
    product["low_stock_threshold"]
]


# ==================================================
# OVERVIEW
# ==================================================

if page == "📊 Overview":
    page_header(
        "Inventory Overview",
        "Real-time visibility into stock, revenue and business health."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Total Products",
            summary["total_products"]
        )

    with c2:
        metric_card(
            "Available Units",
            summary["total_stock_units"]
        )

    with c3:
        metric_card(
            "Inventory Value",
            compact_currency(summary["inventory_value"]),
            currency(summary["inventory_value"])
        )

    with c4:
        metric_card(
            "Sales Revenue",
            compact_currency(summary["total_sales_revenue"]),
            currency(summary["total_sales_revenue"])
        )

    st.write("")
    st.caption(
        "Full inventory value: "
        + currency(summary["inventory_value"])
        + "  |  Total sales revenue: "
        + currency(summary["total_sales_revenue"])
    )

    left, right = st.columns([1.65, 1])

    with left:
        st.subheader("Inventory Distribution")

        if products:
            df = products_table(products)

            fig = px.bar(
                df,
                x="Product",
                y="Stock",
                color="Status",
                color_discrete_map={
                    "Healthy": GREEN,
                    "Low Stock": YELLOW,
                    "Out of Stock": RED
                },
                hover_data=["Price", "Threshold"]
            )

            fig.update_traces(
                marker_line_width=0
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )
        else:
            st.info("Add products to view inventory charts.")

    with right:
        st.subheader("Stock Health")

        healthy_count = sum(
            stock_status(p) == "Healthy"
            for p in products
        )

        low_count = sum(
            stock_status(p) == "Low Stock"
            for p in products
        )

        out_count = sum(
            stock_status(p) == "Out of Stock"
            for p in products
        )

        if products:
            fig = go.Figure(
                go.Pie(
                    labels=[
                        "Healthy",
                        "Low Stock",
                        "Out of Stock"
                    ],
                    values=[
                        healthy_count,
                        low_count,
                        out_count
                    ],
                    hole=0.72,
                    marker=dict(
                        colors=[GREEN, YELLOW, RED]
                    ),
                    textinfo="percent",
                    sort=False
                )
            )

            fig.add_annotation(
                text=f"<b>{len(products)}</b><br>Products",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    size=20,
                    color="#F8FAFC"
                )
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )
        else:
            st.info("No stock data yet.")

    st.subheader("Inventory Alerts")

    if low_stock:
        st.warning(
            f"{len(low_stock)} product(s) require attention."
        )
        show_products(low_stock)
    else:
        st.success(
            "All products are above their low-stock thresholds."
        )

    st.subheader("Recent Transactions")

    if sales:
        recent = pd.DataFrame(sales)

        recent["Product"] = recent["product_id"].map(
            lambda pid: product_map.get(
                pid, {}
            ).get("name", f"Product #{pid}")
        )

        recent["sold_at"] = pd.to_datetime(
            recent["sold_at"],
            errors="coerce"
        )

        recent = recent.rename(
            columns={
                "quantity": "Units",
                "total_amount": "Revenue",
                "sold_at": "Date"
            }
        )

        st.dataframe(
            recent[
                ["Product", "Units", "Revenue", "Date"]
            ].head(8),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No transactions recorded yet.")


# ==================================================
# PRODUCT MANAGEMENT
# ==================================================

elif page == "📦 Products":
    page_header(
        "Product Management",
        "Organize and control your complete inventory."
    )

    a, b, c = st.columns(3)

    with a:
        st.metric("Products", len(products))

    with b:
        st.metric("Low Stock Alerts", len(low_stock))

    with c:
        st.metric(
            "Inventory Value",
            compact_currency(summary["inventory_value"])
        )

    st.write("")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Product Catalog",
        "Add Product",
        "Edit Product",
        "Delete Product"
    ])

    with tab1:
        search = st.text_input(
            "Search inventory",
            placeholder="Search product name..."
        )

        filtered = [
            product for product in products
            if search.casefold() in product["name"].casefold()
        ]

        show_products(filtered)

    with tab2:
        st.subheader("Create New Product")

        with st.form("add_product", clear_on_submit=True):
            name = st.text_input("Product Name")

            price = st.number_input(
                "Price (₹)",
                min_value=0.0,
                step=1.0
            )

            quantity = st.number_input(
                "Initial Stock",
                min_value=0,
                step=1
            )

            threshold = st.number_input(
                "Low Stock Threshold",
                min_value=0,
                value=10,
                step=1
            )

            submitted = st.form_submit_button(
                "Create Product",
                type="primary"
            )

            if submitted:
                if not name.strip():
                    st.error("Enter a product name.")
                else:
                    perform_action(
                        "POST",
                        "/products",
                        {
                            "name": name.strip(),
                            "price": float(price),
                            "quantity": int(quantity),
                            "low_stock_threshold": int(threshold)
                        }
                    )

    with tab3:
        st.subheader("Edit Product Details")

        if products:
            selected_id = st.selectbox(
                "Choose Product",
                list(product_map.keys()),
                format_func=lambda pid: (
                    f"{pid} — {product_map[pid]['name']}"
                ),
                key="edit_select"
            )

            selected = product_map[selected_id]

            with st.form(f"edit_{selected_id}"):
                name = st.text_input(
                    "Product Name",
                    value=selected["name"]
                )

                price = st.number_input(
                    "Price (₹)",
                    min_value=0.0,
                    value=float(selected["price"]),
                    step=1.0
                )

                quantity = st.number_input(
                    "Stock Quantity",
                    min_value=0,
                    value=int(selected["quantity"]),
                    step=1
                )

                threshold = st.number_input(
                    "Low Stock Threshold",
                    min_value=0,
                    value=int(selected["low_stock_threshold"]),
                    step=1
                )

                submitted = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

                if submitted:
                    if not name.strip():
                        st.error("Product name cannot be empty.")
                    else:
                        perform_action(
                            "PUT",
                            f"/products/{selected_id}",
                            {
                                "name": name.strip(),
                                "price": float(price),
                                "quantity": int(quantity),
                                "low_stock_threshold": int(threshold)
                            }
                        )
        else:
            st.info("No products available to edit.")

    with tab4:
        st.subheader("Delete Product")

        st.warning(
            "Products with recorded sales cannot be deleted "
            "because their sales history must be preserved."
        )

        if products:
            delete_id = st.selectbox(
                "Select Product",
                list(product_map.keys()),
                format_func=lambda pid: (
                    product_map[pid]["name"]
                ),
                key="delete_select"
            )

            confirmed = st.checkbox(
                "I understand this will delete the product."
            )

            if st.button(
                "Delete Product",
                disabled=not confirmed
            ):
                perform_action(
                    "DELETE",
                    f"/products/{delete_id}"
                )
        else:
            st.info("No products available.")


# ==================================================
# SALES MANAGEMENT
# ==================================================

elif page == "🛒 Sales":
    page_header(
        "Sales Management",
        "Record transactions and track sales performance."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Revenue",
            compact_currency(summary["total_sales_revenue"])
        )

    with c2:
        st.metric(
            "Units Sold",
            summary["total_units_sold"]
        )

    with c3:
        st.metric("Transactions", len(sales))

    st.write("")
    st.subheader("Record a Sale")

    available = [
        p for p in products
        if p["quantity"] > 0
    ]

    if available:
        available_map = {
            p["id"]: p for p in available
        }

        with st.form("new_sale"):
            selected_id = st.selectbox(
                "Product",
                list(available_map.keys()),
                format_func=lambda pid: (
                    f"{available_map[pid]['name']} "
                    f"— {available_map[pid]['quantity']} available"
                )
            )

            product = available_map[selected_id]

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=int(product["quantity"]),
                value=1,
                step=1
            )

            total = product["price"] * quantity

            st.info(
                f"Transaction Value: {currency(total)}"
            )

            submitted = st.form_submit_button(
                "Confirm Sale",
                type="primary"
            )

            if submitted:
                perform_action(
                    "POST",
                    "/sales",
                    {
                        "product_id": selected_id,
                        "quantity": int(quantity)
                    }
                )
    else:
        st.info(
            "Add products with available stock "
            "to record sales."
        )

    st.divider()
    st.subheader("Transaction History")

    if sales:
        df = pd.DataFrame(sales)

        df["Product"] = df["product_id"].map(
            lambda pid: product_map.get(
                pid, {}
            ).get("name", f"Product #{pid}")
        )

        df["sold_at"] = pd.to_datetime(
            df["sold_at"],
            errors="coerce"
        )

        df = df.rename(
            columns={
                "id": "Sale ID",
                "quantity": "Units",
                "total_amount": "Revenue",
                "sold_at": "Date"
            }
        )

        st.dataframe(
            df[
                ["Sale ID", "Product", "Units", "Revenue", "Date"]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Sales Report",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="inventory_sales.csv",
            mime="text/csv"
        )
    else:
        st.info("No sales recorded.")


# ==================================================
# ANALYTICS
# ==================================================

elif page == "📈 Analytics":
    page_header(
        "Business Analytics",
        "Understand revenue, demand and inventory performance."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Revenue",
            compact_currency(summary["total_sales_revenue"])
        )

    with c2:
        st.metric(
            "Inventory Value",
            compact_currency(summary["inventory_value"])
        )

    with c3:
        st.metric(
            "Units Sold",
            summary["total_units_sold"]
        )

    st.write("")

    if sales:
        df = pd.DataFrame(sales)

        df["sold_at"] = pd.to_datetime(
            df["sold_at"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["sold_at"]
        ).copy()

        if not df.empty:
            df["Date"] = df["sold_at"].dt.date

            daily = df.groupby(
                "Date",
                as_index=False
            )["total_amount"].sum()

            st.subheader("Revenue Over Time")

            fig = px.line(
                daily,
                x="Date",
                y="total_amount",
                markers=True,
                labels={
                    "total_amount": "Revenue (₹)"
                }
            )

            fig.update_traces(
                line_color=PRIMARY,
                line_width=3,
                marker_size=9
            )

            st.plotly_chart(
                style_chart(fig, 390),
                use_container_width=True
            )

        st.subheader("Top Performing Products")

        grouped = (
            pd.DataFrame(sales)
            .groupby("product_id", as_index=False)
            .agg(
                Units=("quantity", "sum"),
                Revenue=("total_amount", "sum")
            )
        )

        grouped["Product"] = grouped["product_id"].map(
            lambda pid: product_map.get(
                pid, {}
            ).get("name", f"Product #{pid}")
        )

        grouped = grouped.sort_values(
            "Revenue",
            ascending=False
        ).head(10)

        fig = px.bar(
            grouped,
            x="Product",
            y="Revenue",
            color_discrete_sequence=[BLUE]
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )
    else:
        st.info(
            "Record sales to unlock revenue analytics."
        )

    st.subheader("Inventory Valuation")

    if products:
        valuation = products_table(products)

        valuation["Value"] = (
            valuation["Price"] * valuation["Stock"]
        )

        valuation = valuation.sort_values(
            "Value",
            ascending=False
        )

        fig = px.bar(
            valuation,
            x="Product",
            y="Value",
            color_discrete_sequence=[GREEN]
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


# ==================================================
# DEMAND FORECASTING
# ==================================================

elif page == "🧠 AI Forecasting":
    page_header(
        "Demand Intelligence",
        "Predict demand and make smarter restocking decisions."
    )

    st.info(
        "Forecasting uses historical average daily sales. "
        "It is a statistical decision-support method, "
        "not a trained AI or machine-learning model."
    )

    if not products:
        st.warning("Add products to enable forecasting.")

    else:
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            selected_id = st.selectbox(
                "Product",
                list(product_map.keys()),
                format_func=lambda pid: (
                    product_map[pid]["name"]
                )
            )

        with c2:
            history_days = st.number_input(
                "History Days",
                min_value=1,
                max_value=365,
                value=30
            )

        with c3:
            forecast_days = st.number_input(
                "Forecast Days",
                min_value=1,
                max_value=365,
                value=7
            )

        with c4:
            lead_time = st.number_input(
                "Lead Time Days",
                min_value=1,
                max_value=365,
                value=3
            )

        forecast, error = api_request(
            "GET",
            f"/forecast/{selected_id}",
            params={
                "history_days": int(history_days),
                "forecast_days": int(forecast_days),
                "lead_time_days": int(lead_time)
            }
        )

        if error:
            st.error(error)

        elif forecast:
            st.write("")

            a, b, c, d = st.columns(4)

            with a:
                st.metric(
                    "Current Stock",
                    forecast["current_stock"]
                )

            with b:
                st.metric(
                    "Daily Demand",
                    forecast["average_daily_demand"]
                )

            with c:
                st.metric(
                    "Predicted Demand",
                    forecast["predicted_units_needed"]
                )

            with d:
                st.metric(
                    "Reorder Units",
                    forecast["recommended_reorder_quantity"]
                )

            risk = forecast["stockout_risk"]

            if risk in ("HIGH", "OUT_OF_STOCK"):
                st.error(f"Stockout Risk: {risk}")
            elif risk == "MEDIUM":
                st.warning(f"Stockout Risk: {risk}")
            else:
                st.success(f"Stockout Risk: {risk}")

            days = forecast[
                "estimated_days_until_stockout"
            ]

            if days is not None:
                st.caption(
                    f"Estimated stock coverage: {days} days"
                )
            else:
                st.caption(
                    "Insufficient recorded demand "
                    "to estimate stock coverage."
                )

            st.subheader("Demand Forecast Comparison")

            chart_data = pd.DataFrame({
                "Category": [
                    "Current Stock",
                    "Predicted Demand",
                    "Recommended Reorder"
                ],
                "Units": [
                    forecast["current_stock"],
                    forecast["predicted_units_needed"],
                    forecast["recommended_reorder_quantity"]
                ]
            })

            fig = px.bar(
                chart_data,
                x="Category",
                y="Units",
                color="Category",
                color_discrete_map={
                    "Current Stock": BLUE,
                    "Predicted Demand": YELLOW,
                    "Recommended Reorder": GREEN
                }
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

            st.caption(forecast["note"])

        st.divider()
        st.subheader("Smart Reorder Recommendations")

        recommendations, error = api_request(
            "GET",
            "/recommendations"
        )

        if error:
            st.error(error)

        elif recommendations:
            rows = []

            for item in recommendations:
                rows.append({
                    "Product": item["product_name"],
                    "Current Stock": item["current_stock"],
                    "Daily Demand": item[
                        "average_daily_demand"
                    ],
                    "Risk": item["stockout_risk"],
                    "Reorder Units": item[
                        "recommended_reorder_quantity"
                    ]
                })

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Recommendations are estimates. "
                "They depend on recorded sales and "
                "configured stock thresholds."
            )
        else:
            st.info("No recommendations available.")


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    '<div class="footer">'
    'InventoryIQ © 2026 | '
    'FastAPI • Streamlit • SQLAlchemy • SQLite'
    '</div>',
    unsafe_allow_html=True
)
