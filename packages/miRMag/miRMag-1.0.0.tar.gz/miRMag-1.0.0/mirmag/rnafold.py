#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import time
from os import path, remove
from subprocess import Popen, PIPE, STDOUT

from mirmag.logger import get_logger
from mirmag.stemloop import is_hairpin


logger = get_logger(logger_name="rnafold", log_to_console=True)


# Energy calculation constants
MAX_ENERGY = +1E+100                    # Unreal energy (+1E+100)
MAX_SEQ_LENGTH = 512                    # Maximum limit of the sequence length for the calculation (512 nt)
WIN32_RNAFOLD_FILE = r"RNAfold.exe"     # Full path to the execute RNAfold file for Windows
LINUX_RNAFOLD_FILE = r"rnafold"         # Full path to the execute RNAfold file for Linux


def get_rnafold_structure(sequence: str) -> (str, str, float):
    """ Run RNAfold program and return its calculations as a result tuple of sequence, structure and energy.

    :param sequence: RNA sequence to calculate its structure.
    :return: tuple(sequence, structure_in_the_dot_bracket_notation, energy) or tuple("", "", MAX_ENERGY).
    """

    if not sequence:
        logger.error(f"Calculation was requested for empty/none sequence. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY

    if platform.system() == "Linux":
        program = LINUX_RNAFOLD_FILE
    elif platform.system() == "Windows":
        program = WIN32_RNAFOLD_FILE
    else:
        logger.error(f"Calculation was requested under unknown platform. Platform: '{platform.system()}'.")
        return "", "", MAX_ENERGY

    try:
        # check RNAfold garbage and delete it
        while path.exists("rna.ps"):
            try:
                remove("rna.ps")         # clean the RNAfold garbage
            except Exception:
                logger.exception(f"Can't remove file rna.ps for the sequence '{sequence}'.\nSleep 0.5 seconds.")
                time.sleep(0.5)
        #
        process = Popen(program, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        output, errors = process.communicate(sequence.encode("UTF-8"))
        data = output.decode("UTF-8").replace("\r\n", " ").strip()
        sequence, structure, *energy_part = data.split(" ")
        energy_part = "".join(energy_part).replace("(", "").replace(")", " ").strip(" ")
        energy = float(energy_part)
        #
        try:
            remove("rna.ps")         # try to clean the RNAfold garbage
        except Exception:
            logger.exception(f"Can't remove file rna.ps for the sequence '{sequence}'. Skip it.")
        #
        return sequence, structure, energy

    except Exception:
        logger.exception(f"Error while calculating the RNAfold structure. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY


def get_simple_stemloop(sequence: str) -> (str, str, float):
    """ Calculate the simple stemloop structure.
        If the predicted final structure is not a hairpin - return tuple("", "", MAX_ENERGY).
        If the sequence length more than MAX_SEQ_LENGTH - return tuple("", "", MAX_ENERGY).

    :param sequence: RNA sequence to calculate its stemloop structure.
    :return: tuple(sequence, structure_in_the_dot_bracket_notation, energy) or tuple("", "", MAX_ENERGY).
    """

    if not sequence or len(sequence) > MAX_SEQ_LENGTH:
        logger.error(f"Calculation was requested for empty/none or too long sequence. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY

    result = get_rnafold_structure(sequence)
    if is_hairpin(result[1]):
        return result
    else:
        return "", "", MAX_ENERGY


def get_complex_stemloop(sequence: str, length: int, step: int) -> (str, str, float):
    """ Calculate the stemloop structures of the sub-sequences and choose the best one stemloop by its energy.

    :param sequence: RNA sequence to calculate its sub-sequence stemloop structures.
    :param length: Length of the sliding window.
    :param step: Step of the sliding window.
    :return: tuple(sub-sequence, structure_in_the_dot_bracket_notation, energy) or tuple("", "", MAX_ENERGY).
    """

    if not sequence:
        logger.error(f"Calculation was requested for empty/none sequence. Sequence: '{sequence}'.")
        return "", "", MAX_ENERGY

    if length is None or not isinstance(length, int) or length <= 0 or length > MAX_SEQ_LENGTH:
        logger.error(f"Calculation was requested with none/negative/big value of the length. Length: '{length}'.")
        return "", "", MAX_ENERGY

    if step is None or not isinstance(step, int) or step <= 0:
        logger.error(f"Calculation was requested with none/negative value of the step. Step: '{step}'.")
        return "", "", MAX_ENERGY

    # Calculate
    stemloop_structure = get_simple_stemloop(sequence[0: length])
    position = int((len(sequence) - length) / step) + 1
    for i in range(1, position):
        temp_stemloop_structure = get_simple_stemloop(sequence[step * i: step * i + length])
        if temp_stemloop_structure[2] < stemloop_structure[2]:
            stemloop_structure = temp_stemloop_structure[:]

    # Get result
    return stemloop_structure


if __name__ == "__main__":
    """ Examples / Use cases. """

    print("result:", get_rnafold_structure("ACUACUUACUACUACGACGGAGCGACUACUUAC"))
    print("result:", get_simple_stemloop("acguacguagcuagcuagcuagcuagcuagcuacguagc"))
    print("result:", get_complex_stemloop("ACGUACGUACGACGUACGUACGUACGACGUACGUACGUACGACGUACGUACACGACGU", 20, 3))
