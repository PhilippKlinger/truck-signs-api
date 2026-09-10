<div align="center">

# Signs for Trucks

![Python version](https://img.shields.io/badge/Python-3.12.x-4c566a?logo=python&&longCache=true&logoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django version](https://img.shields.io/badge/Django-5.2.8-4c566a?logo=django&&longCache=truelogoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django-RestFramework](https://img.shields.io/badge/Django_Rest_Framework-3.16.1-red.svg?longCache=true&style=flat-square&logo=django&logoColor=white&colorA=4c566a&colorB=pink)

![Truck Signs](./src/screenshots/Truck_Signs_logo.png)

__Signs for Trucks__ is an online store to buy pre-designed vinyls with custom lines of letters (often call truck letterings).
The store also allows clients to upload their own designs and to customize them on the website as well.

</div>

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
  - [How to Build the Image](#how-to-build-the-image)
- [Usage](#usage)
  - [Settings](#settings)
  - [Control Application Settings via Env-Variables](#control-application-settings-via-env-variables)
  - [Common Commands](#common-commands)
  - [Running with docker run](#running-with-docker-run)
  - [Persistence and Restarts](#persistence-and-restarts)
  - [Models](#models)
  - [Brief Explanation of the Views](#brief-explanation-of-the-views)
- [CI Workflows](#ci-workflows)
- [Changes and Verification](#changes-and-verification)
- [Repository Contents](#repository-contents)
- [Screenshots of the Django Backend Admin Panel](#screenshots-of-the-django-backend-admin-panel)
  - [Mobile View](#mobile-view)
  - [Desktop View](#desktop-view)
- [Additional Information](#additional-information)
  - [Postgresql Database](#postgresql-database)
  - [Docker](#docker)
  - [Django and DRF](#django-and-drf)
  - [Miscellaneous](#miscellaneous)

## Prerequisites

* [Git](https://git-scm.com/install/)
* Docker Engine or Docker Desktop with Docker Compose v2

## Quickstart

1. Clone the repository:

    ```bash
    git clone <repository-url> truck-signs-api
    cd truck-signs-api
    ```

2. Create the runtime configuration:

    ```bash
    cp .env.example .env
    ```

3. Replace every required blank value in `.env`. Use unique values for
   `SECRET_KEY`, `DB_USER`, `DB_PASSWORD`, and all
   `DJANGO_SUPERUSER_*` variables.

4. Build and start the application:

    ```bash
    docker build -t truck-signs-api:local .
    docker compose config --quiet
    docker compose up -d
    docker compose ps
    ```

The application is available at:

- `http://localhost:8020/`
- `http://localhost:8020/admin/`
- `http://localhost:8020/truck-signs/products/`

### How to Build the Image

Build the default local image:

```bash
docker build -t truck-signs-api:local .
```

To use another image, set its complete reference in `.env`:

```dotenv
BACKEND_IMAGE=ghcr.io/<owner>/<repository>:<tag>
```

The Compose file references an image and does not contain a build context.

## Usage

### Settings

The `settings.py` folder inside the `src/tsa_app` folder contains the different settings configuration for the application.

The `.env.example` file in the project root contains an overview about configuration values that can be set for the app.

### Control Application Settings via Env-Variables

Copy `.env.example` to `.env`, replace the required blank values, and keep
`.env` outside version control.

| Variable | Default or requirement | Purpose |
| --- | --- | --- |
| `MODE` | Compose enforces `prod` | Uses PostgreSQL in the container stack. |
| `DEBUG_ENABLED` | Compose enforces `False` | Disables Django debug mode. |
| `LOG_LEVEL` | `ERROR` | Application log level. |
| `SECRET_KEY` | Required | Django signing key. |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hosts accepted by Django. |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated browser origins accepted by Django. |
| `BACKEND_IMAGE` | `truck-signs-api:local` | Backend image used by Compose. |
| `DB_NAME` | `trucksigns_db` | PostgreSQL database name. |
| `DB_USER` | Required | PostgreSQL account name. |
| `DB_PASSWORD` | Required | PostgreSQL account password. |
| `DB_HOST` | `db` | PostgreSQL hostname; `db` is the Compose service name. |
| `DB_PORT` | `5432` | PostgreSQL port inside the Compose network. |
| `DJANGO_SUPERUSER_USERNAME` | Required | Initial Django administrator name. |
| `DJANGO_SUPERUSER_EMAIL` | Required | Initial Django administrator email address. |
| `DJANGO_SUPERUSER_PASSWORD` | Required | Initial Django administrator password. |

Keep the `DB_HOST` and `DB_PORT` defaults for the supplied Compose stack.
Add the deployment hostname to `ALLOWED_HOSTS` only in the untracked `.env`.

### Common Commands

```bash
docker compose up -d
docker compose ps
docker compose logs --tail 100
docker compose logs -f backend
docker compose restart
docker compose down
```

The entrypoint waits for PostgreSQL, runs migrations and `collectstatic`,
creates the configured superuser if it does not exist, and starts Gunicorn.

### Running with docker run

Docker Compose is the intended way to run the complete stack. To run only the
backend against PostgreSQL on an existing Docker network:

```bash
docker run --rm \
  --name truck-signs-api \
  --network <existing-docker-network> \
  --env-file .env \
  --env DB_HOST=<postgres-hostname-on-that-network> \
  --publish 8020:8000 \
  truck-signs-api:local
```

Do not put real credentials directly into shared commands.

### Persistence and Restarts

PostgreSQL data is stored in the named volume `postgres_data`. Uploaded media
uses `mediafiles_data`. A normal `docker compose down` keeps both volumes.
Static files are regenerated by `collectstatic` when the backend starts.

> [!WARNING]
> `docker compose down -v` deletes the database and media volumes.

Both services use `restart: unless-stopped`.

### Models

Most of the models do what can be inferred from their name. The following dots are notes about some of the models to make clearer their propose:
- __Category Model:__ The category of the vinyls in the store. It contains the title of the category as well as the basic properties shared among products that belong to a same category. For example, _Truck Logo_ is a category for all vinyls that has a logo of a truck plus some lines of letterings (note that the vinyls are instances of the model _Product_). Another category is _Fire Extinguisher_, that is for all vinyls that has a logo of a fire extinguisher.
- __Lettering Item Category:__ This is the category of the lettering, for example: _Company Name_, _VIM NUMBER_, ... Each has a different pricing.
- __Lettering Item Variations:__ This contains a foreign key to the __Lettering Item Category__ and the text added by the client.
- __Product Variation:__ This model has the original product as a foreign key, plus the lettering lines (instances of the __Lettering Item Variations__ model) added by the client.

### Brief Explanation of the Views

Most of the views are CBV imported from _rest_framework.generics_, and they allow the backend api to do the basic CRUD operations expected, and so they inherit from the _ListAPIView_, _CreateAPIView_, _RetrieveAPIView_, ..., and so on.

The behavior of some of the views had to be modified to address functionalities such as creation of order and payment, as in this case, for example, both functionalities are implemented in the same view, and so a _GenericAPIView_ was the view from which it inherits. Another example of this is the _UploadCustomerImage_ View that takes the vinyl template uploaded by the clients and creates a new product based on it.

## CI Workflows

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `build.yaml` | Version-tag push or manual dispatch | Builds the image and pushes `latest` and the current Git ref name to GHCR. |
| `test.yaml` | Relevant push or pull request targeting `main` | Runs Flake8, Black, isort, and the Django tests with Python 3.12. |
| `check-open-pr.yaml` | Push to a non-`main` branch or opening a pull request | Checks that the branch has an open pull request. |

The workflows do not deploy the application to a server.

## Changes and Verification

The container setup was repaired as follows:

- corrected the Python image and pinned PostgreSQL 17 by tag and digest;
- corrected dependency installation, `EXPOSE`, and the entrypoint path and permissions;
- replaced the Compose build context with an image reference;
- removed the PostgreSQL host port and host bind mounts;
- added restart policies, health checking, named persistence, and backend port `8020`;
- added database waiting with `sleep`, migrations, `collectstatic`, idempotent superuser creation, and one Gunicorn start;
- removed insecure Django credential fallbacks.

Verification completed:

- local image build succeeded;
- Compose configuration validation succeeded;
- PostgreSQL became healthy without a published host port;
- the backend returned HTTP `200` on port `8020`;
- `manage.py check` passed and all 28 Django tests succeeded;
- database and superuser data survived stack recreation;
- Gunicorn ran once as PID 1.

## Repository Contents

| Path | Purpose |
| --- | --- |
| `README.md` | Project setup, usage, configuration, and verification. |
| `Dockerfile` | Backend image definition. |
| `docker-compose.yml` | Backend and PostgreSQL runtime configuration. |
| `entrypoint.sh` | Django initialization and Gunicorn startup. |
| `.env.example` | Template for the untracked runtime configuration. |
| `.dockerignore` | Files excluded from the image build context. |
| `.gitignore` | Files excluded from Git. |
| `.github/workflows/` | Build, test, and pull-request workflows. |
| `requirements.txt` | Python dependencies. |
| `pyproject.toml` | Black, isort, and Flake8 configuration. |
| `Procfile` | Legacy process declaration; not used by Compose. |
| `docs/testing.md` | Existing Python quality-check documentation. |
| `src/manage.py` | Django management command entrypoint. |
| `src/tsa_app/` | Django settings, URLs, and WSGI module. |
| `src/tsa_products/` | Models, serializers, views, migrations, and tests. |
| `src/templates/` | Application and admin templates. |
| `src/screenshots/` | Images used by this README. |

> [!NOTE]
> To create Truck vinyls with Truck logos in them, first create the __Category__ Truck Sign,
> and then the __Product__ (can have any name). This is to make sure the frontend retrieves
> the Truck vinyls for display in the Product Grid as it only fetches the products of the
> category Truck Sign.

---

## Screenshots of the Django Backend Admin Panel

### Mobile View

<div style="padding: 0 5rem; width: 100%;  display: flex; gap: 5rem; justify-content: center; flex-wrap: wrap;">

![alt text](./src/screenshots/Admin_Panel_View_Mobile.png)

![alt text](./src/screenshots/Admin_Panel_View_Mobile_2.png)

![alt text](./src/screenshots/Admin_Panel_View_Mobile_3.png)

</div>

### Desktop View


<div style="padding: 0 5rem; width: 100%; display: flex; flex-direction: column; gap: 2rem; align-items: center; justify-content: center;">

![alt text](./src/screenshots/Admin_Panel_View.png)

![alt text](./src/screenshots/Admin_Panel_View_2.png)

![alt text](./src/screenshots/Admin_Panel_View_3.png)

</div>

## Additional Information

### Postgresql Database

- Setup Database: [Digital Ocean Link for Django Deployment on VPS](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

### Docker

- [Docker Oficial Documentation](https://docs.docker.com/)
- Dockerizing Django, PostgreSQL, guinicorn, and Nginx:
    - Github repo of sunilale0: [Link](https://github.com/sunilale0/django-postgresql-gunicorn-nginx-dockerized/blob/master/README.md#nginx)
    - Michael Herman article on testdriven.io: [Link](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)

### Django and DRF

- [Django Official Documentation](https://docs.djangoproject.com/en/5.2/)
- Generate a new secret key: [Stackoverflow Link](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django)
- Modify the Django Admin:
    - Small modifications (add searching, columns, ...): [Link](https://realpython.com/customize-django-admin-python/)
    - Modify Templates and css: [Link from Medium](https://medium.com/@brianmayrose/django-step-9-180d04a4152c)
- [Django Rest Framework Official Documentation](https://www.django-rest-framework.org/)
- More about Nested Serializers: [Stackoverflow Link](https://stackoverflow.com/questions/51182823/django-rest-framework-nested-serializers)
- More about GenericViews: [Testdriver.io Link](https://testdriven.io/blog/drf-views-part-2/)

### Miscellaneous

- Create Virual Environment with Virtualenv and Virtualenvwrapper: [Link](https://docs.python-guide.org/dev/virtualenvs/)
- [Configure CORS](https://www.stackhawk.com/blog/django-cors-guide/)
- [Setup Django with Cloudinary](https://cloudinary.com/documentation/django_integration)
