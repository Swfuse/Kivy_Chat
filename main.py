# -*- coding: utf-8 -*-
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import reactor, protocol
from twisted.internet.protocol import DatagramProtocol


from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
from kivy.core.window import Window
#Window.softinput_mode = 'resize'
#Window.clearcolor = (1, 1, 1, 1)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ChatClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write('CONNECT')
        self.factory.app.on_connect(self.transport)

    def dataReceived(self, data):
        self.factory.app.on_message(data)


class ChatClientFactory(protocol.ClientFactory):
    protocol = ChatClient

    def __init__(self, app):
        self.app = app


class ChatApp(App):
    def connect(self):
        host = self.root.ids.server.text
        self.nick = self.root.ids.nickname.text
        print('-- connecting to ' + host)
        reactor.connectTCP(host, 9096,
                           ChatClientFactory(self))

    def disconnect(self):
        print('-- disconnecting')
        if self.conn:
            dis = u'[b][color=c0392b]{} has been disconnected:[/color][/b] '.format(self.nick)
            self.conn.write(dis)
            self.conn.loseConnection()
            del self.conn
        self.root.current = 'login'
        self.root.ids.chat_logs.text = ''

    def send_msg(self):
        msg = self.root.ids.message.text
        senders = ('%s:%s' % (self.nick, msg))
        print(senders)
      
        #self.conn.write((str('%s:%s' % (self.nick, msg))).encode('utf-8'))
        self.conn.write(senders)
        self.root.ids.chat_logs.text += (
            u'[b][color=2980b9]{}:[/color][/b] {}\n'
            .format(self.nick, msg))
        self.root.ids.message.text = ''

    def on_connect(self, conn):
        print('-- connected')
        self.conn = conn
        con = u'[b][color=27ae60]::{} has been connected::[/color][/b] '.format(self.nick)
        self.conn.write(con)
        self.root.current = 'chatroom'

    def on_message(self, msg):
        self.root.ids.chat_logs.text += msg + '\n'
        
    def run_server(self):
        import server
     
    def check_choose(self):
        if self.root.ids.checkServer.active == True:
            import server   
        elif self.root.ids.checkClient.active == True:
            self.root.current = 'login'
            
            

                    

if __name__ == '__main__':
    # Config.set('graphics', 'width', '800')
    # Config.set('graphics', 'height', '600')
    # Config.set('graphics', 'fullscreen', '0')
    ChatApp().run()
