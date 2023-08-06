#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
from multiprocessing.dummy import Pool as ThreadPool
from os import cpu_count, path
from random import choices
from subprocess import Popen, PIPE

from mirmag.logger import get_logger
from mirmag.stemloop import is_hairpin


logger = get_logger(logger_name="garna", log_to_console=False)  # because of the multiprocessing calculation


# Energy calculation constants
MAX_ENERGY = +1E+100                        # Unreal energy (+1E+100)
MAX_SEQ_LENGTH = 512                        # Maximum limit of the sequence length for the GArna program (512nt)
WIN32_GARNA_FILE = r"software/GArna.exe"    # Full path to execute GArna file for Windows
LINUX_GARNA_FILE = r"software/GArna"        # Full path to execute GArna file for Linux


def get_garna_structure(sequence: str, rand_value: int, constraint: int) -> (str, str, float):
    """ Run GArna program with parameters and return its calculations as a result (sequence, structure and energy).

    :param sequence: RNA sequence to calculate its structure.
    :param rand_value: Random integer number (to use in the GArna genetic algorithm as the beginning state).
    :param constraint: 1 (forcibly forming the stem-loop structure) or 0 (calculate structure as is).
    :return: tuple(sequence, structure_in_the_dot_bracket_notation, energy) or tuple("", "", MAX_ENERGY).
    """

    if not sequence:
        logger.error(f"Calculation was requested for empty/none sequence. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY

    if not rand_value:
        logger.error(f"Calculation was requested for empty/none rand_value. Rand_value: {rand_value}.")
        return "", "", MAX_ENERGY

    if constraint is None:
        logger.critical(f"Calculation was requested for empty/none constraint. Constraint: '{constraint}'.")
        return "", "", MAX_ENERGY

    if platform.system() == "Linux":
        if not path.exists(LINUX_GARNA_FILE):
            program = path.join(path.dirname(path.abspath(mirmag.__file__)), "software", "GArna")
        else:
            program = LINUX_GARNA_FILE

    elif platform.system() == "Windows":
        if not path.exists(WIN32_GARNA_FILE):
            program = path.join(path.dirname(path.abspath(mirmag.__file__)), "software", "GArna.exe")
        else:
            program = WIN32_GARNA_FILE

    else:
        logger.error(f"Calculation was requested under unknown platform. Platform: '{platform.system()}'.")
        return "", "", MAX_ENERGY

    try:
        cmd = [program, sequence, str(rand_value), str(constraint)]
        output, errors = Popen(cmd, stdout=PIPE).communicate()
        energy, structure = output.decode("UTF-8").split("***")         # GArna returns string like "Energy***Structure"
        return sequence, structure, float(energy)

    except Exception:
        logger.exception(f"Error while calculate the GArna structure. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY


def get_simple_stemloop(sequence: str, repeats: int, parallelize: bool = True) -> (str, str, float):
    """ Calculate repeats times the structures with and without constrains, choose the stemloop with the best energy.
        If the predicted final structure is not a hairpin - return tuple("", "", MAX_ENERGY).
        If the sequence length more than MAX_SEQ_LENGTH - return tuple("", "", MAX_ENERGY).

    :param sequence: RNA sequence to calculate its structure.
    :param repeats: Number of repeats' calculations.
    :param parallelize: True (use ThreadPool method) or False (don't use it through the calculation).
    :return: tuple(sequence, structure_in_the_dot-bracket_notation, energy) or tuple("", "", MAX_ENERGY).
    """

    if not sequence or len(sequence) > MAX_SEQ_LENGTH:
        logger.error(f"Calculation was requested for empty/none or too long sequence. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY

    if not repeats or not isinstance(repeats, int) or repeats <= 0:
        logger.error(f"Calculation was requested with incorrect number of repeats. Repeats: '{repeats}'.")
        return "", "", MAX_ENERGY

    # Init some random values for the GArna genetic algorithm
    rand_values = choices(range(1, 100), k=repeats)

    # Calculations
    if parallelize:
        try:
            with ThreadPool(cpu_count()) as pool:   # Create a pool of threads equally to the number of the CPU cores
                data = [(sequence, rand_value, constr) for rand_value in rand_values for constr in [0, 1]]
                result = pool.starmap(get_garna_structure, data)
                pool.close()
                pool.join()

        except Exception:
            logger.exception(f"ThreadPool exception occurred. Sequence: '{sequence}'.")
            return "", "", MAX_ENERGY

        # Keep only stem-loop structures
        result = [item for item in result if is_hairpin(item[1])]

    else:
        result = []
        for rand_value in rand_values:
            for constr in [0, 1]:
                try:
                    seq, structure, energy = get_garna_structure(sequence, rand_value, constr)
                    if is_hairpin(structure):
                        result.append((seq, structure, energy))

                except Exception:
                    logger.exception(f"Some error occurred while GArna executes. Sequence: '{sequence}'.")

    # Get the best structure by its minimal energy
    result_sequence = ""
    result_structure = ""
    result_energy = MAX_ENERGY
    for (seq, structure, energy) in result:
        if energy < result_energy:
            result_sequence = seq
            result_structure = structure
            result_energy = energy

    # Get best result
    return result_sequence, result_structure, result_energy


def get_complex_stemloop(sequence: str, length: int, repeats: int, step: int, parallelize: bool = True) -> (str, str, float):
    """ Calculate the structures of the sub-sequences and choose the best one by the stemloop energy.

    :param sequence: RNA sequence to calculate its sub-sequence stemloop structure.
    :param length: Length of the sliding window.
    :param repeats: Number of repeats' calculations for each sub-sequence.
    :param step: Step of the sliding window.
    :param parallelize: True (use ThreadPool method) or False (don't use it through the calculation).
    :return: tuple(sub-sequence, structure_in_the_dot-bracket_notation, energy) or tuple("", "", MAX_ENERGY).
    """

    if not sequence:
        logger.error(f"Calculation was requested for empty/none sequence. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY

    if length is None or not isinstance(length, int) or length <= 0 or length > MAX_SEQ_LENGTH:
        logger.error(f"Calculation was requested with incorrect value of the length. Length: '{length}'.")
        return "", "", MAX_ENERGY

    if not repeats or not isinstance(repeats, int) or repeats <= 0:
        logger.error(f"Calculation was requested with incorrect value of the repeats. Repeats: '{repeats}'.")
        return "", "", MAX_ENERGY

    if not step or not isinstance(step, int) or step <= 0:
        logger.error(f"Calculation was requested with incorrect value of the step. Step: '{step}'.")
        return "", "", MAX_ENERGY

    # Calculate
    stemloop_structure = get_simple_stemloop(sequence[0: length], repeats, parallelize)
    position = int((len(sequence) - length) / step) + 1
    for i in range(1, position):
        temp_stemloop_structure = get_simple_stemloop(sequence[step * i: step * i + length], repeats, parallelize)
        if temp_stemloop_structure[2] < stemloop_structure[2]:
            stemloop_structure = temp_stemloop_structure[:]

    # Get result
    return stemloop_structure


if __name__ == "__main__":
    """ Examples / Use cases. """

    print("result:", get_garna_structure("ACUACUUACUACUACGACGGAGCGACUACUUAC", rand_value=123, constraint=0))
    print("result:", get_simple_stemloop("acguacguagcuagcuagcuagcuagcuagcuacguagc", 5, True))
    print("result:", get_complex_stemloop("ACGUACGUACGACGUACGUACGUACGACGUACGUACGUACGACGUACGUACACGACGU", 20, 1, 5, True))
