# Streamlit App

A minimal Streamlit application generated with ReapySet.

## Getting Started

Run the application from the project directory:

```bash
streamlit run app.py
```

If you are using `uv`:

```bash
uv run streamlit run app.py
```

Streamlit will start a local development server and open the application in your default browser.

By default, the application is available at: [http://localhost:8501](http://localhost:8501)

## Project Structure

```text
.
├── app.py
├── pages/
│   └── 1_Dashboard.py
└── README.md
```

* `app.py` — Main application entry point.
* `pages/` — Additional pages automatically discovered by Streamlit.
* `rps_template.md` — Project documentation.

## Adding Pages

Create additional Python files inside the `pages` directory, for example:

```text
pages/
├── 1_Dashboard.py
├── 2_Analytics.py
└── 3_Settings.py
```

Streamlit automatically adds these pages to the application’s navigation.

## Development

Streamlit reruns the application whenever the source code changes.

You can stop the development server with: `Ctrl+C`

## Documentation

For more information, see the official [Streamlit documentation](https://docs.streamlit.io/).