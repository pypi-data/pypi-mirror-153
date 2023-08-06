#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mirmag.logger import get_logger


logger = get_logger(logger_name="stemloop", log_to_console=True)


""" All possible variants of the pre-miRNA secondary structures according to the miRBase.org (release 22.1).
    Whitespaces at the end of the lines are required to align the length of the sequences. 

    >hsa-let-7a-1 (-35.60)   [hsa-let-7a-5p:6-27] [hsa-let-7a-3p:57-77]
    [empty line]
         U   GU                uuagggucacac 
    uggga GAG  AGUAGGUUGUAUAGUU            c
    ||||| |||  ||||||||||||||||            c
    aucCU UUC  UCAUCUAACAUAUCaa            a
         -   UG                uagagggucacc 

    >hsa-let-7e (-37.80)   [hsa-let-7e-5p:8-29] [hsa-let-7e-3p:53-74]
    [empty line]
      c   cU   G                U  ----gga  a 
    cc ggg  GAG UAGGAGGUUGUAUAGU ga       gg c
    || |||  ||| |||||||||||||||| ||       ||  
    gg ccC  UUC AUCCUCCGGCAUAUCa cu       cc a
      a   CU   G                -  agaggaa  c 

    >hsa-let-7a-3 (-34.40)   [hsa-let-7a-5p:4-25] [hsa-let-7a-3p:52-72]
    [empty line]
       U   GU                ---------        
    ggg GAG  AGUAGGUUGUAUAGUU         uggggcu 
    ||| |||  ||||||||||||||||         |||||| c
    ucC UUC  UCAUCUAACAUAUCaa         gucccgu 
       U   UG                uaggguauc        
"""


