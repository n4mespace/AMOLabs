#!/bin/python3

import sys

from numpy import (linalg, array, ndarray, concatenate)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QLabel, QGridLayout, QMessageBox,
    QLineEdit, QPushButton, QApplication
)
from typing import List, Tuple


class Lab5(QWidget):
    '''Lab goal is to build a program to solve Linear Equation Systems
    
    Solution works thanks to Jakobi's method
    
    Extends:
        QWidget
    '''
    TEXTSIZE: int = 12
    FONT: QFont = QFont('Arial', TEXTSIZE, QFont.Bold)
    APP_BACKGROUND: str = 'background-color:lightgrey'
    ELEM_BACKGROUND: str = 'background-color:white'
    BTN_BACKGROUND: str = 'background-color:grey'

    # Defaults:
    B: List[List[float]] = [[2.36, 2.37, 2.13],
                            [2.51, 2.4, 2.1],
                            [2.59, 2.41, 2.06]]
    Y: List[float] = [1.48, 1.92, 2.16]

    def __init__(self) -> None:
        '''
        Init main window
        
        '''
        super().__init__()
        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.move(300, 150)
        self.setWindowTitle('Lab5')
        self.setStyleSheet(self.APP_BACKGROUND)

        # Program interface
        self.init_UI()

    @staticmethod
    def solve(B: List[List[float]], Y: List[float]) -> List[float]:
        '''Use Jacobi's method to find SLE's solutions 
        
        Arguments:
            B {List[List[float]]} -- coeffs matrix
            Y {List[float]} -- array of free vars
        
        Returns:
            {List[float]} -- solutions
        
        Raises:
            linalg -- if matrix is singular
        '''
        A: ndarray = concatenate((B, Y), axis=1)

        if not linalg.det(B):
            raise linalg.LinAlgError('Matrix determinant is zero!')

        # Make triangle matrix
        for i in range(A.shape[0]):
            amax = A[i][i]

            for j in range(i + 1, A.shape[0]):
                if A[j][i] > amax:
                    amax = A[j][i]
                    l = j

            temp = array(A[i])
            A[i] = array(A[l])
            A[l] = temp

        # Find norms
        for i in range(A.shape[0]):
            A[i] /= A[i][i]

            for k in range(A.shape[0]):
                if k != i:
                    A[k] -= A[k][i] * A[i]

        # Solution is the last column of A
        solution: List[float] = A.T[-1]
        return solution

    def init_matrix(self) -> None:
        '''
        UI matrix init
        
        '''
        # Placeholders for matrix
        self.x = [[QLineEdit() for _ in range(3)] for _ in range(3)]
        self.y = [QLineEdit() for _ in range(3)]

        # Set default values
        for i in range(len(self.x)):
            for j in range(len(self.x[0])):
                self.x[i][j].setText(str(self.B[i][j]))
                self.x[i][j].setMaximumSize(50, 50)
                self.x[i][j].setStyleSheet(self.ELEM_BACKGROUND)

            self.y[i].setText(str(self.Y[i]))
            self.y[i].setMaximumSize(50, 50)
            self.y[i].setStyleSheet(self.ELEM_BACKGROUND)            

        # Add description
        self.x_lable = [[QLabel(f'x{i+1} * ') for i in range(3)] for _ in range(3)]
        self.equal = [QLabel(' = ') for i in range(3)]

        # Set default font
        [[elem.setFont(self.FONT) for elem in line] for line in self.x_lable]
        [elem.setFont(self.FONT) for elem in self.equal]

    def init_solve_btn(self) -> None:
        '''
        UI button for solution init
        
        '''
        self.btn_solve = QPushButton('Solve')
        self.btn_solve.clicked.connect(self.show_result)
        self.btn_solve.setFont(self.FONT)
        self.btn_solve.setStyleSheet(self.BTN_BACKGROUND)

    def init_UI(self) -> None:
        '''
        UI elements init and attach to grid

        '''
        self.init_matrix()
        self.init_solve_btn()

        # Place elems on a grid
        for i in range(3):
            for j in range(1, 4):
                self.grid.addWidget(self.x_lable[i][j - 1], i + 2, (j) * 2 - 1)
                self.grid.addWidget(self.x[i][j - 1], i + 2, (j) * 2)

            self.grid.addWidget(self.equal[i], i + 2, j * 2 + 1)
            self.grid.addWidget(self.y[i], i + 2, j * 2 + 2)

        self.grid.addWidget(self.btn_solve, 7, 0, 1, 10)
        
        label = QLabel(self)
        label.setText('Matrix:')
        label.setFont(QFont('Arial', 14, QFont.Bold))
        self.grid.addWidget(label, 1, 0, 1, 10)

        self.lbl_result = QLabel('')
        self.lbl_result.setFont(self.FONT)
        self.grid.addWidget(self.lbl_result, 9, 0, 1, 10)


    def show_result(self) -> None:
        '''
        Validate input and show solution
        
        '''
        try:
            B, Y = self.get_input()
            x1, x2, x3 = Lab5.solve(B, Y)

            self.lbl_result.setText(
                f'Result:\nx1 = {x1:.4f}   x2 = {x2:.4f}   x3 = {x3:.4f}')

        except Exception as err:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Incorrect input!')
            msg.setInformativeText(f'Error couse:\n{err}')
            msg.setWindowTitle('Error')
            msg.exec_()

    def get_input(self) -> Tuple[ndarray, ndarray]:
        '''
        Reads input matrix
        
        Returns:
            Tuple[ndarray, ndarray] -- input matrix
        '''
        B = array([[float(elem.text()) for elem in row] for row in self.x])
        Y = array([[float(elem.text())] for elem in self.y])
        return B, Y


if __name__ == '__main__':
    # Init application and run lab5
    app = QApplication(sys.argv[1:])
    lab = Lab5()
    lab.show()
    sys.exit(app.exec_())
