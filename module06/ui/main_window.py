import os
import pickle
import sys

from module06.ui.edit_league_dialog import EditLeagueDialog
from module06.league_model.league import League
from module06.league_model.league_database import LeagueDatabase
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog

complete_file_path = os.path.join(os.path.dirname(__file__), "main_window.ui")
UI_MainWindow, QTBaseWindow = uic.loadUiType(complete_file_path)

class MainWindow(QTBaseWindow, UI_MainWindow):
    """
    This class is the main window of the UI for the league manager application.
    """

    def __init__(self, parent=None):
        """
        This is the constructor for the UI main window.

        After initial setup for PyQt6, a league database is initialized. The league database
        will either be created when the user enters a league name into an empty list widget
        or be loaded when the load option of the file menu is executed.

        The constructor then binds the two file menu options (load and save) and the three buttons
        (add, edit, and delete).

        :param parent: none
        """
        # initial setup
        super().__init__(parent)
        self.setupUi(self)
        # initialize league database object to use
        self.league_db = None
        # file menu items
        self.action_load.triggered.connect(self.action_load_triggered)
        self.action_save.triggered.connect(self.action_save_triggered)
        # buttons
        self.add_league_button.clicked.connect(self.add_league_button_clicked)
        self.delete_league_button.clicked.connect(self.delete_league_button_clicked)
        self.edit_league_button.clicked.connect(self.edit_league_button_clicked)

    def closeEvent(self, event):
        """
        This is a Qt method that is called when the user closes the application.
        A MessageBox is created asking if the user would like to save their changes
        before closing the application.

        If they answer yes, then the action_save_triggered method is executed which provides
        the user with the ability to save an updated database file.

        Answering no means the application is closed without saving (unless the user manually saved
        prior to closing)

        Choosing cancel means the application does not close.

        :param event: this event is the action of closing the application, which automatically calls this method
        :return: none, either event.accept() or event.ignore() are executed based on user choice
        """
        response = QMessageBox.question(
            self,
            "Save?",
            "Do you want to save your changes before exiting?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )

        if response == QMessageBox.StandardButton.Yes:
            self.action_save_triggered()
            event.accept()
        elif response == QMessageBox.StandardButton.No:
            event.accept()
        else:
            event.ignore()

    def action_load_triggered(self):
        """
        This method executes when the load option is clicked from the file menu

        A QFileDialog box opens to the ../league_model/data folder, where the database files
        are stored. A filter only allows .db files to be clickable.

        This file is loaded into the application so the user can make edits to the league.

        :return: none
        """
        # this returns a filename that the user has selected
        fn = QFileDialog.getOpenFileName(self, "Open File", "../league_model/data",
                                         "Database Files (*.db)")

        # load database with file chosen
        with open(fn[0], mode="rb") as file:
            # load LeagueDatabase obj and save the leagues list to update the UI
            loaded_league_db_obj = pickle.load(file)
            self.league_db = loaded_league_db_obj
        self.update_ui()

    def action_save_triggered(self):
        """
        This method executes when the save option is clicked from the file menu

        A QFileDialog box opens to the ../league_model/data folder, where the database files
        are stored. The user can then choose a name to save their database file as. To ensure
        the correct file extension is used, the method also adds .db if not already added by
        the user.

        :return:
        """
        fn = QFileDialog.getSaveFileName(self, "Save File", "../league_model/data",
                                         "Database Files (*.db)")

        # this ensures the file is saved a .db file
        if fn[0]:
            if not fn[0].lower().endswith(".db"):
                fn[0] += ".db"
            self.league_db.save(fn[0])
            self.warn("Database Saved", f"Data saved to file: {fn[0]}")

    def add_league_button_clicked(self):
        """
        This method is executed when the add league button is clicked. A league name
        must be entered by the user or a popup will show stating the user must enter a name.

        Once a league name is entered and add league is clicked, a new League object is created
        and added to the database.

        If no previously created league database has been loaded and the list widget is empty, the
        method creates a new LeagueDatabase object, after which the League object is created and added
        to this new database.

        Then the UI is updated.

        :return: none
        """
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
            # this makes the add team name field blank
            self.league_name_line_edit.setText("")
            self.update_ui()

    def delete_league_button_clicked(self):
        """
        This method is executed when the delete league button is clicked. If the user has not
        selected a league in the list widget, a popup box appears to inform the user that a league
        must be selected.

        Once a league is selected and the delete button is clicked, the league selected is removed
        from the database and the UI is updated.

        :return: none
        """
        selected_league = self.get_selected_league()
        if selected_league is None:
            self.warn("Select League", "You must select a league to delete")
        else:
            self.league_db.remove_league(selected_league)
            self.update_ui()


    def edit_league_button_clicked(self):
        """
        This method is executed when the edit button is clicked. If the user has not
        selected a league in the list widget, a popup box appears to inform the user that a league
        must be selected.

        Once a league is selected and the edit button is clicked, a dialog window for editing
        the selected league is shown to the user.

        Once the user finishes editing the league, the database is only updated if the user clicks
        save in the edit league dialog box. A popup stating if changes were saved or not is given
        to the user once the edit league dialog box is closed.

        :return: none
        """
        # the league selected in the list widget is saved
        selected_league = self.get_selected_league()
        # a message is displayed if no league is selected
        if selected_league is None:
            self.warn("Select League", "You must select a league to edit")
        else:
            # the edit league dialog is called
            dialog = EditLeagueDialog(self.league_db, selected_league)
            # if saved is clicked in the edit league dialog, the UI is updated
            # messages for either changes saved or not is displayed to the user
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.update_ui()
                self.warn("Changes saved", f"Changes to {selected_league.name} were saved")
            else:
                self.warn("Changes not saved", f"Changes to {selected_league.name} were not saved")

    def get_selected_league(self):
        """
        This method is used by the edit and delete league methods to return which
        league is currently selected in the list widget to ensure the correct league is being
        managed by the user.

        :return: the league currently selected in the list widget
        """
        selected = self.league_list_widget.selectedItems()
        if not selected:
            return None
        else:
            selected_item = selected[0]
            selected_league = selected_item.data(Qt.ItemDataRole.UserRole)
            return selected_league

    def update_ui(self):
        """
        This method is called whenever changes are made to the database to ensure the changes
        show up in the UI, such as removing deleted leagues or adding new leagues to the list
        widget.

        :return: none
        """
        row = self.league_list_selected_row()
        self.league_list_widget.clear()
        for league in self.league_db.leagues:
            item = QtWidgets.QListWidgetItem(f"League name: {league.name}")
            item.setData(Qt.ItemDataRole.UserRole, league)
            self.league_list_widget.addItem(item)

        if row != -1 and len(self.league_db.leagues) > row:
            self.league_list_widget.setCurrentItem(self.league_list_widget.item(row))


    def league_list_selected_row(self):
        """
        This method is used by the update UI method to ensure if a league was selected
        in the list widget that the same league is selected (if not deleted) after the
        UI is updated.

        :return: the index of the league selected in the current database leagues list
        """
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
        """
        This method produces a MessageBox based on the parameters.

        :param title: title of the MessageBox
        :param message: the message to be displayed in the MessageBox
        :return: none
        """
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        mb.exec()


if __name__ == '__main__':
    """
    Main method to be able to open the UI to the main window
    """
    # initial setup
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
