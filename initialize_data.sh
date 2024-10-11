#!/bin/sh

# Check if there are any tags or questions already in the database
if poetry run python manage.py check_existing_data; then
  echo "Tags and questions are already loaded, skipping data initialization."
else
  echo "Loading demo tags and questions..."
  poetry run python manage.py create_demo_tags
  poetry run python manage.py create_demo_questions
fi
