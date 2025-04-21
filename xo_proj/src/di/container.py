class Container:
    """Контейнер для зависимостей."""
    _instances = {}

    @staticmethod
    def register(name, instance):
        """Регистрируем зависимость в контейнере."""
        Container._instances[name] = instance

    @staticmethod
    def get(name):
        """Получаем зависимость из контейнера."""
        if name not in Container._instances:
            raise ValueError(f"Зависимость с именем '{name}' не найдена.")
        return Container._instances[name]