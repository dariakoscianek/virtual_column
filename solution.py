import pandas as pd

def is_valid_label(label: str) -> bool:
    if not label:
        return False
    for char in label:
        if not (char.isalpha() or char == "_"):
            return False
    return True

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    if not is_valid_label(new_column):
        return pd.DataFrame([])
    
    for col in df.columns:
        if not is_valid_label(col):
            return pd.DataFrame([])
    
    role = role.strip()
    role_without_spaces = role.replace(" ", "")
    
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+-*")
    for char in role_without_spaces:
        if char not in allowed_chars:
            return pd.DataFrame([])
    
    operator = None
    for op in ["+", "-", "*"]:
        if op in role_without_spaces:
            operator = op
            break
    
    if operator is None:
        return pd.DataFrame([])
    
    equation = role_without_spaces.split(operator)
    
    if len(equation) != 2:
        return pd.DataFrame([])
    
    col1, col2 = equation
    
    if col1 not in df.columns or col2 not in df.columns:
        return pd.DataFrame([])
    
    try:
        if operator == "+":
            result = df[col1] + df[col2]
        elif operator == "-":
            result = df[col1] - df[col2]
        else:
            result = df[col1] * df[col2]
    except Exception:
        return pd.DataFrame([])
    
    df_result = df.copy()
    df_result[new_column] = result
    
    return df_result