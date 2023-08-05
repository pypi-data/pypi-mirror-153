"""Utilities to find all the neighbouring strands from a dataset, given the simplex sequencing summary file."""

from pathlib import Path
import time
import pandas

def find_neighbours(simplex_summary_file: Path, logger, max_time_between_reads: float = 20,
                    max_seqlen_diff: float = 0.1, split_reads: bool = False) :
    """Find neighbouring reads from each channel in the provided simplex summary.
    
    Keyword arguments:
    simplex_summary_file -- path to a simplex summary file from guppy to parse
    logger -- Logging object to direct output to
    max_time_between_reads -- The maximum allowable time gap between two neighbours (in seconds)
    max_seqlen_diff -- The maximum allowable difference in sequence length between neighbours,
        expressed as a factor of the longer pair's length.

    :returns: pair list, plus annotated sequencing summary frame.
    """
    start_time = time.time()

    dtype = {
        "read_id": str,
        "run_id": str,
        "start_time": float,
        "duration": float,
        "channel": int, "mux": int,
        "sequence_length_template": int}

    if split_reads:
        dtype["parent_read_id"] = str

    required_columns = dtype.keys()

    simplex_summary = pandas.read_csv(simplex_summary_file, sep="\t",
        dtype=dtype, usecols=lambda x: x in required_columns)

    logger.info(f"{simplex_summary.shape[0]} reads loaded from simplex summary file")

    simplex_summary.sort_values(["run_id", "channel", "mux", "start_time"], inplace=True)

    if split_reads:
        simplex_summary["parent_read_id_next"] = simplex_summary["parent_read_id"].shift(-1)
        simplex_summary["duration_next"] = simplex_summary["duration"].shift(-1)
    simplex_summary["run_id_next"] = simplex_summary["run_id"].shift(-1)
    simplex_summary["channel_next"] = simplex_summary["channel"].shift(-1)
    simplex_summary["mux_next"] = simplex_summary["mux"].shift(-1)
    simplex_summary["read_id_next"] = simplex_summary["read_id"].shift(-1)
    simplex_summary["start_time_next"] = simplex_summary["start_time"].shift(-1)
    simplex_summary["sequence_length_template_next"] = simplex_summary["sequence_length_template"].shift(-1)
    end_times = simplex_summary["start_time"] + simplex_summary["duration"]

    base_count_differences = (simplex_summary["sequence_length_template_next"] - simplex_summary["sequence_length_template"]).abs()
    max_base_counts = simplex_summary[["sequence_length_template_next", "sequence_length_template"]].max(axis=1)
    simplex_summary["fraction_missing_from_longest"] = base_count_differences / max_base_counts
    simplex_summary["time_gap_until_next_strand"] = (simplex_summary["start_time_next"] - end_times)

    # Mark the candidate pairs.  They must be from the same run_id/channel/mux, be close
    # enough in length and not have too long a gap between them
    simplex_summary["candidate_pair"] = (
        (simplex_summary["run_id"] == simplex_summary["run_id_next"])
        & (simplex_summary["channel"] == simplex_summary["channel_next"])
        & (simplex_summary["mux"] == simplex_summary["mux_next"])
        & (simplex_summary["time_gap_until_next_strand"] < max_time_between_reads)
        & (simplex_summary["fraction_missing_from_longest"] < max_seqlen_diff))

    # Select out the positive pairs.
    candidate_pairs = simplex_summary[simplex_summary['candidate_pair']].copy()
    columns = ["read_id","read_id_next"]
    if split_reads:
        columns += ["parent_read_id", "parent_read_id_next", "start_time", "duration", "start_time_next", "duration_next"]
    candidate_pairs = candidate_pairs[columns]
    logger.info("Candidate pair generation took {:.2f} seconds, {} pairs found".format(time.time() - start_time, candidate_pairs.shape[0]))
    return candidate_pairs, simplex_summary

