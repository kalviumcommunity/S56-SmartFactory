# SmartFactory — Portfolio Notes

## Product
SmartFactory is a manufacturing analytics platform for monitoring machine performance,
uptime, defects, maintenance activity, and operational risk.

## UI direction
The application uses a clean enterprise analytics visual language:
- light workspace background
- dark, high-contrast typography
- restrained blue accent
- consistent cards, tables, and chart containers
- subtle motion only for hierarchy and feedback
- no emoji-based navigation

## Security
Local Supabase credentials belong in `.streamlit/secrets.toml` or environment variables
and must never be committed to the repository.

## Run locally
Install the dependencies listed by the project, configure `SUPABASE_URL` and
`SUPABASE_KEY`, then run:

    python -m streamlit run app.py
