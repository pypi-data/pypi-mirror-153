#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mirmag.logger import get_logger


logger = get_logger(logger_name="mirna", log_to_console=True)


class MiRNA:
    """ Class to describe miRNA sequence. Based on the description of the miRNA from miRBase.org and MiRGeneDB.org.

    Parameters of constructor
    ----------
    header : str
        The sequence of the miRNA header. Header may contain start symbols ">", but it will be removed further!
        Example: "[OPTIONAL >]Title [OPTIONAL AccessionID] [OPTIONAL Description]".
    sequence : str
        The nucleotide sequence.
        Example: "UGAGGUAGTAGGUTGUATAGUT".

    Returns
    -------
    MiRNA object : object
        The miRNA object.
    """

    def __init__(self, header: str, sequence: str):
        """ Initialize miRNA object by its header and nucleotide sequence.

        :param header: The header of the miRNA.
        :param sequence: The nucleotide sequence of the miRNA.
        """

        # init
        self.title = ""
        self.accession = ""
        self.description = ""
        self.sequence = sequence or ""

        try:
            # Check header
            if not header:
                raise Exception("MiRNA was trying to be created with empty/none header.")

            # Adjust header (remove first symbols ">" if they exist in the header)
            header = header.lstrip(">")

            # Calculate and set class variables from header
            if header.count(" ") >= 2:
                self.title, self.accession, self.description = header.split(sep=" ", maxsplit=2)
            elif " " in header:
                self.title, self.accession = header.split(sep=" ")
            else:
                self.title = header

            # Check sequence
            if not sequence:
                raise Exception("MiRNA was trying to be created with empty/none sequence.")

        except Exception:
            logger.exception(f"Exception while creating the MiRNA object.\nHeader:'{header}', sequence:'{sequence}'.")

    def __str__(self) -> str:
        header = f">{self.get_title()} {self.get_accession()} {self.get_description()}"
        return header.strip() + "\n" + self.get_sequence()

    def __repr__(self) -> str:
        return self.__str__()

    def get_title(self) -> str:
        return self.title

    def get_accession(self) -> str:
        return self.accession

    def get_description(self) -> str:
        return self.description

    def get_sequence(self) -> str:
        return self.sequence

    def get_6mer_seed(self) -> str:
        if len(self.sequence) < 7:
            logger.warning(f"Too short miRNA sequence to have full-sized seed. Sequence='{self.sequence}'.")
        return self.get_sequence()[1:7]


if __name__ == "__main__":
    """ Examples / Use cases. """

    m1 = MiRNA(">cel-let-7-5p MIMAT0000001 Caenorhabditis elegans let-7-5p", "AAAGGUAGUAGGUUGUAUAGUU")
    print(m1)

    m2 = MiRNA(header="cel-let-8-5p MIMAT0000002", sequence="CCAGGUAGUAGGUUGUAUAGUU")
    print(m2)

    m3 = MiRNA(">>cel-let-9-5p", "GGAGGUAGUAGGUUGUAUAGUU")
    print(m3)

    m4 = MiRNA("cel-let-10-5p", "UUAGGU")
    print(m4)

    m5 = MiRNA(None, "TTGUTACTTGUTAC")
    print(m5)

    m6 = MiRNA(">Cel-let-11-5p", None)
    print(m6)