class Hairpin5:
    """ Hairpin5 class: the structure of the pre-miRNA stemloop.

    Parameters
    ----------
    Header : str
        The header of the pre-miRNA. Like sequence ">hsa-let-7a-1 (-35.60) [hsa-let-7a-5p:6-27] ...".
        May start with symbol ">" or not.

    s1, s2, s3, s4, s5 : str, str, str, str, str
        Sequences that form the pre-miRNA structure like in the miRBase *.str file.
        "     u   GU                uuagggucacac "
        "uggga gAG  AGUAGGUUGUAUAGUU            c"
        "||||| |||  ||||||||||||||||            c"
        "auccu uuc  ucaucuaacauaucaa            a"
        "     -   ug                uagagggucacc "

    hp5, hp3, hpdb : object, object, object
        miRMag's Hairpin5, Hairpin3 and HairpinDB objects.

    Returns
    -------
    Hairpin5 object : object
        Pre-miRNA object similar to the *.str format of the miRBase.

    get_header : str
        Return the header of the pre-miRNA.

    get_s1, get_s2, get_s3, get_s4, get_s5 : str, str, str, str, str
        Return sequences that form the pre-miRNA structure.

    get_stemloop_without_header : str
        Return the printable string of the pre-miRNA stemloop without the header.
    """

    def __init__(self, **kwargs):

        # Init class variables
        self.header = ""
        self.s1 = ""
        self.s2 = ""
        self.s3 = ""
        self.s4 = ""
        self.s5 = ""

        # Fill the class variables
        try:
            if "header" in kwargs.keys():
                self._init(kwargs["header"], kwargs["s1"], kwargs["s2"], kwargs["s3"], kwargs["s4"], kwargs["s5"])
            elif "hp5" in kwargs.keys():
                self._init5(kwargs["hp5"])
            elif "hp3" in kwargs.keys():
                self._init3(kwargs["hp3"])
            elif "hpdb" in kwargs.keys():
                self._initdb(kwargs["hpdb"])
            else:
                raise Exception(f"Wrong number and/or type of the parameters while creating the Hairpin5 object.")
        except Exception:
            logger.exception(f"Error while creating the Hairpin5 object.\nParameters: {kwargs}.")

    def __str__(self):
        return (self.get_header() + "\n\n" + self.get_s1() + "\n" + self.get_s2() + "\n" +
                self.get_s3() + "\n" + self.get_s4() + "\n" + self.get_s5())

    def __repr__(self):
        return self.__str__()

    def _init(self, header: str, s1: str, s2: str, s3: str, s4: str, s5: str):
        """ Create the Hairpin5 object from several sequences.

        :param header: The header of the pre-miRNA.
        :param s1: Sequence.
        :param s2: Sequence.
        :param s3: Sequence.
        :param s4: Sequence.
        :param s5: Sequence.
        :return: None.
        """

        if not header or not s1 or not s2 or not s3 or not s4 or not s5:
            raise Exception("Hairpin5 object was trying to be created with empty/none parameters: header/s1-s5.")
        else:
            self.header = header
            self.s1 = s1
            self.s2 = s2
            self.s3 = s3
            self.s4 = s4
            self.s5 = s5

    def _init5(self, hp5):
        """ Create the Hairpin5 object from the other Hairpin5 object.

        :param hp5: The Hairpin5 object.
        :return: None.
        """

        if not hp5:
            raise Exception("Hairpin5 object was trying to be created with empty/none parameter: hp5.")
        else:
            self._init(hp5.get_header(), hp5.get_s1(), hp5.get_s2(), hp5.get_s3(), hp5.get_s4(), hp5.get_s5())

    def _init3(self, hp3):
        """ Create the Hairpin5 object from the Hairpin3 object.

        :param hp3: The Hairpin3 object.
        :return: None.
        """

        if not hp3:
            raise Exception("Hairpin5 object was trying to be created with empty/none parameter: hp3.")

        # init data
        header = hp3.get_header()
        s1, s2, s3, s4, s5 = [], [], [], [], []
        p5 = hp3.get_p5()
        st = hp3.get_str()
        p3 = hp3.get_p3()

        # calculate
        for i in range(len(p5)-2):
            if st[i] == " ":
                s1.append(p5[i])
                s2.append(" ")
                s3.append(" ")
                s4.append(" ")
                s5.append(p3[i])
            else:
                s1.append(" ")
                s2.append(p5[i])
                s3.append("|")
                s4.append(p3[i])
                s5.append(" ")

        # Make a cool terminal loop like in the miRBase.org
        if p3[-1] == "-":
            if st[-3] == " ":       # Fix #1 structure
                s1.append(" ")
                s2.append(p5[-2])
                s3.append(p5[-1])
                s4.append(p3[-2])
                s5.append(" ")
            else:                   # Fix #3 structure
                s1.append(" ")
                s2.append(p5[-2])
                s3.append(" ")
                s4.append(p3[-2])
                s5.append(" ")
                #
                s1.append(" ")
                s2.append(" ")
                s3.append(p5[-1])
                s4.append(" ")
                s5.append(" ")
        else:                       # Fix #2 structure
            s1.append(p5[-2])
            s2.append(" ")
            s3.append(" ")
            s4.append(" ")
            s5.append(p3[-2])
            #
            s1.append(" ")
            s2.append(p5[-1])
            s3.append(" ")
            s4.append(p3[-1])
            s5.append(" ")

        # assign
        self.header = header
        self.s1 = "".join(s1)
        self.s2 = "".join(s2)
        self.s3 = "".join(s3)
        self.s4 = "".join(s4)
        self.s5 = "".join(s5)

    def _initdb(self, hpdb):
        """ Create the Hairpin5 object from the HairpinDB object.

        :param hpdb: The HairpinDB object.
        :return: None.
        """

        if not hpdb:
            raise Exception("Hairpin5 object was trying to be created with empty/none parameter: hpdb.")
        else:
            hp3 = Hairpin3(hpdb=hpdb)
            self._init3(hp3=hp3)

    def get_header(self) -> str:
        return self.header

    def get_s1(self) -> str:
        return self.s1

    def get_s2(self) -> str:
        return self.s2

    def get_s3(self) -> str:
        return self.s3

    def get_s4(self) -> str:
        return self.s4

    def get_s5(self) -> str:
        return self.s5

    def get_stemloop_without_header(self):
        return self.get_s1() + "\n" + self.get_s2() + "\n" + self.get_s3() + "\n" + self.get_s4() + "\n" + self.get_s5()


