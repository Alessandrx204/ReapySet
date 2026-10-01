# FastAPI App

A minimal FastAPI application generated with **ReapySet**.

## Getting Started

Run the development server from the project directory:

```bash
uvicorn main:app --reload
```

If you are using `uv`:

```bash
uv run uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Project Structure

```text
.
├── main.py
└── README.md
```

- `main.py` — FastAPI application, data models, and API routes.
- `rps_template.md` — Project documentation.

## Example Endpoints

The starter application includes:

```text
GET   /              Application information
GET   /health        Health check
GET   /items         List items
GET   /items/{id}    Get an item
POST  /items         Create an item
```

You can explore and test all endpoints directly from the interactive documentation at `/docs`.

## Adding an Endpoint

Add a new path operation to `main.py`:

```python
@app.get("/hello/{name}")
def hello(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
```

FastAPI automatically includes the new endpoint in the generated OpenAPI documentation.

## Documentation

See the official FastAPI documentation for routing, validation, dependencies, security, databases, and other features:

https://fastapi.tiangolo.com/