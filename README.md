# DynamicAPI

**DynamicAPI** is a lightweight Python-based tool that allows you to create dynamic RESTful APIs by simply registering a `SELECT` statement and an endpoint path. It’s ideal for scenarios where you want to expose data quickly without writing traditional backend logic.

## 🚀 Features

- Create REST endpoints dynamically via a database
- Write and register your own SQL `SELECT` queries
- Instant access to data through generated APIs
- Swagger UI support with tags and descriptions
- Separation of metadata and query execution databases
- Built with FastAPI and MySQL

## 🛠️ Technologies Used

- Python 3.11+
- FastAPI
- Uvicorn
- MySQL
- SQLAlchemy
- Docker (optional for containerized setup)

## ⚙️ How It Works

1. Register a new API in the metadata database with:
   - `name`: API identifier
   - `endpoint`: route path (e.g., `/patients`)
   - `sql_query`: SQL SELECT statement
   - `tags`: for Swagger UI grouping

2. When the app starts, it reads the registered APIs and dynamically creates the routes.

3. When a request hits the endpoint, the system executes the associated SQL in the execution database and returns the result.

## ▶️ Running the Project

1. **Create the required table** by running the SQL script located at:
   ```
   database/sqls/Create_Table_Apis.sql
   ```

2. **Configure environment variables** by creating a `.env` file with the following entries:
   ```
   API_DATABASE_URL=mysql+aiomysql://user:pwd@db_mysql:3306/dynamicapi
   TARGET_DATABASE_URL=mysql+aiomysql://user:pwd@db_mysql:3306/your-database
   ```

### With Uvicorn

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then access: [http://localhost:8000/docs](http://localhost:8000/docs)

### With Docker (optional)

If you're using Docker, you can build and run containers with your `Dockerfile` and `docker-compose.yml`.

## 🧪 Example

Register this in the database or use Admin APIs :

```sql
INSERT INTO apis (name, endpoint, sql_query, tags)
VALUES (
  'Get Patients',
  '/patients',
  'SELECT * FROM patients',
  'Patients'
);
```

It will instantly expose a `GET /patients` endpoint.

## 📌 Future Plans

- User authentication & API keys
- Support for additional databases (currently MySQL only)
- Admin UI for managing endpoints
- Validation and SQL security improvements

## 📄 License

MIT License – see the `LICENSE` file for details.
