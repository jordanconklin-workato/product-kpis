def debug_analytics_response(response):
    """Print the analytics response data in a readable format"""
    print("\n=== Analytics Response Debug ===")
    
    dimension_headers = [header.name for header in response.dimension_headers]
    metric_headers = [header.name for header in response.metric_headers]
    print("\nHeaders:")
    print(f"Dimensions: {dimension_headers}")
    print(f"Metrics: {metric_headers}")
    
    print("\nRows:")
    for row in response.rows:
        dimensions = [value.value for value in row.dimension_values]
        metrics = [value.value for value in row.metric_values]
        print("\nDimension Values:", dimensions)
        print("Metric Values:", metrics)

    print("\nRow Count:", len(response.rows))
    print("=== End Debug ===\n") 