class Hairpin3:
    """ Hairpin3 class: the structure of the pre-miRNA stemloop.

    Parameters
    ----------
    Header : str
        The header of the pre-miRNA. Like sequence ">hsa-let-7a-1 (-35.60) [hsa-let-7a-5p:6-27] ...".
        May start with symbol ">" or not.

    p5, st, p3 : str, str, str
        Sequences that form pre-miRNA structure.
        "ugggaugAGGUAGUAGGUUGUAUAGUUuuagggucacaccc"
        "||||| |||  ||||||||||||||||              "
        "auccu-uucugucaucuaacauaucaauagagggucacca-"

    hp5, hp3, hpdb : object, object, object
        miRMag's Hairpin5, Hairpin3 and HairpinDB objects.

    Returns
    -------
    Hairpin3 object : object
        The pre-miRNA form, one of three ones.

    get_header : str
        Return the header of the pre-miRNA.

    get_p5, get_str, get_p3 : str, str, str
        Sequences that form pre-miRNA structure.

    get_stemloop_without_header : str
        Return the printable string of the pre-miRNA stemloop without header.
    """

    def __init__(self, **kwargs):

        # Init class variables
        self.header = ""
        self.p5 = ""
        self.st = ""
        self.p3 = ""

        # Fill the class variables
        try:
            if "header" in kwargs.keys():
                self._init(kwargs["header"], kwargs["p5"], kwargs["st"], kwargs["p3"])
            elif "hp5" in kwargs.keys():
                self._init5(kwargs["hp5"])
            elif "hp3" in kwargs.keys():
                self._init3(kwargs["hp3"])
            elif "hpdb" in kwargs.keys():
                self._initdb(kwargs["hpdb"])
            else:
                raise Exception(f"Wrong number and/or type of the parameters while creating the Hairpin3 object.")
        except Exception:
            logger.exception(f"Error while creating the Hairpin3 object.\nParameters: {kwargs}.")

    def __str__(self):
        return self.get_header() + "\n" + self.get_p5() + "\n" + self.get_str() + "\n" + self.get_p3()

    def __repr__(self):
        return self.__str__()

    def _init(self, header: str, p5: str, st: str, p3: str):
        """ Create the Hairpin3 object from several sequences.

        :param header: The header of the pre-miRNA.
        :param p5: p5 branch of the pre-miRNA.
        :param st: pre-miRNA structure in the alphabet {"|", " "}
        :param p3: p3 branch of the pre-miRNA.
        :return: None
        """

        if not header or not p5 or not st or not p3:
            raise Exception("Hairpin3 object was trying to be created with empty/none parameters: header/p5/st/p3.")
        else:
            self.header = header
            self.p5 = p5
            self.st = st
            self.p3 = p3

    def _init5(self, hp5):
        """ Create the Hairpin3 object from the Hairpin5 object.

        :param hp5: The Hairpin5 object.
        :return: None.
        """

        if not hp5:
            raise Exception("Hairpin3 object was trying to be created with empty/none parameters: hp5.")

        # init data
        header = hp5.get_header()
        p5, st, p3 = [], [], []
        s1t = hp5.get_s1()
        s2t = hp5.get_s2()
        s3t = hp5.get_s3()
        s4t = hp5.get_s4()
        s5t = hp5.get_s5()

        # calculate
        for i in range(len(s1t) - 1):
            if s1t[i] == " ":
                p5.append(s2t[i])
            else:
                p5.append(s1t[i])
            if s5t[i] == " ":
                p3.append(s4t[i])
            else:
                p3.append(s5t[i])
            st.append(s3t[i])

        # fix #1 structure
        if s2t[-1] != " " and s3t[-1] != " ":
            p5.append(s2t[-1])
            st.append(" ")
            p3.append(s4t[-1])
            #
            p5.append(s3t[-1])
            st.append(" ")
            p3.append("-")

        # fix #2 structure
        if s2t[-1] != " " and s3t[-1] == " ":
            p5.append(s2t[-1])
            st.append(" ")
            p3.append(s4t[-1])

        # fix #3 structure
        if s2t[-1] == " " and s3t[-1] != " ":
            p5.append(s3t[-1])
            st.append(" ")
            p3.append("-")

        # assign
        self.header = header
        self.p5 = "".join(p5)
        self.st = "".join(st)
        self.p3 = "".join(p3)

    def _init3(self, hp3):
        """ Create the Hairpin3 object from the other Hairpin3 object.

        :param hp3: The Hairpin3 object.
        :return: None.
        """

        if not hp3:
            raise Exception("Hairpin3 object was trying to be created with empty/none parameters: hp3.")
        else:
            self._init(hp3.get_header(), hp3.get_p5(), hp3.get_str(), hp3.get_p3())

    def _initdb(self, hpdb):
        """ Create the Hairpin3 object from the HairpinDB object.

        :param hpdb: The HairpinDB object.
        :return: None.
        """

        if not hpdb:
            raise Exception("Hairpin3 object was trying to be created with empty/none parameters: hpdb.")

        # init data
        header = hpdb.get_header()
        p5, st, p3 = [], [], []
        sequence = hpdb.get_sequence()
        structure = hpdb.get_structure()
        head, tail = 0, len(sequence) - 1

        # calculate
        while head < tail:
            c = structure[head]
            d = structure[tail]

            if c == d:
                # . & .
                p5.append(sequence[head])
                st.append(" ")
                p3.append(sequence[tail])
                #
                head += 1
                tail -= 1
            elif c == ".":
                # x & .
                p5.append(sequence[head])
                st.append(" ")
                p3.append("-")
                #
                head += 1
            elif d == ".":
                # . & x
                p5.append("-")
                st.append(" ")
                p3.append(sequence[tail])
                #
                tail -= 1
            else:
                # x & y
                p5.append(sequence[head])
                st.append("|")
                p3.append(sequence[tail])
                #
                head += 1
                tail -= 1

        # Fix the center of the terminal loop
        if head == tail:
            p5.append(sequence[head])
            st.append(" ")
            p3.append("-")

        """ Fix the loops.
            При построении в bulge/internal-петлях нуклеотиды тяготеют "влево", к основанию шпильки.
            В базе miRBase.org нуклеотиды тяготеют "вправо", к шпилечной петле;
            Переставляем нуклеотиды, чтобы соответствовать базе. Надеюсь оно работает правильно... =)
        """
        b, e = 0, 0
        while e != -1 and e < len(st):
            if st[e] != " ":
                e += 1
                continue
            else:
                # Found a loop
                b = e
                e = st.index("|", b + 1) if ("|" in st[b + 1:]) else -1

                # If it is a last loop (terminal loop) => break.
                if e == -1:
                    break

                # Correction
                t5 = p5[b: e]
                t3 = p3[b: e]

                # Bulge/internal-петля с нужными свойствами (нуклеотиды в 5p-ветви тяготеют "влево")
                if t5[0] != "-" and t5[-1] == "-":
                    subt5 = t5[0: t5.index("-")]
                    for j in range(b, b + len(subt5)):
                        p5[j] = "-"
                    p5[b + len(t5) - len(subt5): b + len(t5)] = subt5[:]

                # Bulge/internal-петля с нужными свойствами (нуклеотиды в 3p-ветви тяготеют "влево")
                if t3[0] != "-" and t3[-1] == "-":
                    subt3 = t3[0: t3.index("-")]
                    for j in range(b, b + len(subt3)):
                        p3[j] = "-"
                    p3[b + len(t3) - len(subt3): b + len(t3)] = subt3[:]

        # assign
        self.header = header
        self.p5 = "".join(p5)
        self.st = "".join(st)
        self.p3 = "".join(p3)

    def get_header(self) -> str:
        return self.header

    def get_p5(self) -> str:
        return self.p5

    def get_str(self) -> str:
        return self.st

    def get_p3(self) -> str:
        return self.p3

    def get_stemloop_without_header(self):
        return self.get_p5() + "\n" + self.get_str() + "\n" + self.get_p3()


