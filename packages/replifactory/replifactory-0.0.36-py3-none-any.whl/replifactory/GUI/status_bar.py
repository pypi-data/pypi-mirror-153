import os
import glob
import ipywidgets as widgets

from ipywidgets import Layout, VBox, HBox

from replifactory.GUI.device_tab import get_ftdi_addresses
from replifactory.experiment import Experiment
from pyftdi.usbtools import UsbTools
from replifactory.GUI.device_control_widgets import DeviceControl
from replifactory.GUI.device_tab import get_device_classes
from IPython.display import clear_output, display

# class ExperimentWidget:
#     def __init__(self, status_bar):
#         self.status_bar = status_bar
#         print("output made")
#         with self.status_bar.output:
#             self.status_bar.main_gui.experiment = Experiment("NewExperiment")
#         # if self.status_bar.main_gui.experiment is not None:
#         #     with self.status_bar.output:
#         #         self.status_bar.main_gui.experiment.status()
# box_layout = Layout(display='flex',
#                     flex_flow='column',
#                     align_items='stretch',
#                     border='solid 1px gray', )


class StatusBar:
    layout_width = "350px"
    config_paths = glob.glob("../**/device_config.yaml", recursive=True)
    config_paths = [os.path.relpath(os.path.join(p, "..")) for p in config_paths]
    experiment_directories = glob.glob("../**/main_run.log", recursive=True)
    experiment_directories = [os.path.relpath(os.path.join(p, "..")) for p in experiment_directories]

    def __init__(self, main_gui):
        self.main_gui = main_gui

        self.head = widgets.Accordion(layout=Layout(width=self.layout_width))
        self.head.set_title(0, "Status")

        style = {"description_width": "70px", "align": "left"}
        self.exp_dir = widgets.Dropdown(options=self.experiment_directories, description="directory",
                                        style=style, index=None)

        self.make_new_exp = widgets.Button(tooltip="new experiment directory", icon="fa-folder-plus", layout=Layout(width='35px'))
        self.make_new_exp.on_click(self.handle_new_experiment)
        self.exp_dir.observe(self.handle_experiment_folder_choice, names="value")

        self.ftdi_address = widgets.Dropdown(description="device", options=get_ftdi_addresses(),
                                             style=style,)
        self.connect_button = widgets.Button(tooltip="link device", icon="fa-link")
        self.reset_connection_button = widgets.Button(tooltip="reset connections", button_style="danger",
                                                      icon="fa-retweet")
        self.reset_connection_button.on_click(self.handle_connection_reset_button)
        self.connect_button.on_click(self.handle_connect_button)

        # self.fit_calibration_button = widgets.Button(description="fit calibration functions", icon="fa-cogs")
        # self.fit_calibration_button.on_click(self.main_gui.device_config_tab.handle_fit_calibration_button)

        self.check_button = widgets.Button(description="TEST", icon="fa-clipboard-check")
        self.run_button = widgets.Button(description="RUN", icon="fa-play", disabled=True)
        self.stop_button = widgets.Button(description="STOP", icon="fa-stop", disabled=True)

        self.check_button.on_click(self.handle_check_button)
        self.run_button.on_click(self.handle_run_button)
        self.stop_button.on_click(self.handle_stop_button)

        self.input = None

        self.head.children = [VBox(self.make_widget_list())]

        self.clear_output_button = widgets.Button(description="clear output", icon="fa-eraser")
        self.clear_output_button.on_click(self.handle_clear_output_button)
        self.output = widgets.Output()
        self.output.layout.width = "340px"

        self.widget = VBox([self.head, self.clear_output_button, self.output])

        # self.update()

    # def ask_question(self, question):
    #     input_label = widgets.Label("How can i help you? ")
    #     input_text = widgets.Text()
    def make_widget_list(self):
        widget_list = [HBox([self.exp_dir, self.make_new_exp]),
                       HBox([self.ftdi_address, self.connect_button, self.reset_connection_button]),
                       # self.fit_calibration_button,
                       self.check_button, HBox([self.run_button, self.stop_button])]
        return widget_list

    def handle_connect_button(self, button):
        button.disabled = True
        self.connect_button.icon = "fa-spinner"
        try:
            self.connect_device()
            self.connect_button.button_style = "success"
            self.connect_button.icon = "fa-check"
            # self.connect_button.description = "device connection OK"
        except:
            button.disabled = False
            self.connect_button.icon = "fa-link"
            self.connect_button.button_style = "warning"

    def handle_connection_reset_button(self, button):
        try:
            self.main_gui.device.spi.terminate()
        except:
            pass
        try:
            self.main_gui.device.i2c.terminate()
        except:
            pass

        self.reset_connection_button.icon = "fa-spinner"
        UsbTools.release_all_devices()

        UsbTools.flush_cache()
        # self.control_widget = DeviceControl(None).widget
        self.update_selection_options()
        self.reset_connection_button.icon = "fa-retweet"
        self.connect_button.disabled = False
        self.connect_button.button_style = ""
        self.connect_button.icon = "fa-link"

    def connect_device(self):
        self.main_gui.device_tab.control_widget = DeviceControl(None, self.main_gui).widget
        with self.output:
            clear_output()
            self.update()

            if self.main_gui.device is not None:
                self.main_gui.device.connect(ftdi_address=self.ftdi_address.value)
            else:
                self.main_gui.device = self.main_gui.device_tab.device_class.value(ftdi_address=self.ftdi_address.value)
                self.main_gui.device.connect()
            # if self.config_path.value is not None:
            #     self.main_gui.device.load_calibration(config_path=self.config_path.value)
            self.main_gui.device_tab.control_widget = DeviceControl(self.main_gui.device, self.main_gui).widget
            self.main_gui.device_tab.update()
        self.main_gui.update()

    def update_selection_options(self):
        self.ftdi_address.options = get_ftdi_addresses()
        self.update()
        self.main_gui.update()

    def handle_clear_output_button(self, b):
        with self.output:
            clear_output()

    def update_paths(self):
        self.exp_dir.unobserve_all()

        config_paths = glob.glob("../**/device_config.yaml", recursive=True)
        self.config_paths = [os.path.relpath(p) for p in config_paths]
        experiment_directories = glob.glob("../**/main_run.log", recursive=True)
        self.experiment_directories = [os.path.relpath(os.path.join(p, "..")) for p in experiment_directories]

        self.exp_dir = widgets.Dropdown(options=self.experiment_directories, description="Experiment",
                                        style={"description_width": "initial"}, index=None)
        self.exp_dir.index = self.exp_dir.options.index(os.path.relpath(self.main_gui.experiment.directory))
        self.exp_dir.observe(self.handle_experiment_folder_choice, names="value")
        self.update()

    def handle_check_button(self, b):
        with self.output:
            clear_output()
            assert not self.main_gui.experiment.is_running()
            self.main_gui.experiment.device.run_self_test()
            self.run_button.disabled = False
            # self.update()

    def handle_run_button(self, b):
        with self.output:
            clear_output()
            self.main_gui.experiment.run()
            self.run_button.disabled = True
            self.stop_button.disabled = False
            # self.update()

    def handle_stop_button(self, b):
        with self.output:
            clear_output()
            self.main_gui.experiment.stop()
            self.stop_button.disabled = True
            self.run_button.disabled = False
            # self.update()

    def update(self):
        self.head.children = [VBox(self.make_widget_list())]
        self.main_gui.reload_status_bar_widget()

    def handle_new_experiment(self, b):
        # if self.main_gui.device is None:
        #     with self.output:
        #         print("PLEASE CONNECT DEVICE TO CREATE NEW EXPERIMENT!")
        # else:
        with self.output:
            clear_output()
            self.q = widgets.Text(description="new directory:", style={"description_width": "initial"},
                                  continuous_update=False)
            b = widgets.Button(description="create directory")
            display(VBox([self.q, b]))
            b.on_click(self.make_new_exp_folder)

    def make_new_exp_folder(self, change):
        directory = self.q.value
        with self.output:
            print("Creating new experiment")
            self.main_gui.experiment = Experiment(directory)
            self.main_gui.experiment.device.make_all_blank_cultures()
            self.update()
            self.main_gui.experiment_tab.update()
        self.update_paths()

    def handle_experiment_folder_choice(self, change):
        directory = change.new
        with self.output:
            clear_output()
            self.main_gui.experiment = Experiment(directory)
        self.update()
        self.main_gui.experiment_tab.update()


