import numpy as np
import Shadow

from core import OE, OE_Container

write_shadow_files = False

class Source(OE):
    def __init__(
        self, name: str, energy: float, delta_energy: float, n_rays: int = 1_000_000
    ):
        oe = Shadow.Source()
        super().__init__(oe, name)

        oe.FDISTR = 3
        oe.F_COLOR = 3
        oe.F_PHOT = 0
        oe.HDIV1 = 0.004
        oe.HDIV2 = 0.004
        oe.IDO_VX = 0
        oe.IDO_VZ = 0
        oe.IDO_X_S = 0
        oe.IDO_Y_S = 0
        oe.IDO_Z_S = 0
        oe.ISTAR1 = 5676561
        oe.NPOINT = n_rays
        oe.PH1 = energy - delta_energy / 2
        oe.PH2 = energy + delta_energy / 2
        oe.SIGDIX = 0.01
        oe.SIGDIZ = 0.00113
        oe.SIGMAX = 0.033
        oe.SIGMAZ = 0.027
        oe.VDIV1 = 0.001
        oe.VDIV2 = 0.001
        self.oe = oe

    def set_energy(self, energy: float, delta_energy: float):
        self.oe.PH1 = energy - delta_energy / 2
        self.oe.PH2 = energy + delta_energy / 2

    def run(self, beam: Shadow.Beam):
        print(f"Running optical element {self.idx:02d}")
        if write_shadow_files:
            self.oe.write(f"start.{self.idx:02d}")

        beam.genSource(self.oe)

        if write_shadow_files:
            self.oe.write(f"end.{self.idx:02d}")
            beam.write("begin.dat")
        return beam


class Slit(OE):
    def __init__(self, name: str):
        oe = Shadow.OE()
        super().__init__(oe, name)

        oe.DUMMY = 0.1
        oe.FWRITE = 3
        oe.F_REFRAC = 2
        oe.F_SCREEN = 1
        oe.I_SLIT = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        oe.N_SCREEN = 1
        oe.RX_SLIT = np.array([55.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        oe.RZ_SLIT = np.array([18.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        oe.T_IMAGE = 595.0
        oe.T_INCIDENCE = 0.0
        oe.T_REFLECTION = 180.0
        oe.T_SOURCE = 10000.0
        self.oe = oe

    def run(self, beam: Shadow.Beam):
        print(f"Running optical element {self.idx}")
        if write_shadow_files:
            self.oe.write(f"start.{self.idx:02d}")

        beam.traceOE(self.oe, self.idx)

        if write_shadow_files:
            self.oe.write(f"end.{self.idx:02d}")
            beam.write(f"star.{self.idx:02d}")
        return beam


class M1(OE):
    def __init__(self, name: str):
        oe = Shadow.OE()
        super().__init__(oe, name)

        oe.ALPHA = 90.0
        oe.CIL_ANG = 90.0
        oe.DUMMY = 0.1
        oe.FCYL = 1
        oe.FHIT_C = 1
        oe.FMIRR = 1
        oe.FWRITE = 1
        oe.F_EXT = 1
        oe.RLEN1 = 180.0
        oe.RLEN2 = 180.0
        oe.RMIRR = 2108.8753452152337
        oe.RWIDX1 = 20.0
        oe.RWIDX2 = 20.0
        oe.T_IMAGE = 35.0
        oe.T_INCIDENCE = 80.825
        oe.T_REFLECTION = 80.825
        oe.T_SOURCE = 0.0
        self.oe = oe

    def run(self, beam: Shadow.Beam):
        print(f"Running optical element {self.idx}")
        if write_shadow_files:
            self.oe.write(f"start.{self.idx:02d}")

        beam.traceOE(self.oe, self.idx)

        if write_shadow_files:
            self.oe.write(f"end.{self.idx:02d}")
            beam.write(f"star.{self.idx:02d}")
        return beam


class M2(OE):
    def __init__(self, name: str, pitch: float):
        oe = Shadow.OE()
        super().__init__(oe, name)

        oe.ALPHA = 180.0
        oe.DUMMY = 0.1
        oe.FCYL = 1
        oe.FHIT_C = 1
        oe.FMIRR = 1
        oe.FWRITE = 1
        oe.F_DEFAULT = 0
        oe.F_MOVE = 1
        oe.RLEN1 = 300.0
        oe.RLEN2 = 300.0
        oe.RWIDX1 = 20.0
        oe.RWIDX2 = 20.0
        oe.SIMAG = 14095.0
        oe.SSOUR = 14095.0
        oe.THETA = 82.75
        oe.T_IMAGE = 19.05
        oe.T_INCIDENCE = 82.75
        oe.T_REFLECTION = 82.75
        oe.T_SOURCE = 0.0
        oe.X_ROT = np.degrees(pitch)
        self.oe = oe

    def run(self, beam: Shadow.Beam):
        print(f"Running optical element {self.idx}")
        if write_shadow_files:
            self.oe.write(f"start.{self.idx:02d}")

        beam.traceOE(self.oe, self.idx)

        if write_shadow_files:
            self.oe.write(f"end.{self.idx:02d}")
            beam.write(f"star.{self.idx:02d}")
        return beam
    


class Beamline(OE_Container):
    def __init__(self):
        super().__init__()

    def run(self, beam: Shadow.Beam, start: str, end: str | None = None):
        section = self.first_last_slicing(start, end)
        for oe in self.oe_list[section]:
            oe.run(beam)
        return beam
