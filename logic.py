import random
import json
import os
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Slot, Signal, Property, QObject

class LanguageManager(QObject):
    languageChanged = Signal()

    def __init__(self):
        super().__init__()
        self._config_file = "config.json"
        self._translations = {
            "English": {
                "score": "Score",
                "restart": "RESTART",
                "game_over": "GAME OVER",
                "final_score": "Final Score",
                "play_again": "Play Again",
                "made_by": "made with ❤️ by Cristian Zeni"
            },
            "Italian": {
                "score": "Punteggio",
                "restart": "RICOMINCIA",
                "game_over": "FINE GIOCO",
                "final_score": "Punteggio Finale",
                "play_again": "Gioca Ancora",
                "made_by": "fatto con ❤️ da Cristian Zeni"
            }
        }
        self._current_lang = self._load_config()

    def _load_config(self):
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, "r") as f:
                    return json.load(f).get("language", "Italian")
            except: pass
        return "Italian"

    def _save_config(self):
        try:
            with open(self._config_file, "w") as f:
                json.dump({"language": self._current_lang}, f)
        except Exception as e:
            print(f"Error saving config: {e}")

    @Property(str, notify=languageChanged)
    def currentLanguage(self):
        return self._current_lang

    @currentLanguage.setter
    def currentLanguage(self, lang):
        if self._current_lang != lang:
            self._current_lang = lang
            self._save_config()
            self.languageChanged.emit()

    @Slot(str, result=str)
    def text(self, key):
        return self._translations.get(self._current_lang, {}).get(key, key)

class GameBoard(QAbstractListModel):
    ColorRole = Qt.UserRole + 1
    scoreChanged = Signal()
    gameOver = Signal()

    def __init__(self, rows=10, cols=15, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self._grid = []
        self._score = 0
        self.generate_board()

    def rowCount(self, parent=QModelIndex()): return len(self._grid)
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid(): return None
        if role == self.ColorRole: return self._grid[index.row()]
        return None
    def roleNames(self): return {self.ColorRole: b"blockColor"}

    @Slot()
    def resetGame(self): self.generate_board()

    def generate_board(self):
        self.beginResetModel()
        self._grid = [random.randint(1, 3) for _ in range(self.rows * self.cols)]
        self._score = 0
        self.endResetModel()
        self.scoreChanged.emit()

    def get_index(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols: return r * self.cols + c
        return -1

    @Slot(int)
    def handleBlockClick(self, index):
        if index < 0 or index >= len(self._grid): return
        color = self._grid[index]
        if color == 0: return
        r, c = divmod(index, self.cols)
        adjacent = self._find_adjacent(r, c, color)
        if len(adjacent) > 1:
            self.beginResetModel()
            for idx in adjacent: self._grid[idx] = 0
            self._apply_gravity()
            self._apply_horizontal_shift()
            self._score += (len(adjacent) - 1) ** 2
            self.scoreChanged.emit()
            self.endResetModel()
            if not self.has_valid_moves(): self.gameOver.emit()

    def _find_adjacent(self, r, c, color):
        to_visit = [(r, c)]; visited = set()
        while to_visit:
            curr_r, curr_c = to_visit.pop()
            idx = self.get_index(curr_r, curr_c)
            if idx != -1 and idx not in visited and self._grid[idx] == color:
                visited.add(idx)
                to_visit.extend([(curr_r-1, curr_c), (curr_r+1, curr_c), (curr_r, curr_c-1), (curr_r, curr_c+1)])
        return visited

    def _apply_gravity(self):
        for c in range(self.cols):
            column = [self._grid[self.get_index(r, c)] for r in range(self.rows)]
            non_empty = [color for color in column if color != 0]
            new_column = [0] * (self.rows - len(non_empty)) + non_empty
            for r in range(self.rows): self._grid[self.get_index(r, c)] = new_column[r]

    def _apply_horizontal_shift(self):
        grid_by_cols = []
        for c in range(self.cols):
            col = [self._grid[self.get_index(r, c)] for r in range(self.rows)]
            if any(color != 0 for color in col): grid_by_cols.append(col)
        while len(grid_by_cols) < self.cols: grid_by_cols.append([0] * self.rows)
        new_grid = [0] * (self.rows * self.cols)
        for c in range(self.cols):
            for r in range(self.rows): new_grid[r * self.cols + c] = grid_by_cols[c][r]
        self._grid = new_grid

    def has_valid_moves(self):
        for r in range(self.rows):
            for c in range(self.cols):
                color = self._grid[self.get_index(r, c)]
                if color == 0: continue
                for dr, dc in [(0, 1), (1, 0)]:
                    ni = self.get_index(r + dr, c + dc)
                    if ni != -1 and self._grid[ni] == color: return True
        return False

    @Property(int, notify=scoreChanged)
    def score(self): return self._score