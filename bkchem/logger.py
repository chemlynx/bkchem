#--------------------------------------------------------------------------
#     This file is part of BKchem - a chemical drawing program
#     Copyright (C) 2004 Beda Kosata <beda@zirael.org>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file gpl.txt in the
#     main directory of the program

#--------------------------------------------------------------------------



import tkMessageBox
from singleton_store import Store
import sys



class logger:
  """provides logging capabilities based on the message types,
  each type is associated with a string describing how to handle it,
  it can be one of ('status_bar','dialog','console','ignore')"""

  type_to_text = {'info':_('Info'),
                  'error':_('Error'),
                  'debug':_('Debug'),
                  'warning': _('Warning'),
                  'hint': _('Hint')}

  handle_to_text = {'status_bar': _('Status bar'),
                    'dialog': _('Dialog'),
                    'console': _('Console'),
                    'ignore': _('Ignore')}



  def __init__( self):
    self.handling = {'info': 'status_bar',
                     'warning': 'dialog',
                     'error': 'dialog',
                     'debug': 'console',
                     'hint': 'status_bar'}


  def log( self, message, message_type="info", delay=4):
    """message_type is one of (info, warning, error, debug, hint),
    delay means the amount of time for which the text should be visible (for 'status-bar' only)""" 
    if message_type not in ('info', 'warning', 'error', 'debug', 'hint'):
      raise ValueError, "unknown message type %s" % message_type

    handle = self.handling[ message_type]
    self.__class__.__dict__['log_to_'+handle]( self, message, message_type=message_type, delay=delay)


  def log_to_ignore( self, message, message_type="info", delay=4):
    pass


  def log_to_status_bar( self, message, message_type="info", delay=4):
    Store.app.update_status( message, time=delay)


  def log_to_console( self, message, message_type="info", delay=4):
    print >> sys.stderr, self.type_to_text[ message_type]+":", message


    
  def log_to_dialog( self, message, message_type="info", delay=4): 
    heading = self.type_to_text[ message_type]
    if message_type == "error":
      tkMessageBox.showerror( heading, message)
    elif message_type == "warning":
      tkMessageBox.showwarning( heading, message)
    elif message_type == "info":
      tkMessageBox.showinfo( heading, message)
    elif message_type == "debug":
      tkMessageBox.showinfo( heading, message)
    elif message_type == "hint":
      tkMessageBox.showinfo( heading, message)
      
  


# logging strategies

batch_mode = {'info': 'ignore',
               'warning': 'console',
               'error': 'console',
               'debug': 'ignore',
               'hint': 'ignore'}


ignorant = {'info': 'ignore',
            'warning': 'ignore',
            'error': 'ignore',
            'debug': 'ignore',
            'hint': 'ignore'}
