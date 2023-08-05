import heyoka as hy

from lieops.solver import realHamiltonEqs
from lieops.solver.heyoka import createHamiltonEqs


def create_full_hy_hamiltonian(bl, tol=1e-15):
    '''
    The heyoka solver can only deal with Hamiltonians which depend smoothly on the time-parameter t.
    
    For hard-edge elements we have to introduce auxiliary parameters which will switch off/on
    the Hamiltonian of a specific element after a certain time. These parameters are introduced here.
    '''
    qeq, peq = 0, 0
    for k in range(len(bl)):
        qp, hameqs = createHamiltonEqs(bl[k].hamiltonian, tol=tol)
        qeq += hameqs[0]*hy.par[k]
        peq += hameqs[1]*hy.par[k]
    return [e for e in zip(*[qp, [qeq] + [peq]])]
