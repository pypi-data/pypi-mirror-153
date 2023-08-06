#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import os

from Bio import pairwise2
from Bio.pairwise2 import format_alignment

from mirmag.logger import get_logger
from mirmag.mirna import MiRNA
from mirmag.stemloop import Hairpin5, Hairpin3, HairpinDB


logger = get_logger(logger_name="utils", log_to_console=True)


def get_gc_score(sequence: str) -> float:
    """ Calculate GC-score of RNA or DNA sequence.
        The calculation is case-insensitive.

    :param sequence: The RNA or DNA sequence.
    :return: The GC-score (ratio) of the sequence. Return -1.0 if the sequence is empty or None.
    """

    if not sequence:
        logger.error(f"GC-score was requested for empty sequence or None object. Sequence:'{sequence}'.")
        return -1.0
    else:
        gc_count = sequence.count("G") + sequence.count("g") + sequence.count("C") + sequence.count("c")
        return gc_count / len(sequence)


def get_ga_score(sequence: str) -> float:
    """ Calculate GA-score of RNA or DNA sequence.
        The calculation is case-insensitive.

    :param sequence: The RNA or DNA sequence.
    :return: The GA-score (ratio) of the sequence. Return -1.0 if the sequence is empty or None.
    """

    if not sequence:
        logger.error(f"GA-score was requested for empty sequence or None object. Sequence:'{sequence}'.")
        return -1.0
    else:
        ga_count = sequence.count("G") + sequence.count("g") + sequence.count("A") + sequence.count("a")
        return ga_count / len(sequence)


def get_fasta_sequences(file_name: str) -> dict:
    """ Read data from [correct] fasta file and return a dictionary of pairs id:sequence.
        The identifiers (or headers, or ids) will be stripped of the '>' begin symbol.

    :param file_name: The name of the fasta file (including full path).
    :return: The dictionary of pairs id:sequence.
    """

    try:
        # Try to read all fasta file to a variable. Strip ends of the lines. Method may be slow!
        with open(file_name, "r") as file:
            data = [line.strip() for line in file.readlines()]
    except Exception:
        logger.exception(f"Exception while read the fasta file: '{file_name}'.")
        return {}

    # Add custom begin string (^#^) and end string (^*^) to all identifiers, strip ">" symbols
    for index, value in enumerate(data):
        if value.startswith(">"):
            data[index] = "^#^" + value.strip(">") + "^*^"

    # Join data into one sequence (^#^id_1^*^CCAAGGUU^#^id_2^*^GGCCAAUU)
    full_sequence = "".join(data)

    # Remove first symbols (^#^) and split sequence to a list of pairs (id^*^seq)
    pairs = full_sequence[3:].split("^#^")

    # Convert the pairs into result dictionary
    result = {}
    for pair in pairs:
        key, sequence = pair.split("^*^")
        result[key] = sequence

    return result


def get_hairpin5_objects(file_name: str) -> dict:
    """ Read data from [correct] miRNA.str file of the miRBase and return a dictionary of pairs id:Hairpin5.

    :param file_name: The name of the *.str file of the miRBase (including full path).
    :return: The dictionary of pairs id:Hairpin5.
    """

    try:
        # Try to read all file lines to one variable. Strip '\n'-ends of the lines. Method may be slow!
        with open(file_name, "r") as file:
            data = [line.strip("\n") for line in file.readlines()]
    except Exception:
        logger.exception(f"Exception while read the data file: '{file_name}'.")
        return {}

    try:
        # Parse the data to the Hairpin5 structures
        headers = data[0::8]
        s1s = data[2::8]
        s2s = data[3::8]
        s3s = data[4::8]
        s4s = data[5::8]
        s5s = data[6::8]
        #
        hp5_dict = dict()
        for header, s1, s2, s3, s4, s5 in zip(headers, s1s, s2s, s3s, s4s, s5s):
            hp5_dict[header] = Hairpin5(header=header, s1=s1, s2=s2, s3=s3, s4=s4, s5=s5)
        #
        return hp5_dict

    except Exception:
        logger.exception(f"Exception while convert the data to the Hairpin5 structures: '{file_name}'.")
        return {}


