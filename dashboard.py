
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st


# ============================================================
# INVENTORYIQ - INVENTORY INTELLIGENCE PLATFORM
# ============================================================

st.set_page_config(
    page_title="InventoryIQ | Inventory Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_API_URL = (
    "https://inventoryiq-inventory-management-system.onrender.com"
)

try:
    API_URL = st.secrets.get(
        "API_URL",
        os.getenv("API_URL", DEFAULT_API_URL)
    )
except Exception:
    API_URL = os.getenv("API_URL", DEFAULT_API_URL)

API_URL = str(API_URL).rstrip("/")


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }

    html, body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #0b1120 !important;
        color: #f8fafc !important;
    }

    [data-testid="stHeader"] {
        background: #0b1120 !important;
    }

    [data-testid="stSidebar"] {
        background: #111c30 !important;
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3, h4, h5, h6,
    p, label, small,
    [data-testid="stMarkdownContainer"] {
        color: #f8fafc;
    }

    h1 {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        font-size: 1.6rem !important;
        font-weight: 750 !important;
    }

    .muted {
        color: #cbd5e1 !important;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 7px;
    }

    .brand-subtitle {
        color: #cbd5e1;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .metric-card {
        background: #192840;
        border: 1px solid #334765;
        border-radius: 14px;
        padding: 23px 22px;
        min-height: 145px;
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 14px;
        font-weight: 650;
        color: #e2e8f0;
        margin-bottom: 12px;
    }

    .metric-value {
        font-size: clamp(23px, 2.3vw, 34px);
        font-weight: 750;
        color: #ffffff;
        overflow-wrap: anywhere;
    }

    .status-good {
        background: #064e3b;
        color: #ffffff !important;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 16px;
        font-weight: 650;
    }

    .status-bad {
        background: #7f1d1d;
        color: #ffffff !important;
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 16px;
        font-weight: 650;
    }

    .notice-success {
        background: #064e3b;
        color: #ffffff !important;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 18px;
        font-size: 15px;
        font-weight: 600;
        margin: 14px 0;
    }

    .notice-warning {
        background: #78350f;
        color: #ffffff !important;
        border: 1px solid #f59e0b;
        border-radius: 10px;
        padding: 18px;
        font-size: 15px;
        font-weight: 600;
        margin: 14px 0;
    }

    .notice-info {
        background: #172554;
        color: #ffffff !important;
        border: 1px solid #3b82f6;
        border-radius: 10px;
        padding: 18px;
        font-size: 15px;
        font-weight: 600;
        margin: 14px 0;
    }

    .notice-error {
        background: #7f1d1d;
        color: #ffffff !important;
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 18px;
        font-size: 15px;
        font-weight: 600;
        margin: 14px 0;
    }

    /* Streamlit alerts - readable in dark mode */
    [data-testid="stAlert"] {
        background: #192840 !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"]
    [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }

    /* Input fields */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea {
        background: #192840 !important;
        color: #ffffff !important;
        border-color: #475569 !important;
    }

    [data-baseweb="select"] > div {
        background: #192840 !important;
        color: #ffffff !important;
        border-color: #475569 !important;
    }

    [data-baseweb="select"] span,
    [data-baseweb="select"] input {
        color: #ffffff !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background: #192840 !important;
        color: #ffffff !important;
    }

    /* Buttons */
    .stButton > button[kind="primary"],
    [data-testid="stFormSubmitButton"]
    button[kind="primary"] {
        background: #2563eb !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
    }

    .stButton > button[kind="secondary"] {
        background: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 9px !important;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        border-color: #60a5fa !important;
        color: #ffffff !important;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 10px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #192840;
        border: 1px solid #334765;
        border-radius: 12px;
        padding: 20px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Horizontal rules */
    hr {
        border-color: #334155 !important;
        margin: 30px 0 !important;
    }

    /* Radio navigation */
    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 9px;
    }

    [data-testid="stSidebar"] label {
        font-weight: 600;
    }

    /* Sliders */
    [data-testid="stSlider"] * {
        color: #f8fafc;
    }

    /* JSON and code output */
    [data-testid="stJson"],
    [data-testid="stCodeBlock"] {
        color: #f8fafc;
    }

    .footer {
        color: #cbd5e1;
        font-size: 13px;
        margin-top: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def success_message(message):
    st.markdown(
        f'<div class="notice-success">✓ {message}</div>',
        unsafe_allow_html=True,
    )


def warning_message(message):
    st.markdown(
        f'<div class="notice-warning">⚠ {message}</div>',
        unsafe_allow_html=True,
    )


def info_message(message):
    st.markdown(
        f'<div class="notice-info">ℹ {message}</div>',
        unsafe_allow_html=True,
    )


def error_message(message):
    st.markdown(
        f'<div class="notice-error">✕ {message}</div>',
        unsafe_allow_html=True,
    )


def api_request(method, endpoint, data=None, params=None):
    url = f"{API_URL}{endpoint}"

    try:
        response = requests.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=60,
        )

        if not response.ok:
            try:
                payload = response.json()
                detail = payload.get(
                    "detail",
                    response.text,
                )
            except ValueError:
                detail = response.text

            if isinstance(detail, list):
                detail = "; ".join(
                    str(item.get("msg", item))
                    if isinstance(item, dict)
                    else str(item)
                    for item in detail
                )

            raise RuntimeError(
                f"API error {response.status_code}: {detail}"
            )

        if not response.content:
            return {}

        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The server timed out. Render free instances "
            "may need time to wake up."
        )
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to the backend API. "
            "Check the Render service."
        )
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(str(exc))


