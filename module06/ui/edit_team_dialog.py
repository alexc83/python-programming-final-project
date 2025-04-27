import sys

from PyQt6 import uic, QtWidgets

UI_MainWindow, QTBaseWindow = uic.loadUiType("edit_team_dialog.ui")


class EditTeamDialog(QTBaseWindow, UI_MainWindow):

    def __init__(self, league_db=None, selected_league=None, parent=None):
        # initial setup
        super().__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    # initial setup
    app = QtWidgets.QApplication(sys.argv)
    window = EditTeamDialog()
    window.show()
    sys.exit(app.exec())