def get_hairpin3_objects(file_name: str) -> dict:
    """ Read data from [correct] file of the Hairpin3 objects and return a dictionary of pairs id:Hairpin3.

    :param file_name: The name of the file with the Hairpin3 data (including full path).
    :return: The dictionary of pairs id:Hairpin3.
    """

    try:
        # Try to read all file lines to one variable. Strip '\n'-ends of the lines. Method may be slow!
        with open(file_name, "r") as file:
            data = [line.strip("\n") for line in file.readlines()]
    except Exception:
        logger.exception(f"Exception while read the data file: '{file_name}'.")
        return {}

    try:
        # Parse the data to the Hairpin3 structures
        headers = data[0::4]
        p5s = data[1::4]
        sts = data[2::4]
        p3s = data[3::4]
        #
        hp3_dict = dict()
        for header, p5, st, p3 in zip(headers, p5s, sts, p3s):
            hp3_dict[header] = Hairpin3(header=header, p5=p5, st=st, p3=p3)
        #
        return hp3_dict

    except Exception:
        logger.exception(f"Exception while convert the data to the Hairpin3 structures: '{file_name}'.")
        return {}


def get_hairpindb_objects(file_name: str) -> dict:
    """ Read data from [correct] file of the HairpinDB objects and return a dictionary of pairs id:HairpinDB.

    :param file_name: The name of the file with the HairpinDB data (including full path).
    :return: The dictionary of pairs id:HairpinDB.
    """

    try:
        # Try to read all file lines to one variable. Strip '\n'-ends of the lines. Method may be slow!
        with open(file_name, "r") as file:
            data = [line.strip("\n") for line in file.readlines()]
    except Exception:
        logger.exception(f"Exception while read the data file: '{file_name}'.")
        return {}

    try:
        # Parse the data to the HairpinDB structures
        headers = data[0::3]
        sequences = data[1::3]
        structures = data[2::3]
        #
        hpdb_dict = dict()
        for header, sequence, structure in zip(headers, sequences, structures):
            hpdb_dict[header] = HairpinDB(header=header, sequence=sequence, structure=structure)
        #
        return hpdb_dict

    except Exception:
        logger.exception(f"Exception while convert the data to the HairpinDB structures: '{file_name}'.")
        return {}


def are_complementary(first_sequence: str, second_sequence: str, allow_gu_pairs: bool = True) -> bool:
    """ Check full complementary of two nucleotide sequences.
        Pairs G:C and A:U are always complementary.
        The pair G:U is considered as complementary only if @allow_gu_pairs was set as True.
        Calculation considers the maximum length of the sequences (missing letters are filled by X).
        The calculation is case-insensitive.

    :param first_sequence: The first nucleotide sequence.
    :param second_sequence: The second nucleotide sequence.
    :param allow_gu_pairs: True (consider G:U pair as complementary pair), False (does not consider).
    :return: True (sequences are full complementary) or False (they are not).
    """

    # Check passed data
    if not first_sequence or not second_sequence:
        logger.error(f"Complementarity was requested for empty sequence(s) or for None object(s).")
        logger.error(f"First sequence: '{first_sequence}', second sequence: '{second_sequence}'.")
        return False

    # Prepare input data to uniform view
    first_sequence = first_sequence.upper().replace("T", "U")
    second_sequence = second_sequence.upper().replace("T", "U")

    # Form verification rules
    rules_list = [("G", "C"), ("C", "G"), ("A", "U"), ("U", "A")]
    if allow_gu_pairs:
        rules_list.extend([("G", "U"), ("U", "G")])

    # Check complementarity
    for (x, y) in itertools.zip_longest(first_sequence, second_sequence, fillvalue="X"):
        if (x, y) not in rules_list:
            return False
    #
    return True


def get_hamming_distance(first_sequence: str, second_sequence: str, case_sensitive: bool = True) -> int:
    """ Return Hamming distance of two EQUAL sequences.
        The Hamming distance between two strings of equal length is the number of positions at which
        the corresponding symbols are different. Calculation may be case-sensitive or insensitive!

     :param first_sequence: The first sequence.
     :param second_sequence: The second sequence.
     :param case_sensitive: True (calculation is case-sensitive) or False (calculation is case-insensitive).
     :return: The Hamming distance or -1 in case of errors.
     """

    # Check passed data
    if not first_sequence or not second_sequence:
        logger.error(f"Hamming distance was requested for empty sequence(s) or for None object(s).")
        logger.error(f"First sequence: '{first_sequence}', second sequence: '{second_sequence}'.")
        return -1

    if len(first_sequence) != len(second_sequence):
        logger.error(f"Hamming distance was requested for sequences with different lengths.")
        logger.error(f"First sequence: '{first_sequence}', second sequence: '{second_sequence}'.")
        return -1

    # Convert sequences
    if not case_sensitive:
        first_sequence = first_sequence.upper()
        second_sequence = second_sequence.upper()

    # Result
    return sum([a != b for (a, b) in zip(first_sequence, second_sequence)])


