# KaamKarwao Backend

KaamKarwao Backend is a microservice-based backend for an on-demand home and field services marketplace. The platform connects customers who need practical tasks completed with workers who can provide those services. A customer can create a task such as electrical repair, plumbing work, fixture installation, pipe repair, tap replacement, or other household maintenance needs. Available workers can discover open tasks, place bids, communicate availability through the bidding flow, and be assigned once a bid is accepted.

The backend is designed around separated business domains so each major part of the platform can evolve independently. It includes user management, worker/customer roles, locations, categories, task creation, bidding, earnings, reviews, attachments, payment preferences, statuses, configuration, real-time updates, and an API Gateway that routes frontend requests to the correct service.

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
  MessageService/             Task chat, message history, and Agora token endpoints
  WalletService/              User wallet management
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
- RabbitMQ, required only for UserService and LocationService event consumers
- Git

SQLite is used by default for local development. Each Django service stores its own `db.sqlite3`.

## Environment Variables

Create your local environment file from the committed template:

```powershell
Copy-Item .env.example .env
```

Set the placeholder values in `.env`, especially `JWT_SIGNING_KEY` and `INTERNAL_SERVICE_SECRET`. All services and the gateway must use the same values for those two variables. `SUPABASE_*` is required for upload features and `AGORA_*` is required for message call-token endpoints.

The gateway, TaskService, BiddingService, and MessageService load the root `.env` file when started from the repository root. Set the same variables in your shell or provide service-local `.env` files when starting services with a different working directory.

## Install Dependencies

From the project root:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
pip install -r TaskService/requirements.txt
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
python MessageService/manage.py migrate
python WalletService/manage.py migrate
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

## Run the Backend Locally

Open a separate terminal for every process, activate the virtual environment in each terminal, and start Redis before the ASGI services or Celery.

### 1. Start Redis

```powershell
redis-server
```

If UserService or LocationService event consumers are enabled, start RabbitMQ too:

```powershell
rabbitmq-server
```

### 2. Start HTTP Django services

Run these commands from the repository root:
(This will also start the websockets)

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
python WalletService/manage.py runserver 0.0.0.0:8013
```


### 3. Start Celery worker and scheduler

EarningService uses Redis-backed Celery jobs to reset earning totals. With Redis running, open two more terminals:

```bash
cd EarningService
celery -A EarningService worker -l info
```

```bash
cd EarningService
celery -A EarningService beat -l info
```

The worker executes queued tasks. Beat schedules the daily reset at 00:00 UTC and the weekly reset at 00:00 UTC every Monday. Run both processes in development; only one Beat instance should run in a shared environment.

### 4. Start the API Gateway

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
| WalletService | 8013 |
| MessageService | 8014 |

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

Task chat room:

```text
ws://localhost:8014/ws/chat/<task_id>/?token=<access_token>
```

If routed through the gateway, use the gateway WebSocket paths configured in `ApiGateway/index.js`.

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

- Do not commit `env/`, `node_modules/`, `__pycache__/`, `.env`, generated local SQLite databases, or Celery scheduler state. See `.gitignore` for the complete list.
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
cd TaskService
daphne -p 8007 TaskService.asgi:application
```

Run the gateway:

```bash
cd ApiGateway
node index.js
```
