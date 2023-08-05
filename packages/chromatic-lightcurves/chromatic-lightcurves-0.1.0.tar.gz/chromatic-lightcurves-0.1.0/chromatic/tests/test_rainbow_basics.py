from ..rainbows import *
from .setup_tests import *


def test_rainbow_basics():

    nw, nt = 24, 48
    r = Rainbow(
        wavelength=np.linspace(1, 2, nw) * u.micron,
        time=np.linspace(-1, 1, nt) * u.hour,
        flux=np.ones((nw, nt)),
    )

    # test the basic sizes and shapes
    assert r.shape == (nw, nt)
    assert r.nwave == nw
    assert r.ntime == nt
    assert r.nflux == nw * nt

    # testing slicing, indexing, masking
    assert r[:, :].shape == (nw, nt)
    assert r[::2, ::3].shape == (nw / 2, nt / 3)
    assert r[2:4, :].shape == (2, nt)
    assert r[np.arange(2, 4), :].shape == (2, nt)
    assert r[r.wavelength < 1.5 * u.micron, :].shape == (nw / 2, nt)
    assert r[:, r.time < 0 * u.day].shape == (nw, nt / 2)

    assert r[r.wavelength < 1.5 * u.micron, r.time < 0 * u.day].shape == (
        nw / 2,
        nt / 2,
    )


def test_essential_properties():
    # create a simulated rainbow
    r = SimulatedRainbow()

    # wavelength
    x = r.wavelength
    r.wavelength = x * 2
    assert np.all(r.wavelength == x * 2)

    # time
    x = r.time
    r.time = x * 2
    assert np.all(r.time == x * 2)

    # flux
    x = r.flux
    r.flux = x * 2
    assert np.all(r.flux == x * 2)

    # uncertainty
    x = r.uncertainty
    r.uncertainty = x * 2
    assert np.all(r.uncertainty == x * 2)

    # ok
    r.ok = np.isfinite(r.flux) == False
    assert np.all(r.ok == False)


def test_automatic_quantity_sorting():
    # create a simulated rainbow
    r = SimulatedRainbow()

    # does a wavelength-shaped array end up in the right spot?
    r.background = np.random.normal(10, 1, r.nwave)
    assert "background" in r.wavelike

    # does a time-shaped array end up in the right spot?
    r.temperature = np.random.normal(10, 1, r.ntime)
    assert "temperature" in r.timelike

    # does a fluxes-shaped array end up in the right spot?
    r.saturated = np.random.normal(0, 1, r.shape) > 2
    assert "saturated" in r.fluxlike

    # does a weirdly-shaped array still get assigned somewhere?
    r.weird = np.random.normal(0, 1, (1, 2, 3, 4))
    r.weird + 1


def test_shape_warnings():
    a = SimulatedRainbow()
    with pytest.warns(match="transpose"):
        a.flux = a.flux.T

    b = SimulatedRainbow()
    with pytest.warns(match="shape"):
        b.wavelength = np.arange(b.nwave + 1)

    c = SimulatedRainbow()
    with pytest.warns(match="shape"):
        c.time = np.arange(c.ntime + 1)

    d = SimulatedRainbow()
    with pytest.warns(match="shape"):
        d.uncertainty = np.ones((d.nwave + 1, d.ntime + 1))

    e = SimulatedRainbow()
    with pytest.warns(match="shape"):
        d.ok = np.ones((d.nwave + 1, d.ntime + 1))


def test_help():
    Rainbow().help()
