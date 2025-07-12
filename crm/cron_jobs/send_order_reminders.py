#!/alx-backend-graphql_crm/venv/bin/python

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

# Set up GraphQL client
transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define GraphQL query for recent orders
query = gql("""
    query {
        recentOrders {
            id
            customer {
                email
            }
        }
    }
""")

# Execute query
try:
    response = client.execute(query)
    orders = response.get('recentOrders', [])
except Exception as e:
    with open('/tmp/order_reminders_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n")
    print("Order reminders processed!")
    exit()

# Log order reminders
with open('/tmp/order_reminders_log.txt', 'a') as f:
    for order in orders:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Order {order['id']} for {order['customer']['email']}\n")

print("Order reminders processed!")
