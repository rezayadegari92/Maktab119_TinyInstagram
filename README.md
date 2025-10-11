# 📸 Tiny Instagram API

A complete Instagram-like REST API built with Django REST Framework, featuring JWT authentication, Swagger documentation, and Docker deployment.

## ✨ Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 📝 **Swagger UI** - Interactive API documentation  
- 🐳 **Docker Ready** - Complete Docker setup with PostgreSQL and Redis
- 👤 **User Profiles** - Public/Private profiles with CRUD operations
- 📸 **Posts** - Create, read, update, delete with multiple images
- ❤️ **Social Features** - Like/Unlike, Comments, Follow/Unfollow
- 🔒 **Privacy Controls** - Followers can access private profiles
- 🎯 **Permission System** - Only owners can modify their content

---

## 🚀 Quick Start

### With Docker (Recommended):

```bash
cd Maktab119_TinyInstagram
docker-compose up --build
```

**Access:**
- Swagger UI: http://localhost:8004/api/docs/
- ReDoc: http://localhost:8004/api/redoc/
- Admin: http://localhost:8004/admin/

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Register (sends OTP) |
| POST | `/api/accounts/verify-otp/` | Verify OTP & get JWT tokens |
| POST | `/api/accounts/login/` | Login & get JWT tokens |
| POST | `/api/accounts/token/refresh/` | Refresh access token |

### Profile Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/profiles/` | List profiles (searchable) |
| GET | `/api/accounts/profile/{id}/` | Get profile |
| POST | `/api/accounts/update-profile/{id}/` | Update own profile |

### Post Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/socials/posts/` | List posts |
| POST | `/api/socials/posts/create/` | Create post |
| GET | `/api/socials/posts/{id}/` | Get post |
| PUT | `/api/socials/posts/{id}/update/` | Update own post |
| DELETE | `/api/socials/posts/{id}/delete/` | Delete own post |
| POST | `/api/socials/posts/{id}/like/` | Like post |
| DELETE | `/api/socials/posts/{id}/unlike/` | Unlike post |

### Comment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/socials/posts/{id}/comment/` | Add comment |
| DELETE | `/api/socials/comments/{id}/delete/` | Delete own comment |

### Follow Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/socials/users/{id}/follow/` | Follow user |
| DELETE | `/api/socials/users/{id}/unfollow/` | Unfollow user |
| GET | `/api/socials/users/{id}/followers/` | Get followers |
| GET | `/api/socials/users/{id}/following/` | Get following |

---

## 🔐 JWT Authentication

### How It Works:

1. **Login** → Get access & refresh tokens
2. **Use** access token in requests:
   ```
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```
3. **Refresh** when access token expires
4. **Client-side logout** - just delete tokens

### Token Lifetimes:
- **Access Token**: 1 day
- **Refresh Token**: 7 days

### Example Login:
```bash
curl -X POST http://localhost:8004/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}'
```

**Response:**
```json
{
  "tokens": {
    "access": "eyJ0eXAi...",
    "refresh": "eyJ0eXAi..."
  },
  "user": {...}
}
```

---

## 🎨 Using Swagger UI

1. Open http://localhost:8004/api/docs/
2. Login to get access token
3. Click **"Authorize"** (🔓 icon)
4. Paste access token
5. Test all endpoints interactively!

---

## 🐳 Docker Setup

### Services:
- **Backend** (Django) - Port 8004
- **PostgreSQL 17** - Port 5433  
- **Redis 7** - Port 6380

### Commands:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose stop

# Rebuild
docker-compose up --build

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

---

## 📦 Tech Stack

- **Django 4.2** - Web framework
- **Django REST Framework** - API toolkit
- **djangorestframework-simplejwt** - JWT authentication
- **drf-spectacular** - Swagger/OpenAPI docs
- **PostgreSQL** - Database
- **Redis** - Caching
- **Docker** - Containerization
- **Pillow** - Image processing

---

## 🔒 Privacy & Permissions

### Profile Privacy:
- **Public**: Anyone can view posts
- **Private**: Only followers can view posts

### Permissions:
- **Posts**: Only owner can update/delete
- **Comments**: Only owner can delete
- **Profiles**: Only owner can update

---

## 🛠️ Development

### Without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 📁 Project Structure

```
Maktab119_TinyInstagram/
├── accounts/              # User & profile management
│   ├── api/v1/
│   │   ├── schemas.py    # Swagger schemas
│   │   ├── serializers.py
│   │   ├── views.py      # JWT auth views
│   │   └── urls.py
│   └── models.py         # User, Profile, OTP
├── socials/              # Social features
│   ├── api/v1/
│   │   ├── schemas.py    # Swagger schemas
│   │   ├── serializers.py
│   │   ├── views.py      # Post, Comment, Follow views
│   │   └── urls.py
│   └── models.py         # Post, Comment, Like, Follow
├── core/                 # Django settings
│   ├── settings.py       # JWT configured
│   └── urls.py           # Main URLs
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Backend container
├── requirements.txt     # Python dependencies
└── JWT_AUTHENTICATION.md # JWT docs
```

---

## 📖 Documentation Files

- **JWT_AUTHENTICATION.md** - Complete JWT authentication guide
- **API Documentation** - http://localhost:8004/api/docs/

---

## 🎯 Key Features

### Authentication ✅
- JWT-based (no sessions)
- Email + OTP registration
- Secure token refresh
- Stateless architecture

### Content Management ✅
- Multi-image posts
- Captions & locations
- Update/delete own content
- Image validation (max 5MB)

### Social Interactions ✅
- Like/unlike posts
- Comment on posts
- Follow/unfollow users
- Privacy-aware interactions

### API Documentation ✅
- Interactive Swagger UI
- Form fields (not JSON)
- File upload support
- Example requests/responses

---

## 🚀 Production Ready

- ✅ Environment variables configured
- ✅ Docker deployment ready
- ✅ PostgreSQL database
- ✅ Redis caching
- ✅ Secure JWT authentication
- ✅ Complete API documentation

---

## 📞 Support

All endpoints are documented at:
- **Swagger UI**: http://localhost:8004/api/docs/
- **ReDoc**: http://localhost:8004/api/redoc/

---

## 🎉 Start Using!

```bash
# Start the project
docker-compose up --build

# Open Swagger UI
http://localhost:8004/api/docs/

# Register → Login → Get JWT Token → Authorize → Use API!
```

**Enjoy your Instagram-like API!** 📸✨
