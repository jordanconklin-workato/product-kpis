from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, 
    Dimension, 
    Metric, 
    Filter, 
    FilterExpression
)
from config.settings import PRODUCT_NAMES
from services.auth_service import get_credentials

def get_analytics_data(property_id, url_path, field_name="unifiedPagePathScreen", match_type="EXACT", start_date="28daysAgo", end_date="today"):
    """Fetch event data from Google Analytics 4 for specific URL path"""
    credentials = get_credentials()
    client = BetaAnalyticsDataClient(credentials=credentials)
    
    # Use EXACT match for sub-pages to avoid overlap
    if '/product-hub/' in url_path and url_path != '/product-hub/':
        match_type = "EXACT"
    
    page_filter = FilterExpression(
        filter=Filter(
            field_name=field_name,
            string_filter={
                "value": url_path,
                "match_type": match_type,
                "case_sensitive": False
            }
        )
    )

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="newVsReturning")
        ],
        metrics=[
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="eventCount")
        ],
        date_ranges=[{"start_date": start_date, "end_date": end_date}],
        dimension_filter=page_filter
    )
    
    return client.run_report(request)

def process_analytics_data(response, url_path):
    """Process the analytics response to get page view and email submission data"""
    result = {
        'Product_Name': PRODUCT_NAMES.get(url_path, ''),
        'URL_Path': url_path,
        'Unique_Users': 0,
        'Email_Submissions': 0,
        'New_Users': 0,
        'Returning_Users': 0
    }
    
    total_users = 0
    for row in response.rows:
        user_type = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        
        if user_type == 'new':
            result['New_Users'] = users
        elif user_type == 'returning':
            result['Returning_Users'] = users
        total_users += users
    
    result['Unique_Users'] = total_users
    
    return result