def load_data(endpoint, params=None):
    try:
        return api_request(
            "GET",
            endpoint,
            params=params,
        )
    except RuntimeError as exc:
        error_message(str(exc))
        return None


def product_options(products):
    return {
        f"{p['id']} - {p['name']}": p
        for p in products
    }


def plot_style(fig, height=390):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#192840",
        font=dict(
            color="#ffffff",
            size=13,
        ),
        height=height,
        margin=dict(
            l=30,
            r=30,
            t=35,
            b=40,
        ),
        legend=dict(
            font=dict(color="#ffffff"),
        ),
    )
    return fig


def show_table(records, columns=None):
    if not records:
        info_message("No records available.")
        return

    frame = pd.DataFrame(records)

    if columns:
        available = [
            column for column in columns
            if column in frame.columns
        ]
        if available:
            frame = frame[available]

    st.dataframe(
        frame,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">◇ InventoryIQ</div>
        <div class="brand-subtitle">
            INVENTORY INTELLIGENCE PLATFORM
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        connected = True
    except RuntimeError:
        connected = False

    if connected:
        st.markdown(
            '<div class="status-good">● API Connected</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-bad">● API Disconnected</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    if st.button(
        "Refresh Dashboard",
        use_container_width=True,
    ):
        st.rerun()

    st.caption("InventoryIQ • v3.1")

    st.markdown(
        f"[Backend: Render API]({API_URL}/docs)"
    )


if not connected:
    st.title("InventoryIQ")
    error_message(
        "The backend API is unavailable. "
        "Check your Render deployment and API_URL."
    )
    st.stop()


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "📊 Overview":
    st.title("Inventory Overview")

    st.markdown(
        '<p class="muted">'
        'Real-time visibility into stock, revenue '
        'and business performance.'
        '</p>',
        unsafe_allow_html=True,
    )

    dashboard = load_data("/dashboard")
    products = load_data("/products")

    if dashboard is None or products is None:
        st.stop()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Total Products",
            dashboard.get("total_products", 0),
        )

    with col2:
        metric_card(
            "Available Units",
            dashboard.get("total_stock_units", 0),
        )

    with col3:
        metric_card(
            "Inventory Value",
            money(dashboard.get("inventory_value", 0)),
        )

    with col4:
        metric_card(
            "Sales Revenue",
            money(
                dashboard.get("total_sales_revenue", 0)
            ),
        )

    st.divider()

    left, right = st.columns([1.6, 1])

    with left:
        st.subheader("Inventory Distribution")

        if products:
            names = [p["name"] for p in products]
            quantities = [
                p["quantity"] for p in products
            ]

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=names,
                    y=quantities,
                    marker_color="#3b82f6",
                    text=quantities,
                    textposition="outside",
                    textfont=dict(
                        color="#ffffff",
                        size=13,
                    ),
                )
            )

            fig.update_layout(
                xaxis_title="Product",
                yaxis_title="Stock",
                showlegend=False,
            )

            fig.update_yaxes(
                rangemode="tozero",
                gridcolor="#334155",
            )

            st.plotly_chart(
                plot_style(fig),
                use_container_width=True,
            )
        else:
            info_message(
                "Add products to view inventory distribution."
            )

    with right:
        st.subheader("Stock Health")

        healthy = sum(
            1 for p in products
            if p["quantity"] > p["low_stock_threshold"]
        )

        low_stock = len(products) - healthy

        if products:
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Healthy",
                            "Low / Out of Stock",
                        ],
                        values=[healthy, low_stock],
                        hole=0.67,
                        marker=dict(
                            colors=[
                                "#34d399",
                                "#fb7185",
                            ]
                        ),
                        textinfo="percent",
                        textfont=dict(
                            color="#ffffff",
                            size=14,
                        ),
                    )
                ]
            )

            fig.update_layout(
                showlegend=True,
            )

            st.plotly_chart(
                plot_style(fig),
                use_container_width=True,
            )
        else:
            info_message(
                "No products available for stock analysis."
            )

    st.divider()

    st.subheader("Low Stock Alerts")

    low_stock_products = dashboard.get(
        "low_stock_products",
        [],
    )

    if low_stock_products:
        warning_message(
            f"{len(low_stock_products)} product(s) "
            "need attention."
        )

        show_table(
            low_stock_products,
            [
                "id",
                "name",
                "quantity",
                "threshold",
            ],
        )
    else:
        success_message(
            "All products are above their "
            "low-stock thresholds."
        )

    st.divider()

    st.markdown(
        '<div class="footer">'
        'InventoryIQ | Inventory Management '
        'and Demand Intelligence'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# PRODUCTS PAGE
# ============================================================

elif page == "📦 Products":
    st.title("Product Management")

    st.markdown(
        '<p class="muted">'
        'Manage products, prices, quantities and stock levels.'
        '</p>',
        unsafe_allow_html=True,
    )

    products = load_data("/products")

    if products is None:
        st.stop()

    st.subheader("Current Inventory")

    search = st.text_input(
        "Search Products",
        placeholder="Search by product name...",
    )

    filtered_products = [
        p for p in products
        if search.lower() in p["name"].lower()
    ]

    show_table(
        filtered_products,
        [
            "id",
            "name",
            "price",
            "quantity",
            "low_stock_threshold",
        ],
    )

    st.divider()

    st.subheader("Add New Product")

    with st.form("add_product_form"):
        name = st.text_input(
            "Product Name",
            placeholder="Example: Dell Laptop",
        )

        col1, col2 = st.columns(2)

        with col1:
            price = st.number_input(
                "Unit Price (₹)",
                min_value=0.0,
                value=0.0,
                step=100.0,
            )

            quantity = st.number_input(
                "Initial Quantity",
                min_value=0,
                value=0,
                step=1,
            )

        with col2:
            threshold = st.number_input(
                "Low Stock Threshold",
                min_value=0,
                value=5,
                step=1,
            )

        submitted = st.form_submit_button(
            "Add Product",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not name.strip():
            error_message(
                "Product name cannot be empty."
            )
        else:
            try:
                api_request(
                    "POST",
                    "/products",
                    data={
                        "name": name.strip(),
                        "price": float(price),
                        "quantity": int(quantity),
                        "low_stock_threshold": int(
                            threshold
                        ),
                    },
                )

                st.toast(
                    "Product added successfully!",
                    icon="✅",
                )
                st.rerun()

            except RuntimeError as exc:
                error_message(str(exc))

    st.divider()

    st.subheader("Update Existing Product")

    if products:
        options = product_options(products)

        selected = st.selectbox(
            "Select Product to Update",
            list(options.keys()),
            key="update_product_selector",
        )

        product = options[selected]

        with st.form(
            f"update_product_{product['id']}"
        ):
            updated_name = st.text_input(
                "Product Name",
                value=product["name"],
            )

            col1, col2 = st.columns(2)

            with col1:
                updated_price = st.number_input(
                    "Price (₹)",
                    min_value=0.0,
                    value=float(product["price"]),
                    step=100.0,
                )

                updated_quantity = st.number_input(
                    "Quantity",
                    min_value=0,
                    value=int(product["quantity"]),
                    step=1,
                )

            with col2:
                updated_threshold = st.number_input(
                    "Low Stock Threshold",
                    min_value=0,
                    value=int(
                        product["low_stock_threshold"]
                    ),
                    step=1,
                )

            update_clicked = st.form_submit_button(
                "Save Changes",
                type="primary",
            )

        if update_clicked:
            if not updated_name.strip():
                error_message(
                    "Product name cannot be empty."
                )
            else:
                try:
                    api_request(
                        "PUT",
                        f"/products/{product['id']}",
                        data={
                            "name": updated_name.strip(),
                            "price": float(updated_price),
                            "quantity": int(
                                updated_quantity
                            ),
                            "low_stock_threshold": int(
                                updated_threshold
                            ),
                        },
                    )

                    st.toast(
                        "Product updated successfully!",
                        icon="✅",
                    )
                    st.rerun()

                except RuntimeError as exc:
                    error_message(str(exc))

        st.divider()

        st.subheader("Delete Product")

        warning_message(
            "Products with sales history cannot be "
            "deleted because historical records "
            "must be preserved."
        )

        delete_confirm = st.checkbox(
            "I understand that deleting this product "
            "cannot be undone."
        )

        if st.button(
            "Delete Selected Product",
            disabled=not delete_confirm,
        ):
            try:
                api_request(
                    "DELETE",
                    f"/products/{product['id']}",
                )

                st.toast(
                    "Product deleted successfully!",
                    icon="✅",
                )
                st.rerun()

            except RuntimeError as exc:
                error_message(str(exc))
    else:
        info_message(
            "Add a product before using update or delete."
        )


# ============================================================
# SALES PAGE
# ============================================================

elif page == "🛒 Sales":
    st.title("Sales Management")

    st.markdown(
        '<p class="muted">'
        'Record sales and automatically update inventory.'
        '</p>',
        unsafe_allow_html=True,
    )

    products = load_data("/products")

    if products is None:
        st.stop()

    st.subheader("Record New Sale")

    if not products:
        warning_message(
            "Add a product before recording sales."
        )
    else:
        options = product_options(products)

        selected = st.selectbox(
            "Select Product",
            list(options.keys()),
        )

        product = options[selected]

        available = int(product["quantity"])

        st.markdown(
            f"**Available Stock:** {available} units"
        )

        quantity = st.number_input(
            "Quantity to Sell",
            min_value=1,
            value=1,
            step=1,
        )

        st.markdown(
            f"**Unit Price:** {money(product['price'])}"
        )

        estimated_total = (
            float(product["price"]) * quantity
        )

        info_message(
            f"Estimated Sale Total: "
            f"{money(estimated_total)}"
        )

        if st.button(
            "Record Sale",
            type="primary",
        ):
            if quantity > available:
                error_message(
                    "Insufficient stock. "
                    f"Only {available} units are available."
                )
            else:
                try:
                    result = api_request(
                        "POST",
                        "/sales",
                        data={
                            "product_id": product["id"],
                            "quantity": int(quantity),
                        },
                    )

                    st.session_state[
                        "last_sale_result"
                    ] = result

                    st.rerun()

                except RuntimeError as exc:
                    error_message(str(exc))

        if "last_sale_result" in st.session_state:
            result = st.session_state.pop(
                "last_sale_result"
            )

            success_message(
                "Sale recorded successfully! "
                f"Amount: "
                f"{money(result.get('total_amount', 0))}. "
                f"Remaining stock: "
                f"{result.get('remaining_stock', 0)}"
            )

    st.divider()

    st.subheader("Sales History")

    sales = load_data("/sales")

    if sales is not None:
        show_table(
            sales,
            [
                "id",
                "product_id",
                "quantity",
                "total_amount",
                "sold_at",
            ],
        )


# ============================================================
# ANALYTICS PAGE
# ============================================================

elif page == "📈 Analytics":
    st.title("Sales Analytics")

    st.markdown(
        '<p class="muted">'
        'Understand sales trends, transactions '
        'and inventory performance.'
        '</p>',
        unsafe_allow_html=True,
    )

    dashboard = load_data("/dashboard")
    sales = load_data("/sales")
    products = load_data("/products")

    if (
        dashboard is None
        or sales is None
        or products is None
    ):
        st.stop()

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Total Revenue",
            money(
                dashboard.get("total_sales_revenue", 0)
            ),
        )

    with col2:
        metric_card(
            "Transactions",
            len(sales),
        )

    with col3:
        metric_card(
            "Inventory Value",
            money(
                dashboard.get("inventory_value", 0)
            ),
        )

    st.divider()

    if sales:
        frame = pd.DataFrame(sales)

        frame["sold_at"] = pd.to_datetime(
            frame["sold_at"],
            errors="coerce",
        )

        frame["total_amount"] = pd.to_numeric(
            frame["total_amount"],
            errors="coerce",
        ).fillna(0)

        frame["quantity"] = pd.to_numeric(
            frame["quantity"],
            errors="coerce",
        ).fillna(0)

        frame["product_id"] = pd.to_numeric(
            frame["product_id"],
            errors="coerce",
        )

        product_names = {
            p["id"]: p["name"]
            for p in products
        }

        frame["product_name"] = (
            frame["product_id"]
            .map(product_names)
            .fillna("Unknown Product")
        )

        st.subheader("Revenue Over Time")

        dated = frame.dropna(
            subset=["sold_at"]
        ).copy()

        if not dated.empty:
            dated["date"] = (
                dated["sold_at"].dt.date
            )

            daily = (
                dated.groupby(
                    "date",
                    as_index=False,
                )["total_amount"]
                .sum()
            )

            fig = px.line(
                daily,
                x="date",
                y="total_amount",
                markers=True,
                labels={
                    "date": "Date",
                    "total_amount": "Revenue (₹)",
                },
            )

            fig.update_traces(
                line_color="#38bdf8",
                line_width=3,
                marker_size=9,
            )

            st.plotly_chart(
                plot_style(fig),
                use_container_width=True,
            )

        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("Revenue by Product")

            revenue_by_product = (
                frame.groupby(
                    "product_name",
                    as_index=False,
                )["total_amount"]
                .sum()
            )

            fig = px.bar(
                revenue_by_product,
                x="product_name",
                y="total_amount",
                labels={
                    "product_name": "Product",
                    "total_amount": "Revenue (₹)",
                },
                color_discrete_sequence=[
                    "#3b82f6"
                ],
            )

            st.plotly_chart(
                plot_style(fig),
                use_container_width=True,
            )

        with right:
            st.subheader("Units Sold by Product")

            units_by_product = (
                frame.groupby(
                    "product_name",
                    as_index=False,
                )["quantity"]
                .sum()
            )

            fig = px.bar(
                units_by_product,
                x="product_name",
                y="quantity",
                labels={
                    "product_name": "Product",
                    "quantity": "Units Sold",
                },
                color_discrete_sequence=[
                    "#34d399"
                ],
            )

            st.plotly_chart(
                plot_style(fig),
                use_container_width=True,
            )

        st.divider()

        st.subheader("Transaction Data")

        show_table(
            frame.to_dict("records"),
            [
                "id",
                "product_name",
                "quantity",
                "total_amount",
                "sold_at",
            ],
        )

    else:
        info_message(
            "No sales have been recorded yet. "
            "Record a sale to unlock analytics."
        )


# ============================================================
# AI FORECASTING PAGE
# ============================================================

elif page == "🧠 AI Forecasting":
    st.title("Demand Forecasting")

    st.markdown(
        '<p class="muted">'
        'Data-driven inventory planning, stockout '
        'risk and reorder recommendations.'
        '</p>',
        unsafe_allow_html=True,
    )

    info_message(
        "Forecasts use historical sales averages. "
        "They are statistical estimates, not "
        "guarantees or predictions from a trained "
        "machine-learning model."
    )

    products = load_data("/products")

    if products is None:
        st.stop()

    if not products:
        warning_message(
            "Add products to generate demand forecasts."
        )
        st.stop()

    options = product_options(products)

    selected = st.selectbox(
        "Select Product",
        list(options.keys()),
    )

    product = options[selected]

    forecast_days = st.slider(
        "Forecast Period (Days)",
        min_value=1,
        max_value=90,
        value=30,
    )

    lead_time_days = st.slider(
        "Supplier Lead Time (Days)",
        min_value=1,
        max_value=30,
        value=7,
    )

    history_days = st.slider(
        "Historical Sales Window (Days)",
        min_value=7,
        max_value=180,
        value=30,
    )

    st.divider()

    if st.button(
        "Generate Demand Forecast",
        type="primary",
    ):
        try:
            result = api_request(
                "GET",
                f"/forecast/{product['id']}",
                params={
                    "forecast_days": forecast_days,
                    "lead_time_days": lead_time_days,
                    "history_days": history_days,
                },
            )

            st.session_state[
                "forecast_result"
            ] = result

            st.session_state[
                "forecast_product_id"
            ] = product["id"]

        except RuntimeError as exc:
            error_message(str(exc))

    if (
        "forecast_result" in st.session_state
        and st.session_state.get(
            "forecast_product_id"
        ) == product["id"]
    ):
        forecast = st.session_state[
            "forecast_result"
        ]

        st.divider()

        st.subheader("Forecast Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            metric_card(
                "Current Stock",
                forecast.get(
                    "current_stock",
                    0,
                ),
            )

        with col2:
            metric_card(
                "Predicted Demand",
                forecast.get(
                    "predicted_units_needed",
                    0,
                ),
            )

        with col3:
            metric_card(
                "Reorder Quantity",
                forecast.get(
                    "recommended_reorder_quantity",
                    0,
                ),
            )

        with col4:
            metric_card(
                "Stockout Risk",
                forecast.get(
                    "stockout_risk",
                    "UNKNOWN",
                ),
            )

        st.divider()

        st.subheader("Demand Analysis")

        daily_demand = float(
            forecast.get(
                "average_daily_demand",
                0,
            )
        )

        predicted = int(
            forecast.get(
                "predicted_units_needed",
                0,
            )
        )

        current = int(
            forecast.get(
                "current_stock",
                0,
            )
        )

        chart = go.Figure()

        chart.add_trace(
            go.Bar(
                x=[
                    "Current Stock",
                    "Forecast Demand",
                ],
                y=[
                    current,
                    predicted,
                ],
                marker_color=[
                    "#3b82f6",
                    "#f59e0b",
                ],
                text=[
                    current,
                    predicted,
                ],
                textposition="outside",
            )
        )

        chart.update_layout(
            yaxis_title="Units",
            showlegend=False,
        )

        st.plotly_chart(
            plot_style(chart),
            use_container_width=True,
        )

        st.markdown(
            f"**Average Daily Demand:** "
            f"{daily_demand:.2f} units"
        )

        days_until_stockout = forecast.get(
            "estimated_days_until_stockout"
        )

        if days_until_stockout is None:
            st.markdown(
                "**Estimated Days Until Stockout:** "
                "Insufficient sales history"
            )
        else:
            st.markdown(
                "**Estimated Days Until Stockout:** "
                f"{days_until_stockout} days"
            )

        st.markdown(
            "**Forecast Method:** "
            f"{forecast.get('forecast_method', 'N/A')}"
        )

        risk = forecast.get(
            "stockout_risk",
            "LOW",
        )

        if risk in [
            "HIGH",
            "OUT_OF_STOCK",
        ]:
            warning_message(
                "High stockout risk detected. "
                "Consider replenishing inventory."
            )
        elif risk == "MEDIUM":
            warning_message(
                "Moderate stockout risk. "
                "Monitor inventory closely."
            )
        else:
            success_message(
                "Inventory is currently at low "
                "stockout risk."
            )

        reorder = forecast.get(
            "recommended_reorder_quantity",
            0,
        )

        if reorder > 0:
            info_message(
                f"Recommended reorder quantity: "
                f"{reorder} units."
            )
        else:
            success_message(
                "No immediate reorder is recommended "
                "under the current forecasting assumptions."
            )

        st.caption(
            forecast.get(
                "note",
                "Forecasts are estimates based on "
                "recorded sales.",
            )
        )

    st.divider()

    st.subheader("Stock Risk Summary")

    recommendations = load_data(
        "/recommendations"
    )

    if recommendations is not None:
        if recommendations:
            summary = []

            for item in recommendations:
                summary.append(
                    {
                        "Product": item.get(
                            "product_name"
                        ),
                        "Current Stock": item.get(
                            "current_stock"
                        ),
                        "Risk": item.get(
                            "stockout_risk"
                        ),
                        "Predicted Demand": item.get(
                            "predicted_units_needed"
                        ),
                        "Recommended Reorder": item.get(
                            "recommended_reorder_quantity"
                        ),
                    }
                )

            show_table(summary)

        else:
            info_message(
                "No stock recommendations available."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    'InventoryIQ | Inventory Management '
    'and Demand Intelligence'
    '</div>',
    unsafe_allow_html=True,
)
