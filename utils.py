def log_pipeline_step(node, kind, value):
    with open("query_logs.txt", "a") as f:
        f.write(f"[{node}] {kind}: {value}\n")