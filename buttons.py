from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty,isValidNumber, convertToNumber
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
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],  
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
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)


                self.addWidget(button , i , j)
                slot = self._makeSlot(
                self._insertToDisplay,
                buttonText,
                )
                self._connectButtonCLicked(button, slot)
    
    def _connectButtonCLicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
           self._connectButtonCLicked(button, self._clear)

        if text == '◀':
           self._connectButtonCLicked(button, self._backspace)

        if text == 'N':
           self._connectButtonCLicked(button, self._invertNumber)
        
        if text in '+-/*^':
            self._connectButtonCLicked(
               button,
                 self._makeSlot(self._configLeftOp, text)
                 )
        if text == '=':
           self._connectButtonCLicked(button, self._eq)
           
    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func( *args, **kwargs)
        return realSlot
    
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return
        
        number = convertToNumber(displayText) * -1

        self.display.setText(str(number))
        self.display.setFocus()
    
    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(text) #insert diferente do settext, n apaga o display.
        self.display.setFocus()
    
    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()
    
    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada!')
            return
        if self._left is None:
            self._left = convertToNumber(displayText)
        
        self._op = text
        self.equation = f'{self._left} {self._op} ??'
    
    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta.')
            return

        self._right = convertToNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = convertToNumber(result)
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
        self.display.setFocus()

        if result == 'error':
            self._left = None
    
    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox
    
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

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
        self.display.setFocus()

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
        self.display.setFocus()
        

    