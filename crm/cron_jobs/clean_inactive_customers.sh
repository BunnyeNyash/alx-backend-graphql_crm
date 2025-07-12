#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Store current working directory
cwd=$(pwd)

# Absolute path to Python and manage.py
PYTHON="alx-backend-graphql_crm/venv/bin/python"
MANAGE_PY="alx-backend-graphql_crm/manage.py"
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Change to project directory
cd /alx-backend-graphql_crm

# Check if manage.py exists
if [ -f "$MANAGE_PY" ]; then
    # Execute Django shell command to delete inactive customers
    $PYTHON $MANAGE_PY shell <<EOF >> $LOG_FILE 2>&1
from crm.models import Customer, Order
from django.utils import timezone
from datetime import timedelta

# Find customers with no orders in the past year
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True) | \
                     Customer.objects.filter(order__order_date__lt=one_year_ago).distinct()
count = inactive_customers.count()
inactive_customers.delete()

# Log the result with timestamp
print(f"{timezone.now().strftime('%Y-%m-%d %H:%M:%S')} - Deleted {count} inactive customers")
EOF

    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleanup script executed successfully" >> $LOG_FILE 2>&1
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Error: Cleanup script failed" >> $LOG_FILE 2>&1
    fi
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Error: manage.py not found at $MANAGE_PY" >> $LOG_FILE 2>&1
fi

# Return to original directory
cd "$cwd"

