# CPSC 4970 - Python Programming
#
# Assignment 6 - Final Project
#
# Author: Alan Cruce
# Date: April 28, 2025

import yagmail

class Emailer:
    """
    Class for emailer object. This makes use of the yagmail module.
    In addition, the sender email address app password was saved using
    the keyring module as instructed.

    Steps for use

    1.) Run configure method to set class variable for sender_email, sole instance also set
    2.) create an emailer object using the constructor
    3.) Use the send_plain_email() method providing a list of emails addresses,
    the subject, and the message itself.

    I was able to successfully test this using another personal email address.
    My sender email address had the email in the sent messages folder, and my
    recipient email address received the message as expected.
    """

    # class variables
    _sender_address = None # set in the configure() method
    _sole_instance = None

    def __init__(self):
        """
        Constructor added in order to create the _yag option from the
        yagmail module.
        """
        if not Emailer._sender_address:
            raise ValueError("Run configure() first to set sender address")
        self._yag = yagmail.SMTP(Emailer._sender_address)

    @classmethod
    def configure(cls, sender_address):
        """
        Class method for setting the sender address.

        This method is run before the constructor to sent sender address
        and set the sole_instance of the class.


        :param sender_address: sender address to set
        :return: none
        """
        cls._sender_address = sender_address

    @classmethod
    def instance(cls):
        """
        Class method for returning the sole instance of the class
        :return: _sole_instance class variable
        """
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        """
        Sends an email using the yagmail module. Assuming the configure() method
        has been run, this method will loop over the list of recipients,
        and email each recipient with the same subject and message.

        :param recipients: list of email addresses to send to
        :param subject: subject of the email
        :param message: message of the email
        :return: none
        """
        for recipient in recipients:
            print(f"Sending email to {recipient}")
            self._yag.send(recipient, subject, message)

def main():
    """
    This method was used to successfuly send an email from
    one of my personal email addresses to another.

    test@gmail.com can be replaced with a real email to test.

    Google app password for sender email must be loaded
    to the keyring.

    :return:
    """
    # Step 1: Configure with your Gmail address
    Emailer.configure("test@gmail.com")  # This email must be registered in keyring!

    # Step 2: Get the singleton instance
    emailer = Emailer.instance()

    # Step 3: Send a test email
    emailer.send_plain_email(
        recipients=["test@gmail.com"],
        subject="Test Email from Python",
        message="This is a test email sent using yagmail and keyring!"
    )

    print("Email sent successfully!")

if __name__ == "__main__":
    main()