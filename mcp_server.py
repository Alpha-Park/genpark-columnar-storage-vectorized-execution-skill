import sys
import json
from client import ColumnarStorageEngine

def main():
    engine = ColumnarStorageEngine()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "insert_batch":
            engine.insert_batch(params.get("rows", []))
            res = {"status": "ok"}
        elif method == "aggregate":
            val, cnt = engine.vectorized_filter_aggregate(
                params.get("filter_col"),
                params.get("op"),
                params.get("threshold"),
                params.get("agg_col"),
                params.get("agg_func", "SUM")
            )
            res = {"value": val, "count": cnt}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
