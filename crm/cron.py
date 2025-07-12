from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

def log_crm_heartbeat():
    # Set up GraphQL client
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Query the hello field
    query = gql("""
        query {
            hello
        }
    """)
    
    try:
        response = client.execute(query)
        status = "OK" if response.get('hello') == "Hello, GraphQL!" else "ERROR"
    except Exception as e:
        status = f"ERROR: {str(e)}"
    
    # Log heartbeat with timestamp
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} CRM is alive - Status: {status}\n")
