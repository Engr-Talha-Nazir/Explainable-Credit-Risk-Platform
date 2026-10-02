# API Reference

The FastAPI service exposes endpoints for predictions, explanations, and counterfactuals.

## Base URL

http://localhost:8000

## Interactive Docs

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints

### GET /health
Health check.

**Response:**
`json
{
  "status": "ok",
  "version": "0.1.0"
}
`

### POST /predict
Return model prediction and probability for a single applicant.

**Request body (example):** JSON with feature names matching training schema (see configs/ and data schema docs).

**Response:**
`json
{
  "prediction": 0,
  "probability": 0.23,
  "label": "reject"
}
`

### POST /explain/shap
Get SHAP local/global explanation for instance(s).

**Response (local):** SHAP values per feature, base value, visualization references/JSON.

### POST /explain/lime
Get LIME local explanation.

**Response:** Feature weights (positive/negative), intercept, local prediction.

### POST /explain/counterfactuals
Generate DiCE counterfactuals (actionable recourse).

**Request:** Input instance + constraints (immutable features, desired class, diversity).

**Response:** List of diverse counterfactual examples with feature changes and new prediction/probability.

### POST /fairness/audit
Run fairness audit on provided dataset or sample (returns metrics summary).

**Response:** Before/after metrics, group-wise stats (JSON).

### GET /models/info
Return model metadata (name, version, features, training config hash).

## Notes

- Feature order/schema must match preprocessing used in training. Validate against src/preprocessing/schema.py (to be implemented).
- All endpoints are read-only for inference/explanation; no data persistence by default.
- For batch requests, prefer chunked calls; large batches may require async/background jobs in production.

## Error Handling

Standard HTTP errors: 400 (bad request/schema mismatch), 422 (validation error), 500 (inference/explanation failure). Errors return structured JSON with detail.
