#!/bin/bash

# Absolute path to Python and manage.py
PYTHON="alx-backend-graphql_crm/venv/bin/python"
MANAGE_PY="alx-backend-graphql_crm/manage.py"
LOG_FILE="/tmp/customer_cleanup_log.txt"

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
