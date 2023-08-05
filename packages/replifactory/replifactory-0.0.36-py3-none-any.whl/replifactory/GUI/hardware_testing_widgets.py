import ipywidgets as widgets
from IPython.core.display import clear_output
from ipywidgets import interactive, fixed, HBox, Layout, VBox


class HarwareTestGUI:
    def __init__(self, main_gui):
        self.main_gui = main_gui
        self.widget = widgets.Accordion(layout=Layout(width="720px"))
        self.widget.set_title(0, "Testing")
        self.self_test_button = widgets.Button(description="self test", icon="fa-list-check")
        self.pump_test_button = widgets.Button(description="start pump test", icon="fa-tint")
        self.pump_select = widgets.Dropdown(options=["pump 1", "pump 2", "pump 4"])
        self.stop_pump_test_button = widgets.Button(description="stop test", button_style="danger", icon="fa-stop")

        self.text_test = widgets.HTML("""<b>Fluid test</b><br>
                Please ensure:<br>
                1. There is water in stock bottles 1 and 2.<br>
                2. Tubing system is installed into valves and pumps. All pumps spin clockwise<br>
                3. Luer connectors are well tightened on the needles.<br>
                4. For testing pump 4 (vacuum), make sure the waste needle is below the liquid level.<br>
                Check jupyter log with level info or debug.<br>""")
        self.output = widgets.Output()
        self.output2 = widgets.Output()

        self.pump_testing_widgets = HBox([self.pump_test_button, self.pump_select, self.stop_pump_test_button])
        self.widget.children = [VBox([self.self_test_button, self.output, self.text_test, self.pump_testing_widgets, self.output2])]

        self.self_test_button.on_click(self.run_self_test)
        self.pump_test_button.on_click(self.run_pump_test)
        self.stop_pump_test_button.on_click(self.stop_pump_test)

    def run_self_test(self, button):
        self.self_test_button.disabled = True
        self.self_test_button.icon = "fa-spinner"
        try:
            with self.output:
                clear_output()
                self.main_gui.device.run_self_test()
        finally:
            self.self_test_button.disabled = False
            self.self_test_button.icon = "fa-list-check"

    def run_pump_test(self, button):
        with self.output2:
            clear_output()
            print("Starting fluid test. Please check jupyter log with level info or debug.")
        pump_number = int(self.pump_select.value[-1])
        self.main_gui.device.testing.background_visual_test_pump(main_gui=self.main_gui, pump_number=pump_number)

    def stop_pump_test(self, button):
        self.main_gui.device.testing.stop()
