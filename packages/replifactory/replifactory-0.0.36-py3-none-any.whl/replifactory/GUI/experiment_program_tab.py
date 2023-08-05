import ipywidgets as widgets
import inspect, sys
from ipywidgets import VBox, Layout, HBox
from IPython.core.display import clear_output
from replifactory.culture.morbidostat import MorbidostatCulture
from replifactory.culture.turbidostat import TurbidostatCulture
from replifactory.culture.chemostat import ChemostatCulture

from replifactory.culture.endurance import EnduranceStressCulture
from replifactory.culture.blank import BlankCulture
from replifactory.culture.batch import BatchCulture
# from replifactory.culture.patients import PatientCulture
import os
import time


class ExperimentProgramTab:
    title = "Experiment"

    def __init__(self, main_gui):
        self.main_gui = main_gui
        self.title = "Experiment"

        # self.load_exp = widgets.Dropdown(options=self.experiment_directories, description="Load experiment",
        #                                  style={"description_width": "initial"}, index=None)
        # self.new_exp_folder = widgets.Text(description="new experiment directory:",
        #                                    style={"description_width": "initial"})
        # make_new_exp = widgets.Button(description="new experiment")
        # make_new_exp.on_click(self.handle_new_experiment)
        # self.load_exp.observe(self.handle_experiment_folder_choice, names="value")
        # self.selector = VBox([self.load_exp, HBox([self.new_exp_folder, make_new_exp])])
        self.vials = widgets.Label("No experiment selected")
        self.widget = VBox([self.vials])

    # def handle_new_experiment(self, b):
    #     if self.main_gui.device is None:
    #         with self.main_gui.status_bar.output:
    #             print("PLEASE CONNECT DEVICE TO CREATE NEW EXPERIMENT!")
    #     else:
    #         with self.main_gui.status_bar.output:
    #             clear_output()
    #             self.main_gui.experiment = Experiment(self.new_exp_folder.value)
    #             self.update()
    #
    # def handle_experiment_folder_choice(self, change):
    #     with self.main_gui.status_bar.output:
    #         clear_output()
    #         self.main_gui.experiment = Experiment(change.new)
    #     self.update()

    def make_vial_widgets(self):
        # if self.main_gui.experiment is not None:
        #     if self.main_gui.experiment.device is not None:
        absdir = os.path.abspath(self.main_gui.experiment.directory)
        title = widgets.HTML('<b>%s:</b>' % absdir,
                             layout=Layout(width="400px"))
        self.vials = VBox([title] + [VialConfigWidget(program_viewer_tab=self, vial_number=v).widget for v in range(1, 8)])

    def update(self):
        self.make_vial_widgets()
        self.widget = VBox([self.vials])
        self.main_gui.update()

    # def make_vial_widget(self, vial_number):
    #     vial = self.main_gui.experiment.device.cultures[vial_number]
    #     title = widgets.HTML('<b>Vial %d:</b>' % vial_number, layout=Layout(width="40px", height="40px"))
    #     culture_options = [BlankCulture, TurbidostatCulture, MorbidostatCulture, EnduranceStressCulture]
    #     culture_options_names = [str(klass)[8:-2] for klass in culture_options]
    #     culture_options += [type(None)]
    #     culture_options_names += ["None"]
    #
    #     vial_culture_index = culture_options.index(type(vial))
    #     algorithm = widgets.Dropdown(options=list(zip(culture_options_names, culture_options)),
    #                                  index=vial_culture_index)
    #
    #     def handle_vial_class_change(change):
    #         if change.new is type(None):
    #             self.main_gui.experiment.device.cultures[vial_number] = None
    #         else:
    #             self.main_gui.experiment.device.cultures[vial_number] = \
    #                 change.new(directory=self.main_gui.experiment.directory, vial_number=vial_number)
    #         self.widget = self.make_vial_widgets()
    #         self.main_gui.update()
    #
    #     algorithm.observe(handle_vial_class_change, names="value")
    #
    #     if vial is not None:
    #         description_style = {}
    #         description_widgets = [
    #             widgets.Text(value=vial.name, description="name", style=description_style, continuous_update=True),
    #             widgets.Textarea(value=vial.description, description="description",
    #                              style=description_style, continuous_update=True, layout=Layout(height="80px"))]
    #         for w in description_widgets:
    #             w.observe(vial.handle_value_change, names="value")
    #         description_box = widgets.VBox(description_widgets)
    #         left_panel = VBox([title, algorithm, description_box])
    #         return HBox([left_panel, vial.widget])
    #     else:
    #         return VBox([title, algorithm])


def get_culture_options():
    culture_options = [BatchCulture, ChemostatCulture, TurbidostatCulture, MorbidostatCulture,
                       EnduranceStressCulture, BlankCulture]  # BlankCulture, PatientCulture
    for name, obj in inspect.getmembers(sys.modules["__main__"]):
        if inspect.isclass(obj):
            if issubclass(obj, BlankCulture):
                if obj not in culture_options:
                    culture_options += [obj]
    return culture_options


