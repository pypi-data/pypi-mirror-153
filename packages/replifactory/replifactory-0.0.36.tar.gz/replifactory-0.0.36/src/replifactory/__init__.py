__version__ = "0.0.36"
from .device.base_device import BaseDevice
from .device.morbidostat_device import MorbidostatDevice
from .culture import TurbidostatCulture, MorbidostatCulture
from .experiment import Experiment
from .GUI.main_gui import MainGuiBuilder as Gui
# from .GUI.main_gui import open_gui
from .GUI.notifier import Notifier
from . import util
from IPython.display import display
import subprocess
import sys


def upgrade_replifactory():
    output = subprocess.check_output([sys.executable, "-m", "pip", "install", "--upgrade", "replifactory"])
    print(output.decode("utf-8"))


class MainGui:
    def __init__(self):
        self.gui = None

    @property
    def widget(self):
        global _main_gui
        if "_main_gui" in globals().keys():
            self.gui = _main_gui
        else:
            if self.gui is None:
                self.gui = Gui()
        # display(self.gui.widget)
        return self.gui.widget

gui = MainGui()


