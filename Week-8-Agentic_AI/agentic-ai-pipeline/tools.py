import pandas as pd


def calculator(operation: str, a: float, b: float) -> float:
    if operation in ["add", "addition", "+"]:
        return a + b
    elif operation in ["subtract", "subtraction", "-"]:
        return a - b
    elif operation in ["multiply", "multiplication", "*"]:
        return a * b
    elif operation in ["divide", "division", "/"]:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError("Invalid operation")


def analyze_data(file_path: str, column: str, operation: str) -> float:
    df = pd.read_csv(file_path)

    column_map = {c.lower(): c for c in df.columns}

    if column.lower() not in column_map:
        raise ValueError("Column not found")

    column = column_map[column.lower()]

    if operation in ["mean", "average"]:
        return float(df[column].mean())
    elif operation == "sum":
        return float(df[column].sum())
    elif operation == "max":
        return float(df[column].max())
    elif operation == "min":
        return float(df[column].min())

    raise ValueError("Invalid operation")