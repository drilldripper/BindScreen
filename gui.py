# -*- coding: utf-8 -*
import time
import bind_screen
import sys
import os
import subprocess

from PyQt4 import QtCore
from PyQt4 import QtGui


class ShowFolderDialog():
    """フォルダを選ぶ"""
    def __init__(self):
        self.path_name = None
    
    def show_folder_dialog(self, widget):
        fd = QtGui.QFileDialog()
        fp = fd.getExistingDirectory()
        self.path_name = fp
        self.path_name = '"' + self.path_name + '"'
        widget.folder_path_box.setText(self.path_name)
        print(fp)

def ShowDirectory(*args):
    """CUIの引数付き実行"""
    cmd = 'python bind_screen.py'
    print(args)
    for arg in args:
        cmd += ' ' + arg
    print(cmd)
    subprocess.Popen(cmd)
    # subprocess.call(cmd)

def main():
    app = QtGui.QApplication(sys.argv)

    panel = QtGui.QWidget()

    button_box_widget = ButtonBoxWidget(parent=panel)

    panel_layout = QtGui.QVBoxLayout()
    panel_layout.addWidget(button_box_widget)
    panel.setLayout(panel_layout)
    panel.setFixedSize(320, 200)

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle("スクリーン製本")
    main_window.setCentralWidget(panel)
    main_window.show()
    show_folder_dialog = ShowFolderDialog()
    # 本体の実行
    button_box_widget.start_button.clicked.connect(
        lambda: ShowDirectory(show_folder_dialog.path_name,
                              button_box_widget.get_instruction_direction(),
                              button_box_widget.get_opening_direction(),
                              button_box_widget.init_time_box.text(),
                              button_box_widget.interval_time_box.text()))

    # ファイルパスをセットする
    button_box_widget.select_button.clicked.connect(
        lambda: show_folder_dialog.show_folder_dialog(button_box_widget))
   
    app.exec_()


class ButtonBoxWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.start_button = QtGui.QPushButton("実行", parent=self)
        self.select_button = QtGui.QPushButton("フォルダ選択", parent=self)

        # 本の見開き方向
        self.opening_directions_radio = QtGui.QButtonGroup()
        self.opening_left_radio = QtGui.QRadioButton("左開き", parent=self)
        self.opening_right_radio = QtGui.QRadioButton("右開き", parent=self)
        self.opening_directions_radio.addButton(self.opening_left_radio)
        self.opening_directions_radio.addButton(self.opening_right_radio)

        # キーボード入力の方向
        self.opening_instructions_radio = QtGui.QButtonGroup()
        self.instruction_left_radio = QtGui.QRadioButton("←", parent=self)
        self.instruction_right_radio = QtGui.QRadioButton("→", parent=self)
        self.opening_instructions_radio.addButton(self.instruction_left_radio)
        self.opening_instructions_radio.addButton(self.instruction_right_radio)


        self.capture_label = QtGui.QLabel('キャプチャ間隔',self)
        self.init_label = QtGui.QLabel('初期化時間',self)

        # フォルダパス名
        self.folder_path_box = QtGui.QLineEdit(self)
        
        # 撮影間隔
        self.interval_time_box = QtGui.QLineEdit(self)
        
        # 初期化時間
        self.init_time_box = QtGui.QLineEdit(self)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.start_button, 0, 0)
        layout.addWidget(self.select_button, 0, 1)
        layout.addWidget(self.capture_label, 1, 0)
        layout.addWidget(self.interval_time_box, 1, 1)
        layout.addWidget(self.opening_left_radio, 0, 2)
        layout.addWidget(self.opening_right_radio, 0, 3)
        layout.addWidget(self.instruction_left_radio, 1, 2)
        layout.addWidget(self.instruction_right_radio, 1, 3)
        layout.addWidget(self.init_label, 2, 0)
        layout.addWidget(self.init_time_box, 2, 1)
        layout.addWidget(self.folder_path_box, 7, 0, 7, 4)
        self.setLayout(layout)
    
    # 本の見開きを取得
    def get_opening_direction(self):
        if self.opening_left_radio.isChecked() and not self.opening_right_radio.isChecked():
            return "LEFT"
        elif not self.opening_left_radio.isChecked() and self.opening_right_radio.isChecked():
            return "RIGHT"

    # キーボードの命令を取得
    def get_instruction_direction(self):
        if self.instruction_left_radio.isChecked() and not self.instruction_right_radio.isChecked():
            return "{LEFT}"
        elif not self.instruction_left_radio.isChecked() and self.instruction_right_radio.isChecked():
            return "{RIGHT}"


if __name__ == '__main__':
    main()
