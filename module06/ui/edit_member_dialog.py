
from PyQt6 import uic

UI_MainWindow, QTBaseWindow = uic.loadUiType("edit_member_dialog.ui")


class EditMemberDialog(QTBaseWindow, UI_MainWindow):

    def __init__(self, selected_member=None, parent=None):
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
        self.selected_member.name = self.member_name_line_edit.text()
        self.selected_member.email = self.member_email_line_edit.text()
        self.accept()

    def cancel_button_clicked(self):
        self.reject()



