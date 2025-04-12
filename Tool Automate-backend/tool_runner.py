
def run_tool(code: str, inputs: dict) -> any:
    local_vars = {}
    exec(code, {}, local_vars)
    func = next((v for v in local_vars.values() if callable(v)), None)
    return func(**inputs) if func else None
