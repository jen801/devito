import pytest
import os
import sys

from benchmarks.user.benchmark import run
from devito import switchconfig
from subprocess import check_call


@pytest.mark.parametrize('mode, problem, op', [
    ('run', 'acoustic', 'forward'), ('run', 'acoustic', 'adjoint'),
    ('run', 'acoustic', 'jacobian'), ('run', 'acoustic', 'jacobian_adjoint'),
    ('run', 'tti', 'forward'), ('run', 'elastic', 'forward'),
    ('run', 'viscoelastic', 'forward'), ('run', 'acoustic_sa', 'forward'),
    ('run', 'acoustic_sa', 'adjoint'), ('run', 'acoustic_sa', 'jacobian'),
    ('run', 'acoustic_sa', 'jacobian_adjoint'), ('run', 'tti', 'jacobian_adjoint')
])
def test_bench(mode, problem, op):
    """
    Test the Devito benchmark framework on various combinations of modes and problems.
    """

    tn = 4
    nx, ny, nz = 16, 16, 16

    pyversion = sys.executable
    baseline = os.path.realpath(__file__).split("tests/test_benchmark.py")[0]
    benchpath = '%sbenchmarks/user/benchmark.py' % baseline

    command_bench = [pyversion, benchpath, mode,
                     '-P', problem, '-d', '%d' % nx, '%d' % ny, '%d' % nz, '--tn',
                     '%d' % tn, '-op', op]
    if mode == "bench":
        command_bench.extend(['-x', '1'])
    check_call(command_bench)


@pytest.mark.parallel(mode=2)
@switchconfig(profiling='advanced')
def test_run_mpi():
    """
    Test the `run` mode over MPI, with all key arguments used.
    """
    kwargs = {
        'space_order': [4],
        'time_order': [2],
        'autotune': 'off',
        'block_shape': [],
        'shape': (16, 16, 16),
        'tn': 4,
        'warmup': False,
        'dump_summary': 'summary.txt',
        'dump_norms': 'norms.txt'
    }
    run('acoustic', **kwargs)
