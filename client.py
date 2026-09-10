class ColumnarStorageEngine:
    """
    Column-oriented storage engine with vectorized evaluation
    and Run-Length Encoding (RLE) compression.
    """
    def __init__(self):
        self.columns = {}

    def insert_batch(self, rows):
        if not rows:
            return
        keys = list(rows[0].keys())
        for k in keys:
            if k not in self.columns:
                self.columns[k] = []
            vals = [r[k] for r in rows]
            self.columns[k].extend(vals)

    def compress_column_rle(self, col_name):
        raw = self.columns.get(col_name, [])
        runs = []
        if not raw:
            return runs
        curr = raw[0]
        cnt = 1
        for x in raw[1:]:
            if x == curr:
                cnt += 1
            else:
                runs.append((curr, cnt))
                curr = x
                cnt = 1
        runs.append((curr, cnt))
        return runs

    def vectorized_filter_aggregate(self, filter_col, op, threshold, agg_col, agg_func="SUM"):
        col_f = self.columns.get(filter_col, [])
        col_a = self.columns.get(agg_col, [])
        mask = []
        for v in col_f:
            if op == ">":
                mask.append(v > threshold)
            elif op == "==":
                mask.append(v == threshold)
            elif op == "<":
                mask.append(v < threshold)
            else:
                mask.append(False)
        filtered_values = [col_a[i] for i, flag in enumerate(mask) if flag]
        if agg_func == "SUM":
            return sum(filtered_values), len(filtered_values)
        elif agg_func == "AVG":
            return (sum(filtered_values) / len(filtered_values) if filtered_values else 0.0), len(filtered_values)
        elif agg_func == "COUNT":
            return len(filtered_values), len(filtered_values)
        return filtered_values, len(filtered_values)
