from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty,isValidNumber
from mainwindow import MainWindow
from display import Display
from PySide6.QtCore import Slot
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from info import Info

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        # self.setStyleSheet(f'Font-size: {MEDIUM_FONT_SIZE}px')
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info:'Info', window: 'MainWindow', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['AC', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],  
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()
    
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    
    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                if buttonText == '':
                    continue
                if buttonText == '0':
                    self.addWidget(button, i, 0, 1, 2)
                else: 
                    self.addWidget(button , i , j)
                slot = self._makeSlot(
                    self._insertButtonTextToDisplay,
                    button,
                    )
                self._connectButtonCLicked(button, slot)
    
    def _connectButtonCLicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'AC':
           self._connectButtonCLicked(button, self._clear)

        if text == '◀':
           self._connectButtonCLicked(button, self.display.backspace)
        
        if text in '+-/*^':
            self._connectButtonCLicked(
               button,
                 self._makeSlot(self._operatorClicked, button)
                 )
        if text == '=':
           self._connectButtonCLicked(button, self._eq)
           

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func( *args, **kwargs)
        return realSlot
    
    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText
        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(buttonText) #insert diferente do settext, n apaga o display.
    
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
    
    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada!')
            return
        if self._left is None:
            self._left = float(displayText)
        
        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'
    
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError('Conta incompleta.')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
            self.display.setText(str(result))
        except ZeroDivisionError:
            self._showError('Divisão por zero!')
        except OverflowError:
            self._showError('Essa conta não pode ser realizada.')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result == 'error':
            self._left = None
    
    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
#         msgBox.setInformativeText('''
#          O Lorem Ipsum é um texto modelo da indústria tipográfica e de impressão. 
#             O Lorem Ipsum tem vindo a ser o texto padrão usado 
#             por estas indústrias desde o ano de 1500, quando 
#             uma misturou os caracteres de um texto para criar 
#             um espécime de livro. Este texto não só sobreviveu 5 séculos, 
#             mas também o salto para a tipografia electrónica, 
#             mantendo-se essencialmente inalterada. Foi popularizada 
#             nos anos 60 com a disponibilização das folhas de Letraset, 
#             que continham passagens com Lorem Ipsum, e mais recentemente
#             com os programas de publicação como o Aldus PageMaker que
#             incluem versões do Lorem Ipsum.   
# ''')

        # msgBox.setStandardButtons(
        #      msgBox.StandardButton.Ok|
        #     msgBox.StandardButton.Save|
        #     msgBox.StandardButton.Cancel 
        # )

        msgBox.exec()

        # msgBox.button(msgBox.StandardButton.Ok).setText('Fechar')
        # result = msgBox.exec()

        # if result == msgBox.StandardButton.Ok:
        #     print('usuario clicou em ok')
        # if result == msgBox.StandardButton.Save:
        #     print('usuario clicou em Save')
        # if result == msgBox.StandardButton.Cancel:
        #     print('usuario clicou em Cancel')

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        

    