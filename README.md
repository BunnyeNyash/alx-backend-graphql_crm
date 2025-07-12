# alx-backend-graphql_crm

## Repository
**Repository**: `alx-backend-graphql_crm`

**Django App**: `crm`

## Repository Structure
```
alx-backend-graphql_crm/
├── alx-backend-graphql_crm/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── schema.py
|   ├── asgi.py
│   ├── wsgi.py
├── crm/
│   ├── __init__.py
│   ├── models.py
│   ├── schema.py
│   ├── filters.py
│   ├── cron.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   ├── management/
│   │   ├── __init__.py
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── seed_db.py
│   ├── cron_jobs/
│   │   ├── clean_inactive_customers.sh
│   │   ├── customer_cleanup_crontab.txt
│   │   ├── send_order_reminders.py
│   │   ├── order_reminders_crontab.txt
├── manage.py
├── requirements.txt
├── seed_db.py
└── README.md
```

## Files:
- `alx-backend-graphql_crm/settings.py`: Django project settings.
- `crm/models.py`: Defines the Django models for Customer, Product, and Order.
- `crm/schema.py`: Defines the GraphQL queries and mutations for the crm app.
- `alx-backend-graphql_crm/schema.py`: Main GraphQL schema combining app schemas.
- `crm/filters.py`: Custom filter classes for querying data.
- `seed_db.py`: Script to seed the database.

## Requirements
**Libraries**: graphene-django, django-filter

**Tools**: GraphiQL for testing, Django ORM for model integration.
