# Complete API Documentation 

All API responses follow a standardized format:
```json
{
    "status_code": 200,
    "message": "Success",
    "data": { ... }
}
```

---

## 1. Authentication APIs

### 1.1 Register New User
- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "username": "johndoe",
    "password": "securepassword123",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
        "phone": "1234567890",
        "address": "123 Main St",
        "city": "New York",
        "state": "NY",
        "pincode": "10001",
        "user_type": "customer"
    }
}
```
*Note: `user_type` can be `customer` or `admin`. Admin users get `is_staff=True`*

- **Success Response** (201 Created):
```json
{
    "status_code": 201,
    "message": "Success",
    "data": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "profile": {
            "phone": "1234567890",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "pincode": "10001",
            "user_type": "customer"
        }
    }
}
```

### 1.2 Login
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": {
        "token":{
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        },
        "user": {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "profile": {
                "phone": "1234567890",
                "address": "123 Main St",
                "city": "New York",
                "state": "NY",
                "pincode": "10001",
                "user_type": "customer"
            }
        }
    }
}
```

### 1.3 Refresh Token
- **URL**: `/api/auth/login/refresh/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

### 1.4 Logout
- **URL**: `/api/auth/logout/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

- **Success Response** (205 Reset Content):
```json
{
    "status_code": 205,
    "message": "Success",
    "data": null
}
```

### 1.5 Get Profile
- **URL**: `/api/auth/profile/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "profile": {
            "phone": "1234567890",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "pincode": "10001",
            "user_type": "customer"
        }
    }
}
```

### 1.6 Update Profile
- **URL**: `/api/auth/profile/`
- **Method**: `PUT` or `PATCH`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body** (All fields optional for PATCH):
```json
{
    "first_name": "John Updated",
    "last_name": "Doe",
    "email": "newemail@example.com",
    "profile": {
        "phone": "9876543210",
        "address": "456 New St",
        "city": "Boston",
        "state": "MA",
        "pincode": "02101"
    }
}
```

---

## 2. Service Management APIs

### 2.1 List Services
- **URL**: `/api/services/`
- **Method**: `GET`
- **Auth Required**: No (but only shows active services for non-admins)
- **Query Params**: 
  - `page=1` (pagination)
  - `limit=10` (items per page)

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": {
        "current_page": 1,
        "total_count": 25,
        "total_pages": 3,
        "data": [
            {
                "id": 1,
                "name": "House Cleaning",
                "slug": "house-cleaning",
                "description": "Professional deep cleaning service",
                "base_price": "50.00",
                "duration_minutes": 120,
                "is_active": true,
                "created_at": "2025-12-29T10:00:00Z",
                "updated_at": "2025-12-29T10:00:00Z"
            }
        ]
    }
}
```

### 2.2 Create Service (Admin Only)
- **URL**: `/api/services/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Request Body**:
```json
{
    "name": "House Cleaning",
    "description": "Professional deep cleaning service",
    "base_price": "50.00",
    "duration_minutes": 120,
    "is_active": true
}
```
*Note: `slug` is auto-generated from `name`*

- **Success Response** (201 Created):
```json
{
    "status_code": 201,
    "message": "Success",
    "data": {
        "id": 1,
        "name": "House Cleaning",
        "slug": "house-cleaning",
        "description": "Professional deep cleaning service",
        "base_price": "50.00",
        "duration_minutes": 120,
        "is_active": true,
        "created_at": "2025-12-29T10:00:00Z",
        "updated_at": "2025-12-29T10:00:00Z"
    }
}
```

### 2.3 Get Service Details
- **URL**: `/api/services/{id}/`
- **Method**: `GET`
- **Auth Required**: No

### 2.4 Update Service (Admin Only)
- **URL**: `/api/services/{id}/`
- **Method**: `PUT` or `PATCH`
- **Headers**: `Authorization: Bearer <admin_access_token>`

