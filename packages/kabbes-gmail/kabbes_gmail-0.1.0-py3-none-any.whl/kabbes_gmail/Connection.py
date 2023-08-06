from parent_class import ParentClass
import yagmail

class Connection( ParentClass ):

    def __init__( self, *args, **kwargs ):

        ParentClass.__init__( self )
        self.get_connection( *args, **kwargs )

    def get_connection( self, gmail_address = None, app_password = None ):

        self.conn = yagmail.SMTP( gmail_address, app_password )
