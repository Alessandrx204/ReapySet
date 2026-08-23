import marimo

app = marimo.App(width="medium")


@app.cell
def _() -> tuple[object]:
    import marimo as mo

    mo.md(
        """
        # Dynamic Marimo Dashboard

        ## A simple reactive dashboard built with marimo 
        (by ReapySet).
        """
    )
    return (mo,)


@app.cell
def _(mo) -> tuple[object, object, object]:
    n1 = mo.ui.number(
        start=1,
        stop=100,
        step=1,
        value=42,
        label="Number A",
    )

    n2 = mo.ui.number(
        start=1,
        stop=100,
        step=1,
        value=18,
        label="Number B",
    )

    operation = mo.ui.dropdown(
        options=[
            "Addition",
            "Multiplication",
            "Power",
        ],
        value="Addition",
        label="Operation",
    )

    mo.hstack(
        [n1, n2, operation],
        justify="start",
        gap=2,
    )

    return n1, n2, operation


@app.cell
def _(n1, n2, operation) -> tuple[int, int, int]:
    a: int = n1.value
    b: int = n2.value
    result: int

    if operation.value == "Addition":
        result = a + b
    elif operation.value == "Multiplication":
        result = a * b
    else:
        result = a**b

    return a, b, result


@app.cell
def _(a: int | float, b: int | float, mo, operation, result: int) -> None:
    mo.md(
        f"""
        ## Result

        **{operation.value}:**

        `{a}` and `{b}` → **`{result}`**
        """
    )


if __name__ == "__main__":
    app.run()