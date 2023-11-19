"""
-*- coding: utf-8 -*-
@CreateTime: 2023/7/17 22:02
@Author: Trainer Chan
@Description: ''''''
"""
import sys
import time
import threading

import cv2
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.firstui import Ui_Form as FirstUi
from ui.secondui import Ui_Form as SecondUi
from ui.thirdui import Ui_Form as ThirdUi
from ui.fourthui import Ui_Form as FourthUi
from ui.stichingui import Ui_Form as StichingUi
from ui.settingsui import Ui_Dialog as SettingsUi
from ui.informationui import Ui_Dialog as InformationUi
from ui.warningui import Ui_Dialog as WarningUi
from settings import SettingsConfig

# BG_COLOR = '#7CA7AE'
SETTING_MANAGE = SettingsConfig()


class SettingsWin(QDialog, SettingsUi):

    def __init__(self, parent=None):
        super(SettingsWin, self).__init__(parent)
        self.setupUi(self)

        self.comboBox.currentTextChanged.connect(self.bits_change)

    def bits_change(self, bits_text):
        SETTING_MANAGE.set_param('BIT_TYPE', bits_text)
        QMessageBox.information(self, 'Success', 'Succeed to Set Bit Type')


class InformationWin(QDialog, InformationUi):
    def __init__(self, parent=None):
        super(InformationWin, self).__init__(parent)
        self.setupUi(self)


class WarningWin(QDialog, WarningUi):

    def __init__(self, parent=None):
        super(WarningWin, self).__init__(parent)
        self.setupUi(self)
        warning_icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
        self.setWindowIcon(warning_icon)
        self.headicon_label.setPixmap(warning_icon.pixmap(48, 48))

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.second_win = SecondWin()
        self.second_win.show()
        self.close()


class PromptWin(QMessageBox):

    def __init__(self, parent=None, title='自动绘画UI', message='<p>Tool on WorkPiece ?</p>', icon=QMessageBox.Information):
        super(PromptWin, self).__init__(parent)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        yes_btn = self.button(QMessageBox.Yes)
        no_btn = self.button(QMessageBox.No)
        self.setFont(font)
        yes_btn.setFont(font)
        no_btn.setFont(font)

        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(icon)


class FirstWin(QWidget, FirstUi):
    def __init__(self, parent=None):
        super(FirstWin, self).__init__(parent)
        self.setupUi(self)

        self.setting_btn.clicked.connect(self.pop_setting)
        self.information_btn.clicked.connect(self.pop_information)
        self.start_btn.clicked.connect(self.go_second)

    def go_second(self):
        self.warning_win = WarningWin()
        self.warning_win.show()
        self.close()

    def pop_setting(self):
        self.setting_win = SettingsWin()
        self.setting_win.show()

    def pop_information(self):
        self.information_win = InformationWin()
        self.information_win.show()


class SecondWin(QWidget, SecondUi):
    def __init__(self, parent=None):
        super(SecondWin, self).__init__(parent)
        self.setupUi(self)

        self.add_btn.clicked.connect(self.go_third)
        self.back_btn.clicked.connect(self.back_first)

    def back_first(self):
        self.first_win = FirstWin()
        self.first_win.show()
        self.close()

    def go_third(self):
        self.third_win = ThirdWin()
        self.third_win.show()
        self.close()


class ThirdWin(QWidget, ThirdUi):

    def __init__(self, parent=None):
        super(ThirdWin, self).__init__(parent)
        self.setupUi(self)

        self.img_path = None

        self.add_btn.clicked.connect(self.select_img)
        self.back_btn.clicked.connect(self.back_second)
        self.start_btn.clicked.connect(self.go_fourth)

    def back_second(self):
        self.second_win = SecondWin()
        self.second_win.show()
        self.close()

    def select_img(self):
        # 选择图片
        file_type_list = ['jpg', 'png', 'jpeg', 'PNG', 'JPG', 'JPEG', 'svg', 'SVG']
        file_path, file_type = QFileDialog.getOpenFileName(self, 'Select Image', '.', 'All Files (*)')
        if not file_path:
            QMessageBox.critical(self, 'Error', 'Please Select an Image File!')
            return
        if file_path.split('.')[-1] not in file_type_list:
            QMessageBox.critical(self, 'Error', 'Please Select an Image File!')
            return
        self.img_path_edit.setText(file_path)
        self.show_img_label.setPixmap(QPixmap(file_path))
        self.img_path = file_path

    def go_fourth(self):
        if not self.img_path:
            QMessageBox.critical(self, 'Error', 'Please Select an Image File!')
            return
        self.fourth_win = FourthWin(img_path=self.img_path)
        self.fourth_win.show()
        self.close()


