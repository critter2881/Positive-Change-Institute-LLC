# API Contract Alignment

The current backend implements:
- `GET /api/product_metadata`
- `GET /api/real_time_liquidity`

The following endpoints are referenced in docs but are not yet implemented in `backend/app.py`:
- `POST /api/transaction`
- `POST /api/analytics`
- `GET /api/market_events`
- `GET /api/predictive_insights`

Update either the docs or the backend when adding production behavior.
