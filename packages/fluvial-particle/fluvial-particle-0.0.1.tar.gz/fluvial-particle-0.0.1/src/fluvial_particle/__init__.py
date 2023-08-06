"""Top-level package for pygeoapi plugin: Fluvial Particle."""

__author__ = "Richard McDonald"
__email__ = "rmcd@usgs.gov"
__version__ = "0.0.1"


from datetime import timedelta
from os import getpid
import pathlib
import time

import numpy as np
import argparse
import h5py
from .Helpers import load_variable_source
from .Settings import Settings
from .FallingParticles import FallingParticles  # noqa
from .LarvalParticles import LarvalBotParticles, LarvalTopParticles  # noqa
from .Particles import Particles  # noqa
from .RiverGrid import RiverGrid


def checkcommandarguments():
    """Check the users command line arguments."""
    parser = argparse.ArgumentParser(
        description="fluvial_particle",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("settings_file", help="User settings file")
    parser.add_argument("output_directory", help="Output directory for results")
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        default=None,
        help="Specify a single integer to fix the seed of the random number generator. Only used in serial mode.",
    )
    parser.add_argument(
        "--no-postprocess",
        "--no_postprocess",
        action="store_false",
        help="Include this flag to prevent RiverGrid post-processing.",
    )
    # note: argparse will convert to key="no_postprocess"

    argdict = vars(parser.parse_args())

    inputfile = pathlib.Path(argdict["settings_file"])
    if not inputfile.exists():
        raise Exception(f"Cannot find settings file {inputfile}")
    outdir = pathlib.Path(argdict["output_directory"])
    if not outdir.is_dir():
        raise Exception(f"Output directory {outdir} does not exist")

    return argdict


def get_prng(timer, seed=None):
    """Generate a random seed using time and the process id.

    Returns
    -------
    seed : int
        The seed on each core

    """
    if seed is None:
        seed = np.int64(np.abs(((timer() * 181) * ((getpid() - 83) * 359)) % 104729))

    print(f"Using seed {seed}", flush=True)

    prng = np.random.RandomState(seed)
    return prng


def load_checkpoint(fname, tidx, start, end, comm=None):
    """Load initial positions from a checkpoint HDF5 file.

    Args:
        fname (str): path to checkpoint HDF5 file
        tidx (int): outer index of HDF5 datasets
        start (int): starting index of this processor's assigned space
        end (int): ending index (non-inclusive)
        comm (mpi4py communicator, optional): for parallel runs.

    Returns:
        x,y,z (NumPy ndarrays): starting position of particles
        t (int): simulation start time
    """
    if comm is None or comm.Get_rank() == 0:
        print("Loading initial particle positions from a checkpoint HDF5 file")
    inputfile = pathlib.Path(fname)
    if not inputfile.exists():
        raise Exception(f"Cannot find load_checkpoint HDF5 file: {fname}")
    if comm is None:
        h5file = h5py.File(fname, "r")
    else:
        h5file = h5py.File(fname, "r", driver="mpio", comm=comm)

    grp = h5file["coordinates"]
    x = grp["x"][tidx, start:end]
    y = grp["y"][tidx, start:end]
    z = grp["z"][tidx, start:end]
    t = grp["time"][tidx].item(0)  # returns t as a Python basic float

    h5file.close()

    return x, y, z, t


