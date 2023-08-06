#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mirmag.logger import get_logger


logger = get_logger(logger_name="organism", log_to_console=True)


class Organism:
    """ Class to classify species of miRNAs or pre-miRNAs by the letters' id in the sequence header.

        Based on the miRNA annotation from miRBase.org (rel. 19/21.0/22.1, e.g. "datasets/miRBase/.../organism.txt").
        Examples of identifiers: aqu, nve, hma, sko, hiv1, etc. All class methods are case-insensitive.

    Parameters of constructor
    ----------
    file_name : str
        The name of the file with miRBase identifiers and their organism classification.
        This name must include the full path to the file.

    Returns
    -------
    Organism object : object
        The object with classification methods.
    """

    def __init__(self, file_name: str):
        """ The constructor of the Organism class.

        :param file_name: The name of the file with miRBase identifiers and their organism classification.
        """

        self.animal_ids = []            # животные, многоклеточные
        self.greenplant_ids = []        # зеленые растения
        self.vertebrata_ids = []        # позвоночные
        self.mammalia_ids = []          # млекопитающие
        self.primates_ids = []          # приматы
        self.musmusculus_ids = []       # мышь
        self.homosapiens_ids = []       # человек

        try:
            with open(file_name, "r") as file:
                for line in file:
                    organism, division, name, tree, *NCBI_taxid = line.lower().split("\t")
                    if "metazoa;" in tree:
                        self.animal_ids.append(organism)
                    if "viridiplantae;" in tree:
                        self.greenplant_ids.append(organism)
                    if "vertebrata;" in tree:
                        self.vertebrata_ids.append(organism)
                    if "mammalia;" in tree:
                        self.mammalia_ids.append(organism)
                    if "primates;" in tree:
                        self.primates_ids.append(organism)
                    if "mus musculus" in name:
                        self.musmusculus_ids.append(organism)
                    if "homo sapiens" in name:
                        self.homosapiens_ids.append(organism)
        except Exception:
            logger.exception(f"Error while creating the Organism object. Source file: '{file_name}'.")

    @staticmethod
    def get_prepared_id(header: str) -> str:
        """ Convert header to lower case, remove '>' symbols if they are presented, return letters before first "-".

        :param header: The header of a miRNA/pre-miRNA sequence.
        :return: The prepared id or empty sequence for the empty/None input.
        """
        if header:
            return header.lower().lstrip(">").split("-")[0]
        else:
            return ""

    # id животного?
    def is_animal(self, header: str) -> bool:
        return self.get_prepared_id(header) in self.animal_ids

    # id зеленых растений?
    def is_greenplant(self, header: str) -> bool:
        return self.get_prepared_id(header) in self.greenplant_ids

    # id позвоночного?
    def is_vertebrata(self, header: str) -> bool:
        return self.get_prepared_id(header) in self.vertebrata_ids

    # id млекопитающего?
    def is_mammalia(self, header: str) -> bool:
        return self.get_prepared_id(header) in self.mammalia_ids

    # id примата?
    def is_primates(self, header: str) -> bool:
        return self.get_prepared_id(header) in self.primates_ids

    # id мыши?
    def is_musmusculus(self, header: str) -> bool:
        return self.get_prepared_id(header) in self.musmusculus_ids

    # id человека?
    def is_homosapiens(self, header: str) -> bool:
        return self.get_prepared_id(header) in self.homosapiens_ids


if __name__ == "__main__":
    """ Examples / Use cases. """

    organism = Organism(file_name=r"datasets/miRBase/rel.22.1/organisms.txt")
    print(organism.is_animal(None))
    print(organism.is_homosapiens(""))
    print(organism.is_musmusculus("12345"))
    print(organism.is_greenplant("ath"))
    print(organism.is_vertebrata(">ath"))
    print(organism.is_mammalia(">>ptvpv2a-mir-P1"))

    organism = Organism(file_name=r"incorrect.txt")
    print(organism.is_homosapiens(">hsa-mir-1"))
