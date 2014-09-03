#coding=utf-8
from gerrit_notify import GerritNotify
from gi.repository import GObject,  Gtk
from os.path import expanduser
from ConfigParser import SafeConfigParser

class TrayiconPlugin (GObject.Object):
    __gtype_name__ = 'TrayiconPlugin'

    object = GObject.property (type=GObject.Object)
    notify = None
    def do_activate (self, notify):
        self.notify = notify
        self.staticon = Gtk.StatusIcon ()
        self.staticon.set_from_stock (Gtk.STOCK_ABOUT)
        self.staticon.connect ("activate", self.trayicon_activate)
        self.staticon.connect ("popup_menu", self.trayicon_popup)
        self.staticon.set_visible (True)

    def trayicon_activate (self, widget, data = None):
        for c in self.notify.open_changes():
            print(c.change_id)

    def trayicon_quit (self, widget, data = None):
        Gtk.main_quit()

    def trayicon_popup (self, widget, button, time, data = None):
        self.menu = Gtk.Menu ()

        menuitem_toggle = Gtk.MenuItem ("Show / Hide")
        menuitem_quit = Gtk.MenuItem ("Quit")

        menuitem_toggle.connect ("activate", self.trayicon_activate)
        menuitem_quit.connect ("activate", self.trayicon_quit)

        self.menu.append (menuitem_toggle)
        self.menu.append (menuitem_quit)

        self.menu.show_all ()
        self.menu.popup(None, None, lambda w,x: self.staticon.position_menu(self.menu, self.staticon), self.staticon, 3, time)

    def do_deactivate (self):
        self.staticon.set_visible (False)
        del self.staticon

def main():
    default_config = {
            'url': 'http://update-your-settings.net',
            'username': None,
            'password': None
            }
    config = SafeConfigParser(default_config)
    p = expanduser('~/.config/gerrit-notify/config')
    config.readfp(open(p))

    notify = GerritNotify(
            config.get('server', 'url'),
            config.get('server', 'username'),
            config.get('server', 'password')
            )
    TrayiconPlugin().do_activate(notify)
    Gtk.main()