class HairpinDB:
    """ HairpinDB class: the structure of the pre-miRNA stemloop.

    Parameters
    ----------
        The header of the pre-miRNA. Like sequence ">hsa-let-7a-1 (-35.60) [hsa-let-7a-5p:6-27] ...".
        May start with symbol ">" or not.

    sequence : str
        Sequence, may be in a {A,C,G,U,T,a,c,g,u,t}-alphabet.
        "uucUGAGUAUUACUUCAGGUACUGGUuguauuaaauaaaaaacggaauaaguuauuaacacagccuaauagagauauuacggauuuacga".

    structure : str
        Sequence in a dot-bracket notation.
        ".((((((((((.((..(((..(((((((...........................)))).))))))...)).)))))).)))).......".

    hp5, hp3, hpdb : object, object, object
        miRMag's Hairpin5, Hairpin3 and HairpinDB objects.

    Returns
    -------
    HairpinDB object : object
        DB-form, one of three ones.

    get_header : str
        Return the header of the pre-miRNA.

    get_sequence : str
        Return the sequence of the pre-miRNA.

    get_structure : str
        Return the secondary structure of the pre-miRNA in dot-bracket notation.

    get_stemloop_without_header : str
        Return the printable string of the pre-miRNA stemloop without header.
    """

    def __init__(self, **kwargs):

        # Init class variables
        self.header = ""
        self.sequence = ""
        self.structure = ""

        # Fill the class variables
        try:
            if "header" in kwargs.keys():
                self._init(kwargs["header"], kwargs["sequence"], kwargs["structure"])
            elif "hp5" in kwargs.keys():
                self._init5(kwargs["hp5"])
            elif "hp3" in kwargs.keys():
                self._init3(kwargs["hp3"])
            elif "hpdb" in kwargs.keys():
                self._initdb(kwargs["hpdb"])
            else:
                raise Exception(f"Wrong number and/or type of the parameters while creating HairpinDB object.")
        except Exception:
            logger.exception(f"Error while creating the HairpinDB object.\nParameters: {kwargs}.")

    def __str__(self):
        return self.get_header() + "\n" + self.get_sequence() + "\n" + self.get_structure()

    def __repr__(self):
        return self.__str__()

    def _init(self, header: str, sequence: str, structure: str):
        """ Create the HairpinDB object from several sequences.

        :param header: The header of the pre-miRNA.
        :param sequence: Sequence of the pre-miRNA.
        :param structure: Sequence of the pre-miRNA structure.
        :return: None
        """

        if not header or not sequence or not structure:
            raise Exception("HairpinDB object was trying to be created with empty/none parameters: header/seq/str.")
        else:
            self.header = header
            self.sequence = sequence
            self.structure = structure

    def _init5(self, hp5):
        """ Create the HairpinDB object from Hairpin5 object.

        :param hp5: The Hairpin5 object.
        :return: None
        """

        if not hp5:
            raise Exception("HairpinDB object was trying to be created with empty/none parameters: hp5.")
        else:
            hp3 = Hairpin3(hp5=hp5)
            self._init3(hp3=hp3)

    def _init3(self, hp3):
        """ Create the HairpinDB object from Hairpin3 object.

        :param hp3: The Hairpin3 object.
        :return: None.
        """

        if not hp3:
            raise Exception("HairpinDB object was trying to be created with empty/none parameters: hp3.")

        # init data
        header = hp3.get_header()
        p5 = hp3.get_p5()
        st = hp3.get_str()
        p3 = hp3.get_p3()

        sequence = (p5 + p3[::-1]).replace("-", "")
        structure = list(sequence)
        head, tail = 0, len(sequence) - 1

        # calculate
        for i in range(len(p5)):
            if st[i] == "|":
                structure[head] = "("
                structure[tail] = ")"
                head += 1
                tail -= 1
            else:
                if p5[i] != "-":
                    structure[head] = "."
                    head += 1
                if p3[i] != "-":
                    structure[tail] = "."
                    tail -= 1

        # assign
        self.header = header
        self.sequence = sequence
        self.structure = "".join(structure)

    def _initdb(self, hpdb):
        """ Create the HairpinDB object from other HairpinDB object.

        :param hpdb: The HairpinDB object.
        :return: None.
        """

        if not hpdb:
            raise Exception("HairpinDB object was trying to be created with empty/none parameters: hpdb.")
        else:
            self.header = hpdb.get_header()
            self.sequence = hpdb.get_sequence()
            self.structure = hpdb.get_structure()

    def get_header(self) -> str:
        return self.header

    def get_sequence(self) -> str:
        return self.sequence

    def get_structure(self) -> str:
        return self.structure

    def get_stemloop_without_header(self):
        return self.get_sequence() + "\n" + self.get_structure()


