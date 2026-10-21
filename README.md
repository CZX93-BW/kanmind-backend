<div align="center">

# KanMind

### Django REST API for Kanban Project Management

A backend for organizing boards, assigning tasks and collaborating through
comments, with explicit access rules and a repeatable Postman regression suite.

<br>

[![Python](https://img.shields.io/badge/Python_3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](#tech-stack)
[![Django](https://img.shields.io/badge/Django_6.1-092E20?style=for-the-badge&logo=django&logoColor=white)](#tech-stack)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-A30000?style=for-the-badge)](#tech-stack)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](#tech-stack)

[![Regression](https://img.shields.io/badge/Recorded_regression-142_passed-22863A?style=flat-square)](#quality-assurance)
[![Authentication](https://img.shields.io/badge/Authentication-Token-2A3647?style=flat-square)](#authentication)
[![Scope](https://img.shields.io/badge/Project-Solo_backend-2A3647?style=flat-square)](#about-the-project)

<br>

[Windows](#windows-installation) ·
[Linux](#linux-installation) ·
[macOS](#macos-installation) ·
[API](#api-endpoints) ·
[Documentation](#project-documentation)

</div>

---

## Table of Contents

- [KanMind](#kanmind)
    - [Django REST API for Kanban Project Management](#django-rest-api-for-kanban-project-management)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
  - [Features](#features)
    - [Authentication](#authentication)
    - [Boards](#boards)
    - [Tasks](#tasks)
    - [Comments](#comments)
  - [Tech Stack](#tech-stack)
  - [Local Installation](#local-installation)
    - [Prerequisites](#prerequisites)
    - [Windows Installation](#windows-installation)
    - [Linux Installation](#linux-installation)
    - [macOS Installation](#macos-installation)
    - [Environment Configuration](#environment-configuration)
    - [Starting an Existing Installation](#starting-an-existing-installation)
  - [Provided Frontend](#provided-frontend)
  - [Authentication](#authentication-1)
  - [API Endpoints](#api-endpoints)
  - [Access Rules and Data Behavior](#access-rules-and-data-behavior)
    - [Boards](#boards-1)
    - [Tasks](#tasks-1)
    - [Comments](#comments-1)
  - [Project Structure](#project-structure)
  - [Quality Assurance](#quality-assurance)
    - [Recorded Results](#recorded-results)
    - [Run the Regression Collection](#run-the-regression-collection)
  - [Development Commands](#development-commands)
  - [Project Documentation](#project-documentation)
  - [Development Workflow](#development-workflow)
  - [Troubleshooting](#troubleshooting)
  - [Scope and Limitations](#scope-and-limitations)

---

## About the Project

**KanMind Backend** was developed by **Bastian Wollny** as a solo project
during the Developer Akademie fullstack training.

The backend implements the API used by the provided KanMind frontend.
Its responsibilities include data persistence, validation, authentication
and authorization.

| Project information | Details |
| --- | --- |
| Project type | Solo backend project |
| Application interface | REST API |
| Authentication | Email and password with DRF tokens |
| Data storage | Local SQLite database |
| Administration | Django Admin |
| API testing | Postman Desktop |
| Frontend | Provided separately by Developer Akademie |
| Delivery | GitHub repository with local setup instructions |

- [Backend repository](https://github.com/CZX93-BW/kanmind-backend)
- [Provided frontend repository](https://github.com/Developer-Akademie-Backendkurs/project.KanMind)

[Back to contents](#table-of-contents)

## Features

### Authentication

- Registration with password confirmation and password validation
- Email-based login
- Token-authenticated API access
- Authenticated user lookup by email
- Custom user model and email-based Django Admin login

### Boards

- Create, retrieve, update and delete boards
- List boards accessible to the authenticated user
- Manage board membership independently of ownership
- Display member, task, to-do and high-priority task counts

### Tasks

- Create and partially update tasks
- Set status, priority, description and due date
- Assign board members as assignees and reviewers
- Retrieve personal assignee and reviewer task lists
- Restrict task deletion to the creator or board owner

### Comments

- Create and list comments on tasks
- Determine comment authors from the authenticated user
- Restrict deletion to the comment author
- Include comment counts in task representations where required

[Back to contents](#table-of-contents)

## Tech Stack

The following versions were used in the Windows development environment.

| Component | Version | Responsibility |
| --- | --- | --- |
| Python | 3.14.3 | Application language |
| Django | 6.1.2 | Models, migrations, administration and project framework |
| Django REST Framework | 3.18.3 | API views, serializers and authentication |
| django-cors-headers | 4.9.0 | Browser access from the local frontend |
| python-dotenv | 1.2.4 | Local environment configuration |
| SQLite | Included with the Python environment | Relational data storage |
| Postman Desktop | — | API requests and regression testing |
| Git and GitHub | — | Version control and delivery |

<details>
<summary><strong>Pinned Python dependencies</strong></summary>

<br>

```text
asgiref==3.12.1
Django==6.1.2
django-cors-headers==4.9.0
djangorestframework==3.18.3
python-dotenv==1.2.4
sqlparse==0.6.0
tzdata==2026.5
```

Install packages from `requirements.txt` rather than installing individual
packages without version constraints.

</details>

[Back to contents](#table-of-contents)

## Local Installation

Choose the instructions for your operating system. Each path covers cloning,
dependencies, environment configuration, database initialization and startup.

| Operating system | Shell | Installation |
| --- | --- | --- |
| Windows | CMD | [Windows instructions](#windows-installation) |
| Linux | Bash | [Linux instructions](#linux-installation) |
| macOS | Zsh or Bash | [macOS instructions](#macos-installation) |

The application has been exercised under Windows. The Linux and macOS
instructions use the corresponding shell commands but have not yet been
verified by a complete installation on those systems.

### Prerequisites

- Python 3.14 with `pip`, `venv` and SQLite support
- Git
- A text editor
- Postman Desktop for the regression suite
- VS Code with Live Server if using the provided frontend

Python 3.14.3 is the recorded development version.

Download resources:

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Postman](https://www.postman.com/downloads/)

On Linux, the packages required for `venv` and SQLite support depend on your
distribution and Python installation. Ensure they are available for the
Python interpreter used below.

### Windows Installation

Use **CMD**. Run these commands individually from the directory in which
you want to create the project folder.

**1. Check the available tools**

```bat
python --version
git --version
```

Ensure `python` resolves to your Python 3.14 installation.

**2. Clone the repository**

```bat
git clone https://github.com/CZX93-BW/kanmind-backend.git
cd kanmind-backend
```

**3. Create the virtual environment and install dependencies**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m pip check
```

**4. Create the local configuration**

For this fresh installation:

```bat
copy .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open `.env` in your editor. Replace the secret-key placeholder with the
generated value and save:

```dotenv
DJANGO_SECRET_KEY='replace-with-your-generated-secret-key'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

**5. Initialize the database**

```bat
python manage.py migrate
python manage.py check
```

Optional: create an account for Django Admin.

```bat
python manage.py createsuperuser
```

**6. Start the server**

```bat
python manage.py runserver
```

Keep the terminal open. Django Admin is available at
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

Continue with the [frontend](#provided-frontend) or
[API authentication](#authentication).

[Back to contents](#table-of-contents)

### Linux Installation

Use **Bash**. These instructions assume Python 3.14 is available as
`python3.14`.

**1. Check the available tools**

```bash
python3.14 --version
git --version
```

**2. Clone the repository**

```bash
git clone https://github.com/CZX93-BW/kanmind-backend.git
cd kanmind-backend
```

**3. Create the virtual environment and install dependencies**

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

After activation, `python` refers to the virtual environment's interpreter.
Install project packages inside this environment without `sudo`.

**4. Create the local configuration**

For this fresh installation:

```bash
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open `.env` in your editor. Replace the secret-key placeholder with the
generated value and save:

```dotenv
DJANGO_SECRET_KEY='replace-with-your-generated-secret-key'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

**5. Initialize the database**

```bash
python manage.py migrate
python manage.py check
```

Optional: create an account for Django Admin.

```bash
python manage.py createsuperuser
```

**6. Start the server**

```bash
python manage.py runserver
```

Keep the terminal open. Django Admin is available at
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

Continue with the [frontend](#provided-frontend) or
[API authentication](#authentication).

[Back to contents](#table-of-contents)

### macOS Installation

Use **Terminal with Zsh or Bash**. These instructions assume an installed
Python 3.14 interpreter is available as `python3.14`.

**1. Check the available tools**

```bash
python3.14 --version
git --version
```

**2. Clone the repository**

```bash
git clone https://github.com/CZX93-BW/kanmind-backend.git
cd kanmind-backend
```

**3. Create the virtual environment and install dependencies**

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

After activation, use the virtual environment's `python` command for the
remaining steps.

**4. Create the local configuration**

For this fresh installation:

```bash
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open `.env` in your editor. Replace the secret-key placeholder with the
generated value and save:

```dotenv
DJANGO_SECRET_KEY='replace-with-your-generated-secret-key'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

**5. Initialize the database**

```bash
python manage.py migrate
python manage.py check
```

Optional: create an account for Django Admin.

```bash
python manage.py createsuperuser
```

**6. Start the server**

```bash
python manage.py runserver
```

Keep the terminal open. Django Admin is available at
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

Continue with the [frontend](#provided-frontend) or
[API authentication](#authentication).

[Back to contents](#table-of-contents)

### Environment Configuration

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required secret key generated for your installation |
| `DJANGO_DEBUG` | Enables development debug output when set to `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated backend hostnames, without schemes or ports |

The configuration loads `.env` from the project root. Existing operating-system
environment variables take precedence.

Keep `.env` private. Only the template `.env.example` belongs in version control.

The database is created as `db.sqlite3` in the project root when migrations
are applied. No database server, database download or manual table creation
is required.

A fresh database contains no project accounts, boards, tasks or comments.
Register accounts through the API or frontend.

The root URL `http://127.0.0.1:8000/` intentionally returns HTTP 404.
Use `/admin/` or a documented `/api/` route.

### Starting an Existing Installation

Open a terminal in the backend directory.

**Windows CMD:**

```bat
.venv\Scripts\activate.bat
python manage.py runserver
```

**Linux and macOS:**

```bash
source .venv/bin/activate
python manage.py runserver
```

You do not need to clone the repository or recreate `.env` for each session.

[Back to contents](#table-of-contents)

## Provided Frontend

The frontend remains in a separate repository and directory.

From the parent directory of the backend, run:

```text
git clone https://github.com/Developer-Akademie-Backendkurs/project.KanMind.git kanmind-frontend
```

Open `kanmind-frontend` in VS Code and serve it with Live Server configured
to use port `5501`.

Open:

[http://127.0.0.1:5501/pages/auth/login.html](http://127.0.0.1:5501/pages/auth/login.html)

Keep the backend running on port `8000`.

The backend currently allows this exact frontend origin:

```text
http://127.0.0.1:5501
```

CORS configuration is located in `core/settings.py` and applies to `/api/`
routes. A different hostname or port requires an appropriate entry in
`CORS_ALLOWED_ORIGINS`.

`localhost` and `127.0.0.1` are different browser origins.

Register your own account to use the application. Add the board owner to
the board's members if that account should create or update tasks.

After changing membership, refresh the frontend if assignee or reviewer
selections still show the previous members.

[Back to contents](#table-of-contents)

## Authentication

Registration and login are public. Other API operations require a valid token.

Use `Content-Type: application/json` for JSON request bodies.

**Registration — `POST /api/registration/`:**

```json
{
  "fullname": "Example User",
  "email": "example@example.com",
  "password": "YourOwnStrongPassword",
  "repeated_password": "YourOwnStrongPassword"
}
```

**Login — `POST /api/login/`:**

```json
{
  "email": "example@example.com",
  "password": "YourOwnStrongPassword"
}
```

Successful registration and login return these fields:

```json
{
  "token": "<returned-token>",
  "fullname": "Example User",
  "email": "example@example.com",
  "user_id": 1
}
```

The user ID and token are generated by the backend.

Send the returned token with protected requests:

```http
Authorization: Token <returned-token>
```

Use the `Token` prefix, not `Bearer`.

Django Admin uses session authentication through its own login page.

[Back to contents](#table-of-contents)

## API Endpoints

All paths are relative to `/api/` and include a trailing slash.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `registration/` | Register a user |
| POST | `login/` | Log in using email and password |
| GET | `email-check/?email=...` | Look up a user by email |
| GET | `boards/` | List accessible boards |
| POST | `boards/` | Create a board |
| GET | `boards/{board_id}/` | Retrieve a board with members and tasks |
| PATCH | `boards/{board_id}/` | Update a board's title or members |
| DELETE | `boards/{board_id}/` | Delete a board |
| POST | `tasks/` | Create a task |
| PATCH | `tasks/{task_id}/` | Partially update a task |
| DELETE | `tasks/{task_id}/` | Delete a task |
| GET | `tasks/assigned-to-me/` | List tasks assigned to the current user |
| GET | `tasks/reviewing/` | List tasks reviewed by the current user |
| GET | `tasks/{task_id}/comments/` | List task comments |
| POST | `tasks/{task_id}/comments/` | Create a task comment |
| DELETE | `tasks/{task_id}/comments/{comment_id}/` | Delete a comment |

| Status | Meaning |
| --- | --- |
| `200 OK` | Successful read, login or update |
| `201 Created` | Resource created |
| `204 No Content` | Resource deleted; response body is empty |
| `400 Bad Request` | Validation failed |
| `401 Unauthorized` | Authentication is missing or invalid |
| `403 Forbidden` | Authenticated user lacks permission |
| `404 Not Found` | Resource or route was not found |

The [Postman test inventory](postman/TEST_CASES.md) documents the individual
test scenarios and expected statuses.

[Back to contents](#table-of-contents)

## Access Rules and Data Behavior

### Boards

- Owners and members can list, retrieve and update their boards.
- Only the owner can delete a board.
- Ownership does not automatically create board membership.
- Updating `members` replaces the membership list; an empty list is allowed.
- Board deletion cascades to its tasks and their comments.

### Tasks

- Creation and updates require board membership, including for board owners.
- The task creator or board owner can delete a task.
- A task cannot be moved to another board.
- Assignees and reviewers must belong to the task's board.
- Existing assignments are revalidated during task updates.
- Sending `null` explicitly clears an assignee or reviewer.
- Task deletion also deletes its comments.

Requests use `assignee_id` and `reviewer_id`. Responses contain nested
`assignee` and `reviewer` objects, or `null`.

| Task field | Values or behavior |
| --- | --- |
| `status` | `to-do`, `in-progress`, `review`, `done` |
| `priority` | `low`, `medium`, `high` |
| `due_date` | Required on creation; format `YYYY-MM-DD` |
| `description` | Defaults to an empty string |
| `assignee_id` | Optional; accepts `null` |
| `reviewer_id` | Optional; accepts `null` |

Creation requires `board`, `title` and `due_date`.
The default status is `to-do`; the default priority is `medium`.

Personal lists filter by the authenticated user's assignee or reviewer
relationship. Being the reviewer alone does not include a task in
`assigned-to-me`.

### Comments

- Reading and creation require board membership.
- The authenticated user determines the author.
- Only the author can delete a comment.
- Deletion must use the comment's matching task URL.
- Comments are returned chronologically.
- Responses contain `id`, `created_at`, `author` and `content`.
- `author` contains the author's full name.

[Back to contents](#table-of-contents)

## Project Structure

| Directory | Responsibility |
| --- | --- |
| `core/` | Settings, central routing, ASGI and WSGI |
| `auth_app/` | User model, manager, admin and admin forms |
| `auth_app/api/` | Registration, login and email lookup |
| `boards_app/` | Board model and administration |
| `boards_app/api/` | Board serializers, views, permissions and routes |
| `tasks_app/` | Task and comment models and administration |
| `tasks_app/api/` | Task and comment API implementation |
| `postman/` | Regression collection and test inventory |
| `docs/` | Architecture, data model, decisions and testing documentation |

Each application includes its database migrations.

| Layer | Responsibility |
| --- | --- |
| URLs | Map request paths to views |
| Authentication | Identify the requesting user |
| Permissions | Decide whether the user may perform the operation |
| Views | Coordinate request handling and responses |
| Serializers | Validate input and define output representations |
| Models and ORM | Describe relationships and access persistent data |

[Back to contents](#table-of-contents)

## Quality Assurance

### Recorded Results

| Check | Recorded result |
| --- | --- |
| Postman regression | 142 passed, 0 failed |
| Django system checks | No issues identified |
| Migration consistency | No changes detected |
| Git whitespace check | No reported errors |
| Frontend integration | Login and board, task and comment workflows exercised |

The badge at the top reflects a recorded development run.
It is not a live CI status.

### Run the Regression Collection

Import:

```text
postman/KanMind_Backend_Regression.postman_collection.json
```

Then:

1. Start the backend.
2. Open **KanMind Backend - Repeatable Regression** in Postman Desktop.
3. Select **No environment**.
4. Check `kmr_base_url` is `http://127.0.0.1:8000/api`.
5. Open the Collection Runner.
6. Select all **142 requests** in their saved order.
7. Use **one iteration** without a data file.
8. Run the complete collection.

The suite creates its own accounts, credentials and resource IDs.
Requests depend on earlier steps, so run the collection from the beginning.

After a successful run, its board, tasks and comments are deleted.
Five generated users remain because there is no user deletion endpoint.
A failed run may leave its board and related objects for investigation.

The suite contains 142 named test blocks, which can each contain multiple
assertions. Passing them does not measure source-code coverage or guarantee
a result on the instructor's undisclosed tests.

Postman does not enforce browser CORS. Frontend integration requires a
separate browser check.

Further information:

- [Regression collection instructions](postman/README.md)
- [Test inventory](postman/TEST_CASES.md)
- [Project testing strategy](docs/TESTING.md)

[Back to contents](#table-of-contents)

## Development Commands

Run these commands from the backend directory with the virtual environment
activated.

| Command | Purpose |
| --- | --- |
| `python manage.py runserver` | Start the development server |
| `python manage.py migrate` | Apply committed migrations |
| `python manage.py createsuperuser` | Create an administrator |
| `python manage.py check` | Run Django system checks |
| `python manage.py makemigrations --check --dry-run` | Detect missing model migrations |
| `python -m pip check` | Check dependency consistency |
| `git diff --check` | Check changed lines for whitespace errors |
| `git status --short` | Inspect the working tree |
| `deactivate` | Leave the virtual environment |

Use the committed migrations during installation.
Create new migrations only when intentionally changing the data model.

[Back to contents](#table-of-contents)

## Project Documentation

The README provides the setup and usage entry point. The following documents
explain the implementation and the reasoning behind it.

| Document | Questions it addresses |
| --- | --- |
| [Architecture](docs/ARCHITECTURE.md) | How are the apps organized? How is a request processed? |
| [Data Model](docs/DATA_MODEL.md) | How are users, boards, tasks and comments related? What happens on deletion? |
| [Authentication and Permissions](docs/AUTH_AND_PERMISSIONS.md) | How does token authentication work? Who may access or change each resource? |
| [Design Decisions](docs/DESIGN_DECISIONS.md) | Why were these models, serializers, validations and view structures chosen? |
| [Testing](docs/TESTING.md) | How are behavior, permissions, integration and installation checked? |

The API test inventory remains in
[`postman/TEST_CASES.md`](postman/TEST_CASES.md) to keep the executable
collection and its scenario documentation together.

[Back to contents](#table-of-contents)

## Development Workflow

This is a solo project with tasks tracked in Trello.

The working process combines:

- Small implementation steps
- Explicit validation and permission rules
- Postman checks for successful and rejected requests
- Browser checks with the provided frontend
- Focused Conventional Commits
- English code documentation and project documentation

Examples from the project:

```text
feat(boards): add board creation endpoint
fix(auth): validate normalized email before registration
refactor(tasks): move personal task filters into get_queryset
test(api): add repeatable Postman regression collection
docs(core): document project configuration and routing
```

The local database, `.env`, virtual environment and generated caches are
excluded from version control. Migrations and pinned dependencies are included.

[Back to contents](#table-of-contents)

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Connection refused | Start the backend and keep its terminal open. |
| HTTP 404 at `/` | Open `/admin/` or a documented API route. |
| HTTP 401 | Supply a valid `Authorization: Token ...` header. |
| Owner cannot create or update tasks | Add the owner to the board's members. |
| Browser CORS error | Match the frontend origin to `CORS_ALLOWED_ORIGINS`. |
| Stale member selections | Refresh the frontend after changing membership. |
| Missing database tables | Run `python manage.py migrate`. |
| Missing secret key | Create `.env`, set `DJANGO_SECRET_KEY` and restart the server. |
| `python3.14` not found | Install Python 3.14 or use the path to your installed interpreter. |
| Virtual environment creation fails | Check that `venv` and its required components are installed for that interpreter. |
| Postman variables are unresolved | Start the complete regression collection from its first request. |

[Back to contents](#table-of-contents)

## Scope and Limitations

- The project targets local development and assessment.
- Production deployment is outside the project scope.
- Linux and macOS installation instructions still require practical verification.
- The provided frontend is maintained separately.
- The API does not provide user deletion or token revocation endpoints.
- Test users remain after regression runs.
- The recorded regression run is sequential; it does not establish behavior
  under concurrent requests or load.
- Passing project tests does not guarantee the outcome of external tests.

---

<div align="center">

**KanMind — Django REST API for Kanban Project Management**

Developed by Bastian Wollny as a solo backend project
during the Developer Akademie fullstack training.

[Back to contents](#table-of-contents)

</div>