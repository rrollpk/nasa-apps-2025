from typing import Union
from fastapi import FastAPI


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






@app.get('/')
def root():
    return{'API de Indicadores Ambientales'}

@app.get('/municipios')
def root():
    return{'API de Indicadores Ambientales'}