def is_hairpin(structure: str) -> bool:
    """ Check sequence for the hairpin structure.

    :param structure: The sequence in dot-bracket notation.
    :return: True (is a hairpin) or False (is not a hairpin).
    """

    if not structure:
        logger.info(f"Function was requested for the empty/none structure: '{structure}'.")
        return False

    bbr = structure.count("(")
    ebr = structure.count(")")
    dots = structure.count(".")

    if (bbr == 0) or (bbr != ebr):
        logger.info(f"Function was requested for the structure with incorrect number of symbols '(' and ')'.\n"
                    f"Structure: '{structure}'. Numbers of '(' and ')': {bbr} and {ebr} correspondingly.")
        return False

    if bbr + ebr + dots != len(structure):
        logger.info(f"Function was requested for the structure with inappropriate symbols!\n"
                    f"Structure: '{structure}'.")
        return False

    head = 0
    tail = len(structure) - 1
    while head < tail:
        if structure[head] == ".":
            head += 1
        elif structure[tail] == ".":
            tail -= 1
        elif structure[head] == "(" and structure[tail] == ")":
            head += 1
            tail -= 1
        else:
            logger.info(f"Function was requested for the structure with multi-loop(s).\n"
                        f"Structure: '{structure}'.")
            return False

    # You're LUCKY! It's a hairpin!
    return True


