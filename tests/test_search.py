import pytest
from unittest.mock import patch
from src.model import Customer
from src.service import search_customers

@pytest.fixture
def mock_customers():
    return [
        Customer(id=1, name="Alejandro", last_name="Zavala", email="ale.zavala@example.com"),
        Customer(id=2, name="Ale", last_name="Perez", email="contacto@ale.com"),
        Customer(id=3, name="Maria", last_name="Gomez", email="maria@ale.com"),
        Customer(id=4, name="Pedro", last_name="Alejandro", email="pedro@test.com")
    ]

@patch('src.service.load_customers')
def test_search_exact_and_partial_order(mock_load, mock_customers):
    # TS-03 y TS-04 ordenamiento
    mock_load.return_value = mock_customers

    results = search_customers("ale")

    assert len(results) == 4
    # Coincidencia exacta "ale" en nombre (id=2) va primero
    assert results[0].id == 2

    # Las parciales se ordenan por apellido: Alejandro (4), Gomez (3), Zavala (1)
    assert results[1].id == 4
    assert results[2].id == 3
    assert results[3].id == 1

@patch('src.service.load_customers')
def test_search_case_insensitive(mock_load, mock_customers):
    # TS-03: Término minúsculas (o viceversa) devuelve cliente de forma insensible
    mock_load.return_value = mock_customers

    # Aunque la búsqueda es en mayúsculas, debe encontrar a "Ale" y a los demás
    results = search_customers("ALE")

    assert len(results) == 4
    assert results[0].id == 2

@patch('src.service.load_customers')
def test_search_unallowed_fields(mock_load, mock_customers):
    # TS-02: Búsqueda que coincida únicamente con campos no permitidos no devuelve resultados
    # Simulamos buscar "555" (un teléfono)
    mock_load.return_value = mock_customers
    results = search_customers("5551234")
    assert len(results) == 0

@patch('src.service.load_customers')
def test_search_no_results(mock_load, mock_customers):
    # Parte de TS-06: Sin coincidencia
    mock_load.return_value = mock_customers

    results = search_customers("invento")
    assert len(results) == 0
