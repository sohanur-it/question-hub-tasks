
# Quizhub Backend API

## Prerequisites
- Docker and Docker Compose installed on your machine
- Poetry for Python dependency management

## Setup
 
1. **Build and Start Containers**
   ```bashs
   docker-compose up --build
   ```
   **It will create tags and questions automatically based on a structure and will also create superuser**

2. **Superuser creds:** (auto generate)
   ```bash
   username: admin@admin.com
   password: admin321
   ```

3. **Create Database Tables**
   Within the Poetry shell, run:
   ```bash
   python manage.py migrate
   ```

4. **Create a Superuser**
   Create an admin user to access the Django admin interface:
   ```bash
   python manage.py createsuperuser
   ```

5. **Access the Application**
   The application will be available at [http://localhost:8000](http://localhost:8000).

6. **Access the Django Admin Interface**
   The Django admin interface will be available at [http://localhost:8000/admin](http://localhost:8000/admin).

7. **Postman Collections**
   ```
   https://api.postman.com/collections/18762711-d54d2f16-475f-4322-a45e-00185f1acbf2?access_key=***
   ```

