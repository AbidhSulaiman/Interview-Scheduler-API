# API Development - Process for scheduling interviews

A simple API to streamline the process of scheduling interviews. This API allows candidates and interviewers to register their availability and enables HR managers to find common available time slots for interviews. By entering the candidate and interviewer IDs, HR managers can retrieve possible interview slots based on the shared availability of both parties. The solution simplifies the interview scheduling process and reduces the burden of coordinating interview times.

### Key Features

- **Implemented Token Authentication**  
  - Ensures only authenticated users can add or update availability slots.
  - Tokens are issued upon login and must be included in the `Authorization` header for protected endpoints.

- **Admin-Only Access for Common Slot Retrieval**  
  - The `get-interview-slots/` endpoint is accessible only to admin users (HR).
  - Ensures secure and restricted access to sensitive functionality.

## Installation

### Start the Application Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AbidhSulaiman/Interview-Scheduler-API.git
   cd Interview-Scheduler-API


2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate # For macOS/Linux
   venv\Scripts\activate # For Windows

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Apply Migrations**
   ```bash
   python manage.py migrate

5. **Run the Server**
   ```bash
   python manage.py runserver

# API Testing with Postman

## 1. Login

To authenticate a user and retrieve a token for subsequent requests, send a POST request to the login endpoint.

### Endpoint:
**POST** `authenticate/login/`

### Request Body (JSON):

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

### Request Response (JSON):

```json
{
    "message": "Login successful",
    "token": "your_token_here"
}
```

## 2. Register Availability

Authenticated users can register or update their availability slots by sending a POST request to the register-availability/ endpoint.

### Endpoint:
**POST** `availability/register-availability/`

### Request Headers:
```json
  Authorization: Token your_token_here
```
### Request Body (JSON):

```json
{
 "date": "2025-01-11",
 "start_time": "09:00:00",
 "end_time": "17:00:00"
 }
```

### Request Response (JSON):

```json
{
"message": "Availability registered successfully.",
 "data": {
   "date": "2025-01-11",
   "start_time": "09:00:00",
   "end_time": "17:00:00"
 }
 }
```
## 3. Get Interview Slots

Admins (HR) can retrieve common interview slots between a candidate and an interviewer by sending a GET request to the get-interview-slots/ endpoint.

### Endpoint:
**GET** `availability/get-interview-slots/`

### Request Headers:
```json
  Authorization: Token your_token_here
```
### Query Parameters:

candidate_id: The ID of the candidate
interviewer_id: The ID of the interviewer
**GET** `/get-interview-slots/?candidate_id=1&interviewer_id=2`

### Request Response (JSON):

```json
{
    "common_slots": [
        {
            "date": "2025-01-11",
            "start_time": "09:00:00",
            "end_time": "10:00:00"
        },
        {
            "date": "2025-01-11",
            "start_time": "11:00:00",
            "end_time": "12:00:00"
        }
    ]
}

```

## Tech Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: SQLite
- **Testing**: Django TestCase

## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```

  


