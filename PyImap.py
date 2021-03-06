import imaplib
import re
import email
import socket
import ssl

class PyImap:
  def __init__(self, server, port, timeout = 10.0):
    self.IMAP_SERVER = server
    self.IMAP_PORT = port
    self.M = None
    self.response = None
    socket.setdefaulttimeout( timeout )
 
  def login(self, username, password):
    error = None
    tries = 3
    while tries > 0:
        try:
            self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
            rc, self.response = self.M.login(username, password)
            break
        except ssl.SSLError, e:
            tries -= 1
            error = e
    if tries > 0:
        return rc
    else:
        raise e

  def list_mail( self, folder='Inbox' ):
    status, count = self.M.select( folder )
    return self.M.search( None, 'All' )

  def delete_msgs( self, msg_list ):
	for num in msg_list:
		self.M.store(num, '+FLAGS', '\\Deleted')
	self.M.expunge()

  def get_msg_body( self, emailmessage ):
	return emailmessage.get_payload()[0].get_payload().strip()

  def get_mail( self, folder='Inbox' ):
    msgs = {}
    status, ids = self.list_mail( folder )
    ids = ids[0].split()
    if ids > 0:
        for num in ids:
            typ, data = self.M.fetch( num, '(RFC822)' )
            msg = email.message_from_string( data[0][1] )
            msgs[num] = msg
    return msgs


  def get_mail_count(self, folder='Inbox'):
    rc, count = self.M.select(folder)
    return count[0]

  def logout(self):
    self.M.close()
    self.M.logout()

