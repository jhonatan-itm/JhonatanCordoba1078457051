from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Repuesto(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    cantidad: int

almacen: List[Repuesto] = []

@app.post("/repuestos/", response_model=Repuesto)
def crear_repuesto(repuesto: Repuesto):
    almacen.append(repuesto)
    return repuesto

@app.get("/repuestos/", response_model=List[Repuesto])
def listar_repuestos():
    return almacen

@app.get("/repuestos/{repuesto_id}", response_model=Repuesto)
def obtener_repuesto(repuesto_id: int):
    for repuesto in almacen:
        if repuesto.id == repuesto_id:
            return repuesto
    raise HTTPException(status_code=404, detail="Repuesto no encontrado")

@app.put("/repuestos/{repuesto_id}", response_model=Repuesto)
def actualizar_repuesto(repuesto_id: int, repuesto_actualizado: Repuesto):
    for idx, repuesto in enumerate(almacen):
        if repuesto.id == repuesto_id:
            almacen[idx] = repuesto_actualizado
            return repuesto_actualizado
    raise HTTPException(status_code=404, detail="Repuesto no encontrado")

@app.delete("/repuestos/{repuesto_id}")
def eliminar_repuesto(repuesto_id: int):
    for idx, repuesto in enumerate(almacen):
        if repuesto.id == repuesto_id:
            del almacen[idx]
            return {"mensaje": "Repuesto eliminado"}
    raise HTTPException(status_code=404, detail="Repuesto no encontrado")