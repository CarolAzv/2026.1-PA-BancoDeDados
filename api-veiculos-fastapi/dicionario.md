# Ative o ambiente virtual
venv\Scripts\Activate.ps1

# Dependencias
pip install -r requirements.txt

pip install fastapi uvicorn[standard]


pip freeze > requirements.txt

# Rodar o API
uvicorn app.main:app --reload