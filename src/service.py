from src.model import Customer
from src.storage import load_customers

def search_customers(term: str) -> list[Customer]:
    """
    Filtra y ordena los clientes basados en un término de búsqueda.
    """
    customers = load_customers('data/customers.json')
    term_lower = term.lower()

    exact_matches = []
    partial_matches = []

    for customer in customers:
        name_lower = customer.name.lower()
        last_name_lower = customer.last_name.lower()
        email_lower = customer.email.lower()

        # Coincidencia exacta por nombre o correo
        is_exact = (term_lower == name_lower or term_lower == email_lower)

        if is_exact:
            exact_matches.append(customer)
            continue

        # Coincidencia parcial en nombre, apellido o correo
        if (term_lower in name_lower or
            term_lower in last_name_lower or
            term_lower in email_lower):
            partial_matches.append(customer)

    # Ordenar coincidencias parciales alfabéticamente por apellido
    partial_matches.sort(key=lambda c: c.last_name.lower())

    # Retornar primero exactas, luego parciales
    return exact_matches + partial_matches
