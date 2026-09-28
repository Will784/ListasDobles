from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    product_id: int
    name: str
    price: float
    category: str

    @property
    def code(self):
        return f"PRD-{self.product_id:04d}"

    @property
    def image_code(self):
        return f"IMG-{self.product_id:04d}"
