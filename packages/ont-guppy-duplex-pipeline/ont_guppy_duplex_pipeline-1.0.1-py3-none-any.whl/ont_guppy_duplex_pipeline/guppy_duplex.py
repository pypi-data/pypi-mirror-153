"""Performs the sequence of processes required for duplex basecalling with Guppy"""
import argparse
import logging
from pathlib import Path
import platform
import shutil
import sys
import subprocess
import sys

import pandas

from .channel_neighbours import find_neighbours
from .candidate_filtering import filter_candidates_to_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("guppy_duplex")

def _find_exe(exe_path: Path, exe_name):
    if exe_path is None:
        # If the exe path is not provided, we assume it's on the path already
        exe_path = Path(exe_name)
        system_name = platform.system()
        if "Windows" in system_name:
            exe_path = exe_path.with_suffix('.exe')

    if shutil.which(str(exe_path)) is None:
        logger.error("cannot find exe " + exe_name + " at " + str(exe_path))
        sys.exit(1)
    else :
        logger.info("Using " + exe_name + " at " + str(exe_path))

    return exe_path


def _check_paths(input_path: Path, save_path: Path) -> None:
    #pylint: disable=unused-argument
    if not input_path.exists():
        logger.error(f"cannot find input_path {str(input_path)}")
        sys.exit(1)


def _construct_simplex_basecall_args(basecaller_exe: Path,
                                     input_path: Path, recursive: bool, save_path: Path,
                                     do_read_splitting: bool,
                                     device: str) -> list:
    basecall_args = [str(basecaller_exe),
                     "--input_path", str(input_path),
                     "--save_path", str(Path.joinpath(save_path, "simplex")),
                     "-x", device,
                     "--config", "dna_r10.4_e8.1_fast.cfg"]
    if do_read_splitting:
        basecall_args += ["--do_read_splitting"]
    if recursive:
        basecall_args += ["-r"]

    return basecall_args


def _construct_duplex_basecall_args(basecaller_exe: Path,
                                    input_path: Path, recursive: bool, save_path: Path,
                                    device: str, chunks_per_runner: int) -> list:
    basecall_args = [str(basecaller_exe),
                     "--input_path", str(input_path),
                     "--save_path", str(Path.joinpath(save_path, "final/duplex")),
                     "-x", device,
                     "--config", "dna_r10.4_e8.1_sup.cfg",
                     "--duplex_pairing_mode", "from_pair_list",
                     "--duplex_pairing_file", str(Path.joinpath(save_path, "final_pairs.txt"))]
    if chunks_per_runner is not None:
        basecall_args += ["--chunks_per_runner", str(chunks_per_runner)]
    if recursive:
        basecall_args += ["-r"]

    return basecall_args


def _construct_suplex_basecall_args(basecaller_exe: Path,
                                    input_path: Path, recursive: bool, save_path: Path,
                                    device: str) -> list:
    basecall_args = [str(basecaller_exe),
                     "--input_path", str(input_path),
                     "--save_path", str(Path.joinpath(save_path, "final/simplex")),
                     "-x", device,
                     "--config", "dna_r10.4_e8.1_sup.cfg",
                     "--read_id_list", str(Path.joinpath(save_path, "whitelist.txt"))]
    if recursive:
        basecall_args += ["-r"]

    return basecall_args


def _simplex_basecall(basecaller_exe: Path, input_path: Path, recursive: bool, save_path: Path,
                      do_read_splitting: bool, device: str) -> int:
    logger.info("\n*********************************\n"
                  "* Fast Pairing Simplex Basecall *\n"
                  "*********************************\n")

    basecall_args = _construct_simplex_basecall_args(basecaller_exe,
                                                     input_path, recursive, save_path,
                                                     do_read_splitting, device)
    logger.info("launching simplex basecaller: " + ' '.join(basecall_args))

    process = subprocess.run(basecall_args, check=False)

    if process.returncode == 0:
        logger.info("simplex basecall returned success")
    else:
        logger.error("simplex basecall returned error")

    return process.returncode


def _duplex_basecall(duplex_basecaller_exe: Path, input_path: Path, recursive: bool, save_path:
                     Path, device: str, chunks_per_runner: int) -> int:
    
    logger.info("\n*******************\n"
                  "* Duplex Basecall *\n"
                  "*******************\n")
    
    basecall_args = _construct_duplex_basecall_args(duplex_basecaller_exe, input_path,
                                                    recursive, save_path, device, chunks_per_runner)
    logger.info("launching duplex basecaller: " + ' '.join(basecall_args))

    process = subprocess.run(basecall_args, check=False)

    if process.returncode == 0:
        logger.info("duplex basecall returned success")
    else:
        logger.error("duplex basecall returned error")

    return process.returncode


