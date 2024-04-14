## Setting up
1) Clone the repository:
   ```bash
   git clone https://github.com/howen02/oyen.git
   ```
4) Change into the project directory:
   ```bash
   cd oyen
   ```
6) Ensure you have Python installed with:
   ```bash
   python3 --version
   ```
   If not, you can install it [here](https://www.python.org/downloads/)
8) Create a virtual environment:
   - On macOS and Linux:
     ```bash
     python3 -m venv venv
     ```
   - On Windows:
     ```bash
     py -m venv venv
     ```
9) Activate the virtual environment:
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
5) Install python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6) Startup frontend server:
    - On macOS and Linux:
        ```bash
        cd frontend && open app.html
        ```
   - On Windows:
     ```bash
     cd frontend && app.html
     ```
7) Startup backend server:
   ```bash
   cd .. && cd backend && uvicorn main:app --reload
   ```

You should now see this page
<img width="1457" alt="image" src="https://github.com/howen02/oyen/assets/108785851/094ba55e-60c7-4527-9ccb-eaee2b6dc72f">

## How it Works
### Signing Up
- User has to input a unique username and password
- Frontend sends a POST request to the backend
- Backend does the following:
   - Checks if username is unique, rejects register if not unique
   - Hashes the password
   - Stores the username and password in the database, along with an ID for the user
### Signing In
- User has to input their registered username and password
- Frontend sends a POST request to the backend to verify if the user has a registered account
- Backend does the following:
   - Look for the user whose username matches the input, rejects if the user does not exist
   - Verifies if the input password hash matches the stored password hash, rejects if password does not match
   - Generates a JWT (JSON Web Token) and stores it in the user's local storage
### Navigating Pages
- If the user already has a valid JWT in their local storage, they get redirected from `app.html` to the login-gated page `home.html`