class VialConfigWidget:
    def __init__(self, program_viewer_tab, vial_number):
        self.program_viewer_tab = program_viewer_tab
        self.main_gui = program_viewer_tab.main_gui
        self.vial_number = vial_number
        self.culture = self.main_gui.experiment.device.cultures[vial_number]
        title = widgets.HTML('<b>Vial %d:</b>' % vial_number, layout=Layout(width="40px", height="40px"))
        self.inoculate = widgets.Button(description="inoculate")
        self.inoculate.on_click(self.handle_inoculate_button)
        try:
            is_active = self.culture._is_active  # todo: replace none
        except:
            is_active = False
        self.active_button = widgets.ToggleButton(description="vial %d" % vial_number, value=bool(is_active), layout=Layout(width="80px"), icon="toggle-off")
        if is_active:
            self.active_button.value = True
            self.active_button.icon = "toggle-on"
            self.active_button.tooltip = "active"
            self.active_button.button_style = "success"
        else:
            self.active_button.button_style = "warning"

        self.active_button.observe(self.handle_active_button)
        self.description_text = widgets.Output()
        if type(self.culture) not in [BlankCulture, type(None)]:
            if self.culture._inoculation_time:
                self.inoculate.disabled = True
                self.inoculate.description = "inoculated"
                self.inoculate.button_style = "info"
                self.inoculate.tooltip = "inoculated on %s"%time.ctime(self.culture._inoculation_time)
        self.blank = widgets.Button(description="OD BLANK",
                                    tooltip="set od_blank to the mean of the past 10 measurements",
                                    layout=Layout(width="100px"))
        self.blank.on_click(self.handle_blank_button)
        culture_options = get_culture_options()
        culture_options_names = [str(klass)[8:-2] for klass in culture_options]
        culture_options += [type(None)]
        culture_options_names += ["None"]
        culture_options_index = culture_options.index(type(self.culture))

        algorithm = widgets.Dropdown(options=list(zip(culture_options_names, culture_options)),
                                     index=culture_options_index)

        algorithm.observe(self.handle_vial_class_change, names="value")

        if self.culture is not None:
            description_style = {}
            description_widgets = [
                widgets.Text(value=self.culture.name, description="name", style=description_style, continuous_update=True),
                widgets.Textarea(value=self.culture.description, description="description",
                                 style=description_style, continuous_update=True, layout=Layout(height="80px"))]
            for w in description_widgets:
                w.observe(self.handle_vial_parameter_change, names="value")
            description_box = widgets.VBox(description_widgets, layout=Layout(height="150px"))
            copy_button = widgets.Button(description="copy parameters", icon="fa-copy")
            paste_button = widgets.Button(description="paste parameters", icon="fa-paste")
            copy_button.on_click(self.handle_copy_button)
            paste_button.on_click(self.handle_paste_button)
            copypaste = HBox([copy_button, paste_button])
            left_panel = VBox([HBox([self.active_button, self.inoculate]),
                               algorithm,
                               description_box,
                               copypaste,
                               self.blank])
            with self.description_text:
                print(self.culture.description_text())
            self.widget = VBox([HBox([left_panel, self.make_parameters_widget()]), self.description_text], layout=Layout(border='solid'))
        else:
            self.widget = VBox([title, algorithm], layout=Layout(border='solid'))

    def handle_active_button(self, b):
        self.culture._is_active = self.active_button.value
        if self.culture._is_active:
            self.active_button.icon = "toggle-on"
            self.active_button.tooltip = "active"
            self.active_button.button_style = "success"
        else:
            self.active_button.icon = "toggle-off"
            self.active_button.tooltip = "inactive"
            self.active_button.button_style = "warning"

    def handle_copy_button(self, b):
        self.main_gui._copy_from_vial = self.vial_number

    def handle_paste_button(self,b):
        source = self.main_gui.device.cultures[self.main_gui._copy_from_vial]
        if type(self.culture)==type(source):
            copy_parameters = [k for k in source.__dict__.keys() if not k.startswith("_") and
                               k not in ["directory", "file_lock", "vial_number", "pumps", "scheduler"]]
            for p in copy_parameters:
                self.culture.__dict__[p] = source.__dict__[p]
                if p == "name":
                    self.culture.__dict__[p] += " - vial %d" % self.vial_number
            self.culture.save()
            self.program_viewer_tab.update()

    def make_parameters_widget(self):
        user_parameters = [k for k in self.culture.__dict__.keys() if not k.startswith("_") and
                           k not in ["name", "description", "directory", "file_lock", "vial_number", "pumps", "scheduler"]]
        parameter_style = {'description_width': '230px'}
        parameter_widgets = [widgets.FloatText(value=self.culture.__dict__[par], description=par, style=parameter_style,
                                               continuous_update=True) for par in user_parameters]
        for w in parameter_widgets:
            w.observe(self.handle_vial_parameter_change, names="value")
        parameter_box = widgets.VBox(parameter_widgets)

        # description_style = {}
        # description_widgets = [widgets.HTML('<b>Vial %d:</b>' % self.vial_number, layout=Layout(width="40px")),
        #                        widgets.Text(value=self.name, description="name", style=description_style, continuous_update=True),
        #                        widgets.Textarea(value=self.description, description="description",
        #                                         style=description_style, continuous_update=True)]
        # for w in description_widgets:
        #     w.observe(self.handle_value_change, names="value")
        # description_box = widgets.VBox(description_widgets)
        # widgets.HBox([description_box, parameter_box])
        return parameter_box

    def handle_blank_button(self, button):
        self.culture.write_blank_od()
        self.program_viewer_tab.update()

    def handle_inoculate_button(self, button):
        self.culture.inoculate()
        button.disabled = True
        button.description = "inoculated"
        button.button_style = "info"
        self.culture.save()

    def handle_vial_parameter_change(self, change):
        parameter_name = change.owner.description
        self.culture.__dict__[parameter_name] = change.new
        self.update_description()
        self.culture.save()

    def update_description(self, change=None):
        with self.description_text:
            clear_output()
            print(self.culture.description_text())

    def handle_vial_class_change(self, change):
        if change.new is type(None):
            self.main_gui.experiment.device.cultures[self.vial_number] = None
        else:
            self.main_gui.experiment.device.cultures[self.vial_number] = \
                change.new(directory=self.main_gui.experiment.directory, vial_number=self.vial_number)
        self.widget = self.__init__(program_viewer_tab=self.program_viewer_tab, vial_number=self.vial_number)
        self.program_viewer_tab.update()
