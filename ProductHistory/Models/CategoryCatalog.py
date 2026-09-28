class CategoryCatalog:
    STYLES = {
        "Tecnología": {"icon": "devices", "gradient": "from-indigo-500 to-cyan-400"},
        "Hogar": {"icon": "chair", "gradient": "from-amber-500 to-orange-400"},
        "Moda": {"icon": "checkroom", "gradient": "from-pink-500 to-rose-400"},
        "Deportes": {"icon": "sports_soccer", "gradient": "from-emerald-500 to-lime-400"},
        "Libros": {"icon": "menu_book", "gradient": "from-violet-500 to-fuchsia-400"},
        "Juguetes": {"icon": "toys", "gradient": "from-sky-500 to-blue-400"},
        "Belleza": {"icon": "spa", "gradient": "from-rose-500 to-red-400"},
    }

    @classmethod
    def options(cls):
        return {name: name for name in cls.STYLES}

    @classmethod
    def first(cls):
        return next(iter(cls.STYLES))

    @classmethod
    def icon_for(cls, category):
        return cls.STYLES.get(category, {"icon": "sell"})["icon"]

    @classmethod
    def gradient_for(cls, category):
        return cls.STYLES.get(category, {"gradient": "from-slate-500 to-slate-400"})["gradient"]