def get_mirna_count(hairpin) -> int:
    """ Function rough estimates the number and the type of the miRNAs in the pre-miRNA.
        In calculation the function uses the pre-miRNA (miRBase) header and uppercase miRNA marking.

    :param hairpin: The Hairpin5, Hairpin3 or HairpinDB object.
    :return: 5 (only 5p miRNA),
             3 (only 3p miRNA),
             2 (both 5p and 3p miRNAs),
            -1 (the structure isn't a hairpin),
            -2 (has more than two miRNA sequences),
            -3 (miRNA crosses center of the terminal loop),
            -4 (pre-miRNA does not contain marked miRNA),
            -5 (some other error during the processing).
    """

    try:
        if isinstance(hairpin, Hairpin3):
            hp3 = hairpin
            hpdb = HairpinDB(hp3=hairpin)
        elif isinstance(hairpin, HairpinDB):
            hp3 = Hairpin3(hpdb=hairpin)
            hpdb = hairpin
        elif isinstance(hairpin, Hairpin5):
            hp3 = Hairpin3(hp5=hairpin)
            hpdb = HairpinDB(hp5=hairpin)
        else:
            raise Exception(f"Wrong number and/or type of the parameter which passed to the function.")
    except Exception:
        logger.exception(f"Error while creating the Hairpin5/3/DB object(s).\nParameters: '{hairpin}'.")
        return -5

    header = hpdb.get_header()
    seq = hpdb.get_sequence()
    st = hpdb.get_structure()

    begin = st.rfind("(")
    end = st.find(")")
    center = (begin + end) // 2

    # Structure is not a hairpin
    if not is_hairpin(st):
        logger.info(f"Function was requested for the non-hairpin structure.\nStructure: '{st}'.")
        return -1

    # Pre-miRNA contains more than two miRNAs
    if header.count("]") > 2:
        logger.info(f"Pre-miRNA's header has more than 2 miRNAs'. Header: '{header}'.")
        return -2

    # Pre-miRNA does not contain marked miRNA
    if max(seq.find("A"), seq.find("C"), seq.find("G"), seq.find("U"), seq.find("T")) == -1:
        logger.info(f"Pre-miRNA sequence does not contain marked miRNA(s).\nSequence: '{seq}'.")
        return -4

    # miRNA crosses the center of the terminal loop
    if begin + end != 2 * center:
        # Case: XXXXxx or xxXXXX
        #       (....) or (....)
        if seq[center] not in "acgut" and seq[center + 1] not in "acgut":
            return -3
    else:
        # Case: XXXxx or xxXXX
        #       (...) or (...)
        if (seq[center - 1] not in "acgut" and seq[center] not in "acgut") or \
                (seq[center] not in "acgut" and seq[center + 1] not in "acgut"):
            return -3

    # Good case: 5p, 3p or both miRNAs
    p5 = hp3.get_p5()
    p3 = hp3.get_p3()
    p5c = max(p5.find("A"), p5.find("C"), p5.find("G"), p5.find("U"), p5.find("T"))
    p3c = max(p3.find("A"), p3.find("C"), p3.find("G"), p3.find("U"), p3.find("T"))
    if p5c != -1 and p3c == -1:
        return 5
    elif p5c == -1 and p3c != -1:
        return 3
    elif p5c != -1 and p3c != -1:
        return 2
    else:
        return -5


