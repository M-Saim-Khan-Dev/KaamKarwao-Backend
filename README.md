# KaamKarwao Backend

KaamKarwao Backend is a microservice-based backend for a task marketplace. It includes user management, locations, categories, tasks, bidding, earnings, reviews, attachments, payment preferences, statuses, configuration, and an API Gateway that routes frontend requests to the correct service.

## Project Structure

```text
KaamKarwao Backend/
  ApiGateway/                 Express gateway, auth middleware, route proxying, Swagger docs
  UserService/                Users, auth, profiles, verification
  UserTypeService/            User role/type management
  LocationService/            Countries, cities, areas, locations
  CategoryService/            Categories and subcategories
  PaymentPreferenceService/   Payment preference management
  AttachmentService/          File attachment upload and storage
  TaskService/                Task CRUD, task feed WebSocket, worker assignment
  BiddingService/             Bidding CRUD and bidding WebSocket flow
  EarningService/             Worker earning totals and scheduled resets
  ReviewService/              Reviews and rating aggregation
  StatusService/              Status lookup data
  ConfigurationService/       App configuration
  requirements.txt            Shared Python dependencies
```

## Prerequisites

- Python 3.12+
- Node.js 18+
- Redis, required for Django Channels and Celery
- Git

SQLite is used by default for local development. Each Django service stores its own `db.sqlite3`.

## Environment Variables

Create a root `.env` file in the project directory:

```env
JWT_SIGNING_KEY=replace-with-a-long-random-secret
INTERNAL_SERVICE_SECRET=replace-with-an-internal-service-secret
REDIS_URL=redis://127.0.0.1:6379/0

USER_SERVICE_URL=http://127.0.0.1:8001/
LOCATION_SERVICE_URL=http://127.0.0.1:8002/
USERTYPE_SERVICE_URL=http://127.0.0.1:8003/
CATEGORY_URL=http://127.0.0.1:8004/
PAYMENT_PREFERENCE_URL=http://127.0.0.1:8005/
ATTACHMENT_URL=http://127.0.0.1:8006/
TASK_URL=http://127.0.0.1:8007/
STATUS_SERVICE_URL=http://127.0.0.1:8008/
CONFIG_SERVICE_URL=http://127.0.0.1:8009/
EARNINGS_SERVICE_URL=http://127.0.0.1:8010/
REVIEW_SERVICE_URL=http://127.0.0.1:8011/
BIDDING_SERVICE_URL=http://127.0.0.1:8012/

SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

Supabase values are needed for upload features. If you are not testing uploads, those values can be left unset.

## Install Dependencies

From the project root:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

Install API Gateway dependencies:

```bash
cd ApiGateway
npm install
cd ..
```

## Database Setup

Run migrations for each Django service:

```bash
python UserService/manage.py migrate
python UserTypeService/manage.py migrate
python LocationService/manage.py migrate
python CategoryService/manage.py migrate
python PaymentPreferenceService/manage.py migrate
python AttachmentService/manage.py migrate
python TaskService/manage.py migrate
python StatusService/manage.py migrate
python ConfigurationService/manage.py migrate
python EarningService/manage.py migrate
python ReviewService/manage.py migrate
python BiddingService/manage.py migrate
```

Create admin users only for services where you need admin access:

```bash
python UserService/manage.py createsuperuser
```

## Seed Data

Some services include seed commands. Run the ones you need:

```bash
python UserTypeService/manage.py seed_data
python UserService/manage.py seed_data
python LocationService/manage.py seed_country
python LocationService/manage.py seed_city
python LocationService/manage.py seed_area
python LocationService/manage.py seed_location
python CategoryService/manage.py seed_data
python PaymentPreferenceService/manage.py seed_data
```

## Run Services Locally

Open separate terminals from the project root.

```bash
python UserService/manage.py runserver 0.0.0.0:8001
python LocationService/manage.py runserver 0.0.0.0:8002
python UserTypeService/manage.py runserver 0.0.0.0:8003
python CategoryService/manage.py runserver 0.0.0.0:8004
python PaymentPreferenceService/manage.py runserver 0.0.0.0:8005
python AttachmentService/manage.py runserver 0.0.0.0:8006
python StatusService/manage.py runserver 0.0.0.0:8008
python ConfigurationService/manage.py runserver 0.0.0.0:8009
python EarningService/manage.py runserver 0.0.0.0:8010
python ReviewService/manage.py runserver 0.0.0.0:8011
```

TaskService and BiddingService use Django Channels. Run them with ASGI:

```bash
daphne -b 0.0.0.0 -p 8007 TaskService.asgi:application
daphne -b 0.0.0.0 -p 8012 BiddingService.asgi:application
```

Run the API Gateway:

```bash
cd ApiGateway
node index.js
```

The gateway runs on:

```text
http://localhost:3000
```

## Service Ports

| Service | Port |
| --- | ---: |
| API Gateway | 3000 |
| UserService | 8001 |
| LocationService | 8002 |
| UserTypeService | 8003 |
| CategoryService | 8004 |
| PaymentPreferenceService | 8005 |
| AttachmentService | 8006 |
| TaskService | 8007 |
| StatusService | 8008 |
| ConfigurationService | 8009 |
| EarningService | 8010 |
| ReviewService | 8011 |
| BiddingService | 8012 |

## API Gateway

The frontend should normally call the API Gateway instead of individual services.

Examples:

```http
POST http://localhost:3000/app/register
POST http://localhost:3000/app/login
GET  http://localhost:3000/app/task
GET  http://localhost:3000/app/category
GET  http://localhost:3000/app/bidding
```

Protected routes require:

```http
Authorization: Bearer <access_token>
```

The gateway validates JWTs and forwards user context to services using headers:

```text
X-User-Id
X-Is-Verified
X-Is-Staff
X-Usertype-Id
```

## WebSockets

Task feed:

```text
ws://localhost:8007/ws/tasks/
```

Bidding room for a task:

```text
ws://localhost:8012/ws/bidding/<task_id>/
```

If routed through the gateway, use the gateway WebSocket paths configured in `ApiGateway/index.js`.

## Celery

EarningService uses Celery for scheduled earning resets.

Start Redis first, then run:

```bash
cd EarningService
celery -A EarningService worker -l info
```

In another terminal:

```bash
cd EarningService
celery -A EarningService beat -l info
```

Scheduled tasks:

- `reset_daily_earnings`
- `reset_weekly_earnings`

## API Documentation

Most Django services expose schema routes:

```text
/schema/
/schema/swagger-ui/
```

The API Gateway also exposes aggregated docs:

```text
http://localhost:3000/api-docs
```

## Development Notes

- Do not commit `env/`, `node_modules/`, `__pycache__/`, `.env`, or `db.sqlite3`.
- Run migrations after changing models.
- Keep `JWT_SIGNING_KEY` the same across services and the API Gateway.
- Keep `INTERNAL_SERVICE_SECRET` the same for internal service-to-service calls.
- Use the API Gateway for frontend requests so service auth headers are set consistently.

## Useful Commands

Check pending migrations:

```bash
python UserService/manage.py makemigrations --check
```

Create migrations for a service:

```bash
python TaskService/manage.py makemigrations
python TaskService/manage.py migrate
```

Run a Django service directly:

```bash
python UserService/manage.py runserver 8001
```

Run an ASGI service:

```bash
daphne -p 8007 TaskService.asgi:application
```

Run the gateway:

```bash
cd ApiGateway
node index.js
```
