import time


class Cleaning:
    def __init__(self,device):
        self.device = device

    def run_cleaning(self):
        print("assuming pumps are primed and calibrated, stock bottles are filled with water")
        for v in range(1, 8):
            print("pumping to vial %d" % v)
            self.device.pump_to(vial=2, p1=5, p2=5)
