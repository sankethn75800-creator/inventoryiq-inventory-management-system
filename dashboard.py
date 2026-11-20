
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st


# ============================================================
# INVENTORYIQ | INVENTORY INTELLIGENCE PLATFORM
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

API_URL = os.getenv("API_URL", DEFAULT_API_URL).rstrip("/")

try:
    API_URL = str(st.secrets.get("API_URL", API_URL)).rstrip("/")
except (FileNotFoundError, KeyError):
    pass


# ============================================================
# FINAL DARK THEME
# ============================================================

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #080f1f !important;
        color: #f8fafc !important;
    }

    [data-testid="stHeader"] {
        background-color: #080f1f !important;
    }

    .block-container {
        max-width: 1500px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin: 0 auto !important;
    }

    [data-testid="stSidebar"] {
        background-color: #101b30 !important;
        border-right: 1px solid #304363 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 7px !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        opacity: 1 !important;
        font-weight: 700 !important;
        letter-spacing: -0.4px;
    }

    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }

    [data-testid="stMain"] p,
    [data-testid="stMain"] label {
        color: #e2e8f0;
    }

    [data-testid="stCaptionContainer"] p {
        color: #cbd5e1 !important;
        opacity: 1 !important;
    }

    /* Metric cards: no forced overflow on parent containers */

    [data-testid="stMetric"] {
        background-color: #192740 !important;
        border: 1px solid #34445f !important;
        border-radius: 14px !important;
        padding: 20px !important;
        min-height: 135px;
    }

    [data-testid="stMetricLabel"] p {
        color: #cbd5e1 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: clamp(1.25rem, 2vw, 2rem) !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] > div {
        color: #ffffff !important;
    }

    [data-testid="stMetricDelta"] {
        color: #34d399 !important;
    }

    [data-testid="stForm"] {
        background-color: #14233b !important;
        border: 1px solid #304363 !important;
        border-radius: 14px !important;
        padding: 20px !important;
    }

    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button {
        background-color: #1c2b45 !important;
        color: #ffffff !important;
        border: 1px solid #425575 !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background-color: #263b5e !important;
        border-color: #60a5fa !important;
    }

    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div,
    [data-baseweb="textarea"] > div {
        background-color: #1b2a44 !important;
        color: #ffffff !important;
        border-color: #425575 !important;
    }

    [data-baseweb="input"] input,
    [data-baseweb="select"] input,
    [data-baseweb="textarea"] textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    [data-baseweb="input"] input::placeholder {
        color: #aebed3 !important;
        -webkit-text-fill-color: #aebed3 !important;
    }

    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: #ffffff !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"] {
        background-color: #1b2a44 !important;
        color: #ffffff !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #344762 !important;
        border-radius: 12px !important;
    }

    [data-testid="stTabs"] button {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #60a5fa !important;
    }

    [data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] {
        background-color: #14233b !important;
        border: 1px solid #344762 !important;
        border-radius: 10px !important;
    }

    hr {
        border-color: #304363 !important;
    }

    a {
        color: #93c5fd !important;
    }

    .iq-brand {
        color: #ffffff !important;
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -0.6px;
        margin-bottom: 8px;
    }

    .iq-subtitle {
        color: #cbd5e1 !important;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.8px;
        margin-bottom: 24px;
    }

    .iq-status {
        background-color: #064e3b;
        color: #ffffff !important;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 15px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .iq-error {
        background-color: #450a0a;
        color: #ffffff !important;
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 15px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .iq-info {
        background-color: #172554;
        color: #ffffff !important;
        border: 1px solid #3b82f6;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }

    .iq-footer {
        color: #cbd5e1 !important;
        font-size: 13px;
        margin-top: 24px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        h1 {
            font-size: 2rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API HELPERS
# ============================================================

def api_request(method, endpoint, **kwargs):
    url = f"{API_URL}{endpoint}"

    try:
        response = requests.request(
            method,
            url,
            timeout=65,
            **kwargs,
        )

        if response.status_code >= 400:
            try:
                body = response.json()
                detail = body.get("detail", response.text)
            except (ValueError, AttributeError):
                detail = response.text

            raise RuntimeError(
                f"API error {response.status_code}: {detail}"
            )

        if not response.content:
            return {}

        return response.json()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "The backend took too long to respond. "
            "Render may be waking up. Please retry."
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to the backend API. "
            "Check the Render service."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Network error: {exc}"
        ) from exc

    except ValueError as exc:
        raise RuntimeError(
            "The API returned an invalid JSON response."
        ) from exc


def get_products(search=None):
    params = {"search": search} if search else None
    return api_request(
        "GET",
        "/products",
        params=params,
    )


def get_sales():
    return api_request("GET", "/sales")


def get_dashboard():
    return api_request("GET", "/dashboard")


def get_forecast(
    product_id,
    history_days=30,
    forecast_days=7,
    lead_time_days=3,
):
    return api_request(
        "GET",
        f"/forecast/{product_id}",
        params={
            "history_days": history_days,
            "forecast_days": forecast_days,
            "lead_time_days": lead_time_days,
        },
    )


def get_recommendations():
    return api_request("GET", "/recommendations")


def money(value):
    return f"₹{float(value or 0):,.2f}"


def show_error(exc):
    st.error(str(exc))


def product_options(products):
    return {
        f"{p['id']} - {p['name']}": p
        for p in products
    }


# ============================================================
# CHART DESIGN
# ============================================================

def style_chart(fig, height=370):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#080f1f",
        plot_bgcolor="#192740",
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="#ffffff",
        ),
        height=height,
        margin=dict(
            l=35,
            r=35,
            t=45,
            b=45,
        ),
        legend=dict(
            font=dict(
                color="#ffffff",
                size=13,
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            tickfont=dict(color="#ffffff"),
            title_font=dict(color="#ffffff"),
            gridcolor="#304363",
            zerolinecolor="#425575",
        ),
        yaxis=dict(
            tickfont=dict(color="#ffffff"),
            title_font=dict(color="#ffffff"),
            gridcolor="#304363",
            zerolinecolor="#425575",
        ),
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="iq-brand">◇ InventoryIQ</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="iq-subtitle">'
        'INVENTORY INTELLIGENCE PLATFORM'
        '</div>',
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
        health = api_request("GET", "/")
        connected = health.get("status") == "running"
    except RuntimeError:
        connected = False

    if connected:
        st.markdown(
            '<div class="iq-status">● API Connected</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="iq-error">● API Disconnected</div>',
            unsafe_allow_html=True,
        )

    if st.button(
        "Refresh Dashboard",
        use_container_width=True,
    ):
        st.rerun()

    st.caption("InventoryIQ • v3.0")

    st.markdown(
        '<div class="iq-footer">'
        'Backend: Render API'
        '</div>',
        unsafe_allow_html=True,
    )

    st.link_button(
        "Open API Documentation",
        f"{API_URL}/docs",
        use_container_width=True,
    )


# ============================================================
# PAGE 1 - INVENTORY OVERVIEW
# ============================================================

if page == "📊 Overview":

    st.title("Inventory Overview")

    st.caption(
        "Real-time visibility into stock, "
        "revenue and business performance."
    )

    try:
        data = get_dashboard()
        products = get_products()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Total Products",
                data.get("total_products", 0),
            )

        with c2:
            st.metric(
                "Available Units",
                data.get("total_stock_units", 0),
            )

        with c3:
            st.metric(
                "Inventory Value",
                money(data.get("inventory_value", 0)),
            )

        with c4:
            st.metric(
                "Sales Revenue",
                money(data.get("total_sales_revenue", 0)),
            )

        st.divider()

        left, right = st.columns([1.6, 1])

        with left:
            st.subheader("Inventory Distribution")

            if products:
                df = pd.DataFrame(products)

                fig = px.bar(
                    df,
                    x="name",
                    y="quantity",
                    color_discrete_sequence=["#3b82f6"],
                    labels={
                        "name": "Product",
                        "quantity": "Stock",
                    },
                )

                fig.update_traces(
                    text=df["quantity"],
                    textposition="outside",
                    textfont_color="#ffffff",
                    cliponaxis=False,
                )

                fig.update_layout(
                    showlegend=False,
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )
            else:
                st.info("No products available yet.")

        with right:
            st.subheader("Stock Health")

            low_stock = int(
                data.get("low_stock_count", 0)
            )

            total = int(
                data.get("total_products", 0)
            )

            healthy = max(total - low_stock, 0)

            if total > 0:
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=[
                                "Healthy",
                                "Low / Out of Stock",
                            ],
                            values=[
                                healthy,
                                low_stock,
                            ],
                            hole=0.65,
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
                    legend=dict(
                        orientation="h",
                        y=-0.1,
                        x=0.5,
                        xanchor="center",
                    )
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )
            else:
                st.info(
                    "Add products to view stock health."
                )

        st.divider()
        st.subheader("Low Stock Alerts")

        low_products = data.get(
            "low_stock_products",
            [],
        )

        if low_products:
            st.warning(
                f"{len(low_products)} product(s) "
                "need attention."
            )

            st.dataframe(
                pd.DataFrame(low_products),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success(
                "All products are above their "
                "low-stock thresholds."
            )

    except RuntimeError as exc:
        show_error(exc)


# ============================================================
# PAGE 2 - PRODUCT MANAGEMENT
# ============================================================

elif page == "📦 Products":

    st.title("Product Management")

    st.caption(
        "Add, update, search and manage inventory."
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "View Products",
            "Add Product",
            "Update Product",
            "Delete Product",
        ]
    )

    # VIEW PRODUCTS

    with tab1:
        st.subheader("Product Inventory")

        search = st.text_input(
            "Search Products",
            placeholder="Enter product name",
        )

        try:
            products = get_products(search)

            if products:
                st.dataframe(
                    pd.DataFrame(products),
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    f"{len(products)} product(s) found."
                )
            else:
                st.info("No matching products found.")

        except RuntimeError as exc:
            show_error(exc)

    # ADD PRODUCT

    with tab2:
        st.subheader("Add New Product")

        with st.form("add_product_form"):

            name = st.text_input("Product Name")

            price = st.number_input(
                "Unit Price (₹)",
                min_value=0.0,
                value=100.0,
                step=1.0,
            )

            quantity = st.number_input(
                "Initial Quantity",
                min_value=0,
                value=10,
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
                try:
                    result = api_request(
                        "POST",
                        "/products",
                        json={
                            "name": name.strip(),
                            "price": float(price),
                            "quantity": int(quantity),
                            "low_stock_threshold": int(
                                threshold
                            ),
                        },
                    )

                    st.success(
                        "Product added successfully! "
                        f"ID: {result.get('id')}"
                    )

                except RuntimeError as exc:
                    show_error(exc)

    # UPDATE PRODUCT

    with tab3:
        st.subheader("Update Product")

        try:
            products = get_products()
            options = product_options(products)

            if options:
                selected = st.selectbox(
                    "Select Product to Update",
                    list(options),
                )

                product = options[selected]

                with st.form("update_product_form"):

                    new_name = st.text_input(
                        "Product Name",
                        value=product["name"],
                    )

                    new_price = st.number_input(
                        "Price (₹)",
                        min_value=0.0,
                        value=float(product["price"]),
                    )

                    new_quantity = st.number_input(
                        "Quantity",
                        min_value=0,
                        value=int(product["quantity"]),
                    )

                    new_threshold = st.number_input(
                        "Low Stock Threshold",
                        min_value=0,
                        value=int(
                            product["low_stock_threshold"]
                        ),
                    )

                    update_clicked = (
                        st.form_submit_button(
                            "Save Changes",
                            type="primary",
                        )
                    )

                if update_clicked:
                    if not new_name.strip():
                        st.error(
                            "Product name cannot be empty."
                        )
                    else:
                        try:
                            api_request(
                                "PUT",
                                f"/products/{product['id']}",
                                json={
                                    "name": new_name.strip(),
                                    "price": float(new_price),
                                    "quantity": int(
                                        new_quantity
                                    ),
                                    "low_stock_threshold": int(
                                        new_threshold
                                    ),
                                },
                            )

                            st.success(
                                "Product updated successfully."
                            )

                        except RuntimeError as exc:
                            show_error(exc)
            else:
                st.info("No products available.")

        except RuntimeError as exc:
            show_error(exc)

    # DELETE PRODUCT

    with tab4:
        st.subheader("Delete Product")

        st.warning(
            "Products with existing sales history "
            "cannot be deleted."
        )

        try:
            products = get_products()
            options = product_options(products)

            if options:
                selected = st.selectbox(
                    "Select Product to Delete",
                    list(options),
                    key="delete_product",
                )

                product = options[selected]

                confirm = st.checkbox(
                    "I confirm that I want to delete "
                    "this product."
                )

                if st.button(
                    "Delete Product",
                    type="primary",
                    disabled=not confirm,
                ):
                    try:
                        api_request(
                            "DELETE",
                            f"/products/{product['id']}",
                        )

                        st.success(
                            "Product deleted successfully."
                        )

                    except RuntimeError as exc:
                        show_error(exc)
            else:
                st.info("No products available.")

        except RuntimeError as exc:
            show_error(exc)


# ============================================================
# PAGE 3 - SALES MANAGEMENT
# ============================================================

elif page == "🛒 Sales":

    st.title("Sales Management")

    st.caption(
        "Record transactions and automatically "
        "update inventory stock."
    )

    try:
        products = get_products()
        options = product_options(products)

        if options:

            st.subheader("Record New Sale")

            selected = st.selectbox(
                "Select Product",
                list(options),
                key="sale_product",
            )

            product = options[selected]
            available = int(product["quantity"])

            quantity = st.number_input(
                "Quantity to Sell",
                min_value=1,
                value=1,
                step=1,
            )

            st.write(
                f"**Unit Price:** "
                f"{money(product['price'])}"
            )

            st.write(
                f"**Available Stock:** {available}"
            )

            estimated_total = (
                float(product["price"]) * quantity
            )

            st.info(
                "Estimated Sale Total: "
                f"{money(estimated_total)}"
            )

            if st.button(
                "Record Sale",
                type="primary",
            ):

                if quantity > available:
                    st.error(
                        "Insufficient stock. "
                        f"Only {available} units available."
                    )
                else:
                    try:
                        result = api_request(
                            "POST",
                            "/sales",
                            json={
                                "product_id": int(
                                    product["id"]
                                ),
                                "quantity": int(quantity),
                            },
                        )

                        st.success(
                            "Sale recorded successfully!"
                        )

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.metric(
                                "Sale ID",
                                result.get("sale_id", "-"),
                            )

                        with c2:
                            st.metric(
                                "Revenue",
                                money(
                                    result.get(
                                        "total_amount", 0
                                    )
                                ),
                            )

                        with c3:
                            st.metric(
                                "Remaining Stock",
                                result.get(
                                    "remaining_stock", 0
                                ),
                            )

                    except RuntimeError as exc:
                        show_error(exc)
        else:
            st.info(
                "Add a product before recording sales."
            )

        st.divider()
        st.subheader("Sales History")

        sales = get_sales()

        if sales:
            df = pd.DataFrame(sales)

            if "sold_at" in df.columns:
                df["sold_at"] = pd.to_datetime(
                    df["sold_at"],
                    errors="coerce",
                )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(
                "No sales transactions recorded."
            )

    except RuntimeError as exc:
        show_error(exc)


# ============================================================
# PAGE 4 - SALES ANALYTICS
# ============================================================

elif page == "📈 Analytics":

    st.title("Sales Analytics")

    st.caption(
        "Understand sales trends and "
        "inventory performance."
    )

    try:
        dashboard_data = get_dashboard()
        sales = get_sales()
        products = get_products()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Revenue",
                money(
                    dashboard_data.get(
                        "total_sales_revenue", 0
                    )
                ),
            )

        with c2:
            st.metric(
                "Transactions",
                len(sales),
            )

        with c3:
            st.metric(
                "Inventory Value",
                money(
                    dashboard_data.get(
                        "inventory_value", 0
                    )
                ),
            )

        st.divider()

        if sales:

            df = pd.DataFrame(sales)

            df["sold_at"] = pd.to_datetime(
                df["sold_at"],
                errors="coerce",
            )

            df["total_amount"] = pd.to_numeric(
                df["total_amount"],
                errors="coerce",
            ).fillna(0)

            df["quantity"] = pd.to_numeric(
                df["quantity"],
                errors="coerce",
            ).fillna(0)

            product_names = {
                p["id"]: p["name"]
                for p in products
            }

            df["product_name"] = df[
                "product_id"
            ].map(product_names).fillna(
                "Unknown Product"
            )

            left, right = st.columns(2)

            with left:
                st.subheader("Daily Sales Revenue")

                valid_dates = df.dropna(
                    subset=["sold_at"]
                ).copy()

                if not valid_dates.empty:

                    valid_dates["date"] = (
                        valid_dates["sold_at"].dt.date
                    )

                    daily = (
                        valid_dates.groupby(
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
                        marker_color="#60a5fa",
                    )

                    st.plotly_chart(
                        style_chart(fig),
                        use_container_width=True,
                    )
                else:
                    st.info(
                        "No valid sales dates available."
                    )

            with right:
                st.subheader("Revenue by Product")

                revenue_by_product = (
                    df.groupby(
                        "product_name",
                        as_index=False,
                    )["total_amount"]
                    .sum()
                )

                fig = px.bar(
                    revenue_by_product,
                    x="product_name",
                    y="total_amount",
                    color_discrete_sequence=[
                        "#34d399"
                    ],
                    labels={
                        "product_name": "Product",
                        "total_amount": "Revenue (₹)",
                    },
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )

            st.divider()
            st.subheader("Transaction Data")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Download Sales Report",
                data=csv,
                file_name="inventoryiq_sales.csv",
                mime="text/csv",
            )

        else:
            st.info(
                "Record sales to generate analytics."
            )

    except RuntimeError as exc:
        show_error(exc)


# ============================================================
# PAGE 5 - AI FORECASTING
# ============================================================

elif page == "🧠 AI Forecasting":

    st.title("Demand Forecasting")

    st.caption(
        "Data-driven inventory planning "
        "and reorder recommendations."
    )

    st.markdown(
        '<div class="iq-info">'
        'Forecasts are statistical estimates based '
        'on recorded sales, not guarantees of '
        'future demand or predictions from a '
        'trained machine-learning model.'
        '</div>',
        unsafe_allow_html=True,
    )

    try:
        products = get_products()
        options = product_options(products)

        if options:

            selected = st.selectbox(
                "Select Product",
                list(options),
            )

            product = options[selected]

            history_days = st.slider(
                "Sales History Period (Days)",
                min_value=7,
                max_value=365,
                value=30,
            )

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

            st.divider()

            forecast_key = (
                product["id"],
                history_days,
                forecast_days,
                lead_time_days,
            )

            if st.button(
                "Generate Demand Forecast",
                type="primary",
            ):
                try:
                    forecast = get_forecast(
                        product["id"],
                        history_days=history_days,
                        forecast_days=forecast_days,
                        lead_time_days=lead_time_days,
                    )

                    st.session_state["forecast_result"] = (
                        forecast
                    )

                    st.session_state["forecast_key"] = (
                        forecast_key
                    )

                except RuntimeError as exc:
                    show_error(exc)

            saved_forecast = st.session_state.get(
                "forecast_result"
            )

            saved_key = st.session_state.get(
                "forecast_key"
            )

            if (
                saved_forecast is not None
                and saved_key == forecast_key
            ):

                forecast = saved_forecast

                st.subheader(
                    f"Forecast: {product['name']}"
                )

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric(
                        "Current Stock",
                        forecast.get(
                            "current_stock", 0
                        ),
                    )

                with c2:
                    st.metric(
                        "Predicted Demand",
                        forecast.get(
                            "predicted_units_needed", 0
                        ),
                    )

                with c3:
                    st.metric(
                        "Daily Demand",
                        forecast.get(
                            "average_daily_demand", 0
                        ),
                    )

                with c4:
                    st.metric(
                        "Recommended Reorder",
                        forecast.get(
                            "recommended_reorder_quantity",
                            0,
                        ),
                    )

                risk = forecast.get(
                    "stockout_risk", "UNKNOWN"
                )

                st.subheader("Stockout Risk")

                if risk in [
                    "HIGH",
                    "OUT_OF_STOCK",
                ]:
                    st.error(
                        f"Stockout Risk: {risk}"
                    )

                elif risk == "MEDIUM":
                    st.warning(
                        f"Stockout Risk: {risk}"
                    )

                else:
                    st.success(
                        f"Stockout Risk: {risk}"
                    )

                days_remaining = forecast.get(
                    "estimated_days_until_stockout"
                )

                if days_remaining is not None:
                    st.write(
                        "**Estimated Days Until "
                        "Stockout:** "
                        f"{days_remaining}"
                    )

                st.divider()

                st.subheader(
                    "Stock vs Predicted Demand"
                )

                chart_df = pd.DataFrame(
                    {
                        "Category": [
                            "Current Stock",
                            "Predicted Demand",
                            "Recommended Reorder",
                        ],
                        "Units": [
                            forecast.get(
                                "current_stock", 0
                            ),
                            forecast.get(
                                "predicted_units_needed",
                                0,
                            ),
                            forecast.get(
                                "recommended_reorder_quantity",
                                0,
                            ),
                        ],
                    }
                )

                fig = px.bar(
                    chart_df,
                    x="Category",
                    y="Units",
                    color="Category",
                    color_discrete_map={
                        "Current Stock": "#3b82f6",
                        "Predicted Demand": "#f59e0b",
                        "Recommended Reorder": "#34d399",
                    },
                )

                fig.update_layout(
                    showlegend=False
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                )

                st.subheader(
                    "Forecast Explanation"
                )

                st.info(
                    forecast.get(
                        "note",
                        "Forecast based on "
                        "historical sales.",
                    )
                )

                with st.expander(
                    "View Detailed Forecast Data"
                ):
                    st.json(forecast)

        else:
            st.info(
                "Add products to generate forecasts."
            )

        st.divider()
        st.subheader("Stock Risk Summary")

        if products:
            risk_data = []

            for p in products:

                qty = int(p["quantity"])
                threshold = int(
                    p["low_stock_threshold"]
                )

                if qty == 0:
                    risk_status = "Out of Stock"
                elif qty <= threshold:
                    risk_status = "Low Stock"
                else:
                    risk_status = "Healthy"

                risk_data.append(
                    {
                        "Product": p["name"],
                        "Current Stock": qty,
                        "Threshold": threshold,
                        "Status": risk_status,
                    }
                )

            st.dataframe(
                pd.DataFrame(risk_data),
                use_container_width=True,
                hide_index=True,
            )

        st.divider()
        st.subheader("Reorder Recommendations")

        if st.button(
            "Generate All Recommendations"
        ):
            try:
                recommendations = (
                    get_recommendations()
                )

                st.session_state[
                    "all_recommendations"
                ] = recommendations

            except RuntimeError as exc:
                show_error(exc)

        recommendations = st.session_state.get(
            "all_recommendations"
        )

        if recommendations is not None:
            if recommendations:
                st.dataframe(
                    pd.DataFrame(
                        recommendations
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "No recommendations available."
                )

    except RuntimeError as exc:
        show_error(exc)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="iq-footer">'
    'InventoryIQ | Inventory Management '
    'and Demand Intelligence'
    '</div>',
    unsafe_allow_html=True,
)
