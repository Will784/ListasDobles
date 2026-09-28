# Historial de Productos con Lista Doblemente Enlazada

Aplicación web que gestiona el historial de productos consultados por un usuario en una tienda. El núcleo es una **lista doblemente enlazada implementada manualmente**, con nodos que tienen referencias `previous` y `next`.

Todo el código (frontend y backend) está escrito únicamente en Python usando [NiceGUI](https://nicegui.io), que construye la interfaz del navegador a partir de código Python. No se escribe HTML, CSS, JavaScript ni TypeScript.

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
cd ProductHistory
python -m venv venv
source venv/bin/activate
pip install -r Requirements.txt
```

En Windows, activa el entorno con `venv\Scripts\activate`.

## Ejecución

```bash
python Main.py
```

Se abrirá el navegador en `http://localhost:8080`.

## Estructura del proyecto

```
ProductHistory/
├── Main.py
├── Requirements.txt
├── README.md
├── Models/
│   ├── Product.py
│   ├── ProductNode.py
│   └── CategoryCatalog.py
├── Structures/
│   └── DoublyLinkedList.py
├── Services/
│   └── HistoryService.py
└── Views/
    └── HistoryView.py
```

- **Models**: `Product` (datos), `ProductNode` (nodo con `previous` y `next`) y `CategoryCatalog` (iconos y colores por categoría).
- **Structures**: `DoublyLinkedList`, la estructura de datos manual.
- **Services**: `HistoryService` valida datos y coordina la lista.
- **Views**: `HistoryView`, la interfaz construida con Python.

Los directorios no contienen `__init__.py`: se usan paquetes de espacio de nombres de Python 3 para respetar la convención de nombres PascalCase.

## Funcionalidades

- Agregar producto al final (`tail`) o justo después del actual.
- Eliminar producto reenlazando los vecinos.
- Buscar por nombre, categoría o código recorriendo los nodos.
- Navegar al producto anterior y siguiente (botones, tarjetas laterales o flechas ← → del teclado).
- Mostrar el historial completo hacia adelante (`next`) o hacia atrás (`previous`).
- Limpiar historial con confirmación.
- Panel del navegador que muestra `previous`, `current` y `next`, junto con `current.previous.next` y `current.next.previous`.
- Tabla de referencias con los punteros de cada nodo y su rol (HEAD, CURRENT, TAIL).
- Cada producto tiene nombre, precio, categoría, código (`PRD-0001`) e identificador de imagen (`IMG-0001`).

## Uso de la lista doblemente enlazada

Cada `ProductNode` guarda un producto y dos referencias:

```
NULL ⇄ [PRD-0001] ⇄ [PRD-0002] ⇄ [PRD-0003] ⇄ NULL
        head                       tail
```

`DoublyLinkedList` mantiene los punteros `head`, `tail` y `current`. No se usa ninguna lista, `deque` ni arreglo de Python para almacenar los productos.

| Operación | Cómo usa las referencias |
|---|---|
| `add_product` | Enlaza el nuevo nodo tras `tail` y actualiza `tail` y `current`. |
| `add_after_current` | Reconecta `current`, el nuevo nodo y el siguiente en ambos sentidos. |
| `remove_product` | Une `previous` con `next` del nodo eliminado y ajusta `head`, `tail` y `current`. |
| `search_products` | Recorre desde `head` siguiendo `next`. |
| `go_previous` / `go_next` | Mueve `current` a `current.previous` o `current.next`. |
| `traverse_forward` / `traverse_backward` | Recorren con `next` desde `head` o con `previous` desde `tail`. |
| `clear` | Desenlaza cada nodo y deja `head`, `tail` y `current` en `None`. |

Los recorridos son generadores que avanzan por las referencias, sin copiar los nodos a otra estructura.

## Notas

- El historial es único y compartido, y se reinicia al detener el servidor.
- La interfaz usa iconos por categoría en lugar de imágenes externas, para funcionar sin conexión a internet.
