import math
import functools
import matplotlib.pyplot as plt
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def LCG(m, a, c, X_n):
    return (a*X_n+c) % m


def MS(extract, fill, seed):
    # Based on Wikipedia Example:
    # https://en.wikipedia.org/wiki/Middle-square_method#Example_implementation
    return int(str(seed**2).zfill(fill)
               [int(fill/2-math.floor(extract/2)):
                int(fill/2+round(extract/2))])


def LFSR(tabs, seed):
    S = "{0:b}".format(seed).zfill(16)
    bits = []
    for t in tabs:
        bits.append(int(S[t-1]))
    bit = functools.reduce(lambda x, y: x ^ y, bits)
    return int(str(bit) + S[:15], 2)


def chi2(observed, expected, possible_outcomes):
    res = 0
    count = []
    # Count numbers
    for i in range(possible_outcomes):
        # range(n) starts at 0
        count.append(observed.count(i+1))
    print(count)

    for c in count:
        res += (c-expected)**2 / expected
    return res


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

    def __init__(self, parent, extract, fill):
        Gtk.Dialog.__init__(self, "Configure MS", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        vbox = Gtk.VBox(spacing=6)
        self.get_content_area().add(vbox)

        self.extract_hbox = Gtk.HBox()
        vbox.pack_start(self.extract_hbox, True, True, 0)

        self.extract_label = Gtk.Label(label="Extract digits: ")
        self.extract_hbox.pack_start(self.extract_label, True, True, 0)

        self.extract_entry = Gtk.Entry()
        self.extract_entry.set_text(str(extract))
        self.extract_hbox.pack_start(self.extract_entry, True, True, 0)

        self.fill_hbox = Gtk.HBox()
        vbox.pack_start(self.fill_hbox, True, True, 0)

        self.fill_label = Gtk.Label(label="Fill digits: ")
        self.fill_hbox.pack_start(self.fill_label, True, True, 0)

        self.fill_entry = Gtk.Entry()
        self.fill_entry.set_text(str(fill))
        self.fill_hbox.pack_start(self.fill_entry, True, True, 0)

        self.show_all()

    def getValue_extract(self):
        return self.extract_entry.get_text()

    def getValue_fill(self):
        return self.fill_entry.get_text()


class LFSRDialog(Gtk.Dialog):

    def __init__(self, parent, tabs):
        Gtk.Dialog.__init__(self, "Configure LFSR", parent, 0,
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
    MS_extract = 3
    MS_fill = 6
    LFSR_tabs = [16, 14, 13, 11]

    rng_seed = 123
    rng_ceiling = 1000
    rng_amount = 100

    def __init__(self):
        Gtk.Window.__init__(self, title="RNG-simulation")

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        self.seed_hbox = Gtk.HBox(homogeneous=True)
        vbox.pack_start(self.seed_hbox, True, True, 0)

        self.seed_label = Gtk.Label(label="Seed: ")
        self.seed_hbox.pack_start(self.seed_label, True, True, 0)

        self.seed_entry = Gtk.Entry()
        self.seed_entry.set_text(str(self.rng_seed))
        self.seed_hbox.pack_start(self.seed_entry, True, True, 0)

        self.rng_ceiling_hbox = Gtk.HBox(homogeneous=True)
        vbox.pack_start(self.rng_ceiling_hbox, True, True, 0)

        self.rng_ceiling_label = Gtk.Label(label="RNG ceiling: ")
        self.rng_ceiling_hbox.pack_start(self.rng_ceiling_label, True, True, 0)

        self.rng_ceiling_entry = Gtk.Entry()
        self.rng_ceiling_entry.set_text(str(self.rng_ceiling))
        self.rng_ceiling_hbox.pack_start(self.rng_ceiling_entry, True, True, 0)

        self.rng_amount_hbox = Gtk.HBox(homogeneous=True)
        vbox.pack_start(self.rng_amount_hbox, True, True, 0)

        self.rng_amount_label = Gtk.Label(label="Amount to generate: ")
        self.rng_amount_hbox.pack_start(self.rng_amount_label, True, True, 0)

        self.rng_amount_entry = Gtk.Entry()
        self.rng_amount_entry.set_text(str(self.rng_amount))
        self.rng_amount_hbox.pack_start(self.rng_amount_entry, True, True, 0)

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

        self.btn_run = Gtk.Button.new_with_label("Run Simulation")
        self.btn_run.connect("clicked", self.on_button_run)
        vbox.pack_start(self.btn_run, True, True, 0)

    def on_button_run(self, button):
        self.rng_seed = int(self.seed_entry.get_text())
        self.rng_ceiling = int(self.rng_ceiling_entry.get_text())
        self.rng_amount = int(self.rng_amount_entry.get_text())
        print(self.LCG_m, self.LCG_a, self.LCG_c, self.MS_extract)

        print("Generating %s random numbers" % self.rng_amount)

        # Generate numbers with LCG, MS and LFSR

        lcg_list = [LCG(self.LCG_m, self.LCG_a, self.LCG_c, self.rng_seed)]
        for i in range(self.rng_amount-1):
            lcg_list.append(LCG(self.LCG_m, self.LCG_a,
                                self.LCG_c, lcg_list[i]))
        print("LCG: %s" % lcg_list)

        ms_list = [MS(self.MS_extract, self.MS_fill, self.rng_seed)]
        for i in range(self.rng_amount-1):
            ms_list.append(MS(self.MS_extract, self.MS_fill, ms_list[i]))
        print("MS: %s" % ms_list)

        lfsr_list = [LFSR(self.LFSR_tabs, self.rng_seed)]
        for i in range(self.rng_amount-1):
            lfsr_list.append(LFSR(self.LFSR_tabs, lfsr_list[i]))
        print("LFSR: %s" % lfsr_list)

        # Adjust numbers to ceiling and round/convert to integers

        lcg_list = list(map(lambda x: int(x/(self.LCG_m-1)*self.rng_ceiling),
                            lcg_list))
        ms_list = list(map(lambda x:
                           int(x/(10**self.MS_extract-1)*self.rng_ceiling),
                           ms_list))
        # 2^16 - 1 = 65535
        lfsr_list = list(map(lambda x: int(x/65535*self.rng_ceiling),
                             lfsr_list))
        print("LCG adjusted and rounded: %s" % lcg_list)
        print("MS adjusted and rounded: %s" % ms_list)
        print("LFSR adjusted and rounded: %s" % lfsr_list)

        # Calculate Chi2

        e = self.rng_amount/self.rng_ceiling
        print("e: %s" % e)
        lcg_chi2 = chi2(lcg_list, e, self.rng_ceiling)
        ms_chi2 = chi2(ms_list, e, self.rng_ceiling)
        lfsr_chi2 = chi2(lfsr_list, e, self.rng_ceiling)
        print("LCG chi2: %s" % lcg_chi2)
        print("MS chi2: %s" % ms_chi2)
        print("LFSR chi2: %s" % lfsr_chi2)

        # Plot results

        plt.figure()
        plt.title(("Linear Congruential Method - %s numbers under %s with" +
                   " seed: %s\n" + "χ²: %s") %
                  (self.rng_amount, self.rng_ceiling, self.rng_seed, lcg_chi2))
        lcg_plot = plt.plot(lcg_list, 'ro',
                            label=("modulus m: %s \n" +
                                   "multiplier a: %s \n" +
                                   "increment c: %s") %
                            (self.LCG_m, self.LCG_a, self.LCG_c))
        plt.legend(handles=lcg_plot)

        plt.figure()
        plt.title(("Middle Square Method - %s numbers under %s with seed:" +
                   " %s\n" + "χ²: %s") %
                  (self.rng_amount, self.rng_ceiling, self.rng_seed, ms_chi2))
        ms_plot = plt.plot(ms_list, 'ro',
                           label="Extract digits: %s \nFill digits %s" %
                           (self.MS_extract, self.MS_fill))
        plt.legend(handles=ms_plot)

        plt.figure()
        plt.title(("Linear Feedback Shift Register - %s numbers under %s" +
                   " with seed: %s\n" + "χ²: %s") %
                  (self.rng_amount, self.rng_ceiling, self.rng_seed,
                   lfsr_chi2))
        lfsr_plot = plt.plot(lfsr_list, 'ro',
                             label="Tabs: %s" % str(self.LFSR_tabs)[1:-1])
        plt.legend(handles=lfsr_plot)

        plt.show()

    def on_button_LGC(self, button):
        dialog = LCGDialog(self, self.LCG_m, self.LCG_a, self.LCG_c)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
            self.LCG_m = int(dialog.getValue_m())
            self.LCG_a = int(dialog.getValue_a())
            self.LCG_c = int(dialog.getValue_c())
            print("m: %s" % self.LCG_m)
            print("a: %s" % self.LCG_a)
            print("c: %s" % self.LCG_c)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")

        dialog.destroy()

    def on_button_MS(self, button):
        dialog = MSDialog(self, self.MS_extract, self.MS_fill)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
            self.MS_extract = int(dialog.getValue_extract())
            self.MS_fill = int(dialog.getValue_fill())
            print("MS extract: %s" % self.MS_extract)
            print("MS fill: %s" % self.MS_fill)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")

        dialog.destroy()

    def on_button_LFSR(self, button):
        dialog = LFSRDialog(self, self.LFSR_tabs)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
            self.LFSR_tabs = int(dialog.getValue_tabs())
            print("tabs: %s" % self.LFSR_tabs)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")

        dialog.destroy()


sWindow = SettingsWindow()
sWindow.show_all()
sWindow.connect("destroy", Gtk.main_quit)
Gtk.main()
