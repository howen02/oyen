# Software Engineering Intern Assessment

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
7) Startup backend server:
   ```bash
   cd backend && uvicorn main:app --reload
   ```
9) Startup frontend server in a separate terminal window:
   ```bash
   cd frontend && open app.html
   ```

You should now see this page
![image](https://github.com/howen02/oyen/assets/108785851/7c04eb96-e527-41bf-93f6-197e2d62dde2)
