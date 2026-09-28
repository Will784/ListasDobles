from nicegui import ui

from Models.CategoryCatalog import CategoryCatalog

GLASS = "!bg-white/5 !text-white border border-white/10 rounded-2xl shadow-2xl"


class HistoryView:
    def __init__(self, service):
        self.service = service
        self.search_text = ""
        self.direction = "forward"
        self.name_input = ui.element("div")
        self.price_input = ui.element("div")
        self.category_select = ui.element("div")
        self.position_toggle = ui.element("div")

    @staticmethod
    def pointer_label(node):
        return "NULL" if node is None else node.product.code

    @staticmethod
    def format_price(price):
        return f"${price:,.2f}"

    def build(self):
        ui.dark_mode().enable()
        ui.colors(primary="#6366f1", secondary="#06b6d4", accent="#f43f5e")
        ui.query("body").classes("bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950 text-white")
        ui.keyboard(on_key=self.handle_key)
        with ui.column().classes("w-full max-w-7xl mx-auto p-4 md:p-8 gap-6"):
            self.build_header()
            self.render_navigator()
            with ui.element("div").classes("grid grid-cols-1 lg:grid-cols-3 gap-6 w-full items-start"):
                with ui.column().classes("w-full gap-6 lg:col-span-1 min-w-0"):
                    self.build_form_card()
                    self.build_search_card()
                with ui.column().classes("w-full gap-6 lg:col-span-2 min-w-0"):
                    self.build_chain_card()
                    self.render_pointer_table()

    def build_header(self):
        with ui.row().classes("w-full items-center justify-between gap-4"):
            with ui.row().classes("items-center gap-3"):
                ui.icon("history", size="2.5rem").classes("text-indigo-400")
                with ui.column().classes("gap-0"):
                    ui.label("Historial de Productos").classes("text-3xl font-extrabold")
                    ui.label("Lista doblemente enlazada en acción: previous · current · next").classes(
                        "text-slate-400"
                    )
            self.render_stats()

    @ui.refreshable
    def render_stats(self):
        history = self.service.history
        with ui.row().classes("gap-2"):
            self.stat_chip("Nodos", str(history.size), "account_tree")
            self.stat_chip("head", self.pointer_label(history.head), "first_page")
            self.stat_chip("current", self.pointer_label(history.current), "my_location")
            self.stat_chip("tail", self.pointer_label(history.tail), "last_page")

    def stat_chip(self, title, value, icon):
        with ui.row().classes("items-center gap-2 px-3 py-1 rounded-full bg-white/10"):
            ui.icon(icon).classes("text-indigo-300")
            ui.label(title).classes("text-xs text-slate-400 font-mono")
            ui.label(value).classes("text-sm font-bold font-mono")

    def render_product(self, product, large):
        gradient = CategoryCatalog.gradient_for(product.category)
        icon = CategoryCatalog.icon_for(product.category)
        box_size = "h-40" if large else "h-28"
        with ui.column().classes("w-full items-center gap-2"):
            with ui.column().classes(
                f"w-full {box_size} rounded-xl bg-gradient-to-br {gradient} items-center justify-center gap-1"
            ):
                ui.icon(icon, size="3rem" if large else "2rem").classes("text-white")
                ui.label(product.image_code).classes("text-xs font-mono text-white/80")
            ui.label(product.name).classes("text-lg font-bold text-center")
            price_style = "text-2xl text-emerald-300" if large else "text-lg text-emerald-200"
            ui.label(self.format_price(product.price)).classes(f"font-extrabold {price_style}")
            ui.badge(product.category, color="secondary")
            ui.label(product.code).classes("text-xs font-mono text-slate-400")

    def render_slot(self, title, pointer, node, emphasized, handler):
        style = "!border-2 !border-indigo-400" if emphasized else "opacity-75 hover:opacity-100"
        card = ui.card().classes(f"{GLASS} w-full items-center gap-3 p-5 transition-all {style}")
        with card:
            with ui.row().classes("w-full items-center justify-between"):
                ui.label(title).classes("text-sm font-bold tracking-widest text-indigo-300")
                ui.label(pointer).classes("text-xs font-mono px-2 py-0.5 rounded bg-white/10")
            if node is None:
                with ui.column().classes("w-full h-56 items-center justify-center"):
                    ui.icon("block", size="3rem").classes("text-slate-500")
                    ui.label("NULL").classes("text-2xl font-mono font-bold text-slate-500")
                    ui.label("No hay producto en esta posición").classes("text-xs text-slate-500")
            else:
                self.render_product(node.product, emphasized)
        if node is not None and handler is not None:
            card.classes("cursor-pointer")
            card.on("click", handler)

    @ui.refreshable
    def render_navigator(self):
        history = self.service.history
        current = history.current
        previous_node = current.previous if current is not None else None
        next_node = current.next if current is not None else None
        with ui.card().classes(f"{GLASS} w-full p-6 gap-4"):
            with ui.row().classes("w-full items-center justify-between gap-3"):
                with ui.column().classes("gap-0"):
                    ui.label("Navegador de referencias").classes("text-xl font-bold")
                    ui.label(
                        "Usa los botones, haz clic en las tarjetas laterales o las flechas ← → del teclado"
                    ).classes("text-sm text-slate-400")
                with ui.row().classes("gap-2"):
                    back = ui.button("Anterior", icon="arrow_back", on_click=self.go_previous)
                    back.props("rounded color=primary")
                    back.set_enabled(previous_node is not None)
                    forward = ui.button("Siguiente", icon="arrow_forward", on_click=self.go_next)
                    forward.props("rounded color=primary")
                    forward.set_enabled(next_node is not None)
            if current is None:
                self.render_empty_state()
                return
            with ui.element("div").classes("grid grid-cols-1 lg:grid-cols-3 gap-4 w-full items-center"):
                self.render_slot("ANTERIOR", "current.previous", previous_node, False, self.go_previous)
                self.render_slot("ACTUAL", "current", current, True, None)
                self.render_slot("SIGUIENTE", "current.next", next_node, False, self.go_next)
            back_link = previous_node.next if previous_node is not None else None
            forward_link = next_node.previous if next_node is not None else None
            readout = (
                ("current.previous", previous_node),
                ("current", current),
                ("current.next", next_node),
                ("current.previous.next", back_link),
                ("current.next.previous", forward_link),
            )
            with ui.column().classes("w-full gap-1 p-4 rounded-xl bg-black/30 font-mono text-sm"):
                for key, node in readout:
                    with ui.row().classes("items-center gap-3"):
                        ui.label(key).classes("w-52 text-indigo-300")
                        ui.label("→").classes("text-slate-500")
                        ui.label(self.pointer_label(node)).classes("font-bold")

    def render_empty_state(self):
        with ui.column().classes("w-full items-center py-10 gap-3"):
            ui.icon("inbox", size="3rem").classes("text-slate-500")
            ui.label("El historial está vacío: head, current y tail apuntan a NULL").classes("text-slate-300")
            button = ui.button("Cargar productos de ejemplo", icon="download", on_click=self.load_samples)
            button.props("rounded color=primary")

    def build_form_card(self):
        with ui.card().classes(f"{GLASS} w-full p-5 gap-3"):
            ui.label("Agregar producto").classes("text-lg font-bold")
            self.name_input = ui.input("Nombre del producto").props("outlined dense rounded").classes("w-full")
            self.price_input = (
                ui.number("Precio", min=0, format="%.2f").props("outlined dense rounded prefix=$").classes("w-full")
            )
            self.category_select = (
                ui.select(CategoryCatalog.options(), value=CategoryCatalog.first(), label="Categoría")
                .props("outlined dense rounded")
                .classes("w-full")
            )
            ui.label("Posición de inserción").classes("text-xs text-slate-400")
            self.position_toggle = ui.toggle(
                {"end": "Al final (tail)", "after": "Después del actual"}, value="end"
            ).props("no-caps rounded")
            ui.button("Agregar al historial", icon="add_circle", on_click=self.add_product).props(
                "rounded color=primary"
            ).classes("w-full")

    def build_search_card(self):
        with ui.card().classes(f"{GLASS} w-full p-5 gap-3"):
            ui.label("Buscar producto").classes("text-lg font-bold")
            ui.input(
                "Nombre, categoría o código", on_change=self.handle_search_change
            ).props("outlined dense rounded clearable").classes("w-full")
            self.render_search_results()

    @ui.refreshable
    def render_search_results(self):
        if not self.search_text.strip():
            ui.label("Escribe para recorrer la lista nodo por nodo.").classes("text-sm text-slate-400")
            return
        found = 0
        for node in self.service.search_products(self.search_text):
            found += 1
            product = node.product
            with ui.row().classes("w-full items-center justify-between p-2 rounded-lg bg-white/5"):
                with ui.column().classes("gap-0"):
                    ui.label(product.name).classes("text-sm font-semibold")
                    ui.label(f"{product.code} · {product.category}").classes("text-xs text-slate-400 font-mono")
                ui.button(icon="my_location", on_click=lambda pid=product.product_id: self.go_to(pid)).props(
                    "flat dense round color=primary"
                )
        if found == 0:
            ui.label("Sin resultados para la búsqueda.").classes("text-sm text-amber-300")
        else:
            ui.label(f"{found} resultado(s) encontrado(s)").classes("text-xs text-slate-400")

    def build_chain_card(self):
        with ui.card().classes(f"{GLASS} w-full p-5 gap-3"):
            with ui.row().classes("w-full items-center justify-between gap-3"):
                ui.label("Historial completo").classes("text-lg font-bold")
                with ui.row().classes("items-center gap-2"):
                    ui.toggle(
                        {"forward": "Inicio → Fin (next)", "backward": "Fin → Inicio (previous)"},
                        value=self.direction,
                        on_change=self.change_direction,
                    ).props("no-caps rounded dense")
                    ui.button("Limpiar historial", icon="delete_sweep", on_click=self.ask_clear).props(
                        "rounded outline color=negative dense"
                    )
            self.render_chain()

    @ui.refreshable
    def render_chain(self):
        history = self.service.history
        if history.is_empty():
            ui.label("No hay productos en el historial.").classes("text-slate-400 py-6")
            return
        if self.direction == "forward":
            nodes = history.traverse_forward()
        else:
            nodes = history.traverse_backward()
        with ui.row().classes("w-full items-center gap-2 flex-nowrap overflow-x-auto pb-3"):
            ui.label("NULL").classes("font-mono text-slate-500 px-2")
            for node in nodes:
                ui.icon("sync_alt").classes("text-indigo-300")
                self.render_chain_node(node)
            ui.icon("sync_alt").classes("text-indigo-300")
            ui.label("NULL").classes("font-mono text-slate-500 px-2")

    def render_chain_node(self, node):
        history = self.service.history
        product = node.product
        is_current = node is history.current
        border = "!border-2 !border-indigo-400" if is_current else "border border-white/10"
        with ui.card().classes(f"!bg-white/5 !text-white rounded-xl p-3 gap-1 min-w-[230px] {border}"):
            with ui.row().classes("gap-1 h-5"):
                if node is history.head:
                    ui.badge("HEAD", color="positive")
                if is_current:
                    ui.badge("CURRENT", color="primary")
                if node is history.tail:
                    ui.badge("TAIL", color="secondary")
            with ui.row().classes("items-center gap-2"):
                ui.icon(CategoryCatalog.icon_for(product.category)).classes("text-indigo-300")
                ui.label(product.name).classes("text-sm font-bold")
            ui.label(f"{product.code} · {self.format_price(product.price)}").classes(
                "text-xs font-mono text-slate-300"
            )
            ui.label(f"previous: {self.pointer_label(node.previous)}").classes("text-xs font-mono text-slate-400")
            ui.label(f"next: {self.pointer_label(node.next)}").classes("text-xs font-mono text-slate-400")
            with ui.row().classes("w-full justify-between"):
                ui.button("Ver", icon="visibility", on_click=lambda pid=product.product_id: self.go_to(pid)).props(
                    "flat dense size=sm"
                )
                ui.button(icon="delete", on_click=lambda pid=product.product_id: self.remove_product(pid)).props(
                    "flat dense round size=sm color=negative"
                )

    @ui.refreshable
    def render_pointer_table(self):
        history = self.service.history
        with ui.card().classes(f"{GLASS} w-full p-5 gap-3"):
            ui.label("Tabla de referencias (punteros de cada nodo)").classes("text-lg font-bold")
            if history.is_empty():
                ui.label("Sin nodos para mostrar.").classes("text-slate-400")
                return
            with ui.grid(columns=5).classes("w-full gap-x-4 gap-y-2 font-mono text-sm overflow-x-auto"):
                for header in ("previous", "Nodo", "next", "Producto", "Rol"):
                    ui.label(header).classes("text-indigo-300 font-bold")
                for node in history.traverse_forward():
                    role = ""
                    if node is history.head:
                        role += "HEAD "
                    if node is history.current:
                        role += "CURRENT "
                    if node is history.tail:
                        role += "TAIL"
                    highlight = "text-indigo-300 font-bold" if node is history.current else ""
                    ui.label(self.pointer_label(node.previous)).classes(highlight)
                    ui.label(node.product.code).classes(highlight)
                    ui.label(self.pointer_label(node.next)).classes(highlight)
                    ui.label(node.product.name).classes(highlight)
                    ui.label(role.strip() or "—").classes(highlight)

    def refresh_all(self):
        self.render_stats.refresh()
        self.render_navigator.refresh()
        self.render_chain.refresh()
        self.render_pointer_table.refresh()
        self.render_search_results.refresh()

    def handle_key(self, event):
        if not event.action.keydown:
            return
        if event.key.arrow_left:
            self.go_previous()
        elif event.key.arrow_right:
            self.go_next()

    def handle_search_change(self, event):
        self.search_text = event.value or ""
        self.render_search_results.refresh()

    def change_direction(self, event):
        self.direction = event.value
        self.render_chain.refresh()

    def go_previous(self):
        if not self.service.go_previous():
            ui.notify("Ya estás en el primer producto: previous es NULL", type="warning")
            return
        self.refresh_all()

    def go_next(self):
        if not self.service.go_next():
            ui.notify("Ya estás en el último producto: next es NULL", type="warning")
            return
        self.refresh_all()

    def go_to(self, product_id):
        if self.service.go_to(product_id):
            ui.notify("Producto seleccionado como current", type="info")
        self.refresh_all()

    def add_product(self):
        try:
            self.service.add_product(
                self.name_input.value,
                self.price_input.value,
                self.category_select.value,
                self.position_toggle.value,
            )
        except ValueError as error:
            ui.notify(str(error), type="negative")
            return
        self.name_input.value = ""
        self.price_input.value = 0
        ui.notify("Producto agregado al historial", type="positive")
        self.refresh_all()

    def remove_product(self, product_id):
        if self.service.remove_product(product_id):
            ui.notify("Producto eliminado y referencias reenlazadas", type="positive")
        self.refresh_all()

    def load_samples(self):
        self.service.load_sample_data()
        ui.notify("Productos de ejemplo cargados", type="positive")
        self.refresh_all()

    def ask_clear(self):
        if self.service.history.is_empty():
            ui.notify("El historial ya está vacío", type="warning")
            return
        with ui.dialog() as dialog, ui.card():
            ui.label("¿Seguro que deseas limpiar todo el historial?").classes("text-lg font-bold")
            ui.label("Se desenlazarán todos los nodos y head, current y tail quedarán en NULL.").classes(
                "text-sm text-slate-400"
            )
            with ui.row().classes("w-full justify-end"):
                ui.button("Cancelar", on_click=dialog.close).props("flat")
                ui.button("Limpiar", on_click=lambda: self.confirm_clear(dialog)).props("color=negative")
        dialog.open()

    def confirm_clear(self, dialog):
        self.service.clear_history()
        dialog.close()
        ui.notify("Historial limpiado", type="positive")
        self.refresh_all()