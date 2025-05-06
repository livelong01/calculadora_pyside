from PySide6.QtWidgets import  QMainWindow, QVBoxLayout, QWidget # type: ignore




class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # COnfigurando o layout basico
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)

        #  titulo da janela
        self.setWindowTitle('Calculadora')

    def adjustFixedSize(self):
        # Ultima coisa a ser feita
        self.adjustSize()
        # dps q ela abrir, vai se ajustar e vai ficar fixa naquele tamanho.
        self.setFixedSize(self.width(), self.height())
    
    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)


    