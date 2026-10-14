# Iris Prediction API (Beginner Project)

A small machine-learning API built with **FastAPI**. It predicts an Iris flower species from four measurements. The model is trained using scikit-learn's built-in Iris dataset and saved with `joblib`.

## Project structure

```text
ml_api_project/
├── README.md
├── generate_model.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── model.joblib        # created by generate_model.py
└── tests/
    └── test_api.sh
```

## 1. Open the project

Extract the ZIP file, then open the `ml_api_project` folder in VS Code.

## 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Create the serialized model file

Run this from the project root (the folder containing `generate_model.py`):

```bash
python generate_model.py
```

This creates `app/model.joblib`. It prints the test accuracy as well. The API loads this serialized model once at startup.

## 5. Start the API

```bash
uvicorn app.main:app --reload
```

Open these URLs in your browser:
- Home: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive API testing: http://127.0.0.1:8000/docs

Keep the terminal open while testing.

## 6. Test a prediction

In `/docs`, expand **POST /predict**, click **Try it out**, and submit:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Example response shape (the confidence can vary slightly):
```json
{
  "prediction_id": 0,
  "prediction": "setosa",
  "confidence": 0.98,
  "input": {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }
}
```

## 7. Test with cURL

Windows PowerShell, macOS, or Linux:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

For Windows Command Prompt, put the curl command on one line.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Checks that the API/model is loaded |
| POST | `/predict` | Validates JSON and returns a prediction |

All four measurements must be positive numbers. Missing fields, text values, or zero/negative measurements are rejected with a validation error.

## 8. Run the included smoke test

Start the API in one terminal, then open a second terminal in the project root and run:
```bash
bash tests/test_api.sh
```
The shell test uses `curl` and requires the API to already be running.

## GitHub checklist

Commit `README.md`, `app/main.py`, `generate_model.py`, `requirements.txt`, and `tests/test_api.sh`. You can include `app/model.joblib` after generating it. Do not commit `.venv/` or secrets.

## Important note

This is an educational demonstration using the classic Iris dataset, not a medical or high-stakes model. Prediction confidence is not a guarantee of correctness.