class InputWidget:
    def __init__(self, q):
        self.name = q
        self.input = widgets.FloatText(description=q, style={'description_width': 'initial'})
        self.submit = widgets.Button(description="submit")
        self.widget = HBox([self.input, self.submit])


class UserInputFloat:
    def __init__(self, status_bar, question, action=None):
        self.status_bar = status_bar
        self.question = question
        self.action = action
        with self.status_bar.output:
            clear_output()
            q = widgets.FloatText(description=question, continuous_update=False)
            display(q)
        q.observe(self.on_answer, names="value")

    def on_answer(self, change):
        with self.status_bar.output:
            clear_output()
            print(self.question, "\nuser input:", change.new)
            if self.action is callable:
                self.action(change.new)


class UserInputText:
    def __init__(self, status_bar, question, action=None):
        self.status_bar = status_bar
        self.question = question
        self.action = action
        with self.status_bar.output:
            clear_output()
            q = widgets.Text(description=question, continuous_update=False)
            display(q)
        q.observe(self.on_answer, names="value")

    def on_answer(self, change):
        with self.status_bar.output:
            clear_output()
            print(self.question, "\nuser input:", change.new)
            if self.action is callable:
                print("calling")
                self.action(change.new)


class UserInputConfirm:
    def __init__(self, status_bar, question, action=None):
        self.status_bar = status_bar
        self.question = question
        self.action = action
        with self.status_bar.output:
            clear_output()
            y = widgets.Button(description="Yes", button_style="success")
            n = widgets.Button(description="No", button_style="danger")
            q = HBox([y, n])
            display(q)
        y.on_click(self.on_yes)
        n.on_click(self.on_no)

    def on_yes(self, button):
        with self.status_bar.output:
            clear_output()
            print("yass")

    def on_no(self, button):
        with self.status_bar.output:
            clear_output()
            print("nope")
