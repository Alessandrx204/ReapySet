from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout

import sys


app = QApplication(sys.argv)

window = QWidget()

btn_txt_element: list[str] = ["Python","Kotlin/Java","C/C++","C#","Ts/JavaScript","GDscript", "Rust","Ruby", "SOON™" ]




def init_mwindow(p_window, p_btn_txt_element:list[str], p_per_row:int=5):


    window_layout = QGridLayout(p_window)
    # each button takes 2 cloumns, ofset od odd rows is +1 column
    for i, program_lang in enumerate(p_btn_txt_element):


        btn_in_row = i // p_per_row #integer division
        index_column = i % p_per_row
        row_offset = 1 if (btn_in_row % 2 == 1) else 0
        col = index_column * 2 + row_offset
        button = QPushButton(program_lang, p_window)
        button.clicked.connect(lambda checked=False, btn_txt=program_lang: print(btn_txt))
        window_layout.addWidget(button, btn_in_row, col, 1, 2)



    p_window.setLayout(window_layout)
    p_window.show()


init_mwindow(window, btn_txt_element)




app.exec()