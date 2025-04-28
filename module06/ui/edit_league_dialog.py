import copy

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QDialog

from module06.league_model.team import Team
from module06.ui.edit_team_dialog import EditTeamDialog

UI_MainWindow, QTBaseWindow = uic.loadUiType("edit_league_dialog.ui")



class EditLeagueDialog(QTBaseWindow, UI_MainWindow):

    def __init__(self, league_db=None, selected_league=None, parent=None):
        # initial setup
        super().__init__(parent)
        self.setupUi(self)
        self.league_db = league_db
        self.selected_league_original = selected_league
        self.selected_league_copy = copy.deepcopy(selected_league)
        self.update_ui()
        # buttons
        self.add_team_button.clicked.connect(self.add_team_button_clicked)
        self.delete_team_button.clicked.connect(self.delete_team_button_clicked)
        self.edit_team_button.clicked.connect(self.edit_team_button_clicked)
        self.export_data_button.clicked.connect(self.export_data_button_clicked)
        self.import_data_button.clicked.connect(self.import_data_button_clicked)
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)


    def add_team_button_clicked(self):
        # checks if there is a name entered and throws a message if not
        if self.team_name_line_edit.text() == "":
            self.warn("Enter Name", "You must enter a team name to add")
        else:
            # creates a new League object using the name provided by the user
            new_team = Team(self.league_db.next_oid(),
                                self.team_name_line_edit.text())
            # updates the league copy object and updates the UI
            self.selected_league_copy.add_team(new_team)
            # this makes the add team name field blank
            self.team_name_line_edit.setText("")
            self.update_ui()


    def delete_team_button_clicked(self):
        selected_team = self.get_selected_team()
        if selected_team is None:
            self.warn("Select Team", "You must select a team to delete")
        else:
            self.selected_league_copy.remove_team(selected_team)
            self.update_ui()

    def edit_team_button_clicked(self):
        selected_team = self.get_selected_team()
        if selected_team is None:
            self.warn("Select Team", "You must select a team to edit")
        else:
            dialog = EditTeamDialog(self.league_db, self.selected_league_copy, selected_team)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.update_ui()
                self.warn("Changes saved", f"Changes to {selected_team.name} were saved")
            else:
                self.warn("Changes not saved", f"Changes to {selected_team.name} were not saved")

    def export_data_button_clicked(self):
        fn = QFileDialog.getSaveFileName(self, "Save File", "./league_model/data",
                                         "CSV Files (*.csv)")
        # this ensures the file is saved a .csv file
        if fn[0]:
            if not fn[0].lower().endswith(".csv"):
                fn[0] += ".csv"
            self.league_db.export_league_teams(self.selected_league_copy, fn[0])
            self.warn("Data Imported", f"Data Imported to file: {fn[0]}")

    def import_data_button_clicked(self):
        # this returns a filename that the user has selected
        fn = QFileDialog.getOpenFileName(self, "Open File", "./league_model/data",
                                         "CSV Files (*.csv)")
        self.league_db.import_league_teams(self.selected_league_copy, fn[0])
        self.update_ui()

    def save_button_clicked(self):
        leagues = self.league_db.leagues
        index = leagues.index(self.selected_league_original)
        leagues[index] = self.selected_league_copy
        self.accept()

    def cancel_button_clicked(self):
        # self.warn("Changes not saved", "Changes will not be saved")
        self.reject()

    def get_selected_team(self):
        selected = self.team_list_widget.selectedItems()
        if not selected:
            return None
        else:
            selected_item = selected[0]
            selected_team = selected_item.data(Qt.ItemDataRole.UserRole)
            return selected_team

    def update_ui(self):
        row = self.team_list_selected_row()
        self.team_list_widget.clear()
        for team in self.selected_league_copy.teams:
            # self.league_list_widget.addItem(f"League name: {league.name}")
            item = QtWidgets.QListWidgetItem(f"Team name: {team.name}")
            item.setData(Qt.ItemDataRole.UserRole, team)
            self.team_list_widget.addItem(item)

        if row != -1 and len(self.selected_league_copy.teams) > row:
            self.team_list_widget.setCurrentItem(self.team_list_widget.item(row))

    def team_list_selected_row(self):
        selected = self.team_list_widget.selectedItems()
        if len(selected) == 0:
            return -1
        assert len(selected) == 1
        selected_item = selected[0]
        selected_team = selected_item.data(Qt.ItemDataRole.UserRole)
        for i, team in enumerate(self.selected_league_copy.teams):
            if team == selected_team:
                return i
        return -1

    def warn(self, title, message):
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        mb.exec()
