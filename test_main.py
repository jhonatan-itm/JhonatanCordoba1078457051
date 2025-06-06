from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_repuesto():
    response = client.post("/repuestos/", json={
        "id": 1,
        "nombre": "Filtro de aceite",
        "descripcion": "Filtro para motor",
        "cantidad": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["nombre"] == "Filtro de aceite"
    assert data["cantidad"] == 10

def test_listar_repuestos():
    response = client.get("/repuestos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_obtener_repuesto():
    response = client.get("/repuestos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_actualizar_repuesto():
    response = client.put("/repuestos/1", json={
        "id": 1,
        "nombre": "Filtro de aire",
        "descripcion": "Filtro actualizado",
        "cantidad": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Filtro de aire"
    assert data["cantidad"] == 5

def test_eliminar_repuesto():
    response = client.delete("/repuestos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["mensaje"] == "Repuesto eliminado"
