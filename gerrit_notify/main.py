#coding=utf-8
from gerrit_notify import GerritNotify
from gi.repository import GObject,  Gtk
from os.path import expanduser
import subprocess
from ConfigParser import SafeConfigParser

class TrayiconPlugin (GObject.Object):
    notify = None
    def do_activate (self, notify):
        self.notify = notify
        self.staticon = Gtk.StatusIcon.new_from_file(self.notify.icon)
        self.staticon.connect ("activate", self.trayicon_activate)
        self.staticon.connect ("popup_menu", self.trayicon_popup)
        self.staticon.set_tooltip_markup("<span font_size='small'>Gerrit Notifier</span>")
        self.staticon.set_visible (True)

    def trayicon_activate (self, widget, data = None):
        pass

    def trayicon_quit (self, widget, data = None):
        Gtk.main_quit()

    def populate_menuitem_submenu(self, menuitem, changes):
        menu = Gtk.Menu ()
        menuitem.set_submenu(menu)
        if len(changes) == 0:
            menuitem.set_sensitive(False)
            return

        for c in changes:
            menutitem_change = Gtk.MenuItem (str(c))
            menutitem_change.connect("activate", self.change_clicked, c)
            menu.append(menutitem_change)

    def new_change_menuitem(self, name, populator_func):
        new_menuitem = Gtk.MenuItem(name)
        self.populate_menuitem_submenu(new_menuitem, populator_func())
        return new_menuitem

    def change_clicked(self, widget, change = None):
        subprocess.Popen(["xdg-open", change.permalink()])

    def trayicon_popup (self, widget, button, time, data = None):
        self.menu = Gtk.Menu ()
        menuitem_quit = Gtk.MenuItem ("Quit")

        self.menu.append(self.new_change_menuitem("Incoming changes", self.notify.incoming_changes))
        self.menu.append(self.new_change_menuitem("Outgoing changes", self.notify.outgoing_changes))
        self.menu.append(self.new_change_menuitem("Open changes", self.notify.open_changes))

        menuitem_quit.connect ("activate", self.trayicon_quit)

        self.menu.append (menuitem_quit)

        self.menu.show_all ()
        self.menu.popup(None, None, lambda w,x: self.staticon.position_menu(self.menu, self.staticon), self.staticon, 3, time)

    def do_deactivate (self):
        self.staticon.set_visible (False)
        del self.staticon

def main():
    # add a 'Settings' menu item to edit these values
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

