"""Utilities to filter pre-called neigbouring pairs, by attempting to align the ends of the reads"""

from collections import defaultdict
#import glob
from pathlib import Path
import time
import pandas
import parasail
import pyfastx

base_complements = {
    'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'X': 'X', 'N': 'N',
    'a': 't', 't': 'a', 'c': 'g', 'g': 'c', 'x': 'x', 'n': 'n',
}
comp_trans = str.maketrans(''.join(base_complements.keys()), ''.join(base_complements.values()))


def reverse_complement(seq):
    """Reverse complement sequence.

    Keyword arguments:
    seq -- input sequence string.
    :returns: reverse-complemented string.
    """
    return seq.translate(comp_trans)[::-1]


def filter_candidates_to_file(candidate_pairs: pandas.core.frame.DataFrame,
                              seq_file_folder: Path,
                              logger,
                              bases_to_align: int = 250,
                              align_threshold: float = 0.6,
                              penalty_open: int = 4,
                              penalty_extend: int = 1,
                              score_match: int = 2,
                              score_mismatch: int = -1,
                              split_reads: bool = False) :
    """Filter pre-paired neigbouring reads, by aligning the ends of the reads, to generate a pairs file

    Keyword arguments:
    candidate_pairs -- The pre-paired neigbouring reads
    seq_file_folder -- Folder containing the called reads in candidate_pairs
    logger -- Logging object to direct output to
    bases_to_align -- Length of read-end window to attempt alignment over
    align_threshold -- Miniumum score for alignement to be considered a success.
    penalty_open -- Gap opening option to parasail
    penalty_extend -- Gap extension option to parasail
    score_match -- Match score option to parasail
    score_mismatch -- Mismatch score option to parasail
    """
    start_time = time.time()

    # Load seqs from fastx files
    seq_files = []
    for ext in ("fastq", "fastq.gz", "fq", "fq.gz"):
        seq_files += Path(seq_file_folder).rglob(f"*.{ext}")
        # seq_files += glob.glob(f"{seq_file_folder}/**/*.{ext}", recursive=True)

    temp_read_ids = list(candidate_pairs["read_id"])
    comp_read_ids = list(candidate_pairs["read_id_next"])

    if split_reads:
        temp_start_times = list(candidate_pairs["start_time"])
        comp_start_times = list(candidate_pairs["start_time_next"])
        temp_duration = list(candidate_pairs["duration"])
        comp_duration = list(candidate_pairs["duration_next"])
        temp_parent_read_ids = list(candidate_pairs["parent_read_id"])
        comp_parent_read_ids = list(candidate_pairs["parent_read_id_next"])
    seq_ends = {}

    # Create a set from the template and complement read id lists, so we can search them efficiently
    temp_read_id_set = set(temp_read_ids)
    comp_read_id_set = set(comp_read_ids)
    for file in seq_files:
        # # TODO: progress logging, eg
        # if i % 50 == 0:
        #    logger.info(
        #        "Processed {}/{} input fastq files.".format(i, len(seq_files)))
        fastx = pyfastx.Fastx(str(file))
        for name, sequence, _, _ in fastx:
            if name in temp_read_id_set:
                # store the end of the template strand
                seq_ends[(name, 0)] = str(sequence[-bases_to_align:])
            if name in comp_read_id_set:  # a read can be in both
                # store the RC of the start of the complement strand
                seq_ends[(name, 1)] = reverse_complement(str(sequence[:bases_to_align]))
    found_read_percentage = 100 * (len(seq_ends) / (2 * len(candidate_pairs))) if len(candidate_pairs) != 0 else 100
    logger.info(f"Found {found_read_percentage:.1f}% of required reads.")

    # Now that we have our sequence ends, we can align them
    score_matrix = parasail.matrix_create("ACGT", score_match, score_mismatch)
    stats_counter = defaultdict(int)
    alignment_scores = []

    for i, read_pair in enumerate(zip(temp_read_ids, comp_read_ids)):
        # TODO: add some progress tracking
        #print(item)
        try:
            template_seq = seq_ends[(read_pair[0], 0)]
        except KeyError:
            logger.debug(f"Skipped template {read_pair[0]}: sequence missing.")
            stats_counter["skipped"] += 1
            stats_counter["template missing"] += 1
            continue
        try:
            complement_seq = seq_ends[(read_pair[1], 1)]
        except KeyError:
            logger.debug(f"Skipped complement {read_pair[1]}: sequence missing.")
            stats_counter["skipped"] += 1
            stats_counter["complement missing"] += 1
            continue

        if len(template_seq) == 0 or len(complement_seq) == 0:
            logger.debug(f"Skipped {read_pair}, reads too short.")
            stats_counter["skipped"] += 1
            continue

        # Run a semi-global alignment (sg) with zero end-penalty for seq2 (dx)
        result = parasail.sg_dx_trace_scan_16(template_seq, complement_seq,
                                              penalty_open, penalty_extend,
                                              score_matrix)
        # scale score to read length
        alignment_score = result.score / result.len_ref
        if alignment_score > align_threshold:
            logger.debug(f"\n{read_pair[0]} {read_pair[1]}: {alignment_score}")
            logger.debug(f"\n{template_seq}\n{complement_seq}")

        if split_reads:
            alignment_scores.append((read_pair[0], read_pair[1], alignment_score,
                                     temp_parent_read_ids[i], comp_parent_read_ids[i],
                                     temp_start_times[i], comp_start_times[i],
                                     temp_duration[i], comp_duration[i]))
        else:
            alignment_scores.append((read_pair[0], read_pair[1], alignment_score))
        align_quality = "pass" if alignment_score > align_threshold else "fail"
        stats_counter[align_quality] += 1

    output_columns = ["read_id_temp", "read_id_comp", "score"]
    if split_reads:
        output_columns += ["temp_parent_read_id", "comp_parent_read_id", "start_time_temp", "duration_temp", "start_time_comp", "duration_comp"]

    pair_alignment_scores = pandas.DataFrame(alignment_scores, columns=output_columns)
    logger.debug(stats_counter)

    #pair_alignment_scores.to_csv(
    #   Path(seq_file_folder, f"../read_pair_alignment_scores.csv"), index=False)
    passing_pairs = pair_alignment_scores.query(f"score > {align_threshold}")
    output_columns.remove("score")
    passing_pairs[output_columns].to_csv(
        Path(seq_file_folder, "../final_pairs.txt"),
        index=False, header=False, sep=" ")

    elapsed_time = time.time() - start_time
    logger.info(f"Pair filtering took {elapsed_time:.2f} seconds, "
                f"{passing_pairs.shape[0]} pairs passed")
