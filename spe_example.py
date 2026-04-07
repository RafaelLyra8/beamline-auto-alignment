import matplotlib.pyplot as plt
import numpy as np
from optcore import units

from beamline import *

energy_list = np.linspace(8, 80, int(73 / 4))

fig, ax = plt.subplots(1, 1, figsize=(12, 8), sharex=True)


def do_energy_scan(
    beamline: Beamline,
    min_energy: float = 8.0,
    max_energy: float = 80.0,
    energy_points: int = 73,
    normalized: bool = True,
):

    energy_array = np.linspace(min_energy, max_energy, energy_points)
    intensities = []

    for energy in energy_array:

        beamline.src.set_energy(energy=energy, delta_energy=0.01)
        Alfa, Beta, Gamma = sx700_angles(
            energy=energy, cff=2, line_density=180, normal_or_surface=0
        )
        beamline.m_pgm.set_angles(angle=Gamma)
        beamline.g_pgm.set_angles(incidence_angle=Alfa, reflection_angle=-Beta)

        beam = Shadow.Beam()
        beam = beamline.run(beam, start="src", end="m1")
        try:
            info_beam = beam.histo1(col=1, nolost=1)
            intensities.append(info_beam["intensity"])
        except:
            intensities.append(0.0)

    intensities = np.array(intensities)
    if normalized:
        intensities /= max(intensities)

    return energy_array, intensities


if __name__ == "__main__":

    ref_energy = 80 * units.eV

    simulate_all_slits: bool = False

    beamline = Beamline()

    beamline.append(
        Source(name="src", n_rays=10_000, energy=ref_energy, delta_energy=0.01)
    )
    beamline.append(Slit(name="slit"))
    beamline.append(M1(name="m1"))
    beamline.append(M2(name="m2", pitch=0 * 40 * units.urad))

    Alfa, Beta, Gamma = sx700_angles(
        energy=ref_energy, cff=2, line_density=180, normal_or_surface=0
    )

    beamline.append(MPGM(name="m_pgm", angle=Gamma, rz=0))
    beamline.append(
        GPGM(
            name="g_pgm",
            incidence_angle=Alfa,
            reflection_angle=-Beta,
            rz=np.degrees(0 * 1000e-6),
        )
    )

    if simulate_all_slits:
        beamline.append(
            Capillar(
                name="c1",
                aperture=5.0,
                source_distance=4342.0,
                hor_translation=0.0,
                ver_translation=0.0,
            )
        )
        beamline.append(
            Capillar(
                name="c2",
                aperture=3.0,
                source_distance=211.0,
                hor_translation=0.0,
                ver_translation=0.0,
            )
        )
        beamline.append(
            Capillar(
                name="c3",
                aperture=1.5,
                source_distance=211.0,
                hor_translation=0.0,
                ver_translation=0.0,
            )
        )

        beamline.append(
            SSAperture(
                name="ss-a", hor_aperture=1.0, ver_aperture=0.05, source_distance=236.0
            )
        )

        beamline.append(
            Capillar(
                name="c4",
                aperture=1.5,
                source_distance=236.0,
                hor_translation=0.0,
                ver_translation=0.0,
            )
        )
        beamline.append(
            Capillar(
                name="c5",
                aperture=3.0,
                source_distance=211.0,
                hor_translation=0.0,
                ver_translation=0.0,
            )
        )
        beamline.append(
            Capillar(
                name="c6",
                aperture=5.0,
                source_distance=211.0,
                hor_translation=0.0,
                ver_translation=0.0,
            )
        )
    else:
        beamline.append(
            SSAperture(
                name="ss-a", hor_aperture=1.0, ver_aperture=0.05, source_distance=5000.0
            )
        )

    energies, intensities = do_energy_scan(
        beamline=beamline,
        min_energy=8,
        max_energy=80,
        energy_points=21,
        normalized=True,
    )

    plt.plot(energies, intensities)

    plt.xlabel("Energy [eV]")
    plt.ylabel("Intensity")

    plt.minorticks_on()
    plt.grid(which="major", alpha=0.5)
    plt.grid(which="minor", linestyle=":", alpha=0.25)

    plt.yscale("log")

    plt.tight_layout()
    plt.show()
