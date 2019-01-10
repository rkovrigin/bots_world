from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class Wall(object):

    def represent_itself(self, representation_no):
        return QColor(76, 14, 0, 200)  # brown color 4C2400

    def execute_command(self, x, y):
        pass
