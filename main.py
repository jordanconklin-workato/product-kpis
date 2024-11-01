from google.oauth2.credentials import Credentials
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, 
    Dimension, 
    Metric, 
    Filter, 
    FilterExpression
)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd
from datetime import datetime
from google.auth.transport.requests import Request
import os.path
import pickle
from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_credentials():
    """Get valid credentials for Google APIs"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_analytics_data(property_id, url_path, field_name, match_type):
    """Fetch event data from Google Analytics 4 for specific URL path"""
    credentials = get_credentials()
    client = BetaAnalyticsDataClient(credentials=credentials)
    
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
            Dimension(name="eventName"),
        ],
        metrics=[
            Metric(name="eventCount"),
            Metric(name="totalUsers"),
            Metric(name="eventCountPerUser")
        ],
        date_ranges=[{
            "start_date": "28daysAgo",
            "end_date": "today"
        }],
        dimension_filter=page_filter
    )
    
    response = client.run_report(request)
    return response

def process_analytics_data(response, url_path):
    """Process the analytics response to get page view data"""
    # Define product names mapping
    product_names = {
        '/products/ipaas': 'Enterprise iPaaS',
        '/platform/workbot': 'Workflow Bots',
        '/integrations': 'App Connectors',
        '/platform/workflow-apps': 'Low Code Apps',
        '/platform/data-orchestration': 'Data Orchestration',
        '/platform/b2b-edi': 'B2B/EDI',
        '/platform/api-management': 'API Management',
        '/platform/insights': 'Process Insights',
        '/platform/mdm': 'Data Hub / MDM',
        '/platform/copilots': 'Copilots',
        '/product-hub/': 'Product Hub'
    }
    
    for row in response.rows:
        if row.dimension_values[0].value == 'page_view':
            return {
                'Product_Name': product_names.get(url_path, ''),  # Add product name
                'URL_Path': url_path,
                'Unique_Users': row.metric_values[1].value
            }
    return None

def update_spreadsheet(all_data, range_name):
    """Update Google Spreadsheet with just total users data"""
    credentials = get_credentials()
    service = build('sheets', 'v4', credentials=credentials)
    
    # TODO env var
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    RANGE_NAME = range_name
    
    # Update headers to include Product_Name
    headers = ['Product_Name', 'URL_Path', 'Unique_Users', 'Date', 'Time']
    values = [headers]
    
    # Add current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    
    for item in all_data:
        if item:  # Check if data exists
            values.append([
                item['Product_Name'],  # Add product name to values
                item['URL_Path'],
                item['Unique_Users'],
                current_date,
                current_time
            ])
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

def debug_analytics_response(response):
    """Print the analytics response data in a readable format"""
    print("\n=== Analytics Response Debug ===")
    
    # Print dimensions header
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

def main():
    # TODO env var
    # Replace with your GA4 property ID
    PROPERTY_ID = os.getenv('GA_PROPERTY_ID')
    
    # First set of URLs (original paths)
    url_paths_sheet1 = ['/products/ipaas', '/platform/workbot', '/integrations', 
                       '/platform/workflow-apps', '/platform/data-orchestration', 
                       '/platform/b2b-edi', '/platform/api-management', 
                       '/platform/insights', '/platform/mdm', '/platform/copilots']
    
    # Product hub path
    url_paths_sheet2 = ['/product-hub/']
    
    try:
        # Process Sheet1 data with ENDS_WITH
        all_data_sheet1 = []
        for url_path in url_paths_sheet1:
            response = get_analytics_data(PROPERTY_ID, url_path, "unifiedPagePathScreen", "ENDS_WITH")
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet1.append(processed_data)
        
        # Process Sheet2 data with CONTAINS
        all_data_sheet2 = []
        for url_path in url_paths_sheet2:
            response = get_analytics_data(PROPERTY_ID, url_path, "unifiedPagePathScreen", "CONTAINS")
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet2.append(processed_data)
        
        # Update both sheets
        update_spreadsheet(all_data_sheet1, 'Sheet1!A1')
        update_spreadsheet(all_data_sheet2, 'Sheet2!A1')
        
        print(f"Total users data successfully transferred to spreadsheet! Timestamp: {datetime.now()}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()