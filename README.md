# Project Name

Project Name is a Python-based application that uses FastAPI and MongoDB.

## Installation

Follow these steps to set up the project:

```bash
# Step 1: Install virtualenv
pip install virtualenv

# Step 2: Create a virtual environment
python -m venv .venv

# Step 3: Activate the virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Step 4: Install dependencies
pip install -r requirements.txt
```

## Setup MongoDB

1. Go to your MongoDB account.
2. Click on "Connect" and choose "Python" as the driver.
3. Copy the connection string.
4. Update the `.env` file with the MongoDB connection string.

## Running the Project

To start the FastAPI server, run the following command:

```bash
uvicorn app.main:app --reload
```

