from core import OE, OE_Container
from beamline import Beamline, Source, Slit, M1, M2

import Shadow
from optlnls.plot import plot_beam
from optlnls.importing import read_shadow_beam

if __name__ == "__main__":

    beamline = Beamline()

    beamline.append(
        Source(
            name="src",
            energy=20,
            delta_energy=1,
            n_rays=100_000
    ))

    beamline.append(
        M2(...)
    )

    beam = Shadow.Beam()

    beamline.run(
        beam=beam,
        start="src",
        end="src"
    )

    loop_beam = beam.duplicate()

    beam2D = read_shadow_beam(
            beam=beam,
            x_column_index=3,
            y_column_index=1
    )
    output_beam = plot_beam(
        beam2D=beam2D,
        show_plot=True,
        fitType=3,
        textA=2,textB=5,
        x_range=1,x_range_min=-0.1,x_range_max=0.1,
        y_range=1,y_range_min=-0.1,y_range_max=0.1,
        zero_pad_x=2,
        outfilename=f"reference_beam_20eV"
    )