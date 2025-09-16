from src.chesstools.controllers import Controller
from src.chesstools.views import View

view = View()
controller = Controller(view)
controller.run()