def get_alignments(first_sequence: str, second_sequence: str, alignment_type: str, case_sensitive: bool = True,
                   match: float = 5.0, mismatch: float = -4.0, gap_open: float = -10.0, gap_extend: float = -0.5):
    """ Calculate "global" (Needleman-Wunsch) or "local" (Smith–Waterman) alignments for two nucleotide sequences.
        Default parameters according to http://www.ebi.ac.uk/Tools/psa/emboss_water/nucleotide.html
        Alignments may be case-sensitive or case-insensitive!

    :param first_sequence: The first [nucleotide] sequence.
    :param second_sequence: The second [nucleotide] sequence.
    :param alignment_type: The type of the alignment - string "global" or "local".
    :param case_sensitive: True (alignment is case-sensitive) or False (alignment is case-insensitive).
    :param match: The match score.
    :param mismatch: The mismatch score.
    :param gap_open: The score of the gap opening.
    :param gap_extend: The score of the gap extending.
    :return: The alignments of two sequences (in BioPython/pairwise2/align format), or None in case of errors.
    """

    # Check passed data
    if not first_sequence or not second_sequence or not alignment_type:
        logger.error(f"Alignment was requested without necessary parameters (strings are empty or None).")
        logger.error(f"First sequence: '{first_sequence}', second sequence: '{second_sequence}'.")
        logger.error(f"Alignment type: '{alignment_type}'.")
        return None

    # Convert sequences
    if not case_sensitive:
        first_sequence = first_sequence.upper()
        second_sequence = second_sequence.upper()

    # Calculate
    alignments = None
    if alignment_type.lower() == "local":
        alignments = pairwise2.align.localms(first_sequence, second_sequence, match, mismatch, gap_open, gap_extend)
    elif alignment_type.lower() == "global":
        alignments = pairwise2.align.globalms(first_sequence, second_sequence, match, mismatch, gap_open, gap_extend)
    else:
        logger.error(f"Incorrect type of the alignment: '{alignment_type}'.")

    # Result
    return alignments


def get_rcbp_sequence(sequence: str, convert_u: bool = True) -> str:
    """ Get reverse complementary base pairing sequence of the given DNA sequence.
        5'-ACGUT-3' -->> 5'-AACGT-3'

    :param sequence: DNA sequence.
    :param convert_u: True (convert U-symbol to A), False (do not).
    :return: Reverse complementary base pairing sequence or empty string in case of errors.
    """

    if not sequence:
        logger.error(f"RCBP-function was requested for empty sequence or for None object. Sequence: '{sequence}'.")
        return ""

    replace_rule = {"A": "T", "a": "t", "T": "A", "t": "a", "C": "G", "c": "g", "G": "C", "g": "c"}
    if convert_u:
        replace_rule.update({"U": "A", "u": "a"})

    return "".join(map(lambda x: replace_rule.get(x, x), sequence))[::-1]


def join_files(input_files: list, output: str) -> None:
    """ Join data from many files into the one.

    :param input_files: The list of the names of the input files (including full paths).
    :param output: Output file name with data from the input files.
    :return: None.
    """

    try:
        with open(output, "w") as output_f:
            for input_file in input_files:
                with open(input_file) as input_f:
                    for line in input_f:
                        output_f.write(line)
    except Exception:
        logger.exception(f"Error while join the files. Input files: {input_files}, output file: {output}")


