import sys
from PyQt5.QtWidgets import *
import math

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_number = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel("Equation: ")
        self.equation = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(label_equation, self.equation)

        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### 사칙연산 버튼을 layout_number 레이아웃에 추가
        layout_number.addWidget(button_plus, 4, 3)
        layout_number.addWidget(button_minus, 3, 3)
        layout_number.addWidget(button_product, 2, 3)
        layout_number.addWidget(button_division, 1, 3)

        ### =, C, CE, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("CE")
        button_clear2 = QPushButton("C")
        button_backspace = QPushButton("Backspace")

        ### =, C, CE backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_clear2.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, C, CE, backspace 버튼을 레이아웃에 추가
        layout_number.addWidget(button_clear, 0, 1)
        layout_number.addWidget(button_clear2, 0, 2)
        layout_number.addWidget(button_backspace, 0, 3)
        layout_number.addWidget(button_equal, 5, 3)

        ### %, 역수, 제곱, 제곱근 버튼 생성
        button_remain = QPushButton("%")
        button_inverse = QPushButton("1/x")
        button_square = QPushButton("x^2")
        button_squareroot = QPushButton("루트 x")
        
        ## %, 역수, 제곱, 제곱근 버튼 클릭 시 시그널 설정
        button_remain.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_inverse.clicked.connect(self.button_inverse_clicked)
        button_square.clicked.connect(self.button_square_clicked)
        button_squareroot.clicked.connect(self.button_squareroot_clicked)

        ## %, 역수, 제곱, 제곱근 버튼 레이아웃에 추가
        layout_number.addWidget(button_remain, 0, 0)
        layout_number.addWidget(button_inverse, 1, 0)
        layout_number.addWidget(button_square, 1, 1)
        layout_number.addWidget(button_squareroot, 1, 2)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number+5, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 5, 1)

        ### 소숫점 버튼과 +/- 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 5, 2)
        
        button_plusminus = QPushButton("+/-")
        button_plusminus.clicked.connect(self.button_plus_minus_clicked)
        layout_number.addWidget(button_plusminus, 5, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_number)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    global clear
    clear = 1
    global number1
    number1 = 0
    global operation1
    def number_button_clicked(self, num):
        global clear
        if(clear == 0):
            self.equation.setText("")
            clear = 1
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        
        global number1
        global operation1
        if(number1 == 0):
            operation1 = operation
            number1 = float(equation)
            self.equation.setText("")
        else:
            if(operation1 == '+'):
                equation = number1 + float(equation)
            elif(operation1 == '-'):
                equation = number1 - float(equation)
            elif(operation1 == '*'):
                equation = number1 * float(equation)
            elif(operation1 == '/'):
                equation = number1 / float(equation)
            elif(operation1 == '%'):
                equation = number1 % float(equation)       
            self.equation.setText("")
            self.equation.setText(str(equation))
            operation1 = operation
            number1 = equation
            global clear
            clear = 0

    def button_equal_clicked(self):
        equation = self.equation.text()
        global number1, operation1
        if(operation1 == '+'):
            equation = number1 + float(equation)
        elif(operation1 == '-'):
            equation = number1 - float(equation)
        elif(operation1 == '*'):
            equation = number1 * float(equation)
        elif(operation1 == '/'):
            equation = number1 / float(equation)
        elif(operation1 == '%'):
            equation = number1 % float(equation)       
        self.equation.setText("")
        self.equation.setText(str(equation))
        number1 = 0
        global clear
        clear = 0

    def button_clear_clicked(self):
        self.equation.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)
    
    def button_inverse_clicked(self):
        equation = self.equation.text()
        equation = float(1)/float(equation)
        self.equation.setText("")
        self.equation.setText(str(equation))

    def button_square_clicked(self):
        equation = self.equation.text()
        equation = math.pow(float(equation), 2)
        self.equation.setText("")
        self.equation.setText(str(equation))

    def button_squareroot_clicked(self):
        equation = self.equation.text()
        equation = math.sqrt(float(equation))
        self.equation.setText("")
        self.equation.setText(str(equation))

    def button_plus_minus_clicked(self):
        equation = self.equation.text()
        equation = -float(equation)
        self.equation.setText("")
        self.equation.setText(str(equation))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())