# Boatable Social Network

## Introduction

Boatable Social Network is a comprehensive platform that connects boat enthusiasts through a rich ecosystem of services. The platform leverages a microservices architecture to deliver functionalities like social interactions, marketplace transactions, logistics management, and AI-driven assistance, ensuring scalability and maintainability.

## Getting Started

To get started with the Boatable Social Network, follow these steps:

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    ```
2.  Navigate to the project directory:

    ```bash
    cd boatable
    ```
3.  Copy the `.env.example` file to `.env`:

    ```bash
    cp .env.example .env
    ```
4.  Update the `.env` file with your actual database and API keys.
5.  Run the bootstrap script:

    ```bash
    ./scripts/bootstrap.sh
    ```

This will build the Docker containers and start the services.

## Codebase Structure

- **backend/**: FastAPI-powered microservices.
  - **social/**: Manages user profiles, groups, and authentication.
  - **marketplace/**: Handles product listings, services, and order management.
  - **facility/**: Oversees logistics including storage and transportation.
  - **ai/**: Provides chat support and tailored recommendations.
- **frontend/**: Vue 3 + Vite PWA delivering a fluid user experience.
- **infra/**: Contains Kubernetes manifests and Terraform scripts for cloud infrastructure.
- **scripts/**: Utility scripts for bootstrapping and running tests.
- **tests/**: Automated tests to ensure system health.
- **.github/**: CI/CD workflows for continuous integration and testing.

## Functions and Interactions

- **Social Graph & User Interactions**: Real-time connection management, friend requests, and group interactions.
- **Marketplace Operations**: Listing services/products and managing orders through RESTful endpoints.
- **Database Interactions**: Each service uses Pydantic models and ORM for managing database operations.
- **AI Assistance**: Chat functionalities and recommendations powered by custom AI logic.
- **Tools & Apps**: Docker for containerization, Kubernetes for orchestration, and Terraform for infrastructure-as-code.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```
2. Navigate to the project directory:
    ```bash
    cd boatable
    ```
3. Setup environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your database and API key details
    ```
4. Build and run the Docker containers:
    ```bash
    ./scripts/bootstrap.sh
    ```
5. Setup the frontend:
    ```bash
    cd frontend/web
    npm install
    npm run dev
    ```

## DigitalOcean Droplet Ubuntu Deployment

1. Create a new Ubuntu droplet on DigitalOcean.
2. Connect via SSH:
    ```bash
    ssh root@your_droplet_ip
    ```
3. Install Docker and Docker Compose:
    ```bash
    apt update && apt upgrade -y
    apt install docker.io docker-compose -y
    systemctl enable docker
    systemctl start docker
    ```
4. Clone the repository:
    ```bash
    git clone <repository_url>
    cd boatable
    ```
5. Configure production environment:
    ```bash
    cp .env.example .env
    # Edit .env with production database and API keys
    ```
6. Launch the application:
    ```bash
    ./scripts/bootstrap.sh
    ```

## Web Server Hosting and SSL Certification

1. Install and configure Nginx as a reverse proxy:
    ```bash
    apt install nginx -y
    ```
    Example Nginx configuration:
    ```nginx
    server {
        listen 80;
        server_name your_domain.com;
        location / {
            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
    Test and restart Nginx:
    ```bash
    nginx -t
    systemctl restart nginx
    ```
2. Secure your site with SSL using Let's Encrypt:
    ```bash
    apt install certbot python3-certbot-nginx -y
    certbot --nginx -d your_domain.com
    ```
3. Update your domain registrar DNS to point to your droplet's IP.

## Site Setup and Testing

- Verify endpoints:
  - Social: /api/social/...
  - Marketplace: /api/marketplace/...
- Run application tests:
    ```bash
    pytest
    ```
- Monitor logs:
    ```bash
    docker-compose logs -f
    ```

## Troubleshooting

- Ensure Docker and Docker Compose are correctly installed.
- Verify that the environment variables in `.env` are accurate.
- Check Nginx configuration with:
    ```bash
    nginx -t
    ```
- Consult Docker logs for backend service errors.
- For SSL issues, inspect logs in `/var/log/letsencrypt/`.
- Confirm that firewall settings allow traffic on ports 80 and 443.

## Project Structure

```text
boatable/
├── backend/
│   ├── social/                       # FastAPI service for core social graph
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py               # <‑‑ service entrypoint
│   │       ├── models.py             # Pydantic + ORM models
│   │       ├── schemas.py
│   │       ├── crud.py
│   │       ├── database.py          # moved from common for local context import
│   │       └── routers/
│   │           ├── __init__.py
│   │           ├── users.py          # /users endpoints
│   │           └── groups.py         # /groups endpoints
│   │           └── auth.py          # /auth endpoints
│   ├── marketplace/                  # FastAPI service for services/products
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── models.py
│   │       └── routers/
│   │           ├── services.py       # /services endpoints
│   │           └── orders.py         # /orders endpoints
│   ├── facility/                     # Facility & logistics micro‑service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── models.py
│   │       └── routers/
│   │           ├── storage.py        # /storage units
│   │           └── transport.py      # /transport jobs
│   └── ai/                           # AI assistant & recommendations
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app/
│           ├── __init__.py
│           ├── main.py
│           ├── assistants/
│           │   ├── chat.py
│           │   └── recommendations.py
│           └── models.py
│
├── frontend/
│   └── web/                          # Vue 3 + Vite PWA
│       ├── package.json
│       ├── vite.config.ts
│       └── src/
│           ├── main.ts
│           ├── App.vue
│           └── components/
│               ├── Navbar.vue
│               ├── Feed.vue
│               ├── ServiceCard.vue
│               └── ...
│
├── infra/
│   ├── kubernetes/
│   │   ├── base/                     # reusable manifests
│   │   │   ├── namespace.yaml
│   │   │   ├── postgres.yaml
│   │   │   ├── neo4j.yaml
│   │   │   └── elastic.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       │   └── kustomization.yaml
│   │       └── prod/
│   │           └── kustomization.yaml
│   └── terraform/
│       └── main.tf                   # cloud infra as‑code
│
├── scripts/
│   ├── bootstrap.sh                  # local dev bootstrap
│   └── run_tests.sh
│
├── tests/
│   ├── __init__.py
│   └── test_social_health.py
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # build + test pipeline
│
├── .flake8                           # flake8 config
├── .gitignore                        # git ignore
├── docker-compose.yml                # local dev stack
├── Makefile                          # common shortcuts (make dev/test)
├── .env.example                      # sample env vars
└── README.md                         # project overview & getting started
```
