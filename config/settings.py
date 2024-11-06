from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

# URL paths configuration
URL_PATHS_SHEET1 = [
    '/products/ipaas', '/platform/workbot', '/integrations', 
    '/platform/workflow-apps', '/platform/data-orchestration', 
    '/platform/b2b-edi', '/platform/api-management', 
    '/platform/insights', '/platform/mdm', '/platform/copilots'
]

URL_PATHS_SHEET2 = [
    '/product-hub/',
    '/product-hub/product-scoop-may-2024/',
    '/product-hub/product-scoop-june-2024/',
    '/product-hub/product-scoop-july-2024/',
    '/product-hub/product-scoop-august-2024/',
    '/product-hub/product-scoop-september-2024/',
    '/product-hub/product-scoop-october-2024/',
    '/product-hub/platform-connector-releases-in-july-2024/',
    '/product-hub/platform-connector-releases-in-august-2024/',
    '/product-hub/platform-connector-releases-in-september-2024/'
]

# Product names mapping
PRODUCT_NAMES = {
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
    '/product-hub/': 'Product Hub',
    '/product-hub/product-scoop-july-2024/': 'Product Scoop July',
    '/product-hub/product-scoop-august-2024/': 'Product Scoop August',
    '/product-hub/product-scoop-september-2024/': 'Product Scoop September',
    '/product-hub/platform-connector-releases-in-july-2024/': 'Connector Releases July',
    '/product-hub/platform-connector-releases-in-august-2024/': 'Connector Releases August',
    '/product-hub/platform-connector-releases-in-september-2024/': 'Connector Releases September'
}