def simulate(settings, argvars, timer, comm=None):  # noqa
    """Run the fluvial particle simulation.

    Args:
        settings (dict subclass): parameter settings for the simulation
        argvars (dict): dictionary holding command line argument variables
        timer (time object): does timing
        comm (MPI intracomm object): for parallel runs only, MPI communicator
    """
    t0 = timer()

    # Get rank, number of processors, global number of particles, and local slice indices
    rank = 0
    size = 1
    if comm is not None:
        rank = comm.Get_rank()
        size = comm.Get_size()

    master = rank == 0

    if master:
        print("Beginning simulation", flush=True)

    # Command-line arguments
    output_directory = argvars["output_directory"]
    seed = argvars["seed"]
    postprocessflg = argvars["no_postprocess"]

    # Time Variables
    starttime = 0.0
    endtime = settings["SimTime"]
    dt = settings["dt"]

    # 2D or 3D particle tracking
    track3d = settings["Track3D"]
    print_inc_time = settings["PrintAtTick"]

    # The grid source files
    file_name_2d = settings["file_name_2d"]
    file_name_3d = settings["file_name_3d"]

    # Number of particles to simulate
    npart = settings["NumPart"]
    globalnparts = npart * size  # total number of particles across processors
    start = rank * npart  # slice starting index for HDF5 file
    end = start + npart  # slice ending index (non-inclusive) for HDF5 file

    # Type of Particles class or subclass to simulate
    particles = settings["ParticleType"]

    # Initialize RiverGrid object
    river = RiverGrid(track3d, file_name_2d, file_name_3d)

    # Initialize particle positions
    if isinstance(settings["StartLoc"], tuple):
        # Particles all start at one point
        xstart, ystart, zstart = settings["StartLoc"]
        x = np.full(npart, fill_value=xstart, dtype=np.float64)
        y = np.full(npart, fill_value=ystart, dtype=np.float64)
        z = np.full(npart, fill_value=zstart, dtype=np.float64)
    elif isinstance(settings["StartLoc"], str):
        filepath = pathlib.Path(settings["StartLoc"])

        if not filepath.exists():
            raise Exception(f"The StartLoc file ({str}) does not exist")

        suffix = filepath.suffix
        if suffix == ".h5":
            # Particle positions loaded from an HDF5 file
            tidx = -1
            if "StartIdx" in settings.keys():
                tidx = settings["StartIdx"]
            x, y, z, starttime = load_checkpoint(
                settings["StartLoc"], tidx, start, end, comm
            )
        elif suffix == ".csv":
            pstime, x, y, z = load_variable_source(settings["StartLoc"])
            settings["PartStartTime"] = pstime

    else:
        raise Exception("StartLoc must be tuple or HDF5 checkpoint file path")

    # Get NumPy random state
    rng = get_prng(timer, seed)

    # Initialize class of particles instance
    particles = particles(npart, x, y, z, rng, river, **settings)

    particles.initial_validation(starttime=0.0, frac=0.5)

    # Calc simulation and printing times
    if starttime >= endtime:
        raise Exception(
            f"Simulation start time must be less than end time; current values: {starttime}, {endtime}"
        )
    times = np.arange(starttime + dt, endtime + dt, dt)
    n_times = times.size
    print_inc = np.max([np.int32(print_inc_time / dt), 1])  # bound below
    print_inc = np.min([print_inc, n_times])  # bound above
    print_times = times[print_inc - 1 : n_times : print_inc]
    if print_times[-1] != times[-1]:
        # add final time to print_times if not already
        print_times = np.append(print_times, times[-1])
    n_prints = print_times.size + 1  # plus one so we can write t=0 to file

    # Create HDF5 particles dataset; collective in MPI
    fname = output_directory + "//particles.h5"
    dset_kwargs = {}
    if "hdf5_dataset_kwargs" in settings.keys():
        dset_kwargs = settings["hdf5_dataset_kwargs"]
    parts_h5 = particles.create_hdf5(
        n_prints, globalnparts, fname=fname, comm=comm, **dset_kwargs
    )

    if comm is not None:
        comm.Barrier()

    # Write initial conditions to file
    particles.write_hdf5(parts_h5, 0, start, end, starttime, rank)

    if comm is not None:
        comm.Barrier()

    if master:
        if size > 1:
            s = f"Simulating {globalnparts} particles, {npart} on each rank"
        else:
            s = f"Simulating {globalnparts} particles"
        print(s, flush=True)
        print(f"Particle class: {type(particles).__name__}", flush=True)
        if track3d:
            print("Velocity field will be interpolated from 3D grid", flush=True)
        else:
            print("Velocity field will be interpolated from 2D grid", flush=True)
        print(
            f"Simulation start time is {starttime}, maximum end time is {endtime}, using timesteps of {dt} (all in seconds).",
            flush=True,
        )

    t0 = timer()

    for i in range(n_times):
        particles.move(times[i], dt)

        # Check that there are still active particles
        if particles.in_bounds_mask is not None:
            if ~np.any(particles.in_bounds_mask):
                if comm is None:
                    print(
                        f"No active particles remain; exiting loop at time T={times[i]}",
                        flush=True,
                    )
                else:
                    print(
                        f"No active particles remain on processor {rank}; exiting local loop at T={times[i]}",
                        flush=True,
                    )
                break

        # Write to HDF5
        tidx = np.searchsorted(print_times, times[i])
        if print_times[tidx] == times[i]:
            particles.write_hdf5(
                parts_h5, np.int32(i / print_inc) + 1, start, end, times[i], rank
            )

            if master:
                e = timer() - t0
                elapsed = str(timedelta(seconds=e))

                if i == 0:
                    print(
                        f"Remaining time steps {n_times - i - 1}/{n_times} || Elapsed Time: {elapsed} h:m:s",
                        flush=True,
                    )
                else:
                    time_per_time = np.float64(e / i)
                    eta = str(timedelta(seconds=((n_times - i) * time_per_time)))
                    print(
                        f"Remaining time steps {n_times - i - 1}/{n_times} || Elapsed Time: {elapsed} h:m:s || ETA {eta} h:m:s",
                        flush=True,
                    )

    if comm is not None:
        comm.Barrier()

    # COLLECTIVE file close
    parts_h5.close()

    if master:
        particles.create_hdf5_xdmf(output_directory, n_prints, globalnparts)
        print(
            f"Finished simulation in {str(timedelta(seconds=timer() - t0))} h:m:s",
            flush=True,
        )

    if master and postprocessflg:
        print("Post-processing...")
        river.postprocess(output_directory, n_prints, globalnparts, **dset_kwargs)

    if comm is not None:
        comm.Barrier()

    if master:
        print(f"Finished in {str(timedelta(seconds=timer()-t0))} h:m:s", flush=True)


def track_serial():
    """Run fluvial particle in serial."""
    argdict = checkcommandarguments()
    settings_file = argdict["settings_file"]
    options = Settings.read(settings_file)

    simulate(options, argdict, timer=time.time)


def track_mpi():
    """Run fluvial particle in parallel."""
    from mpi4py import MPI

    comm = MPI.COMM_WORLD

    argdict = checkcommandarguments()
    settings_file = argdict["settings_file"]
    seed = argdict["seed"]
    if seed is not None:
        print("Warning: user-input seed ignored in parallel execution mode.")
        argdict["seed"] = None
    options = Settings.read(settings_file)

    simulate(options, argdict, timer=MPI.Wtime, comm=comm)
