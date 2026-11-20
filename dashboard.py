
st.markdown("""
<style>
/* ===== INVENTORYIQ PROFESSIONAL DARK THEME ===== */

.stApp {
    background-color: #0B1120;
    color: #F8FAFC;
}

.block-container {
    max-width: 1550px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main text and headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p {
    color: #F8FAFC;
}

.stApp h1 {
    font-weight: 800;
}

/* All form labels */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] span {
    color: #F8FAFC !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* Tabs */
button[data-baseweb="tab"],
button[data-baseweb="tab"] p {
    color: #CBD5E1 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #A5B4FC !important;
}

[data-baseweb="tab-highlight"] {
    background-color: #818CF8 !important;
}

/* Text inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    opacity: 1 !important;
}

/* Input placeholders */
input::placeholder,
textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

/* Input containers */
[data-baseweb="input"],
[data-baseweb="textarea"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
}

/* Number input controls */
[data-testid="stNumberInput"] button,
[data-testid="stNumberInput"] button svg {
    color: #334155 !important;
}

/* Select boxes */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Dropdown menus */
[role="listbox"],
[role="option"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

[role="option"] * {
    color: #111827 !important;
}

/* Forms */
[data-testid="stForm"] {
    background-color: #111A2C;
    border: 1px solid #35445F;
    border-radius: 14px;
    padding: 18px;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid #3B82F6 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
}

.stButton button *,
.stFormSubmitButton button * {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #1D4ED8 !important;
}

/* Disabled buttons */
.stButton button:disabled {
    background-color: #334155 !important;
    color: #CBD5E1 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #19243B, #141D30);
    border: 1px solid #2B3852;
    border-radius: 15px;
    padding: 19px 17px;
    min-height: 128px;
}

[data-testid="stMetricLabel"] p {
    color: #CBD5E1 !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 750 !important;
    font-size: clamp(19px, 1.8vw, 30px) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111A2C;
    border-right: 1px solid #26334B;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #E2E8F0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px;
    border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #202D46;
}

[data-testid="stSidebar"] [data-testid="stRadio"]
label:has(input:checked) {
    background-color: #26345C;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #2B3852;
    border-radius: 12px;
    overflow: hidden;
}

/* Branding */
.brand {
    font-size: 27px;
    font-weight: 850;
    color: #F8FAFC;
    padding: 16px 0 5px;
}

.brand span {
    color: #818CF8 !important;
}

.brand-subtitle {
    color: #A5B4CC !important;
    font-size: 11px;
    letter-spacing: 1.5px;
    margin-bottom: 26px;
}

.subtitle {
    color: #CBD5E1 !important;
    font-size: 15px;
    margin: -4px 0 24px;
}

.section-label {
    color: #A5B4CC !important;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1px;
    margin-top: 16px;
    margin-bottom: 8px;
}

/* API connection status */
.status-online {
    background-color: #12382F;
    border: 1px solid #236A54;
    color: #6EE7B7 !important;
    padding: 12px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 650;
}

.status-offline {
    background-color: #42202B;
    color: #FDA4AF !important;
    padding: 12px;
    border-radius: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8 !important;
    font-size: 12px;
    margin-top: 50px;
    padding: 20px;
    border-top: 1px solid #26334B;
}

/* Responsive layout */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .brand {
        font-size: 23px;
    }
}
</style>
""", unsafe_allow_html=True)
