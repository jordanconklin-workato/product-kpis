from googleapiclient.discovery import build
from datetime import datetime
import os
from services.auth_service import get_credentials

def update_spreadsheet(all_data, range_name, quarter=""):
    """Update Google Spreadsheet with users and email submissions data"""
    credentials = get_credentials()
    service = build('sheets', 'v4', credentials=credentials)
    
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    
    # Define quarter labels based on sheet and quarter
    quarter_labels = {
        ('Sheet1', 'Q2'): 'Q2 (May, June, July)',
        ('Sheet1', 'Q3'): 'Q3 (August, September, October)',
        ('Sheet2', 'Q2'): 'Q2 (April, May, June)',
        ('Sheet2', 'Q3'): 'Q3 (July, August, September)'
    }
    
    # Extract sheet name from range (e.g., 'Sheet1!A1' -> 'Sheet1')
    sheet_name = range_name.split('!')[0]
    
    # Get appropriate quarter label
    quarter_label = quarter_labels.get((sheet_name, quarter), quarter)
    
    headers = [
        f'Product_Name {quarter_label}' if quarter else 'Product_Name', 
        'URL_Path', 'Unique_Users', 'New_Users', 'Returning_Users',
        'Email_Submissions', 'Date', 'Time'
    ]
    values = [headers]
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    
    sorted_data = sorted(all_data, key=lambda x: x['URL_Path'] if x else '')
    
    for item in sorted_data:
        if item:
            values.append([
                item['Product_Name'],
                item['URL_Path'],
                item['Unique_Users'],
                item['New_Users'],
                item['Returning_Users'],
                item['Email_Submissions'],
                current_date,
                current_time
            ])
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()