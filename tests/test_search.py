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

@patch('src.service.load_customers')
def test_search_exact_match_last_name(mock_load):
    # CR-02: Coincidencia exacta en last_name (insensible a mayúsculas/minúsculas) se prioriza antes que parciales
    mock_load.return_value = [
        Customer(id=1, name="Carlos", last_name="Perezosa", email="carlos@example.com"),
        Customer(id=2, name="Lucia", last_name="Perez", email="lucia@example.com"),
        Customer(id=3, name="Perezoso", last_name="Alvarez", email="perezoso@example.com"),
    ]

    results = search_customers("pErEz")

    assert [c.id for c in results] == [2, 3, 1]

@patch('src.service.load_customers')
def test_search_deterministic_tie_breaking_by_id(mock_load):
    # CR-02: Desempate determinista por id ascendente en coincidencias exactas y en parciales con mismo apellido
    mock_load.return_value = [
        Customer(id=10, name="Alex", last_name="Gomez", email="alex10@example.com"),
        Customer(id=4, name="Bruno", last_name="Alex", email="bruno4@example.com"),
        Customer(id=7, name="Alex", last_name="Zavala", email="alex7@example.com"),
        Customer(id=9, name="Alexia", last_name="Lopez", email="alexia9@example.com"),
        Customer(id=3, name="Alexander", last_name="Lopez", email="alexander3@example.com"),
        Customer(id=6, name="Alexis", last_name="Alpha", email="alexis6@example.com"),
    ]

    results = search_customers("alex")

    # Exactas ordenadas por id ascendente: 4, 7, 10
    # Parciales ordenadas por apellido (Alpha -> 6, Lopez -> 3 luego 9)
    assert [c.id for c in results] == [4, 7, 10, 6, 3, 9]

