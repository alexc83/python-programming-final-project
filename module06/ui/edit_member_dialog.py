import os

from PyQt6 import uic

complete_file_path = os.path.join(os.path.dirname(__file__), "edit_member_dialog.ui")
UI_MainWindow, QTBaseWindow = uic.loadUiType(complete_file_path)


class EditMemberDialog(QTBaseWindow, UI_MainWindow):
    """
    This class is for the edit member dialog that allows a user to update the name and email
    for a current team member.
    """

    def __init__(self, selected_member=None, parent=None):
        """
        This is the constructor for the edit member dialog class. The selected team member is
        passed in. In addition, the current name and email for the team member is pre-populated
        in the name and email line edit fields in the UI.

        :param selected_member: the team member selected to be edited
        :param parent:
        """
        # initial setup
        super().__init__(parent)
        self.setupUi(self)
        # team member being edited
        self.selected_member = selected_member
        # set current name and email into the text field
        self.member_name_line_edit.setText(selected_member.name)
        self.member_email_line_edit.setText(selected_member.email)
        # buttons
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)

    def save_button_clicked(self):
        """
        Thie method is executed when the save button is clicked. The text in the member name and
        member email line edits are saved into the name and email fields for the selected member
        object, ensuring the changes are updated.

        The dialog box is closed.

        :return: none
        """
        self.selected_member.name = self.member_name_line_edit.text()
        self.selected_member.email = self.member_email_line_edit.text()
        self.accept()

    def cancel_button_clicked(self):
        """
        This method is executed when the cancel button is clicked. No changes are saved, therefore
        the data in the name and email line edit fields are not saved into the selected member
        object fields.

        The dialog box is closed.

        :return:
        """
        self.reject()



