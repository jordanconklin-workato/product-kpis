import os
from datetime import datetime
from services.analytics_service import get_analytics_data, process_analytics_data
from services.sheets_service import update_spreadsheet
from utils.debug_utils import debug_analytics_response
from config.settings import URL_PATHS_SHEET1, URL_PATHS_SHEET2

def main():
    PROPERTY_ID = os.getenv('GA_PROPERTY_ID')
    
    try:
        # Process Sheet1 data with ENDS_WITH for Quarter 2
        all_data_sheet1_Q2 = []
        for url_path in URL_PATHS_SHEET1:
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "ENDS_WITH",
                "2024-05-01", "2024-07-31"
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet1_Q2.append(processed_data)

        # Process Sheet1 data with ENDS_WITH for Quarter 3
        all_data_sheet1_Q3 = []
        for url_path in URL_PATHS_SHEET1:
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "ENDS_WITH",
                "2024-08-01", "2024-10-31"
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet1_Q3.append(processed_data)
        
        # Process Sheet2 data for both quarters
        all_data_sheet2_Q2 = []
        all_data_sheet2_Q3 = []
        for url_path in URL_PATHS_SHEET2:
            # Q2 data
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "CONTAINS",
                "2024-05-01", "2024-07-31"
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet2_Q2.append(processed_data)
            
            # Q3 data
            response = get_analytics_data(
                PROPERTY_ID, url_path, "unifiedPagePathScreen", "CONTAINS",
                "2024-08-01", "2024-10-31"
            )
            debug_analytics_response(response)
            processed_data = process_analytics_data(response, url_path)
            all_data_sheet2_Q3.append(processed_data)

        # Update all sheets
        update_spreadsheet(all_data_sheet1_Q2, 'Sheet1!A1', 'Q2')
        update_spreadsheet(all_data_sheet1_Q3, 'Sheet1!A13', 'Q3')
        update_spreadsheet(all_data_sheet2_Q2, 'Sheet2!A1', 'Q2')
        update_spreadsheet(all_data_sheet2_Q3, 'Sheet2!A10', 'Q3')
        
        print(f"Total users data successfully transferred to spreadsheet! Timestamp: {datetime.now()}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()