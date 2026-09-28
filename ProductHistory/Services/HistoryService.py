from Models.CategoryCatalog import CategoryCatalog
from Models.Product import Product
from Structures.DoublyLinkedList import DoublyLinkedList


class HistoryService:
    SAMPLE_PRODUCTS = (
        ("Auriculares Inalámbricos Pro", 89.99, "Tecnología"),
        ("Lámpara de Escritorio LED", 34.50, "Hogar"),
        ("Zapatillas Runner Ultra", 119.00, "Deportes"),
        ("Chaqueta Impermeable", 74.90, "Moda"),
        ("Cien Años de Soledad", 18.75, "Libros"),
        ("Set de Bloques Creativos", 42.00, "Juguetes"),
    )

    def __init__(self):
        self.history = DoublyLinkedList()
        self.next_id = 1

    def build_product(self, name, price, category):
        clean_name = (name or "").strip()
        if len(clean_name) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        if price is None or float(price) <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if category not in CategoryCatalog.STYLES:
            raise ValueError("Selecciona una categoría válida.")
        product = Product(self.next_id, clean_name, round(float(price), 2), category)
        self.next_id += 1
        return product

    def add_product(self, name, price, category, position):
        product = self.build_product(name, price, category)
        if position == "after":
            return self.history.add_after_current(product)
        return self.history.add_product(product)

    def remove_product(self, product_id):
        return self.history.remove_product(product_id)

    def search_products(self, text):
        if not text or not text.strip():
            return iter(())
        return self.history.search_products(text)

    def go_previous(self):
        return self.history.go_previous()

    def go_next(self):
        return self.history.go_next()

    def go_to(self, product_id):
        return self.history.go_to(product_id)

    def clear_history(self):
        self.history.clear()

    def load_sample_data(self):
        for name, price, category in self.SAMPLE_PRODUCTS:
            self.add_product(name, price, category, "end")
        self.history.go_to(self.next_id - len(self.SAMPLE_PRODUCTS) + 2)