def get_unique_mirnas_list(input_file: str) -> list:
    """ Form list of unique miRNAs with compact /short/ grouped header.
        The headers will be without any ">" symbols! and contain only title and accession.

    :param input_file: Input fasta file with the miRNA (or any others) sequences.
    :return: List of tuples like (miRNA_header|miRNA_header|..., miRNA_sequence) with grouped unique miRNA sequences.
    """

    all_mirnas = get_fasta_sequences(input_file)
    all_mirnas = [MiRNA(header=key, sequence=value) for (key, value) in all_mirnas.items()]
    all_mirnas = {f"{mirna.get_title()} {mirna.get_accession()}".strip(): mirna.get_sequence() for mirna in all_mirnas}

    unique_mirnas = dict()
    for key_all in all_mirnas.keys():

        is_presented = False

        for key_uniq in unique_mirnas:
            if all_mirnas[key_all] == unique_mirnas[key_uniq]:
                unique_mirnas[f"{key_uniq}|{key_all}"] = all_mirnas[key_all]
                del unique_mirnas[key_uniq]
                is_presented = True
                break

        if not is_presented:
            unique_mirnas[key_all] = all_mirnas[key_all]

    return list(unique_mirnas.items())


def split_mirnas_to_files(mirnas: list, output_dir: str, count: int = 1000, file_patter: str = "mirnas_part"):
    """ Split miRNAs from list to several small fasta-files. By default, miRNAs are divided by 1000 sequences per file.
        The header of the input miRNAs does not contain the symbol ">".

    :param mirnas: List of the tuples like (miRNA_header, miRNA_sequence).
    :param output_dir: Directory to save the fasta-files with miRNAs.
    :param count: The number of the miRNAs per one file.
    :param file_patter: The pattern of the name of the created files.
    :return: None.
    """

    os.makedirs(output_dir, exist_ok=True)

    total = len(mirnas) // count
    if len(mirnas) % count:
        total += 1

    for index in range(0, total):
        file_name = os.path.join(output_dir, f"{file_patter}{index}.fa")
        with open(file_name, "w") as file:
            for mirna in mirnas[index * count: (index + 1) * count]:
                file.write(f">{mirna[0]}\n{mirna[1]}\n")

    return True


if __name__ == "__main__":
    """ Examples / Use cases. """

    gc_score = get_gc_score("ACGUTtugca")
    print(f"GC-score: {gc_score}")

    ga_score = get_ga_score("ACGUTtugca")
    print(f"GA-score: {ga_score}")

    fasta_data = get_fasta_sequences(file_name=r"datasets/miRBase/rel.22.1/mature.fa")
    print(f"Length of the data from fasta file: {len(fasta_data)}")

    hp5_dict = get_hairpin5_objects(file_name=r"datasets/miRBase/rel.22.1/miRNA.str")
    print(f"Length of the data from Hairpin5 file: {len(hp5_dict)}")

    hp3_dict = get_hairpin3_objects(file_name=r"")      # TODO : insert real filename
    print(f"Length of the data from Hairpin3 file: {len(hp3_dict)}")

    hpdb_dict = get_hairpindb_objects(file_name=r"")    # TODO : insert real filename
    print(f"Length of the data from HairpinDB file: {len(hpdb_dict)}")

    print("ACGUTacgutACGUT and UGCAAugcaaUGCAA are complementary?", end="\t")
    print(are_complementary("ACGUTacgutACGUT", "UGCAAugcaaUGCAA"))

    print("Hamming distance of ACGUT and AC-Ut: ", get_hamming_distance("ACGUT", "AC-Ut"))
    print("Hamming distance of ACGUT and ACUt: ", get_hamming_distance("ACGUT", "ACUt", case_sensitive=False))

    alignments = get_alignments("UGGGCGAGGGCGGCUGAGCGGC", "UGGGGGAGAUGGGGGUUGA", "local")
    print("First example of alignments:", alignments)
    for alignment in alignments:
        print(format_alignment(*alignment))

    alignments = get_alignments("acgut", "ACGUT", "global", case_sensitive=False)  # Case-insensitive
    print("Second example of alignments:", alignments)
    for alignment in alignments:
        print(format_alignment(*alignment))

    alignments = get_alignments("acgut", "ACGUT", "global", True)  # Case sensitive
    print("Third example of alignments:", alignments)
    for alignment in alignments:
        print(format_alignment(*alignment))

    sequence = "ACGUTACGUT"
    rcbp_seq = get_rcbp_sequence(sequence)
    print(f"Reverse complementary base pairing sequence of {sequence}: {rcbp_seq}")

    join_files(input_files=["1.txt", "2.txt"], output="3.txt")

    unique_mirnas = get_unique_mirnas_list(r"datasets/miRBase/rel.22.1/mature.fa")
    print(f"Number of unique miRNAs: {len(unique_mirnas)}")

    split_mirnas_to_files(unique_mirnas, "temp")
