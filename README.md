# Meal Calorie Count Backend

A **FastAPI + PostgreSQL** based backend service for managing users, authentication, and meal calorie tracking.  
This project is containerized with **Docker** and built to be production-ready, with modular structure, rate limiting, and testing support.

---

## 🚀 Features

- 🔑 **User Authentication** (JWT-based login & register)
- 🍽 **Meal Tracking** (add, update, delete, list meals)
- 📊 **Calorie Count API** with search and filtering
- 🐘 **PostgreSQL Integration** via SQLModel
- ⚡ **FastAPI** for high-performance REST APIs
- 🐳 **Dockerized** setup (backend + Postgres)
- 🛡 **Rate limiting** using SlowAPI
- ✅ **Unit Tests** with pytest & respx

---

## 📂 Project Structure

```

meal\_backend\_v2/
│── app/
│   ├── api/               # API route handlers
│   ├── core/              # Config & security
│   ├── db/                # Database session & models
│   ├── schemas/           # Pydantic schemas
│   ├── main.py            # FastAPI entrypoint
│── tests/                 # Unit & integration tests
│── Dockerfile             # Backend container setup
│── docker-compose.yml     # Orchestration with PostgreSQL
│── requirements.txt       # Python dependencies
│── .gitignore
│── README.md

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/meal-calorie-backend.git
cd meal-calorie-backend/meal_backend_v2
````

### 2️⃣ Create Virtual Environment (Optional if not using Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Run with Docker (Recommended)

```bash
docker-compose up --build
```

The backend will be available at:
👉 [http://localhost:8000](http://localhost:8000)

Interactive API docs:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📝 API Endpoints

### Auth

* `POST /auth/register` → Register new user
* `POST /auth/login` → Login & get JWT

### Meals

* `GET /meals/` → List all meals
* `POST /meals/` → Add a meal
* `PUT /meals/{id}` → Update a meal
* `DELETE /meals/{id}` → Delete a meal

---

## 🐳 Environment Variables

Create a `.env` file in the project root:

```ini
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/meals
JWT_SECRET=supersecretkey
JWT_ALGORITHM=HS256
```

---

## 📈 Future Improvements

* 🔍 Add search with fuzzy matching (RapidFuzz already installed)
* 📱 Add frontend integration (React/Next.js)
* 🌐 Deploy to cloud (Heroku / AWS ECS)

---

## 👨‍💻 Author
Developed by **Harshith R.**

