import math

import streamlit as st


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if not math.isfinite(weight_kg) or weight_kg <= 0:
        raise ValueError("Weight must be a positive number.")
    if not math.isfinite(height_cm) or height_cm <= 0:
        raise ValueError("Height must be a positive number.")

    height_m = height_cm / 100
    return weight_kg / (height_m * height_m)


def get_bmi_category(bmi: float) -> tuple[str, str, str]:
    if bmi < 18.5:
        return "Underweight", "Below 18.5", "#397fa0"
    if bmi < 25:
        return "Normal", "18.5 to 24.9", "#287957"
    if bmi < 30:
        return "Overweight", "25.0 to 29.9", "#c17a24"
    return "Obesity range", "30.0 and above", "#bd554b"


st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f4f8f5 0%, #edf4f1 55%, #f8f5ef 100%);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"],
    [data-testid="stWidgetLabel"], [data-testid="stCaptionContainer"],
    [data-testid="stMarkdownContainer"] p, label {
        color: #263e34;
    }
    [data-testid="stNumberInput"] [data-baseweb="input"] {
        background: #ffffff !important;
        border: 1px solid #ccddd2 !important;
        border-radius: 6px;
    }
    [data-testid="stNumberInput"] input {
        background: #ffffff !important;
        color: #263e34 !important;
    }
    [data-testid="stNumberInput"] button {
        background: #ffffff !important;
        color: #263e34 !important;
    }
    .block-container { max-width: 960px; padding-top: 3rem; padding-bottom: 3rem; }
    h1, h2, h3 { font-family: Georgia, "Times New Roman", serif; color: #173d32; }
    h1 { font-size: 2.8rem; font-weight: 500; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.88);
        border-color: #d9e5dd;
        border-radius: 8px;
    }
    [data-testid="stMetricValue"] { color: #173d32; font-family: Georgia, "Times New Roman", serif; }
    [data-testid="stFormSubmitButton"] button {
        background: #1f684c;
        border-color: #1f684c;
        color: #ffffff;
        min-height: 2.8rem;
    }
    .eyebrow {
        color: #39745b;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .intro { color: #52665c; margin-top: -0.65rem; margin-bottom: 1.8rem; }
    .result-category { font-size: 1.15rem; font-weight: 700; margin: 0.35rem 0 1rem; }
    .scale { position: relative; height: 12px; border-radius: 8px; margin: 1.5rem 0 0.55rem; }
    .scale-marker {
        position: absolute;
        top: -5px;
        width: 3px;
        height: 22px;
        border: 1px solid #ffffff;
        border-radius: 2px;
        background: #173d32;
        transform: translateX(-50%);
        box-shadow: 0 0 0 1px #173d32;
    }
    .scale-labels { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px; color: #62746a; font-size: 0.68rem; }
    .scale-labels span:nth-child(2), .scale-labels span:nth-child(3) { text-align: center; }
    .scale-labels span:last-child { text-align: right; }
    .note { color: #69796f; font-size: 0.8rem; line-height: 1.5; }
    @media (max-width: 640px) {
        .block-container { padding-top: 1.6rem; }
        h1 { font-size: 2.2rem; }
        .scale-labels { font-size: 0.61rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Health, measured simply</div>', unsafe_allow_html=True)
st.title("BMI calculator")
st.markdown(
    '<p class="intro">A quick estimate based on your weight and height.</p>',
    unsafe_allow_html=True,
)

input_column, result_column = st.columns([0.95, 1.05], gap="large")

with input_column:
    with st.container(border=True):
        st.subheader("Your measurements")
        with st.form("bmi_form"):
            weight_kg = st.number_input(
                "Weight",
                min_value=1.0,
                max_value=500.0,
                value=70.0,
                step=0.5,
                format="%.1f",
                help="Enter your weight in kilograms.",
            )
            height_cm = st.number_input(
                "Height",
                min_value=50.0,
                max_value=280.0,
                value=170.0,
                step=0.5,
                format="%.1f",
                help="Enter your height in centimeters.",
            )
            st.caption("Weight in kg · Height in cm")
            submitted = st.form_submit_button("Calculate BMI", use_container_width=True)

if submitted:
    try:
        st.session_state.bmi_value = calculate_bmi(weight_kg, height_cm)
        st.session_state.bmi_error = None
    except ValueError as error:
        st.session_state.bmi_value = None
        st.session_state.bmi_error = str(error)

with result_column:
    with st.container(border=True):
        st.subheader("Your result")
        bmi_value = st.session_state.get("bmi_value")
        bmi_error = st.session_state.get("bmi_error")

        if bmi_error:
            st.error(bmi_error)
        elif bmi_value is None:
            st.write("Your BMI and range will appear here after calculation.")
        else:
            category, range_text, category_color = get_bmi_category(bmi_value)
            st.metric("Body mass index", f"{bmi_value:.1f}")
            st.markdown(
                f'<p class="result-category" style="color:{category_color}">{category}</p>',
                unsafe_allow_html=True,
            )
            st.caption(f"Adult range: {range_text}")
            marker_position = min(max(bmi_value / 40 * 100, 0), 100)
            st.markdown(
                f"""
                <div class="scale" style="background:linear-gradient(to right,
                    #78a9bf 0%, #78a9bf 46.25%,
                    #69a984 46.25%, #69a984 62.5%,
                    #e5b55d 62.5%, #e5b55d 75%,
                    #d17769 75%, #d17769 100%);">
                    <span class="scale-marker" style="left:{marker_position:.2f}%"></span>
                </div>
                <div class="scale-labels">
                    <span>Underweight</span><span>Normal</span>
                    <span>Overweight</span><span>Obesity</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.caption(
    "BMI is a general screening measure for adults, not a diagnosis. "
    "It may not reflect individual health or body composition."
)
