from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(
    title="FastAPI App",
    description="A FastAPI application generated with ReapySet.",
    version="0.1.0",
)


class Item(BaseModel):
    name: str
    price: float
    available: bool = True


items: dict[int, Item] = {}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "FastAPI application is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items")
def get_items() -> dict[int, Item]:
    return items


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    item = items.get(item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return item


@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: Item) -> dict[str, int | Item]:
    item_id = max(items, default=0) + 1
    items[item_id] = item

    return {
        "id": item_id,
        "item": item,
    }