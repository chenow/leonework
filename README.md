# LEONEWORK

Project for website https://leonework.com
The project aims at conecting students searching for internships or apprenticeships with companies offering them.

The website includes:

-   Presentation pages
-   Inscription pages
-   Matching pages (between students and companies)
-   Chat pages (between students and companies)
-   Administration pages (for the website administrators)
-   Stripe payment
-   Mail sending (for confirmation, password reset, etc.)

## Getting Started

### Prerequisites

Having a python environment with python 3.10 or higher.
having a postgresql database with a user and a password.
A docker-compose file is provided to setup a postgresql database. To do so, run:

    docker-compose up -d

### env & database setup

-   Complete the .env file following .env.example variables.
-   Setup an environment
-   Install the requirements
    ```bash
    pip install -r freeze.txt
    ```
-   Create the database
    ```bash
    python manage.py migrate
    ```

Default users are created with the first migration.

### Usage

Run the server with the following command:

```bash
python manage.py runserver
```

Then navigate to http://127.0.0.1:8000
