
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="InventoryIQ | Inventory Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_API_URL = (
    "https://inventoryiq-inventory-management-system.onrender.com"
)

API_URL = str(
    st.secrets.get(
        "API_BASE_URL",
        os.getenv("API_BASE_URL", DEFAULT_API_URL),
    )
).rstrip("/")

# --------------------------------------------------
# DARK THEME
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B1120;
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background-color: #111B2E;
    }

    h1, h2, h3, h4, h5, h6,
    p, label, span {
        color: #F8FAFC;
    }

    [data-testid="stMetric"] {
        background: #17243B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #FFFFFF;
    }

    div[data-testid="stForm"] {
        background: #17243B;
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 20px;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: #111827 !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #111827 !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        background-color: #FFFFFF !important;
    }

    [data-testid="stNumberInput"] button {
        color: #111827 !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #F8FAFC !important;
        font-weight: 600;
    }

    [data-testid="stTabs"] button p {
        color: #E2E8F0 !important;
    }

    [data-testid="stAlert"] p {
        color: inherit !important;
    }

    [data-testid="stDataFrame"] {
        background: #17243B;
    }

    .stButton > button[kind="primary"],
    [data-testid="stFormSubmitButton"] button {
        background-color: #2563EB;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #1D4ED8;
        color: #FFFFFF !important;
    }

    hr {
        border-color: #334155;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# API HELPERS
# --------------------------------------------------

def api_request(method, endpoint, data=None, params=None):
    try:
        response = requests.request(
            method=method,
            url=f"{API_URL}{endpoint}",
            json=data,
            params=params,
            timeout=75,
        )

        response.raise_for_status()

        if not response.content:
            return {}

        return response.json()

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        raise RuntimeError(
            f"API error {response.status_code}: {detail}"
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Backend connection failed: {error}"
        )


def get_data(endpoint):
    try:
        return api_request("GET", endpoint)
    except RuntimeError as error:
        st.error(str(error))
        return None


def perform_action(method, endpoint, payload=None):
    try:
        result = api_request(
            method,
            endpoint,
            data=payload,
        )
        st.success("Operation completed successfully.")
        return result

    except RuntimeError as error:
        st.error(str(error))
        return None


def money(value):
    return f"₹{float(value or 0):,.2f}"


def normalize_list(data, key):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        result = data.get(key, [])
        return result if isinstance(result, list) else []

    return []


def product_name(product):
    return str(product.get("name", "Unnamed product"))


def stock_status(product):
    quantity = int(product.get("quantity", 0))
    threshold = int(product.get("low_stock_threshold", 10))

    if quantity == 0:
        return "Out of Stock"

    if quantity <= threshold:
        return "Low Stock"

    return "Healthy"


def display_table(records):
    if records:
        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No records available yet.")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("◈ InventoryIQ")
    st.caption("INVENTORY INTELLIGENCE PLATFORM")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📊 Overview",
            "📦 Products",
            "🛒 Sales",
            "📈 Analytics",
            "🧠 AI Forecasting",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.subheader("System Status")

    try:
        api_request("GET", "/")
        st.success("● API Connected")
        connected = True

    except RuntimeError:
        st.error("● Backend Offline")
        connected = False

    if st.button("Refresh Dashboard", use_container_width=True):
        st.rerun()

    st.caption("InventoryIQ • v2.0")
    st.caption(f"Backend: {API_URL}")

if not connected:
    st.error(
        "The backend is unavailable. Check your Render "
        "service and API_BASE_URL configuration."
    )
    st.stop()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

products_response = get_data("/products")

if products_response is None:
    st.stop()

products = normalize_list(products_response, "products")

sales_response = get_data("/sales")
sales = normalize_list(sales_response, "sales")

total_products = len(products)

available_units = sum(
    int(p.get("quantity", 0)) for p in products
)

inventory_value = sum(
    float(p.get("price", 0)) * int(p.get("quantity", 0))
    for p in products
)

sales_revenue = sum(
    float(s.get("total_amount", 0))
    for s in sales
)
)

