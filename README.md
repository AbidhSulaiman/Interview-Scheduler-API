# API Development - Process for scheduling interviews

A simple yet powerful API to streamline the process of scheduling interviews. This API allows candidates and interviewers to register their availability and enables HR managers to find common available time slots for interviews. By entering the candidate and interviewer IDs, HR managers can retrieve possible interview slots based on the shared availability of both parties. The solution simplifies the interview scheduling process and reduces the burden of coordinating interview times.


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

## Test API

