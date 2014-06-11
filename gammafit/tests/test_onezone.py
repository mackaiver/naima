# Licensed under a 3-clause BSD style license - see LICENSE.rst
from astropy import units as u
import numpy as np
from numpy.testing import assert_approx_equal
from astropy.tests.helper import pytest

try:
    import emcee
    HAS_EMCEE = True
except ImportError:
    HAS_EMCEE = False


electronozmpars={
        'seedspec':'CMB',
        'index':2.0,
        'cutoff':1e13*u.eV,
        'beta':1.0,
        'ngamd':100,
        'gmin':1e4,
        'gmax':1e10,
        }


def test_electronozm():
    """
    test sync and IC calculation
    """
    from ..onezone import ElectronOZM

    ozm = ElectronOZM(np.logspace(0,15,1000)*u.eV, 1, **electronozmpars)
    ozm.calc_outspec()

    lsy=np.trapz(ozm.specsy*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert( lsy.unit == u.erg/u.s )
    assert_approx_equal(lsy.value, 2.527857584e-4)

    lic=np.trapz(ozm.specic*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert( lic.unit == u.erg/u.s )
    assert_approx_equal(lic.value, 2.832788802e-4)

def test_seed_input():
    """
    test initialization of different input formats for seed photon fields
    """
    from ..onezone import ElectronOZM

    ozm = ElectronOZM(np.logspace(0,15,1000)*u.eV, 1,
            seedspec = 'CMB')

    ozm = ElectronOZM(np.logspace(0,15,1000)*u.eV, 1,
            seedspec = ['CMB','FIR','NIR'],)

    ozm = ElectronOZM(np.logspace(0,15,1000)*u.eV, 1,
            seedspec = ['CMB',['test',5000*u.K,0],],)

    ozm = ElectronOZM(np.logspace(0,15,1000)*u.eV, 1,
            seedspec = ['CMB',['test2',5000*u.K,15*u.eV/u.cm**3],],)

def test_electronozm_evolve():
    """
    test electron evolution
    """
    from ..onezone import ElectronOZM

    ozm = ElectronOZM(np.logspace(0,15,1000)*u.eV, 1, evolve_nelec=True, **electronozmpars)
    ozm.calc_outspec()

    lsy=np.trapz(ozm.specsy*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert( lsy.unit == u.erg/u.s )
    assert_approx_equal(lsy.value, 915035075.9510874)

    lic=np.trapz(ozm.specic*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert( lic.unit == u.erg/u.s )
    assert_approx_equal(lic.value, 8288470921.689767)


def test_protonozm():
    """
    test ProtonOZM
    """
    from ..onezone import ProtonOZM

    # Exponential cutoff powerlaw
    ozm = ProtonOZM(np.logspace(9,15,100)*u.eV, 1, index=2.0, cutoff=1e13*u.eV, beta=1.0)
    ozm.calc_outspec()
    lpp=np.trapz(ozm.specpp*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert_approx_equal(lpp.value,1.3959817466686348e-15, significant=5)
    # Powerlaw
    ozm.cutoff=None
    ozm.calc_outspec()
    lpp=np.trapz(ozm.specpp*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert_approx_equal(lpp.value,5.770536614281706e-15, significant=5)
    # Broken Powerlaw
    ozm.index1=1.5
    ozm.index2=1.5
    ozm.E_break=10*u.TeV
    ozm.calc_outspec()
    lpp=np.trapz(ozm.specpp*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert_approx_equal(lpp.value,3.754818148524127e-13, significant=5)

    # different Etrans
    ozm = ProtonOZM(np.logspace(9,15,100)*u.eV, 1, index=2.0, cutoff=1e13*u.eV, beta=1.0,
            Etrans = 1*u.TeV)
    ozm.calc_outspec()
    lpp=np.trapz(ozm.specpp*ozm.outspecene,ozm.outspecene).to('erg/s')
    assert_approx_equal(lpp.value,1.1852004994595184e-15, significant=5)


def test_log():
    from ..onezone import ProtonOZM, ElectronOZM

    ozm = ElectronOZM(np.logspace(11,13,10)*u.eV, 1, nolog=True)
    ozm.calc_outspec()

    ozm = ElectronOZM(np.logspace(11,13,10)*u.eV, 1, debug=True)
    ozm.calc_outspec()

    ozm = ProtonOZM(np.logspace(11,13,10)*u.eV, 1, nolog=True)
    ozm.calc_outspec()

    ozm = ProtonOZM(np.logspace(11,13,10)*u.eV, 1, debug=True)
    ozm.calc_outspec()

