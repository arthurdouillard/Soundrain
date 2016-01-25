from kivy.app           import App
from kivy.uix.widget    import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup     import Popup
from kivy.core.window   import Window

from tool_soundrain     import *

class SoundrainWin(Widget):
    """Main window"""

    client_id = None

    def search_url(self):
        """When button 'search' is clicked.
           Look if URL exists, and fill info"""

        if not check_url(self.ids['UrlTxt'].text):
            print("Wrong!")
        else:
            print("Yes!")

    def get_id(self):
        """Get id from the Popup"""

        if len(self.ids['IdTxt'].strip) == 0:
            self.search_url()
        else:
            self.client_id = self.ids['IdTxt'].strip()
            self.ids['PopId'].dismiss()

class SoundrainApp(App):
    """App"""

    def build(self):
        return SoundrainWin()

if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    SoundrainApp().run()
