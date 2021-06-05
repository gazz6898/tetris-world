from typing import Callable


class TetrisInput():
    def __init__(self):
        self.keys_held: dict[int, bool] = {}
        self.keydown_handlers: dict[int, list[Callable[[], None]]] = {}
        self.keyup_handlers: dict[int, list[Callable[[], None]]] = {}

    def register_keydown_handler(self,
                                 key: int,
                                 func: Callable[[], None],
                                 cancel_keys: "list[int]" = []) -> None:
        key_handlers = self.keydown_handlers.get(key, [])

        def handler_wrapper(f):
            return lambda: None if any(map(lambda k: self.keys_held.get(k, False), cancel_keys)) else f()

        key_handlers.append(handler_wrapper(func))

        self.keydown_handlers[key] = key_handlers

    def register_keyup_handler(self, key: int, func: Callable[[], None]) -> None:
        key_handlers = self.keyup_handlers.get(key, [])
        key_handlers.append(func)
        self.keyup_handlers[key] = key_handlers

    def handle_keydown_event(self, key):
        for handler in self.keydown_handlers.get(key, []):
            handler()

        self.keys_held[key] = True

    def handle_keyup_event(self, key):
        for handler in self.keyup_handlers.get(key, []):
            handler()

        self.keys_held[key] = False
