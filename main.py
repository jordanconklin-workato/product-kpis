import os
from datetime import datetime, date
from services.analytics_service import get_analytics_data, process_analytics_data
from services.sheets_service import update_spreadsheet
from utils.debug_utils import debug_analytics_response
from config.settings import URL_PATHS_SHEET1, URL_PATHS_SHEET2_Q2, URL_PATHS_SHEET2_Q3

def main():
    PROPERTY_ID = os.getenv('GA_PROPERTY_ID')
    today = date.today().strftime('%Y-%m-%d')
    
    try:
        # Process Sheet1 data - tracking specific time periods
        all_data_sheet1_Q2 = []
        for url_path in URL_PATHS_SHEET1:
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "ENDS_WITH",
                "2024-05-01", "2024-07-31"  # Q2 period (May-July)
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet1_Q2.append(processed_data)

        all_data_sheet1_Q3 = []
        for url_path in URL_PATHS_SHEET1:
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "ENDS_WITH",
                "2024-08-01", "2024-10-31"  # Q3 period (Aug-Oct)
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet1_Q3.append(processed_data)
        
        # Process Sheet2 data - tracking full year for different quarter content
        all_data_sheet2_Q2 = []
        for url_path in URL_PATHS_SHEET2_Q2:  # Q2 content (Apr-June)
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "CONTAINS",
                "2024-01-01", today  # Full year tracking
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet2_Q2.append(processed_data)

        all_data_sheet2_Q3 = []
        for url_path in URL_PATHS_SHEET2_Q3:  # Q3 content (July-Sept)
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "CONTAINS",
                "2024-01-01", today  # Full year tracking
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet2_Q3.append(processed_data)

        # Update all sheets
        update_spreadsheet(all_data_sheet1_Q2, 'Sheet1!A1', 'Q2')
        update_spreadsheet(all_data_sheet1_Q3, 'Sheet1!A14', 'Q3')
        update_spreadsheet(all_data_sheet2_Q2, 'Sheet2!A1', 'Q2')
        update_spreadsheet(all_data_sheet2_Q3, 'Sheet2!A9', 'Q3')
        
        print(f"Total users data successfully transferred to spreadsheet! Timestamp: {datetime.now()}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()