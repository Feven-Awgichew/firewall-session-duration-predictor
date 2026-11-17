import joblib
import pandas as pd
import streamlit as st
from pathlib import Path

# ---------------------------------------------------------
# Firewall Session Duration Predictor
# This app expects the COMPLETE fitted preprocessing +
# Random Forest pipeline exported from your regression notebook.
# ---------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "models" / "firewall_duration_model.joblib"

st.set_page_config(
    page_title="Firewall Session Duration Predictor",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ Firewall Session Duration Predictor")
st.write(
    "Enter firewall session information to estimate the session duration "
    "using the trained Random Forest regression model."
)

@st.cache_resource
def load_model(path: Path):
    return joblib.load(path)

if not MODEL_PATH.exists():
    st.error("The trained model file has not been added yet.")
    st.markdown(
        """
        **To connect your model:**
        1. Open your regression notebook.
        2. Run the model-export code in `export_model_from_notebook.py`.
        3. Make sure the exported file is saved as
           `models/firewall_duration_model.joblib`.
        4. Restart this Streamlit app.
        """
    )
    st.stop()

try:
    model = load_model(MODEL_PATH)
except Exception as exc:
    st.error(f"Could not load the model: {exc}")
    st.info(
        "Make sure the model was exported with joblib and that the "
        "scikit-learn version is compatible with this environment."
    )
    st.stop()

st.subheader("Session information")

with st.form("prediction_form"):
    action = st.text_input(
        "Firewall Action",
        placeholder="Enter an Action category, e.g. allow",
        help="Enter a category that appeared in the training data. "
             "Use the exact spelling and capitalization.",
    )

    nat_port = st.number_input(
        "NAT Destination Port",
        min_value=0,
        max_value=65535,
        value=443,
        step=1,
        help="Enter the NAT destination port number.",
    )

    submitted = st.form_submit_button(
        "Predict session duration",
        use_container_width=True,
    )

if submitted:
    if not action.strip():
        st.warning("Please enter a firewall Action category.")
    else:
        # Keep the column names and order consistent with model training.
        input_data = pd.DataFrame(
            [{
                "Action": action.strip(),
                "NAT Destination Port": float(nat_port),
            }]
        )

        try:
            prediction = float(model.predict(input_data)[0])

            st.success("Prediction completed!")
            st.metric(
                label="Predicted session duration",
                value=f"{prediction:,.2f} seconds",
            )

            if prediction >= 0:
                minutes = prediction / 60
                st.caption(f"Approximately {minutes:,.2f} minutes.")
            else:
                st.caption(
                    "The model returned a negative estimate. "
                    "Interpret this cautiously; the model has not been "
                    "post-processed to constrain predictions to zero."
                )

            with st.expander("View submitted input"):
                st.dataframe(input_data, use_container_width=True)

        except Exception as exc:
            st.error(f"Prediction failed: {exc}")
            st.info(
                "Check that the Action value is represented in the "
                "training data and that the saved model expects the two "
                "columns: Action and NAT Destination Port."
            )

st.divider()
st.caption(
    "Academic demonstration only. Predictions are estimates from a "
    "machine learning model and should not be treated as operational "
    "firewall measurements."
)
