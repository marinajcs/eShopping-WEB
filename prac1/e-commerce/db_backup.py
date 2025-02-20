import subprocess
from pydantic import BaseModel, FilePath, EmailStr, ValidationError
from pymongo import MongoClient

container = "prac1-mongo-1"
port = 27017
output_dir = "/backups"

cmd = f'mongodump -p {port} -o {output_dir}'

try:
    subprocess.run(cmd, check=True, shell=True)
    print("Copia de seguridad exitosa.")
except subprocess.CalledProcessError as e:
    print(f"Error al realizar la copia de seguridad: {e}")
