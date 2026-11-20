
import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="InventoryIQ | Inventory Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_API_URL = (
    "https://inventoryiq-inventory-management-system.onrender.com"
)

API_URL = str(
    st.secrets.get(
        "API_BASE_URL",
        os.getenv("API_BASE_URL", DEFAULT_API_URL)
    )
).rstrip("/")


# ==========================================
# PROFESSIONAL DARK THEME
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background-color: #111B2E;
}

h1, h2, h3 {
    color: #FFFFFF !important;
}

[data-testid="stMetric"] {
    background: #17243B;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] p,
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

div[data-testid="stForm"] {
    background: #17243B;
    border: 1px solid #475569;
    border-radius: 12px;
    padding: 20px;
}

[data-testid="stWidgetLabel"] p {
    color: #F8FAFC !important;
    font-weight: 600;
}

[data-testid="stAlert"] p {
    color: inherit !important;
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
""", unsafe_allow_html=True)


# ==========================================
# API HELPERS
# ==========================================

def api_request(method, endpoint, data=None, params=None):
    try:
        response = requests.request(
            method=method,
            url=f"{API_URL}{endpoint}",
            json=data,
            params=params,
            timeout=75
        )

        response.raise_for_status()

        if not response.content:
            return {}

        return response.json()

    except requests.exceptions.HTTPError as error:
        response = error.response

        try:
            detail = response.json().get(
                "detail", response.text
            )
        except (ValueError, AttributeError):
            detail = response.text

        raise RuntimeError(
            f"API error {response.status_code}: {detail}"
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Backend connection failed: {error}"
        ) from error


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
            data=payload
        )
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
    return str(product.get("name", "Unnamed Product"))


def stock_status(product):
    quantity = int(product.get("quantity", 0))
    threshold = int(
        product.get("low_stock_threshold", 10)
    )

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
            hide_index=True
        )
    else:
        st.info("No records available.")


def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#17243B",
        font_color="#F8FAFC",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    return fig


# ==========================================
# SIDEBAR
# ==========================================

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
            "🧠 AI Forecasting"
        ],
        label_visibility="collapsed"
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

    if st.button(
        "Refresh Dashboard",
        use_container_width=True
    ):
        st.rerun()

    st.caption("InventoryIQ • v2.1")
    st.caption(f"Backend: {API_URL}")


if not connected:
    st.error(
        "Backend unavailable. Check your Render service."
    )
    st.stop()


# ==========================================
# LOAD LIVE DATA
# ==========================================

products_response = get_data("/products")

if products_response is None:
    st.stop()

products = normalize_list(
    products_response, "products"
)

sales_response = get_data("/sales")

if sales_response is None:
    st.stop()

sales = normalize_list(sales_response, "sales")

total_products = len(products)

available_units = sum(
    int(p.get("quantity", 0))
    for p in products
)

inventory_value = sum(
    float(p.get("price", 0))
    * int(p.get("quantity", 0))
    for p in products
)

sales_revenue = sum(
    float(s.get("total_amount", 0))
    for s in sales
)

total_units_sold = sum(
    int(s.get("quantity", 0))
    for s in sales
)

low_stock_products = [
    p for p in products
    if int(p.get("quantity", 0))
    <= int(p.get("low_stock_threshold", 10))
]


# ==========================================
# OVERVIEW
# ==========================================

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
            chart_data = pd.DataFrame([
                {
                    "Product": product_name(p),
                    "Stock": int(p.get("quantity", 0))
                }
                for p in products
            ])

            fig = px.bar(
                chart_data,
                x="Product",
                y="Stock",
                color="Product"
            )

            fig.update_layout(showlegend=False)

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        else:
            st.info("Add products to view inventory.")

    with right:
        st.subheader("Stock Health")

        healthy = (
            total_products - len(low_stock_products)
        )

        if total_products:
            fig = px.pie(
                names=[
                    "Healthy",
                    "Low / Out of Stock"
                ],
                values=[
                    healthy,
                    len(low_stock_products)
                ],
                hole=0.65,
                color_discrete_sequence=[
                    "#34D399",
                    "#FB7185"
                ]
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        else:
            st.info("No stock data available.")

    st.subheader("Inventory Alerts")

    if low_stock_products:
        for product in low_stock_products:
            st.warning(
                f"{product_name(product)}: "
                f"{product.get('quantity', 0)} "
                "units remaining"
            )
    else:
        st.success(
            "All products are above their stock thresholds."
        )

    st.subheader("Recent Transactions")

    recent_sales = sorted(
        sales,
        key=lambda s: s.get("sold_at") or "",
        reverse=True
    )[:10]

    display_table(recent_sales)


# ==========================================
# PRODUCT MANAGEMENT
# ==========================================

elif page == "📦 Products":

    st.title("Product Management")
    st.caption("Organize and control your inventory.")

    c1, c2, c3 = st.columns(3)

    c1.metric("Products", total_products)
    c2.metric(
        "Low Stock Alerts",
        len(low_stock_products)
    )
    c3.metric(
        "Inventory Value",
        money(inventory_value)
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Product Catalog",
        "Add Product",
        "Edit Product",
        "Delete Product"
    ])

    # PRODUCT CATALOG

    with tab1:

        st.subheader("Product Catalog")

        search = st.text_input(
            "Search Products",
            placeholder="Enter product name"
        )

        filtered = [
            p for p in products
            if search.lower()
            in product_name(p).lower()
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
                "Status": stock_status(p)
            }
            for p in filtered
        ]

        display_table(table_data)

    # ADD PRODUCT

    with tab2:

        st.subheader("Create New Product")

        with st.form("add_product_form"):

            name = st.text_input("Product Name")

            price = st.number_input(
                "Price (₹)",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

            quantity = st.number_input(
                "Initial Stock",
                min_value=0,
                value=0,
                step=1
            )

            threshold = st.number_input(
                "Low Stock Threshold",
                min_value=0,
                value=5,
                step=1
            )

            submitted = st.form_submit_button(
                "Add Product",
                type="primary"
            )

            if submitted:

                if not name.strip():
                    st.error(
                        "Product name is required."
                    )
                else:
                    payload = {
                        "name": name.strip(),
                        "price": float(price),
                        "quantity": int(quantity),
                        "low_stock_threshold": int(threshold)
                    }

                    result = perform_action(
                        "POST",
                        "/products",
                        payload
                    )

                    if result is not None:
                        st.success(
                            "Product added successfully."
                        )
                        st.rerun()

    # EDIT PRODUCT

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
                key="edit_product"
            )

            current = options[selected]

            with st.form(
                f"edit_form_{current['id']}"
            ):

                updated_name = st.text_input(
                    "Product Name",
                    value=product_name(current)
                )

                updated_price = st.number_input(
                    "Price (₹)",
                    min_value=0.0,
                    value=float(
                        current.get("price", 0)
                    )
                )

                updated_quantity = st.number_input(
                    "Stock Quantity",
                    min_value=0,
                    value=int(
                        current.get("quantity", 0)
                    )
                )

                updated_threshold = st.number_input(
                    "Low Stock Threshold",
                    min_value=0,
                    value=int(
                        current.get(
                            "low_stock_threshold", 10
                        )
                    )
                )

                submitted = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

                if submitted:

                    if not updated_name.strip():
                        st.error(
                            "Product name cannot be empty."
                        )
                    else:
                        payload = {
                            "name": updated_name.strip(),
                            "price": float(updated_price),
                            "quantity": int(
                                updated_quantity
                            ),
                            "low_stock_threshold": int(
                                updated_threshold
                            )
                        }

                        result = perform_action(
                            "PUT",
                            f"/products/{current['id']}",
                            payload
                        )

                        if result is not None:
                            st.success(
                                "Product updated successfully."
                            )
                            st.rerun()

        else:
            st.info("Add a product first.")

    # DELETE PRODUCT

    with tab4:

        st.subheader("Delete Product")

        if products:

            options = {
                f"{p['id']} - {product_name(p)}": p
                for p in products
            }

            selected = st.selectbox(
                "Choose Product",
                list(options.keys()),
                key="delete_product"
            )

            current = options[selected]

            st.warning(
                "Products with sales history cannot be "
                "deleted because their transaction records "
                "must be preserved."
            )

            confirm = st.checkbox(
                "I understand this action cannot be undone."
            )

            if st.button(
                "Delete Product",
                type="primary",
                disabled=not confirm
            ):

                result = perform_action(
                    "DELETE",
                    f"/products/{current['id']}"
                )

                if result is not None:
                    st.success(
                        "Product deleted successfully."
                    )
                    st.rerun()

        else:
            st.info("No products available.")


# ==========================================
# SALES MANAGEMENT
# ==========================================

elif page == "🛒 Sales":

    st.title("Sales Management")

    st.caption(
        "Record transactions and track revenue."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Transactions", len(sales))
    c2.metric(
        "Total Revenue",
        money(sales_revenue)
    )
    c3.metric(
        "Units Sold",
        total_units_sold
    )

    st.divider()

    st.subheader("Record New Sale")

    available_products = [
        p for p in products
        if int(p.get("quantity", 0)) > 0
    ]

    if available_products:

        options = {
            f"{p['id']} - {product_name(p)}": p
            for p in available_products
        }

        selected = st.selectbox(
            "Select Product",
            list(options.keys())
        )

        selected_product = options[selected]

        max_stock = int(
            selected_product.get("quantity", 0)
        )

        with st.form("record_sale_form"):

            sale_quantity = st.number_input(
                "Quantity to Sell",
                min_value=1,
                max_value=max_stock,
                value=1,
                step=1
            )

            unit_price = float(
                selected_product.get("price", 0)
            )

            sale_total = (
                unit_price * int(sale_quantity)
            )

            st.write(
                f"Unit Price: {money(unit_price)}"
            )

            st.info(
                f"Estimated Sale Total: "
                f"{money(sale_total)}"
            )

            submitted = st.form_submit_button(
                "Record Sale",
                type="primary"
            )

            if submitted:

                payload = {
                    "product_id": int(
                        selected_product["id"]
                    ),
                    "quantity": int(sale_quantity)
                }

                result = perform_action(
                    "POST",
                    "/sales",
                    payload
                )

                if result is not None:
                    st.success(
                        "Sale recorded successfully."
                    )
                    st.rerun()

    elif products:
        st.warning(
            "All products are out of stock."
        )

    else:
        st.info(
            "Add products before recording sales."
        )

    st.divider()

    st.subheader("Sales History")

    display_table(
        sorted(
            sales,
            key=lambda s: s.get("sold_at") or "",
            reverse=True
        )
    )


# ==========================================
# SALES ANALYTICS
# ==========================================

elif page == "📈 Analytics":

    st.title("Sales Analytics")

    st.caption(
        "Understand sales and inventory performance."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Revenue",
        money(sales_revenue)
    )

    c2.metric(
        "Transactions",
        len(sales)
    )

    c3.metric(
        "Units Sold",
        total_units_sold
    )

    c4.metric(
        "Inventory Value",
        money(inventory_value)
    )

    st.divider()

    if sales:

        df = pd.DataFrame(sales)

        df["total_amount"] = pd.to_numeric(
            df["total_amount"],
            errors="coerce"
        ).fillna(0)

        df["quantity"] = pd.to_numeric(
            df["quantity"],
            errors="coerce"
        ).fillna(0)

        product_names = {
            str(p["id"]): product_name(p)
            for p in products
        }

        df["Product"] = (
            df["product_id"]
            .astype(str)
            .map(product_names)
            .fillna(
                df["product_id"].astype(str)
            )
        )

        grouped = (
            df.groupby(
                "Product",
                as_index=False
            )
            .agg(
                Revenue=("total_amount", "sum"),
                Units_Sold=("quantity", "sum")
            )
        )

        left, right = st.columns(2)

        # REVENUE BY PRODUCT

        with left:

            st.subheader("Revenue by Product")

            fig = px.bar(
                grouped,
                x="Product",
                y="Revenue",
                color="Product",
                labels={
                    "Revenue": "Revenue (₹)"
                }
            )

            fig.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        # UNITS SOLD BY PRODUCT

        with right:

            st.subheader("Units Sold by Product")

            fig = px.bar(
                grouped,
                x="Product",
                y="Units_Sold",
                color="Product",
                labels={
                    "Units_Sold": "Units Sold"
                }
            )

            fig.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        # REVENUE OVER TIME

        if "sold_at" in df.columns:

            df["Date"] = pd.to_datetime(
                df["sold_at"],
                errors="coerce",
                utc=True
            ).dt.date

            daily = (
                df.dropna(
                    subset=["Date"]
                )
                .groupby(
                    "Date",
                    as_index=False
                )["total_amount"]
                .sum()
            )

            if not daily.empty:

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

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True
                )

        st.subheader("Transaction History")

        if "sold_at" in df.columns:
            df = df.sort_values(
                "sold_at",
                ascending=False
            )

        display_table(
            df.to_dict("records")
        )

    else:

        st.info(
            "Record sales to generate analytics."
        )


# ==========================================
# DEMAND FORECASTING
# ==========================================

elif page == "🧠 AI Forecasting":

    st.title("Demand Forecasting")

    st.caption(
        "Data-driven inventory planning and "
        "reorder recommendations."
    )

    st.info(
        "Forecasts are statistical estimates based "
        "on recorded sales, not predictions from a "
        "trained machine-learning model."
    )

    if not products:

        st.warning(
            "Add products to generate forecasts."
        )

        st.stop()

    options = {
        f"{p['id']} - {product_name(p)}": p
        for p in products
    }

    selected = st.selectbox(
        "Select Product",
        list(options.keys())
    )

    selected_product = options[selected]

    history_days = st.slider(
        "Sales History (Days)",
        min_value=7,
        max_value=365,
        value=30
    )

    forecast_days = st.slider(
        "Forecast Period (Days)",
        min_value=7,
        max_value=90,
        value=30
    )

    lead_time = st.slider(
        "Supplier Lead Time (Days)",
        min_value=1,
        max_value=30,
        value=7
    )

    st.divider()

    if st.button(
        "Generate Demand Forecast",
        type="primary"
    ):

        try:

            forecast = api_request(
                "GET",
                f"/forecast/{selected_product['id']}",
                params={
                    "history_days": history_days,
                    "forecast_days": forecast_days,
                    "lead_time_days": lead_time
                }
            )

            current_stock = int(
                forecast.get("current_stock", 0)
            )

            daily_demand = float(
                forecast.get(
                    "average_daily_demand", 0
                )
            )

            predicted_demand = int(
                forecast.get(
                    "predicted_units_needed", 0
                )
            )

            reorder_quantity = int(
                forecast.get(
                    "recommended_reorder_quantity", 0
                )
            )

            stockout_risk = forecast.get(
                "stockout_risk",
                "UNKNOWN"
            )

            days_until_stockout = forecast.get(
                "estimated_days_until_stockout"
            )

            historical_units = int(
                forecast.get(
                    "historical_units_sold", 0
                )
            )

            st.success(
                "Demand forecast generated successfully."
            )

            st.subheader("Forecast Results")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Current Stock",
                current_stock
            )

            c2.metric(
                "Daily Demand",
                f"{daily_demand:.2f}"
            )

            c3.metric(
                "Predicted Demand",
                predicted_demand
            )

            c4.metric(
                "Recommended Reorder",
                reorder_quantity
            )

            st.divider()

            left, right = st.columns([2, 1])

            # FORECAST CHART

            with left:

                st.subheader(
                    "Stock vs Predicted Demand"
                )

                chart_data = pd.DataFrame({
                    "Metric": [
                        "Current Stock",
                        "Predicted Demand",
                        "Reorder Quantity"
                    ],
                    "Units": [
                        current_stock,
                        predicted_demand,
                        reorder_quantity
                    ]
                })

                fig = px.bar(
                    chart_data,
                    x="Metric",
                    y="Units",
                    color="Metric"
                )

                fig.update_layout(
                    showlegend=False
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True
                )

            # STOCK RISK

            with right:

                st.subheader("Stockout Risk")

                if stockout_risk in [
                    "HIGH",
                    "OUT_OF_STOCK"
                ]:

                    st.error(
                        f"Risk: {stockout_risk}"
                    )

                elif stockout_risk == "MEDIUM":

                    st.warning(
                        "Risk: MEDIUM"
                    )

                elif stockout_risk == "LOW":

                    st.success(
                        "Risk: LOW"
                    )

                else:

                    st.info(
                        f"Risk: {stockout_risk}"
                    )

                if days_until_stockout is not None:

                    st.metric(
                        "Estimated Days Until Stockout",
                        days_until_stockout
                    )

                else:

                    st.info(
                        "Stockout time cannot be estimated "
                        "without recorded demand."
                    )

            st.divider()

            # REORDER RECOMMENDATIONS

            st.subheader(
                "Intelligent Reorder Recommendation"
            )

            if reorder_quantity > 0:

                st.warning(
                    f"Consider ordering "
                    f"{reorder_quantity} additional units."
                )

            else:

                st.success(
                    "Current inventory does not require "
                    "immediate replenishment based on "
                    "the selected forecasting method."
                )

            st.subheader("Forecast Information")

            info1, info2, info3 = st.columns(3)

            info1.metric(
                "Historical Units Sold",
                historical_units
            )

            info2.metric(
                "History Window",
                f"{history_days} days"
            )

            info3.metric(
                "Supplier Lead Time",
                f"{lead_time} days"
            )

            st.caption(
                forecast.get(
                    "note",
                    "Forecast based on historical sales."
                )
            )

        except RuntimeError as error:

            st.error(str(error))

    st.divider()

    # STOCK RISK SUMMARY

    st.subheader("Stock Risk Summary")

    risk_data = [
        {
            "Product": product_name(p),
            "Current Stock": p.get(
                "quantity", 0
            ),
            "Threshold": p.get(
                "low_stock_threshold", 10
            ),
            "Status": stock_status(p)
        }
        for p in products
    ]

    display_table(risk_data)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "InventoryIQ | Inventory Management "
    "and Demand Intelligence"
)
