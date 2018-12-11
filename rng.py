import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class LCGDialog(Gtk.Dialog):

    def __init__(self, parent, m, a, c):
        Gtk.Dialog.__init__(self, "Configure LCG", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        vbox = Gtk.VBox(spacing=6)
        self.get_content_area().add(vbox)

        self.m_hbox = Gtk.HBox()
        vbox.pack_start(self.m_hbox, True, True, 0)

        self.m_label = Gtk.Label(label="modulus m: ")
        self.m_hbox.pack_start(self.m_label, True, True, 0)

        self.m_entry = Gtk.Entry()
        self.m_entry.set_text(str(m))
        self.m_hbox.pack_start(self.m_entry, True, True, 0)

        self.a_hbox = Gtk.HBox()
        vbox.pack_start(self.a_hbox, True, True, 0)

        self.a_label = Gtk.Label(label="multiplier a: ")
        self.a_hbox.pack_start(self.a_label, True, True, 0)

        self.a_entry = Gtk.Entry()
        self.a_entry.set_text(str(a))
        self.a_hbox.pack_start(self.a_entry, True, True, 0)

        self.c_hbox = Gtk.HBox()
        vbox.pack_start(self.c_hbox, True, True, 0)

        self.c_label = Gtk.Label(label="increment c: ")
        self.c_hbox.pack_start(self.c_label, True, True, 0)

        self.c_entry = Gtk.Entry()
        self.c_entry.set_text(str(c))
        self.c_hbox.pack_start(self.c_entry, True, True, 0)

        self.show_all()

    def getValue_m(self):
        return self.m_entry.get_text()

    def getValue_a(self):
        return self.a_entry.get_text()

    def getValue_c(self):
        return self.c_entry.get_text()


class MSDialog(Gtk.Dialog):

    def __init__(self, parent, max):
        Gtk.Dialog.__init__(self, "Configure MS", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        hbox = Gtk.HBox(spacing=6)
        self.get_content_area().add(hbox)

        self.max_label = Gtk.Label(label="Max digits: ")
        hbox.pack_start(self.max_label, True, True, 0)

        self.max_entry = Gtk.Entry()
        self.max_entry.set_text(str(max))
        hbox.pack_start(self.max_entry, True, True, 0)

        self.show_all()

    def getValue_max(self):
        return self.max_entry.get_text()


class LFSRDialog(Gtk.Dialog):

    def __init__(self, parent, tabs):
        Gtk.Dialog.__init__(self, "Configure MS", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        hbox = Gtk.HBox(spacing=6)
        self.get_content_area().add(hbox)

        self.tabs_label = Gtk.Label(label="Tabs: ")
        hbox.pack_start(self.tabs_label, True, True, 0)

        self.tabs_entry = Gtk.Entry()
        # Remove last two characters from String
        self.tabs_entry.set_text(str(tabs)[1:-1])
        hbox.pack_start(self.tabs_entry, True, True, 0)

        self.show_all()

    def getValue_tabs(self):
        return list(map(int, self.tabs_entry.get_text().split(",")))


class SettingsWindow(Gtk.Window):

    LCG_m = 2**31
    LCG_a = 1103515245
    LCG_c = 12345
    MS_max = 3
    LFSR_tabs = [16, 14, 13, 11]

    rng_seed = 0
    rng_ceiling = 999

    def __init__(self):
        Gtk.Window.__init__(self, title="RNG-simulation")

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        self.seed_hbox = Gtk.HBox()
        vbox.pack_start(self.seed_hbox, True, True, 0)

        self.seed_label = Gtk.Label(label="Seed: ")
        self.seed_hbox.pack_start(self.seed_label, True, True, 0)

        self.seed_entry = Gtk.Entry()
        self.seed_entry.set_text(str(self.rng_seed))
        self.seed_hbox.pack_start(self.seed_entry, True, True, 0)

        self.rng_ceiling_hbox = Gtk.HBox()
        vbox.pack_start(self.rng_ceiling_hbox, True, True, 0)

        self.rng_ceiling_label = Gtk.Label(label="RNG ceiling: ")
        self.rng_ceiling_hbox.pack_start(self.rng_ceiling_label, True, True, 0)

        self.rng_ceiling_entry = Gtk.Entry()
        self.rng_ceiling_entry.set_text(str(self.rng_ceiling))
        self.rng_ceiling_hbox.pack_start(self.rng_ceiling_entry, True, True, 0)

        self.conf_LGC = Gtk.Button.\
            new_with_label("Configure Linear Congruential Generator")
        self.conf_LGC.connect("clicked", self.on_button_LGC)
        vbox.pack_start(self.conf_LGC, True, True, 0)

        self.conf_MS = Gtk.Button.\
            new_with_label("Configure Middle-Square")
        self.conf_MS.connect("clicked", self.on_button_MS)
        vbox.pack_start(self.conf_MS, True, True, 0)

        self.conf_LFSR = Gtk.Button.\
            new_with_label("Configure Linear-Feedback Shift Register (16-bit)")
        self.conf_LFSR.connect("clicked", self.on_button_LFSR)
        vbox.pack_start(self.conf_LFSR, True, True, 0)

        self.conf_CC20 = Gtk.Button.\
            new_with_label("Configure ChaCha20")
        vbox.pack_start(self.conf_CC20, True, True, 0)

        self.btn_run = Gtk.Button.new_with_label("Run Simulation")
        self.btn_run.connect("clicked", self.on_button_run)
        vbox.pack_start(self.btn_run, True, True, 0)

    def on_button_run(self, button):
        print(self.LCG_m, self.LCG_a, self.LCG_c, self.MS_isFloor)

    def on_button_LGC(self, button):
        dialog = LCGDialog(self, self.LCG_m, self.LCG_a, self.LCG_c)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
            self.LCG_m = dialog.getValue_m()
            self.LCG_a = dialog.getValue_a()
            self.LCG_c = dialog.getValue_c()
            print("m: %s" % self.LCG_m)
            print("a: %s" % self.LCG_a)
            print("c: %s" % self.LCG_c)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")

        dialog.destroy()

    def on_button_MS(self, button):
        dialog = MSDialog(self, self.MS_max)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
            self.MS_max = dialog.getValue_max()
            print("MS Max: %s" % self.MS_max)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")

        dialog.destroy()

    def on_button_LFSR(self, button):
        dialog = LFSRDialog(self, self.LFSR_tabs)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
            self.LFSR_tabs = dialog.getValue_tabs()
            print("tabs: %s" % self.LFSR_tabs)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")

        dialog.destroy()


sWindow = SettingsWindow()
sWindow.show_all()
sWindow.connect("destroy", Gtk.main_quit)
Gtk.main()