class FourthWin(QWidget, FourthUi):

    def __init__(self, parent=None, img_path=None):
        super(FourthWin, self).__init__(parent)
        self.setupUi(self)

        self.zoom_map = {
            'start_btn': True,
            'stop_btn': False,
        }

        self.zoom_frame.setEnabled(False)
        self.speed_label.setText(SETTING_MANAGE.get_param('SPEED'))
        self.bits_label.setText(SETTING_MANAGE.get_param('BIT_TYPE'))
        self.graphicsView.set_image(img_path)

        self.coordinates_edit.returnPressed.connect(self.zoom_to_coordinate)
        self.scan_btn.clicked.connect(self.scan_to)
        self.confirm_btn.clicked.connect(self.zoom_to_coordinate)
        self.reset_zoom_btn.clicked.connect(self.graphicsView.reset_zoom)
        self.start_btn.clicked.connect(self.enable_zoom)
        self.stop_btn.clicked.connect(self.enable_zoom)
        self.back_btn.clicked.connect(self.back_third)

    def scan_to(self):
        prompt_win = PromptWin()
        result = prompt_win.exec_()
        self.sticking_win = StichingWin()
        if result == QMessageBox.Yes:
            self.sticking_win.show()
        if result == QMessageBox.No:
            prompt_no_win = PromptWin(message='<p style="color:red;">Please place it down</p><p>Tool on WorkPiece ?</p>')
            dd_result = prompt_no_win.exec_()
            while dd_result == QMessageBox.No:
                dd_result = prompt_no_win.exec_()
            else:
                self.sticking_win.show()

    def enable_zoom(self):
        self.zoom_frame.setEnabled(self.zoom_map[self.sender().objectName()])

    def zoom_to_coordinate(self):
        text = self.coordinates_edit.text()
        if not text:
            QMessageBox.warning(self, 'Warning', 'Please Enter the Coordinates as (x, y)')
            return
        coordinates = text.split(",")
        if len(coordinates) == 2:
            x = int(coordinates[0].strip())
            y = int(coordinates[1].strip())
            self.graphicsView.zoom_to_coordinate(x, y)

    def back_third(self):
        self.third_win = ThirdWin()
        self.third_win.show()
        self.close()


class StichingWin(QWidget, StichingUi):

    def __init__(self, parent=None):
        super(StichingWin, self).__init__(parent)
        self.setupUi(self)

        self.show_pixmap = None

        self.take_btn.clicked.connect(self.capture_thread)
        self.save_btn.clicked.connect(self.save_photo)
        self.done_btn.clicked.connect(self.close)

    def capture_thread(self):
        self.take_btn.setEnabled(False)
        tt_thread = threading.Thread(target=self.capture, args=())
        tt_thread.start()

    def capture(self):
        # 此处0表示默认摄像头，1不是默认，准确判断需要尝试,比如1,2,3之类
        # 我使用0来测试，你可以尝试1
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            t_box = QMessageBox(QMessageBox.Critical, 'Error', 'USB Camera not Found!', QMessageBox.Ok)
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            t_box.setFont(font)
            ok_btn = t_box.button(QMessageBox.Ok)
            ok_btn.setFont(font)
            t_box.exec_()
            return
        ret, frame = self.camera.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.show_pixmap = QPixmap.fromImage(q_image)
            self.show_label.setPixmap(self.show_pixmap)
        self.take_btn.setEnabled(True)

    def save_photo(self):
        if self.show_pixmap is None:
            t_box = QMessageBox(QMessageBox.Critical, 'Error', 'No Picture Can Be Saved!', QMessageBox.Ok)
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            t_box.setFont(font)
            ok_btn = t_box.button(QMessageBox.Ok)
            ok_btn.setFont(font)
            t_box.exec_()
            return
        img_name = str(int(time.time())) + '.jpg'
        try:
            self.show_pixmap.save('ON-CNC//Marker//' + img_name)
        except Exception as e:
            t_box = QMessageBox(QMessageBox.Critical, 'Error', str(e), QMessageBox.Ok)
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            t_box.setFont(font)
            ok_btn = t_box.button(QMessageBox.Ok)
            ok_btn.setFont(font)
            t_box.exec_()
        else:
            t_box = QMessageBox(QMessageBox.Information, '自动绘画UI', 'Save Success!', QMessageBox.Ok)
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            t_box.setFont(font)
            ok_btn = t_box.button(QMessageBox.Ok)
            ok_btn.setFont(font)
            t_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = FirstWin()
    win.show()
    sys.exit(app.exec_())
