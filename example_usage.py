from client import ColumnarStorageEngine

def main():
    print("=== Testing Columnar Storage Engine & Vectorized Execution ===")
    col = ColumnarStorageEngine()
    data = [
        {"id": 1, "region": "US", "amount": 100},
        {"id": 2, "region": "US", "amount": 250},
        {"id": 3, "region": "EU", "amount": 180},
        {"id": 4, "region": "US", "amount": 300},
        {"id": 5, "region": "APAC", "amount": 400}
    ]
    col.insert_batch(data)
    rle = col.compress_column_rle("region")
    print("RLE compression for 'region':", rle)

    total_us, count_us = col.vectorized_filter_aggregate("region", "==", "US", "amount", "SUM")
    print(f"US Total Sales: {total_us}, Count: {count_us}")

    assert total_us == 650
    assert count_us == 3
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
