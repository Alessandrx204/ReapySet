import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        """
        # Starter Template
        This notebook was automatically generated using ReapySet.
        """
    )
    return (mo,)


@app.cell
def _():
    import random

    def sum_numbers(a: int, b: int) -> int:
        return a + b

    def main() -> int:
        print("Running main programme...")

        # random numbers
        num1: int = random.randint(1, 100)
        num2: int = random.randint(1, 100)

        result_ = sum_numbers(num1, num2)
        print(f"Calculated sum of {num1} and {num2}: {result}")
        return result_

    result = main()
    return main, result, sum_numbers


if __name__ == "__main__":
    app.run()