### 2.5 Delete Service (Admin Only)
- **URL**: `/api/services/{id}/`
- **Method**: `DELETE`
- **Headers**: `Authorization: Bearer <admin_access_token>`

### 2.6 Search Services
- **URL**: `/api/services/search/?q=cleaning`
- **Method**: `GET`
- **Auth Required**: No
- **Query Params**: `q=<search_term>`

---

## 3. Service Provider APIs

### 3.1 Create Service Provider
- **URL**: `/api/providers/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
```json
{
    "user": 1,
    "services": [1, 2, 3],
    "experience_years": 5,
    "is_available": true,
    "rating": "4.50"
}
```

- **Success Response** (201 Created):
```json
{
    "status_code": 201,
    "message": "Success",
    "data": {
        "id": 1,
        "user": 1,
        "services": [1, 2, 3],
        "experience_years": 5,
        "is_available": true,
        "rating": "4.50"
    }
}
```

### 3.2 List Service Providers
- **URL**: `/api/providers/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`
- **Pagination**: Same as services

---

## 4. Booking Management APIs

### 4.1 Create Booking
- **URL**: `/api/bookings/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
```json
{
    "service": 1,
    "provider": 1,
    "scheduled_date": "2025-12-30T10:00:00Z"
}
```
*Note: `booking_number`, `customer`, and `total_amount` are auto-generated*

- **Success Response** (201 Created):
```json
{
    "status_code": 201,
    "message": "Success",
    "data": {
        "id": 1,
        "booking_number": "BK-20251229-A3F",
        "customer": 1,
        "customer_name": "johndoe",
        "provider": 1,
        "provider_name": "jane_provider",
        "service": 1,
        "service_name": "House Cleaning",
        "status": "pending",
        "scheduled_date": "2025-12-30T10:00:00Z",
        "total_amount": "50.00",
        "created_at": "2025-12-29T10:00:00Z",
        "updated_at": "2025-12-29T10:00:00Z",
        "completed_at": null
    }
}
```

### 4.2 List User Bookings
- **URL**: `/api/bookings/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`
- **Query Params**:
  - `search=BK-2025` (Search by booking number, customer name, or service name)
  - `status=pending` (Filter by status: pending, confirmed, in_progress, completed, cancelled)
  - `date=2025-12-30` (Filter by scheduled date YYYY-MM-DD)
- **Note**: Returns only the authenticated user's bookings (all bookings for admins)


### 4.3 Get Booking Details
- **URL**: `/api/bookings/{id}/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`

