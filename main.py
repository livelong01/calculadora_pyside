# QSS - Estilos do QT for Python
 # https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
 # Dark Theme
 # https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html

from PySide6.QtWidgets import QApplication # type: ignore
import sys
from display import Display
from mainwindow import MainWindow
from variables import WINDOW_ICON_PATH
from PySide6.QtGui import QIcon 
from info import Info
from style import setupTheme
from buttons import Button, ButtonsGrid




if __name__ == '__main__':
    #  Cria a nossa aplicacao
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    #  Define o Ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #  Info
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)

    #  Display
    display = Display()
    # display.setPlaceholderText('Digite Algo') #OPCIONAL
    window.addWidgetToVLayout(display)

    #  Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

   

    #  Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()