def get_mirna_positions(hairpin, branch: int) -> (int, int):
    """ Get miRNA positions in the Hairpin3 pre-miRNA with marked miRNA sequences.
        Programming counting of the positions.
        In case of the incorrect location of the miRNA its end sets equal to the length of the pre-miRNA branch.

    :param hairpin: Pre-miRNA.
    :param branch:  Branch of the miRNA sequence.
    :return: [begin, end) of the miRNA in Hairpin3 notation, or (-1, -1) in case of errors.
    """

    try:
        if isinstance(hairpin, Hairpin3):
            hp3 = hairpin
        elif isinstance(hairpin, HairpinDB):
            hp3 = Hairpin3(hpdb=hairpin)
        elif isinstance(hairpin, Hairpin5):
            hp3 = Hairpin3(hp5=hairpin)
        else:
            raise Exception(f"Wrong number and/or type of the parameter which passed to the function.")
    except Exception:
        logger.exception(f"Error while creating the Hairpin3 object(s).\nParameters: '{hairpin}'\nBranch: {branch}.")
        return -1, -1

    begin, end = -1, -1
    if branch == 5:
        sequence = hp3.get_p5()
    elif branch == 3:
        sequence = hp3.get_p3()
    else:
        logger.exception(f"Error while find the miRNA sequence.\nParameters: '{hairpin}'\nBranch: {branch}.")
        return -1, -1

    for index, value in enumerate(sequence):
        if value in "ACGUT":
            begin = index
            break

    for index, value in enumerate(sequence[::-1]):
        if value in "ACGUT":
            end = len(sequence) - index
            break

    return begin, end


if __name__ == "__main__":
    """ Examples / Use cases. """

    # Header
    header = ">hsa-let-7a-1 (-35.60)   [hsa-let-7a-5p:6-27] [hsa-let-7a-3p:57-77]"

    # Hairpin5 structure
    s1 = "     U   GU                uuagggucacac "
    s2 = "uggga GAG  AGUAGGUUGUAUAGUU            c"
    s3 = "||||| |||  ||||||||||||||||            c"
    s4 = "aucCU UUC  UCAUCUAACAUAUCaa            a"
    s5 = "     -   UG                uagagggucacc "
    hp5 = Hairpin5(header=header, s1=s1, s2=s2, s3=s3, s4=s4, s5=s5)

    # Hairpin3 structure
    p5 = "ugggaugagguaguagguuguauaguuuuagggucacaccc"
    st = "||||| |||  ||||||||||||||||              "
    p3 = "aucCU-UUCUGUCAUCUAACAUAUCaauagagggucacca-"
    hp3 = Hairpin3(header=header, p5=p5, st=st, p3=p3)

    # HairpinDB structure
    seq = "ugggaUGAGGUAGUAGGUUGUAUAGUUuuagggucacacccaccacugggagauaacuauacaaucuacugucuuuccua"
    stu = "(((((.(((..((((((((((((((((...........................))))))))))))))))..))))))))"
    hpdb = HairpinDB(header=header, sequence=seq, structure=stu)

    print("{}\n{}\n{}\n\n".format(hp5, hp3, hpdb))

    print(f"{hp5.get_stemloop_without_header()}\n"
          f"{hp3.get_stemloop_without_header()}\n"
          f"{hpdb.get_stemloop_without_header()}\n")

    print(is_hairpin(stu), get_mirna_count(hp5), get_mirna_count(hp3), get_mirna_count(hpdb))

    print(get_mirna_positions(hairpin=hp5, branch=3))
    print(get_mirna_positions(hairpin=hp3, branch=5))
