SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "border-right": "1px solid #dee2e6",
    "overflow-y": "auto"
}

CONTENT_STYLE = {
    "margin-left": "22rem",
    "padding": "30px",
    "background-color": "#ffffff"
}

HTML_STYLES = """
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f7fa;
                }
    
                .sidebar-header {
                    color: #2c3e50;
                    margin-bottom: 20px;
                }
    
                .filter-label {
                    color: #34495e;
                    margin-top: 15px;
                    margin-bottom: 5px;
                    font-size: 14px;
                }
    
                .filter-input {
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                    font-size: 14px;
                }
    
                .filter-dropdown {
                    width: 100%;
                }
    
                .button-group {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                }
    
                .apply-button {
                    flex: 1;
                    padding: 10px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }
    
                .apply-button:hover {
                    background-color: #2980b9;
                }
    
                .reset-button {
                    flex: 1;
                    padding: 10px;
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }
    
                .reset-button:hover {
                    background-color: #c0392b;
                }
    
                .current-filters {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #ecf0f1;
                    border-radius: 6px;
                    font-size: 13px;
                    color: #34495e;
                    border-left: 4px solid #3498db;
                }
    
                .quick-stats {
                    font-size: 12px;
                    color: #7f8c8d;
                    line-height: 1.5;
                }
    
                .main-header {
                    color: #2c3e50;
                    margin-bottom: 30px;
                }
    
                .stats-summary {
                    background-color: #ecf0f1;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    display: flex;
                    justify-content: space-around;
                    text-align: center;
                }
    
                .stat-item {
                    padding: 10px;
                }
    
                .stat-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                }
    
                .stat-label {
                    font-size: 14px;
                    color: #7f8c8d;
                    margin-top: 5px;
                }
    
                .charts-row {
                    display: flex;
                    gap: 20px;
                    margin-bottom: 20px;
                }
    
                .chart-container {
                    flex: 1;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 15px;
                }
    
                .chart {
                    height: 100%;
                }
    
                .tips-section {
                    background-color: #e8f4fc;
                    padding: 25px;
                    border-radius: 8px;
                    margin-top: 30px;
                    border-left: 5px solid #3498db;
                }
    
                .ai-tips-container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 6px;
                    margin: 15px 0;
                    font-size: 16px;
                    line-height: 1.6;
                    border: 1px solid #bdc3c7;
                    min-height: 80px;
                }
    
                .tip-button {
                    padding: 10px 20px;
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }
    
                .tip-button:hover {
                    background-color: #27ae60;
                }
    
                .filter-tag {
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    margin-right: 5px;
                    margin-bottom: 5px;
                }
    
                .no-data {
                    text-align: center;
                    padding: 40px;
                    color: #7f8c8d;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""