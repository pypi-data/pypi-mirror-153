import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk

disp=Gdk.Display.get_default()
scr=disp.get_default_screen()
win_pos=scr.get_active_window().get_origin()
print("win: %d x %d" % (win_pos.x, win_pos.y))
rect=disp.get_monitor_at_point(win_pos.x, win_pos.y).get_geometry()
print("monitor: %d x %d" % (rect.width, rect.height))
