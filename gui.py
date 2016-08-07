# -*- coding: utf-8 -*
import time
import bind_screen
import sys
import os
import subprocess

from PyQt4 import QtCore
from PyQt4 import QtGui

    
def show_folder_dialog(widget):
    """GUIフォルダ選択"""
    fd = QtGui.QFileDialog()
    folder_path = fd.getExistingDirectory()
    widget.folder_path_box.setText('"' + folder_path + '"')


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
    panel.setFixedSize(400, 300)

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle("スクリーン製本")
    main_window.setCentralWidget(panel)
    main_window.show()

    # スクリプト実行
    button_box_widget.start_button.clicked.connect(
        lambda: ShowDirectory(button_box_widget.folder_path_box.text(),
                              button_box_widget.get_instruction_direction(),
                              button_box_widget.get_opening_direction(),
                              button_box_widget.init_time_box.text(),
                              button_box_widget.interval_time_box.text(),
                              button_box_widget.get_trim_checkbox(),
                              button_box_widget.get_zip_checkbox()
                              ))

    # ファイルパスをセットする
    button_box_widget.select_button.clicked.connect(
        lambda: show_folder_dialog(button_box_widget))
   
    app.exec_()


class ButtonBoxWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.setup_ui()
        

    def setup_ui(self):
        self.start_button = QtGui.QPushButton("実行", parent=self)
        self.select_button = QtGui.QPushButton("フォルダ選択", parent=self)
        self.check_trim = QtGui.QCheckBox("画像のトリミングを行う", self)
        self.check_zip = QtGui.QCheckBox("圧縮フォルダを出力する", self)


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
        self.instruction_up_radio = QtGui.QRadioButton("↑", parent=self)
        self.instruction_down_radio = QtGui.QRadioButton("↓", parent=self)
        self.opening_instructions_radio.addButton(self.instruction_left_radio)
        self.opening_instructions_radio.addButton(self.instruction_right_radio)
        self.opening_instructions_radio.addButton(self.instruction_up_radio)
        self.opening_instructions_radio.addButton(self.instruction_down_radio)

        self.capture_label = QtGui.QLabel('キャプチャ間隔(秒)',self)
        self.init_label = QtGui.QLabel('初期化時間(秒)',self)
        self.input_key_label = QtGui.QLabel('--キー入力--',self)
        self.opening_direction_label = QtGui.QLabel('--見開き方向--',self)
        self.output_folder_path_label = QtGui.QLabel('出力先フォルダ',self)


        # フォルダパス名
        self.folder_path_box = QtGui.QLineEdit(self)
        # 撮影間隔
        self.interval_time_box = QtGui.QLineEdit(self)
        # 初期化時間
        self.init_time_box = QtGui.QLineEdit(self)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.start_button, 0, 0)
        layout.addWidget(self.init_label, 2, 0)
        layout.addWidget(self.init_time_box, 2, 1)

        layout.addWidget(self.capture_label, 1, 0)
        layout.addWidget(self.interval_time_box, 1, 1)

        layout.addWidget(self.opening_direction_label, 0, 3)
        layout.addWidget(self.opening_left_radio, 1, 3)
        layout.addWidget(self.opening_right_radio, 1, 5)

        layout.addWidget(self.input_key_label, 3, 3)
        layout.addWidget(self.instruction_left_radio, 5, 3)
        layout.addWidget(self.instruction_right_radio, 5, 5)
        layout.addWidget(self.instruction_up_radio, 4, 4)
        layout.addWidget(self.instruction_down_radio, 6, 4)

        layout.addWidget(self.folder_path_box, 7, 0, 7, 4)
        layout.addWidget(self.output_folder_path_label, 8, 0)
        layout.addWidget(self.select_button, 8, 1)

        layout.addWidget(self.check_trim, 3, 0, 3, 2)
        layout.addWidget(self.check_zip, 4, 0, 4, 2)

        self.setLayout(layout)


    def get_opening_direction(self):
        """本の見開きを取得"""
        if self.opening_left_radio.isChecked() and not self.opening_right_radio.isChecked():
            return "LEFT"
        elif not self.opening_left_radio.isChecked() and self.opening_right_radio.isChecked():
            return "RIGHT"
        

    def get_instruction_direction(self):
        """キーボードの命令を取得"""
        if self.instruction_left_radio.isChecked():
            return "{LEFT}"
        elif self.instruction_right_radio.isChecked():
            return "{RIGHT}"
        elif self.instruction_up_radio.isChecked():
            return "{UP}"
        elif self.instruction_down_radio.isChecked():
            return "{DOWN}"


    def get_zip_checkbox(self):
        """zipチェックボックスの状態を取得"""
        if self.check_zip.isChecked():
            return "--zip"
        else:
            return ""


    def get_trim_checkbox(self):
        """トリミングチェックボックスの状態を取得"""
        if self.check_trim.isChecked():
            return "--trim"
        else:
            return ""

if __name__ == '__main__':
    main()
