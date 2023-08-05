from replifactory.culture.culture_functions import dilute_adjust_drug1
from replifactory.culture.turbidostat import TurbidostatCulture
import time
import numpy as np
import os
import threading


class CsvDataLogger:
    def __init__(self, directory, variable_name):
        self.lock = threading.Lock()
        header = "time,%s\n" % variable_name
        if not header.endswith("\n"):
            header = header+"\n"
        self.header = header
        self.filepath = os.path.join(directory, variable_name+".csv")
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w+") as f:
                f.write(header)

    def log_line(self, line):
        if not line.endswith("\n"):
            line = line+"\n"
        assert self.lock.acquire(timeout=10)
        try:
            with open(self.filepath, "a") as f:
                f.write(line)
        finally:
            self.lock.release()


class MorbidostatCulture(TurbidostatCulture):
    # active_pumps = (1, 2, 4)

    def __init__(self, directory: str = None, vial_number: int = None, name: str = "Species 1",
                 description: str = "Strain 1"):
        self.t_doubling_rescue_limit = 24
        self.t_doubling_stress_limit = 4
        self.delay_stress_increase_generations = 4
        self.delay_stress_decrease_hrs = 16

        # Running parameters
        self._last_stress_increase_time = None
        super().__init__(directory=directory, vial_number=vial_number, name=name, description=description)
        del self.medium2_c_target

    def description_text(self):
        dilution_factor = (self.default_dilution_volume + self.dead_volume)/self.dead_volume
        generations_per_dilution = np.log2(dilution_factor)
        stress_increase_percent = (dilution_factor - 1)*100/2
        stress_decrease_percent = (dilution_factor - 1)*100
        generations_for_stress_double = self.delay_stress_increase_generations / np.log2((dilution_factor+1)/2)

        max_flow_rate = self.default_dilution_volume / (self.minimum_dilution_delay_mins / 60)  # mL/h
        max_dilution_rate_per_hr = np.log(dilution_factor) / (self.minimum_dilution_delay_mins / 60)
        max_td = np.log(2) / max_dilution_rate_per_hr

        t = f"""When OD > {self.od_max_limit:.2f}, the {self.dead_volume:.1f}mL culture is diluted with {self.default_dilution_volume:.1f}mL total volume, at most every {self.minimum_dilution_delay_mins:.1f} mins.
Every ~{self.delay_stress_increase_generations:.1f} generations the stress (medium2 concentration) is increased by {stress_increase_percent:.1f}% if t_doubling < {self.t_doubling_stress_limit:.1f}h.
The stress is decreased by {stress_decrease_percent:.1f}% if over the last {self.delay_stress_decrease_hrs:.1f}h no dilutions were made and max(t_doubling)<{self.t_doubling_rescue_limit:.1f}h.
               dilution factor: 1/{dilution_factor:.2f} (every {generations_per_dilution:.2f} generations)
                 max flow rate: {max_flow_rate:.2f} mL/h
             min doubling time: {max_td*60:.1f} min
      min stress doubling time: {generations_for_stress_double:.2f} generations"""
        return t

    def update(self):
        if self.is_active():
            self.update_growth_rate()

            if self.od > np.float32(self.od_max_limit):
                if self.time_to_increase_stress() and self.growing_fast_enough:
                    self.lower_od_increase_stress()
                else:
                    self.lower_od()
            if self.time_to_rescue and self.growing_too_slow:
                self.lower_od_decrease_stress()

    @property
    def growing_fast_enough(self):
        return self.t_doubling < self.t_doubling_stress_limit

    def time_to_increase_stress(self):
        if not np.isfinite(np.float32(self._last_stress_increase_time)):
            return False
        else:
            df = self.get_df_generations()
            last_stress_increase_generation = float(df[df.index <= self._last_stress_increase_time].iloc[-1])
            current_generation = self.log2_dilution_coefficient
            return current_generation - last_stress_increase_generation > self.delay_stress_increase_generations
            # hrs_since_stress_increase = (time.time() - self._last_stress_increase_time) / 3600
            # return hrs_since_stress_increase > self.delay_stress_increase_hrs

    @property
    def hrs_since_stress_increase(self):
        if not np.isfinite(np.float32(self._last_stress_increase_time)):
            return np.float32(time.time() - self._inoculation_time) / 3600
        else:
            return (time.time() - self._last_stress_increase_time) / 3600

    @property
    def last_stress_increase_generation(self):
        df = self.get_df_generations()
        return float(df[df.index <= self._last_stress_increase_time].iloc[-1])

    @property
    def time_to_rescue(self):
        hrs_inactive = self.minutes_since_last_dilution / 60
        return hrs_inactive > np.float32(self.delay_stress_decrease_hrs)

    @property
    def growing_too_slow(self):
        if self.t_doubling < 0:
            return True
        else:
            return self.t_doubling > np.float32(self.t_doubling_rescue_limit)

    def lower_od(self):
        """keep stress level"""
        dilute_adjust_drug1(culture=self, target_concentration=self.medium2_concentration)

    def lower_od_decrease_stress(self):
        self._last_stress_increase_time = int(time.time())
        dilute_adjust_drug1(culture=self, target_concentration=0)

    # def rescue_if_necessary(self):
    #     hrs_inactive = self.minutes_since_last_dilution / 60
    #     if hrs_inactive > np.float32(self.delay_stress_decrease_hrs):
    #         if self.t_doubling > np.float32(self.t_doubling_rescue_limit) or self.t_doubling < 0:
    #             self.decrease_stress()

    def lower_od_increase_stress(self, stress_increase_factor=None):
        self._last_stress_increase_time = int(time.time())
        dilute_adjust_drug1(culture=self, stress_increase_factor=stress_increase_factor)

    # def decrease_stress(self):
    #     """
    #     makes standard dilution with no drug
    #     :return:
    #     """
    #     # dilution_factor = (self.dead_volume + self.default_dilution_volume) / self.dead_volume
    #     # stress_decrease_factor = dilution_factor
    #     self.dilute(pump1_volume=self.default_dilution_volume,
    #                 pump2_volume=0)

    def check(self):
        super().check()
        assert np.isfinite(self.t_doubling_stress_limit)
        assert np.isfinite(self.t_doubling_rescue_limit)
        assert np.isfinite(self.delay_stress_decrease_hrs)
        assert np.isfinite(self.delay_stress_increase_generations)
        assert np.isfinite(self.device.pump_stock_concentrations[2])
        assert callable(self.device.pump2.calibration_function)
