from parent_class import ParentClass
import py_starter as ps

class Email( ParentClass ):

    DEFAULT_KWARGS = {
        'to': None,
        'subject': None,
        'content': []
    }

    def __init__( self, conn, **kwargs ):

        ParentClass.__init__( self )
        self.conn = conn

        joined_kwargs = ps.merge_dicts( Email.DEFAULT_KWARGS, kwargs )
        self.set_atts( joined_kwargs )

    def send( self, print_off: bool = True ):
        
        if print_off:
           print ('Sending email to ' + str(self.to))

        try:
            self.conn.conn.send( self.to, self.subject, self.content )
        except:
            return False
        return True

    @staticmethod
    def make_html_link( link_address, link_text_to_show ):
        return '<a href="{link_address}">{link_text_to_show}</a>'.format( link_address = link_address, link_text_to_show = link_text_to_show )

