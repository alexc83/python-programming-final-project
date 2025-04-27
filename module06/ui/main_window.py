import os
import pickle
import sys

from module06.ui.edit_league_dialog import EditLeagueDialog
from module06.league_model.league import League
from module06.league_model.league_database import LeagueDatabase
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog

UI_MainWindow, QTBaseWindow = uic.loadUiType("main_window.ui")

class MainWindow(QTBaseWindow, UI_MainWindow):

    def __init__(self, parent=None):
        # initial setup
        super().__init__(parent)
        self.setupUi(self)
        # initialize league database object to use
        self.league_db = None
        # load league database if db file exists and put into the UI
        self.load_existing_db()
        # file menu items
        self.action_load.triggered.connect(self.action_load_triggered)
        self.action_save.triggered.connect(self.action_save_triggered)
        # buttons
        self.add_league_button.clicked.connect(self.add_league_button_clicked)
        self.delete_league_button.clicked.connect(self.delete_league_button_clicked)
        self.edit_league_button.clicked.connect(self.edit_league_button_clicked)

    def load_existing_db(self):
        """
        This method checks to see if a league.db file already exists
        and loads that data into the list widget and updates the UI
        so users do not need to load a db file everytime the program
        is opened.

        :return: none
        """
        db_file_path = "../league_model/data/league.db"
        if os.path.exists(db_file_path):
            LeagueDatabase.load(db_file_path)
            self.league_db = LeagueDatabase.instance()
            self.update_ui()

    def action_load_triggered(self):
        """
        This method executes when the load option is clicked from the file menu

        A QFileDialog box opens to the /league_model/data folder, where the database files
        are stored. A filter only allows .db files to be clickable.

        :return: none
        """
        # this returns a filename that the user has selected
        fn = QFileDialog.getOpenFileName(self, "Open File", "./league_model/data",
                                         "Database Files (*.db)")

        # load database with file chosen
        with open(fn[0], mode="rb") as file:
            # load LeagueDatabase obj and save the leagues list to update the UI
            loaded_league_db_obj = pickle.load(file)
            self.league_db = loaded_league_db_obj
        self.update_ui()

    def action_save_triggered(self):
        fn = QFileDialog.getSaveFileName(self, "Save File", "./league_model/data/league.db",
                                         "Database Files (*.db)")

        # this ensures the file is saved a .db file
        if fn[0]:
            if not fn[0].lower().endswith(".db"):
                fn[0] += ".db"
            self.league_db.save(fn[0])

    def add_league_button_clicked(self):
        # checks if there is a name entered and throws a message if not
        if self.league_name_line_edit.text() == "":
            self.warn("Enter Name", "You must enter a league name to add")
        # adds the league if a name is entered
        else:
            # creates a new database if none is loaded
            if self.league_db is None:
                LeagueDatabase._sole_instance = LeagueDatabase()
                self.league_db = LeagueDatabase.instance()

            # creates a new League object using the name provided by the user
            new_league = League(self.league_db.next_oid(),
                                self.league_name_line_edit.text())
            # updates the LeagueDatabase object and updates the UI
            self.league_db.add_league(new_league)
            self.update_ui()

    def delete_league_button_clicked(self):
        selected_league = self.get_selected_league()
        if selected_league is None:
            self.warn("Select League", "You must select a league to delete")
        else:
            self.league_db.remove_league(selected_league)
            self.update_ui()


    def edit_league_button_clicked(self):
        selected_league = self.get_selected_league()
        if selected_league is None:
            self.warn("Select League", "You must select a league to edit")
        else:
            dialog = EditLeagueDialog(self.league_db, selected_league)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.update_ui()
                self.warn("Changes saved", f"Changes to {selected_league.name} were saved")
            else:
                self.warn("Changes not saved", f"Changes to {selected_league.name} were not saved")

    def get_selected_league(self):
        selected = self.league_list_widget.selectedItems()
        if not selected:
            return None
        else:
            selected_item = selected[0]
            selected_league = selected_item.data(Qt.ItemDataRole.UserRole)
            return selected_league

    def update_ui(self):
        row = self.league_list_selected_row()
        self.league_list_widget.clear()
        for league in self.league_db.leagues:
            # self.league_list_widget.addItem(f"League name: {league.name}")
            item = QtWidgets.QListWidgetItem(f"League name: {league.name}")
            item.setData(Qt.ItemDataRole.UserRole, league)
            self.league_list_widget.addItem(item)

        if row != -1 and len(self.league_db.leagues) > row:
            self.league_list_widget.setCurrentItem(self.league_list_widget.item(row))


    def league_list_selected_row(self):
        selected = self.league_list_widget.selectedItems()
        if len(selected) == 0:
            return -1
        assert len(selected) == 1
        selected_item = selected[0]
        selected_league = selected_item.data(Qt.ItemDataRole.UserRole)
        for i, league in enumerate(self.league_db.leagues):
            if league == selected_league:
                return i
        return -1

    def warn(self, title, message):
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        mb.exec()


if __name__ == '__main__':
    # initial setup
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