def _suplex_basecall(basecaller_exe: Path, input_path: Path, recursive: bool, save_path: Path,
                     pairing_summary, device: str) -> int:

    logger.info("\n************************\n"
                  "* SUP Simplex Basecall *\n"
                  "************************\n")

    # Generate a whitelist file containing only read ids that are not in a duplex pair.
    pairing_file = str(Path.joinpath(save_path, "final_pairs.txt"))
    duplex_pairs  = pandas.read_csv(pairing_file, sep=" ", header=None)
    all_read_ids = pairing_summary["read_id"]
    temp_read_ids = list(duplex_pairs[0])
    comp_read_ids = list(duplex_pairs[1])
    simplex_read_ids = all_read_ids[~all_read_ids.isin(temp_read_ids)]
    simplex_read_ids = simplex_read_ids[~simplex_read_ids.isin(comp_read_ids)]
    simplex_read_ids.to_csv(Path.joinpath(save_path, "whitelist.txt"), index=False, header=False)
    
    basecall_args = _construct_suplex_basecall_args(basecaller_exe, input_path, recursive,
                                                    save_path, device)
    logger.info("launching simplex basecaller: " + ' '.join(basecall_args))

    process = subprocess.run(basecall_args, check=False)

    if process.returncode == 0:
        logger.info("simplex basecall returned success")
    else:
        logger.error("simplex basecall returned error")

    return process.returncode


def _build_pairs_file(save_path: Path, split_reads: bool) :
    simplex_summary_file = Path.joinpath(save_path, "simplex/sequencing_summary.txt")
    if not simplex_summary_file.exists() :
        logger.error("Simplex basecall did not produce valid sequencing summary file")
        sys.exit(1)

    neighbours, simplex_summary = find_neighbours(simplex_summary_file, logger, split_reads=split_reads)

    # Note - we're not filtering on pass or fail folder at the moment
    sequence_file_path = Path.joinpath(save_path, "simplex")
    filter_candidates_to_file(neighbours, sequence_file_path, logger, split_reads=split_reads)

    return simplex_summary


def duplex_pipeline(basecaller_exe: Path, duplex_basecaller_exe: Path, input_path: Path, save_path: Path,
                    disable_logging: bool, skip_simplex: bool, skip_duplex: bool, call_non_duplex_reads: bool,
                    device: str, split_reads: bool, duplex_chunks_per_runner: int, recursive: bool) -> None:
    """Main pipeline function"""

    if disable_logging:
        logging.disable()

    # Set defaults for optional parameters
    basecaller_exe = _find_exe(basecaller_exe, "guppy_basecaller")
    duplex_basecaller_exe = _find_exe(duplex_basecaller_exe, "guppy_basecaller_duplex")

    # Parameter validation
    _check_paths(input_path, save_path)

    # Simple basecall the input folder.
    if not skip_simplex:
        returncode = _simplex_basecall(basecaller_exe, input_path, recursive, save_path, split_reads, device)
        if returncode != 0:
            sys.exit(returncode)

    # Pairing
    simplex_summary = _build_pairs_file(save_path, split_reads)

    # Duplex basecall the pairs
    if not skip_duplex:
        returncode = _duplex_basecall(duplex_basecaller_exe, input_path,
                                      recursive, save_path, device, duplex_chunks_per_runner)
        if returncode != 0:
            sys.exit(returncode)

    if call_non_duplex_reads:
        returncode = _suplex_basecall(basecaller_exe, input_path, recursive, save_path,
                                      simplex_summary, device)
        if returncode != 0:
            sys.exit(returncode)


def main():
    parser = argparse.ArgumentParser(
        description="All-in-one processing of r10.4 duplex reads using guppy")
    parser.add_argument("--basecaller_exe",
                        help="Path to the guppy_basecaller executable. If "
                        "unspecified it is assumed that the basecaller exe is in the path.",
                        default=None,
                        type=Path)
    parser.add_argument("--duplex_basecaller_exe",
                        help="Path to the guppy_basecaller_duplex executable. If "
                        "unspecified it is assumed that the duplex basecaller exe is in the path.",
                        default=None,
                        type=Path)
    parser.add_argument("--input_path", "-i",
                        help="Directory to read fast5 input files from.",
                        default=None,
                        type=Path,
                        required=True)
    parser.add_argument("--save_path", "-s",
                        help="Directory to write resulting sequence files to.",
                        default=None,
                        type=Path,
                        required=True)
    parser.add_argument("--disable_logging",
                        help="Turn off logging.",
                        action="store_true")
    parser.add_argument("--skip_simplex",
                        help="Skip simplex basecall step (the pipeline will assume "
                        "the sequencing_summary.txt file exists ).",
                        action="store_true")
    parser.add_argument("--skip_duplex",
                        help="Skip duplex basecall step.",
                        action="store_true")
    parser.add_argument("--call_non_duplex_reads",
                        help="Perform high accuracy basecall of all reads which do not "
                        "participate in a duplex pair.",
                        action="store_true")
    parser.add_argument("--device", "-d",
                        help="CUDA device string to pass to basecallers.",
                        default="cuda:0")
    parser.add_argument("--do_read_splitting",
                        help="Perform read-splitting during the simplex basecall step.",
                        action="store_true")
    parser.add_argument("--duplex_chunks_per_runner",
                        help="--chunks_per_runner value to pass to guppy when "
                        "performing duplex basecalling. Decrease "
                        "this if guppy gives an out-of-memory error.",
                        default=None)
    parser.add_argument("--recursive", "-r",
                        help="Search for input files recursively.",
                        action="store_true")
    args = parser.parse_args()

    duplex_pipeline(args.basecaller_exe, args.duplex_basecaller_exe, args.input_path, args.save_path,
                    args.disable_logging, args.skip_simplex, args.skip_duplex, args.call_non_duplex_reads,
                    args.device, args.do_read_splitting, args.duplex_chunks_per_runner, args.recursive)


if __name__ == "__main__":
    main()
