from modes import DominanceMode

class SetupOption:
    """Jedna nastavitelná položka v menu."""
    def __init__(self, label: str, values: list, default_index: int = 0):
        self.label = label
        self.values = values
        self.index = default_index

    @property
    def value(self):
        return self.values[self.index]

    def next(self):
        self.index = (self.index + 1) % len(self.values)

    def prev(self):
        self.index = (self.index - 1) % len(self.values)

class SetupScreen:
    def __init__(self):
        self.options = [
            SetupOption("Počet hráčů", [2, 3, 4, 5, 6], default_index=0),
            SetupOption("Herní mód",   ["Dominance"], default_index=0),
            SetupOption("Délka hry",   [20, 100, 200, 300, 500], default_index=0),
            SetupOption("Počáteční skóre", [0 ,50, 100, 200, 500], default_index=1),
            SetupOption("Interval akce",   [10, 20, 30, 50], default_index=1),
            SetupOption("Počáteční pozice", ["Náhodné", "Prázdná"],    default_index=0),
            SetupOption("Velikost mřížky", ["Malá", "Střední", "Velká"], default_index=1),
        ]
        self.selected = 0  # index vybrané položky
        self.player_names = []  # vyplní se po potvrzení počtu hráčů
        self.naming = False    # jsme ve fázi zadávání jmen?
        self.naming_index = 0  # který hráč se právě jmenuje

    def handle_key(self, key) -> bool:
        """Vrátí True pokud je setup dokončen."""
        import pygame
        if self.naming:
            return self._handle_naming(key)

        if key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif key == pygame.K_LEFT:
            self.options[self.selected].prev()
        elif key == pygame.K_RIGHT:
            self.options[self.selected].next()
        elif key == pygame.K_RETURN:
            # přejdi na zadávání jmen
            num_players = self.options[0].value
            self.player_names = [f"Hráč {i+1}" for i in range(num_players)]
            self.naming = True
            self.naming_index = 0
        return False

    def _handle_naming(self, key) -> bool:
        """Vrátí True pokud jsou všechna jména zadána."""
        import pygame
        if key == pygame.K_RETURN:
            self.naming_index += 1
            if self.naming_index >= len(self.player_names):
                return True  # setup dokončen
        elif key == pygame.K_BACKSPACE:
            self.player_names[self.naming_index] = \
                self.player_names[self.naming_index][:-1]
        return False

    def handle_text(self, text: str):
        """Zpracuje textový vstup při zadávání jmen."""
        if self.naming:
            self.player_names[self.naming_index] += text
    
    def build_game(self):
        """Sestaví Game objekt z nastavení."""
        from game import Game
        size_map = {
            "Malá":   (800, 600, 10),   
            "Střední": (1100, 700, 10),
            "Velká":  (1300, 900, 10),
        }
        num_players  = self.options[0].value
        mode_name    = self.options[1].value
        max_ticks    = self.options[2].value
        start_score  = self.options[3].value
        interval     = self.options[4].value
        random_start = self.options[5].value == "Náhodné"
        size_width, size_height, cell_size = size_map.get(self.options[6].value, (800, 600, 10))


        if mode_name == "Dominance":
            mode = DominanceMode(max_ticks=max_ticks)

        game = Game(
            num_players=num_players,
            action_interval=interval,
            mode=mode,
            start_score=start_score,
            player_names=self.player_names,
            random_start=random_start,
            window_width=size_width,
            window_height=size_height,
            cell_size=cell_size
        )
        return game