low_stock_products = [
    p for p in products
    if int(p.get("quantity", 0))
    <= int(p.get("low_stock_threshold", 10))
]

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "📊 Overview":

    st.title("Inventory Overview")
    st.caption(
        "Real-time visibility into stock, revenue "
        "and business performance."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Products", total_products)
    c2.metric("Available Units", available_units)
    c3.metric("Inventory Value", money(inventory_value))
    c4.metric("Sales Revenue", money(sales_revenue))

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Inventory Distribution")

        if products:
            chart_data = pd.DataFrame(
                [
                    {
                        "Product": product_name(p),
                        "Stock": int(p.get("quantity", 0)),
                    }
                    for p in products
                ]
            )

            fig = px.bar(
                chart_data,
                x="Product",
                y="Stock",
                color="Product",
                template="plotly_dark",
            )

            fig.update_layout(
                paper_bgcolor="#0B1120",
                plot_bgcolor="#17243B",
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add products to view inventory charts.")

    with right:
        st.subheader("Stock Health")

        healthy = total_products - len(low_stock_products)

        if total_products:
            fig = px.pie(
                names=["Healthy", "Low / Out of Stock"],
                values=[healthy, len(low_stock_products)],
                hole=0.65,
                color_discrete_sequence=[
                    "#34D399",
                    "#FB7185",
                ],
            )

            fig.update_layout(
                paper_bgcolor="#0B1120",
                font_color="#FFFFFF",
                showlegend=True,
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No stock data yet.")

    st.subheader("Inventory Alerts")

    if low_stock_products:
        for product in low_stock_products:
            st.warning(
                f"{product_name(product)}: "
                f"{product.get('quantity', 0)} units remaining"
            )
    else:
        st.success(
            "All products are above their low-stock thresholds."
        )

    st.subheader("Recent Transactions")
    display_table(sales[-10:][::-1])

# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

elif page == "📦 Products":

    st.title("Product Management")
    st.caption("Organize and control your inventory.")

    c1, c2, c3 = st.columns(3)

    c1.metric("Products", total_products)
    c2.metric("Low Stock Alerts", len(low_stock_products))
    c3.metric("Inventory Value", money(inventory_value))

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Product Catalog",
            "Add Product",
            "Edit Product",
            "Delete Product",
        ]
    )

    with tab1:
        st.subheader("Product Catalog")

        if products:
            search = st.text_input(
                "Search products",
                placeholder="Enter product name",
            )

            filtered = [
                p for p in products
                if search.lower() in product_name(p).lower()
            ]

            table_data = [
                {
                    "ID": p.get("id"),
                    "Product": product_name(p),
                    "Price": money(p.get("price", 0)),
                    "Stock": p.get("quantity", 0),
                    "Threshold": p.get(
                        "low_stock_threshold", 10
                    ),
                    "Status": stock_status(p),
                }
                for p in filtered
            ]

            display_table(table_data)
        else:
            st.info("No products added yet.")

    with tab2:
        st.subheader("Create New Product")

        with st.form("add_product_form"):
            name = st.text_input("Product Name")

            price = st.number_input(
                "Price (₹)",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

            quantity = st.number_input(
                "Initial Stock",
                min_value=0,
                value=0,
                step=1,
            )

            threshold = st.number_input(
                "Low Stock Threshold",
                min_value=0,
                value=5,
                step=1,
            )

            submitted = st.form_submit_button(
                "Add Product",
                type="primary",
            )

            if submitted:
                if not name.strip():
                    st.error("Product name is required.")
                else:
                    payload = {
                        "name": name.strip(),
                        "price": float(price),
                        "quantity": int(quantity),
                        "low_stock_threshold": int(threshold),
                    }

                    if perform_action(
                        "POST",
                        "/products",
                        payload,
                    ) is not None:
                        st.rerun()

    with tab3:
        st.subheader("Update Product")

        if products:
            options = {
                f"{p['id']} - {product_name(p)}": p
                for p in products
            }

            selected = st.selectbox(
                "Select Product",
                list(options.keys()),
                key="edit_product",
            )

            current = options[selected]

            with st.form(f"edit_form_{current['id']}"):
                updated_name = st.text_input(
                    "Product Name",
                    value=product_name(current),
                )

                updated_price = st.number_input(
                    "Price (₹)",
                    min_value=0.0,
                    value=float(current.get("price", 0)),
                )

                updated_quantity = st.number_input(
                    "Stock Quantity",
                    min_value=0,
                    value=int(current.get("quantity", 0)),
                )

                updated_threshold = st.number_input(
                    "Low Stock Threshold",
                    min_value=0,
                    value=int(
                        current.get("low_stock_threshold", 10)
                    ),
                )

                update_clicked = st.form_submit_button(
                    "Save Changes",
                    type="primary",
                )

                if update_clicked:
                    payload = {
                        "name": updated_name.strip(),
                        "price": float(updated_price),
                        "quantity": int(updated_quantity),
                        "low_stock_threshold": int(
                            updated_threshold
                        ),
                    }

                    if not payload["name"]:
                        st.error("Product name cannot be empty.")
                    elif perform_action(
                        "PUT",
                        f"/products/{current['id']}",
                        payload,
                    ) is not None:
                        st.rerun()
        else:
            st.info("Add a product first.")

    with tab4:
        st.subheader("Delete Product")

        if products:
            options = {
                f"{p['id']} - {product_name(p)}": p
                for p in products
            }

            selected = st.selectbox(
                "Choose Product to Delete",
                list(options.keys()),
                key="delete_product",
            )

            current = options[selected]

            confirm = st.checkbox(
                "I understand this action cannot be undone."
            )

            if st.button(
                "Delete Product",
                type="primary",
                disabled=not confirm,
            ):
                if perform_action(
                    "DELETE",
                    f"/products/{current['id']}",
                ) is not None:
                    st.rerun()
        else:
            st.info("No products available.")

# --------------------------------------------------
# SALES
# --------------------------------------------------

elif page == "🛒 Sales":

    st.title("Sales Management")
    st.caption("Record transactions and track revenue.")

    c1, c2, c3 = st.columns(3)

    c1.metric("Transactions", len(sales))
    c2.metric("Total Revenue", money(sales_revenue))

    total_sold = sum(
        int(s.get("quantity", 0)) for s in sales
    )

    c3.metric("Units Sold", total_sold)

    st.divider()

    st.subheader("Record New Sale")

    if products:
        options = {
            f"{p['id']} - {product_name(p)}": p
            for p in products
            if int(p.get("quantity", 0)) > 0
        }

        if options:
            with st.form("record_sale"):
                selected = st.selectbox(
                    "Select Product",
                    list(options.keys()),
                )

                selected_product = options[selected]

                sale_quantity = st.number_input(
                    "Quantity to Sell",
                    min_value=1,
                    max_value=int(
                        selected_product.get("quantity", 1)
                    ),
                    value=1,
                )

                st.write(
                    "Unit Price:",
                    money(selected_product.get("price", 0)),
                )

                total = (
                    float(selected_product.get("price", 0))
                    * int(sale_quantity)
                )

                st.info(f"Estimated Sale Total: {money(total)}")

                submitted = st.form_submit_button(
                    "Record Sale",
                    type="primary",
                )

                if submitted:
                    payload = {
                        "product_id": int(
                            selected_product["id"]
                        ),
                        "quantity": int(sale_quantity),
                    }

                    if perform_action(
                        "POST",
                        "/sales",
                        payload,
                    ) is not None:
                        st.rerun()
        else:
            st.warning("All products are out of stock.")
    else:
        st.info("Add products before recording sales.")

    st.divider()
    st.subheader("Sales History")

    display_table(sales[::-1])

# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

elif page == "📈 Analytics":

    st.title("Sales Analytics")
    st.caption("Understand sales and inventory performance.")

    c1, c2, c3 = st.columns(3)

    c1.metric("Revenue", money(sales_revenue))
    c2.metric("Transactions", len(sales))
    c3.metric("Inventory Value", money(inventory_value))

    st.divider()

    if sales:
        df = pd.DataFrame(sales)

        if "total_price" in df.columns:
            df["total_price"] = pd.to_numeric(
                df["total_price"],
                errors="coerce",
            ).fillna(0)

            st.subheader("Sales Revenue by Product")

            if "product_id" in df.columns:
                names = {
                    p["id"]: product_name(p)
                    for p in products
                }

                df["Product"] = df["product_id"].map(
                    names
                ).fillna(
                    df["product_id"].astype(str)
                )

                grouped = (
                    df.groupby("Product", as_index=False)[
                        "total_price"
                    ]
                    .sum()
                )

                fig = px.bar(
                    grouped,
                    x="Product",
                    y="total_price",
                    color="Product",
                    template="plotly_dark",
                    labels={
                        "total_price": "Revenue (₹)"
                    },
                )

                fig.update_layout(
                    paper_bgcolor="#0B1120",
                    plot_bgcolor="#17243B",
                    showlegend=False,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            date_column = next(
                (
                    col
                    for col in [
                        "created_at",
                        "sale_date",
                        "date",
                    ]
                    if col in df.columns
                ),
                None,
            )

            if date_column:
                df["Date"] = pd.to_datetime(
                    df[date_column],
                    errors="coerce",
                ).dt.date

                daily = (
                    df.dropna(subset=["Date"])
                    .groupby("Date", as_index=False)[
                        "total_price"
                    ]
                    .sum()
                )

                if not daily.empty:
                    st.subheader("Revenue Over Time")

                    fig = px.line(
                        daily,
                        x="Date",
                        y="total_price",
                        markers=True,
                        template="plotly_dark",
                    )

                    fig.update_layout(
                        paper_bgcolor="#0B1120",
                        plot_bgcolor="#17243B",
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    )

        st.subheader("Transaction Data")
        display_table(sales)

    else:
        st.info(
            "Record sales to generate analytics."
        )

# --------------------------------------------------
# AI FORECASTING
# --------------------------------------------------

elif page == "🧠 AI Forecasting":

    st.title("Demand Forecasting")
    st.caption(
        "Data-driven inventory planning and "
        "reorder recommendations."
    )

    st.info(
        "Forecasts are estimates based on recorded sales. "
        "They are not guarantees of future demand."
    )

    if not products:
        st.warning(
            "Add products and record sales to generate forecasts."
        )
        st.stop()

    options = {
        f"{p['id']} - {product_name(p)}": p
        for p in products
    }

    selected = st.selectbox(
        "Select Product",
        list(options.keys()),
    )

    selected_product = options[selected]

    forecast_days = st.slider(
        "Forecast Period (Days)",
        min_value=7,
        max_value=90,
        value=30,
    )

    lead_time = st.slider(
        "Supplier Lead Time (Days)",
        min_value=1,
        max_value=30,
        value=7,
    )

    st.divider()

    if st.button(
        "Generate Demand Forecast",
        type="primary",
    ):
        product_id = selected_product["id"]

        # Uses the deployed backend's forecasting API.
        forecast = None

        candidate_endpoints = [
            f"/forecast/{product_id}",
            f"/products/{product_id}/forecast",
        ]

        for endpoint in candidate_endpoints:
            try:
                forecast = api_request(
                    "GET",
                    endpoint,
                    params={"days": forecast_days},
                )
                break
            except RuntimeError:
                continue

        if isinstance(forecast, dict):
            st.success("Forecast generated.")

            st.subheader("Forecast Results")
            st.json(forecast)

        else:
            # Transparent fallback calculation using
            # recorded sales and current inventory.
            product_sales = [
                s for s in sales
                if str(s.get("product_id"))
                == str(product_id)
            ]

            quantity_sold = sum(
                int(s.get("quantity", 0))
                for s in product_sales
            )

            sale_dates = []

            for sale in product_sales:
                raw_date = (
                    sale.get("created_at")
                    or sale.get("sale_date")
                    or sale.get("date")
                )

                if raw_date:
                    parsed = pd.to_datetime(
                        raw_date,
                        errors="coerce",
                        utc=True,
                    )

                    if not pd.isna(parsed):
                        sale_dates.append(parsed)

            if not sale_dates:
                st.warning(
                    "Not enough dated sales data to estimate "
                    "daily demand reliably. Record sales over "
                    "multiple days to enable forecasting."
                )
            else:
                first_sale = min(sale_dates)
                last_sale = pd.Timestamp.now(tz="UTC")

                observed_days = max(
                    1,
                    (last_sale - first_sale).days + 1,
                )

                daily_demand = (
                    quantity_sold / observed_days
                )

                predicted_demand = (
                    daily_demand * forecast_days
                )

                current_stock = int(
                    selected_product.get("quantity", 0)
                )

                lead_time_demand = (
                    daily_demand * lead_time
                )

                safety_stock = (
                    daily_demand * 3
                )

                reorder_point = (
                    lead_time_demand + safety_stock
                )

                suggested_order = max(
                    0,
                    round(
                        predicted_demand
                        + safety_stock
                        - current_stock
                    ),
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Estimated Daily Demand",
                    f"{daily_demand:.2f}",
                )

                c2.metric(
                    "Forecast Demand",
                    f"{predicted_demand:.0f} units",
                )

                c3.metric(
                    "Current Stock",
                    current_stock,
                )

                st.subheader("Reorder Recommendation")

                st.metric(
                    "Suggested Order Quantity",
                    suggested_order,
                )

                st.metric(
                    "Estimated Reorder Point",
                    round(reorder_point),
                )

                if current_stock <= reorder_point:
                    st.warning(
                        "Reordering is recommended based "
                        "on estimated demand."
                    )
                else:
                    st.success(
                        "Current stock is above the "
                        "estimated reorder point."
                    )

                st.caption(
                    "Method: average daily sales over the "
                    "observed period, with a three-day "
                    "safety-stock allowance."
                )

    st.divider()
    st.subheader("Stock Risk Summary")

    risk_data = [
        {
            "Product": product_name(p),
            "Current Stock": p.get("quantity", 0),
            "Threshold": p.get(
                "low_stock_threshold", 10
            ),
            "Status": stock_status(p),
        }
        for p in products
    ]

    display_table(risk_data)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "InventoryIQ | Inventory Management "
    "and Demand Intelligence"
)
