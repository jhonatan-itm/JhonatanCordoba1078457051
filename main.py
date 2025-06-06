from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

class Repuesto(BaseModel):
    id: int = Field(..., gt=0, description="ID must be a positive integer")
    nombre: str = Field(..., min_length=1)
    descripcion: Optional[str] = None
    cantidad: int = Field(..., ge=0, description="Cantidad debe ser 0 o mayor")

class RepuestoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = Field(None, ge=0)

almacen: List[Repuesto] = []

def encontrar_repuesto(repuesto_id: int) -> Optional[int]:
    for idx, repuesto in enumerate(almacen):
        if repuesto.id == repuesto_id:
            return idx
    return None

@app.post("/repuestos/", response_model=Repuesto, status_code=201)
def crear_repuesto(repuesto: Repuesto):
    if encontrar_repuesto(repuesto.id) is not None:
        raise HTTPException(status_code=400, detail="El ID del repuesto ya existe")
    almacen.append(repuesto)
    logging.info(f"Repuesto creado: {repuesto}")
    return repuesto

@app.get("/repuestos/", response_model=List[Repuesto])
def listar_repuestos():
    return almacen

@app.get("/repuestos/{repuesto_id}", response_model=Repuesto)
def obtener_repuesto(repuesto_id: int):
    idx = encontrar_repuesto(repuesto_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    return almacen[idx]

@app.put("/repuestos/{repuesto_id}", response_model=Repuesto)
def actualizar_repuesto(repuesto_id: int, repuesto_actualizado: Repuesto):
    idx = encontrar_repuesto(repuesto_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    if repuesto_id != repuesto_actualizado.id:
        raise HTTPException(status_code=400, detail="No se puede cambiar el ID del repuesto")
    almacen[idx] = repuesto_actualizado
    logging.info(f"Repuesto actualizado: {repuesto_actualizado}")
    return repuesto_actualizado

@app.patch("/repuestos/{repuesto_id}", response_model=Repuesto)
def modificar_parcial_repuesto(repuesto_id: int, cambios: RepuestoUpdate):
    idx = encontrar_repuesto(repuesto_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    stored = almacen[idx]
    update_data = cambios.dict(exclude_unset=True)
    actualizado = stored.copy(update=update_data)
    almacen[idx] = actualizado
    logging.info(f"Repuesto modificado parcialmente: {actualizado}")
    return actualizado

@app.delete("/repuestos/{repuesto_id}", status_code=200)
def eliminar_repuesto(repuesto_id: int):
    idx = encontrar_repuesto(repuesto_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    eliminado = almacen.pop(idx)
    logging.info(f"Repuesto eliminado: {eliminado}")
    return {"mensaje": f"Repuesto con ID {repuesto_id} eliminado correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
