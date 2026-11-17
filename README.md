# Firewall Session Duration Predictor

A small Streamlit demo for the regression assignment **Predicting Firewall Session Duration Using Machine Learning**.

The app accepts:
- `Action`
- `NAT Destination Port`

It returns a predicted `Elapsed Time (sec)` using your trained Random Forest regression pipeline.

## Project structure

```text
firewall_session_duration_streamlit/
├── app.py
├── requirements.txt
├── export_model_from_notebook.py
├── README.md
└── models/
    └── README.md
```

## Important: add your trained model

The ZIP does **not** contain a trained model because the model artifact was not available when this project package was created. You must export the fitted model from your notebook.

1. Open your regression notebook.
2. Confirm that `rf_reduced_model` is the fitted pipeline selected for the reduced Random Forest model.
3. In the notebook, set the working directory to this project folder, or use the full path to its `models` directory.
4. Run the code in `export_model_from_notebook.py` (or copy it into a notebook cell).
5. Confirm that this file exists:

   `models/firewall_duration_model.joblib`

The saved object must be the **complete fitted preprocessing + Random Forest pipeline**, not just the estimator. It must accept a pandas DataFrame with these exact columns:

- `Action`
- `NAT Destination Port`

The model's preprocessing must handle the `Action` categorical feature, as it did during training.

## Setup

Python 3.10 or newer is recommended.

### Windows

Open PowerShell or Command Prompt in this project folder:

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Ubuntu / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the app

From the project folder:

```bash
streamlit run app.py
```

Streamlit will print a local address, usually:

`http://localhost:8501`

Open that address in your browser.

## Input guidance

- Enter an `Action` category exactly as it appears in your training data (including capitalization).
- Enter a valid NAT destination port from 0 to 65535.
- Use values that are meaningful for your dataset. The app does not validate whether a port/action combination occurred in the original data.

## Notes

- This is an academic demonstration, not a production firewall system.
- Predictions are estimates, not guaranteed measurements.
- A model trained with a particular scikit-learn version may emit a compatibility warning or fail to load under a substantially different version. If that happens, export and run the app using compatible package versions.