### 4.4 Update Booking Status (Admin Only)
- **URL**: `/api/bookings/{id}/status/`
- **Method**: `PATCH`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Request Body**:
```json
{
    "status": "confirmed"
}
```
*Valid statuses: `pending`, `confirmed`, `in_progress`, `completed`, `cancelled`*

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": {
        "status": "confirmed"
    }
}
```

### 4.5 Cancel Booking (Customer)
- **URL**: `/api/bookings/{id}/`
- **Method**: `DELETE`
- **Headers**: `Authorization: Bearer <access_token>`
- **Note**: Only works if status is `pending`. Sets status to `cancelled`.

- **Success Response** (204 No Content):
```json
{
    "status_code": 204,
    "message": "Success",
    "data": null
}
```

### 4.6 Admin: View All Bookings
- **URL**: `/api/bookings/admin/all/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`

---

## 5. Activity Logs APIs (Admin Only)

### 5.1 List Activity Logs
- **URL**: `/api/logs/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Query Params**:
  - `action=User Login` (filter by action)
  - `entity_type=Booking` (filter by entity type)
  - `username=johndoe` (filter by username)

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": [
        {
            "id": 1,
            "user_id": 1,
            "username": "johndoe",
            "action": "User Login",
            "entity_type": "User",
            "entity_id": "1",
            "details": {
                "username": "johndoe"
            },
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0...",
            "timestamp": "2025-12-29T10:00:00Z"
        }
    ]
}
```

### 5.2 Create Activity Log (Internal)
- **URL**: `/api/logs/create/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`

### 5.3 User Activity History
- **URL**: `/api/logs/user/{userId}/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`

---

## 6. Analytics APIs (Admin Only)

### 6.1 Dashboard Analytics
- **URL**: `/api/analytics/dashboard/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": {
        "total_bookings": 150,
        "completed_bookings": 120,
        "cancelled_bookings": 10,
        "total_revenue": "15000.00",
        "active_customers": 45,
        "active_providers": 12,
        "today_bookings": 8,
        "today_revenue": "800.00"
    }
}
```

### 6.2 Booking Status Analytics
- **URL**: `/api/analytics/bookings/status/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": [
        {
            "status": "completed",
            "count": 120
        },
        {
            "status": "pending",
            "count": 20
        },
        {
            "status": "cancelled",
            "count": 10
        }
    ]
}
```

### 6.3 Top Booked Services
- **URL**: `/api/analytics/services/top-booked/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Query Params**: `limit=10` (default: 10)

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": [
        {
            "id": 1,
            "name": "House Cleaning",
            "booking_count": 50,
            "base_price": "50.00"
        },
        {
            "id": 2,
            "name": "Plumbing",
            "booking_count": 35,
            "base_price": "75.00"
        }
    ]
}
```

### 6.4 Revenue Analytics
- **URL**: `/api/analytics/revenue/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Query Params**: `days=30` (default: 30)

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": {
        "period_days": 30,
        "total_revenue": "15000.00",
        "daily_breakdown": [
            {
                "date": "2025-12-29",
                "revenue": "500.00",
                "bookings": 5
            },
            {
                "date": "2025-12-28",
                "revenue": "450.00",
                "bookings": 4
            }
        ]
    }
}
```

### 6.5 Provider Performance
- **URL**: `/api/analytics/providers/performance/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <admin_access_token>`

- **Success Response** (200 OK):
```json
{
    "status_code": 200,
    "message": "Success",
    "data": [
        {
            "id": 1,
            "username": "john_provider",
            "total_bookings": 30,
            "completed_bookings": 25,
            "total_revenue": "2500.00",
            "rating": "4.50",
            "is_available": true
        },
        {
            "id": 2,
            "username": "jane_provider",
            "total_bookings": 28,
            "completed_bookings": 22,
            "total_revenue": "2200.00",
            "rating": "4.70",
            "is_available": true
        }
    ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "status_code": 400,
    "message": "Validation Error",
    "data": {
        "email": ["This field must be unique."],
        "password": ["This field is required."]
    }
}
```

### 401 Unauthorized
```json
{
    "status_code": 401,
    "message": "Authentication credentials were not provided.",
    "data": {}
}
```

### 403 Forbidden
```json
{
    "status_code": 403,
    "message": "You do not have permission to perform this action.",
    "data": {}
}
```

### 404 Not Found
```json
{
    "status_code": 404,
    "message": "Not found.",
    "data": {}
}
```

---

## Automatic Activity Logging

The following actions are automatically logged:
- ✅ User Registration
- ✅ User Login
- ✅ Booking Creation
- ✅ Booking Cancellation
- ✅ Booking Status Updates
- ✅ Service Creation
- ✅ Service Updates
- ✅ Service Deletion

All logs include: `username`, `action`, `entity_type`, `entity_id`, `details`, `ip_address`, `user_agent`, and `timestamp`.

---

## Rate Limiting

To ensure API stability, the following rate limits are enforced:
- **Authenticated Users**: 100 requests per 15 minutes.
- **Anonymous Users**: 20 requests per minute.

If you exceed these limits, the API will return a `429 Too Many Requests` response.


Most endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

Tokens expire after 60 minutes. Use the refresh token endpoint to get a new access token.

---

## Admin Panel

Django Jazzmin admin interface available at: `http://127.0.0.1:8000/admin/`

Features:
- Modern, dark-themed UI
- Custom icons for all models
- Read-only activity logs
- Full CRUD for all entities
- Search and filter capabilities
