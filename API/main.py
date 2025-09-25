from typing import Union
import fastapi import FastApi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app = FastAPI()


@app.get(/)
def root():
    return{'API de Indicadores Ambientales'}

@app.get(/munipios)
def root():
    return{'API de Indicadores Ambientales'}


