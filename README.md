# README.md

# Repolit Project

Repolit is a web application designed to manage files and categories with user authentication. This project is structured into a backend and frontend, allowing for a clear separation of concerns.

## Table of Contents

- [README.md](#readmemd)
- [Repolit Project](#repolit-project)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [License](#license)

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/repolit.git
    cd repolit
    ```

2. Create a virtual environment:
    ```
    python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```tall the required packages:
   ```
   pip install -r requirements.txt
    ```
    pip install -r requirements.txt
    ``` up your environment variables in the `.env` file.

## Usage

To start the application, run:
```
python app.py
```

Visit `http://localhost:5000` in your web browser to access the application.

## Project Structure

```
repolit/
├── .env
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── backend/
│   ├── __init__.py
│   ├── models.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── file_controller.py
│   │   └── category_controller.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── supabase_service.py
│   ├── hooks/
│   │   ├── __init__.py
│   │   └── auth_hooks.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── frontend/
│   ├── __init__.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   ├── register_view.py
│   │   ├── file_view.py
│   │   ├── file_upload.py
│   │   └── dashboard_view.py
│   └── components/
│       ├── __init__.py
│       ├── menu_sidebar.py
│       ├── file_card.py
│       └── header.py
│
└── assets/
      └── images/
```


## License

This project is licensed under the GNU v3 License. See the LICENSE file for details.