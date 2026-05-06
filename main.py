import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from logic import GameBoard, LanguageManager

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    lang_manager = LanguageManager()
    game_board = GameBoard(10, 15)

    # Esponiamo gli oggetti a QML
    engine.rootContext().setContextProperty("lang", lang_manager)
    engine.rootContext().setContextProperty("gameBoard", game_board)

    qml_file = Path(__file__).parent / "pymarble" / "Main.qml"
    engine.load(str(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)