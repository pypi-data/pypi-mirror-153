#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy

import matplotlib.pyplot as plt
from mirmag.logger import get_logger
from mirmag.matrix import Matrix
from mirmag.stemloop import Hairpin5, Hairpin3, HairpinDB, get_mirna_count, get_mirna_positions
from mirmag.utils import get_hairpin5_objects, get_hairpin3_objects, get_hairpindb_objects
import numpy as np


logger = get_logger(logger_name="mhmm", log_to_console=True)


def plot_bar(sample1: list, sample2: list, label1: str, label2: str, file_name: str):
    """ Plot bar with uniform style. """

    x = np.arange(len(sample1))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, sample1, width, label=label1)
    rects2 = ax.bar(x + width / 2, sample2, width, label=label2)

    ax.legend()

    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig(file_name)
    plt.show()
    
    
class MHMM:
    """

    """

    def __init__(self):
        self.NoUnS = 4  # To emulate structural states {M, N, I, D} and Hidden states {Helix/+, Loop/-}
        self.map_table = [2, 1, 2, 2, 3, 1, 2, 1, 2, 3, 2, 1, 2, 1, 3, 2, 2, 1, 2, 3, 4, 4, 4, 4]
        self.ind_table = [0, 0, 1, 2, 0, 1, 3, 2, 4, 1, 5, 3, 6, 4, 2, 7, 8, 5, 9, 3, 0, 1, 2, 3]

        self.t_table5 = Matrix(m=9, n=9)
        self.t_table5r = Matrix(m=9, n=9)
        self.e_table5 = Matrix(m=9, n=10)

        self.t_table3 = Matrix(m=9, n=9)
        self.t_table3r = Matrix(m=9, n=9)
        self.e_table3 = Matrix(m=9, n=10)

    def training_model_by_one_candidate(self, begin, end, p5, p3, t_table, e_table, need_end_correction: bool = True):
        """
        Модель с нулевым состоянием (стартовым)
        //! begin - first symbol of miRNA,
        //! end   - symbol after the last miRNA's symbol,
        //! numeration from the zero.
        """

        # Корректировка окончания микроРНК на 2нт в сторону терминальной петли.
        if need_end_correction:
            end = min(end + 2, len(p5))

        prev = 0
        for i in range(len(p5)):

            if begin <= i < end:
                curr = self.NoUnS + self.get_state(p5[i], p3[i])
            else:
                curr = self.get_state(p5[i], p3[i])

            t_table.inc_value(prev, curr)
            e_table.inc_value(curr, self.ind_table[self.get_index(p5[i], p3[i])])
            prev = curr

    def training_model_by_file(self, file_name: str, file_type: str) -> None:
        """ Выполнить обучение СММ по данным из файла. Данные могут быть в hairpin5, hairpinp3 или hairpindb-форматах.

        :param file_name: Файл с данными для обучения.
        :param file_type: Тип данных в файле для обучения.
        :return: None.
        """

        if file_type == "hairpin5":
            premirnas = [Hairpin3(hp5=hp5) for hp5 in get_hairpin5_objects(file_name).values()]
        elif file_type == "hairpin3":
            premirnas = get_hairpin3_objects(file_name).values()
        elif file_type == "hairpindb":
            premirnas = [Hairpin3(hpdb=hpdb) for hpdb in get_hairpindb_objects(file_name).values()]
        else:
            raise Exception(f"Incorrect file type. File: {file_name}, type: {file_type}.")


        for hp3 in premirnas:

            mirna_counts = get_mirna_count(hp3)

            if mirna_counts not in [2, 3, 5]:
                continue

            if mirna_counts != 3:
                b, e = get_mirna_positions(hp3, 5)
                self.training_model_by_one_candidate(b, e, hp3.get_p5(), hp3.get_p3(), self.t_table5, self.e_table5)

            if mirna_counts != 5:
                b, e = get_mirna_positions(hp3, 3)
                self.training_model_by_one_candidate(b, e, hp3.get_p5(), hp3.get_p3(), self.t_table3, self.e_table3)

        # Form transponizes matrix
        self.t_table5r = Matrix(array=self.t_table5.get_array())
        self.t_table5r.transponize()
        self.t_table3r = Matrix(array=self.t_table3.get_array())
        self.t_table3r.transponize()

        # Normalize all matrixes
        self.t_table5.normalize(False)
        self.t_table3.normalize(False)
        self.t_table5r.normalize(False)
        self.t_table3r.normalize(False)
        self.e_table5.normalize(False)
        self.e_table3.normalize(False)

        print(self.t_table5)
        print()
        print(self.t_table3)
        print()
        print(self.e_table5)
        print()
        print(self.e_table3)


    def training_model_by_dataset(self) -> None:
        pass

    def get_state(self, c1, c2):
        if c1 in 'aA':
            if c2 in 'aA':
                return self.map_table[0]
            elif c2 in 'uUtT':
                return self.map_table[1]
            elif c2 in 'gG':
                return self.map_table[2]
            elif c2 in 'cC':
                return self.map_table[3]
            elif c2 in '-':
                return self.map_table[4]
            else:
                return self.map_table[4]    # ????
        elif c1 in 'uUtT':
            if c2 in 'aA':
                return self.map_table[5]
            elif c2 in 'uUtT':
                return self.map_table[6]
            elif c2 in 'gG':
                return self.map_table[7]
            elif c2 in 'cC':
                return self.map_table[8]
            elif c2 in '-':
                return self.map_table[9]
            else:
                return self.map_table[9]    # ????
        elif c1 in 'gG':
            if c2 in 'aA':
                return self.map_table[10]
            elif c2 in 'uUtT':
                return self.map_table[11]
            elif c2 in 'gG':
                return self.map_table[12]
            elif c2 in 'cC':
                return self.map_table[13]
            elif c2 in '-':
                return self.map_table[14]
            else:
                return self.map_table[14]    # ????
        elif c1 in 'cC':
            if c2 in 'aA':
                return self.map_table[15]
            elif c2 in 'uUtT':
                return self.map_table[16]
            elif c2 in 'gG':
                return self.map_table[17]
            elif c2 in 'cC':
                return self.map_table[18]
            elif c2 in '-':
                return self.map_table[19]
            else:
                return self.map_table[19]    # ????
        elif c1 in '-':
            if c2 in 'aA':
                return self.map_table[20]
            elif c2 in 'uUtT':
                return self.map_table[21]
            elif c2 in 'gG':
                return self.map_table[22]
            elif c2 in 'cC':
                return self.map_table[23]
            elif c2 in '-':
                return self.map_table[0]
            else:
                return self.map_table[0]    # ????
        else:
            return self.map_table[0]

    @staticmethod
    def get_index(c1, c2):
        if c1 in 'aA':
            if c2 in 'aA':
                return 0
            elif c2 in 'uUtT':
                return 1
            elif c2 in 'gG':
                return 2
            elif c2 in 'cC':
                return 3
            elif c2 in '-':
                return 4
            else:
                return 4    # ????
        elif c1 in 'uUtT':
            if c2 in 'aA':
                return 5
            elif c2 in 'uUtT':
                return 6
            elif c2 in 'gG':
                return 7
            elif c2 in 'cC':
                return 8
            elif c2 in '-':
                return 9
            else:
                return 9    # ????
        elif c1 in 'gG':
            if c2 in 'aA':
                return 10
            elif c2 in 'uUtT':
                return 11
            elif c2 in 'gG':
                return 12
            elif c2 in 'cC':
                return 13
            elif c2 in '-':
                return 14
            else:
                return 14    # ????
        elif c1 in 'cC':
            if c2 in 'aA':
                return 15
            elif c2 in 'uUtT':
                return 16
            elif c2 in 'gG':
                return 17
            elif c2 in 'cC':
                return 18
            elif c2 in '-':
                return 19
            else:
                return 19    # ????
        elif c1 in '-':
            if c2 in 'aA':
                return 20
            elif c2 in 'uUtT':
                return 21
            elif c2 in 'gG':
                return 22
            elif c2 in 'cC':
                return 23
            elif c2 in '-':
                return 0
            else:
                return 0    # ????
        else:
            return 0

    def classify_mirnas_by_model(self, branch, p5, p3) -> (str, str, str, str):
        """

        :return:
        """

        pass

        if branch == 5:
            self.t_table = self.t_table5
            self.t_tabler = self.t_table5r
            self.e_table = self.e_table5
            branch  = p5
        elif branch == 3:
            self.t_table = self.t_table3
            self.t_tabler = self.t_table3r
            self.e_table = self.e_table3
            branch = p3
        else:
            # TODO: сделать нормально.
            return None

        # Init
        curr, prev, ind = 0, 0, 0
        length = len(branch)    # len(p5) ?

        P = numpy.zeros((2, length), numpy.double)
        S = numpy.zeros((2, length), numpy.double)

        # Forward - step
        prev = self.get_state(p5[0], p3[0])
        for i in range(1, length):
            curr = self.get_state(p5[i], p3[i])
            ind = self.ind_table[self.get_index(p5[i], p3[i])]

            pTT = P[0][i - 1] * self.t_table.get_value(prev + self.NoUnS, curr + self.NoUnS)
            pTF = P[0][i - 1] * self.t_table.get_value(prev + self.NoUnS, curr)
            pFT = (1.0 - P[0][i - 1]) * self.t_table.get_value(prev, curr + self.NoUnS)
            pFF = (1.0 - P[0][i - 1]) * self.t_table.get_value(prev, curr)

            if pTT > pFT:
                pT = pTT * self.e_table.get_value(curr + self.NoUnS, ind)
            else:
                pT = pFT * self.e_table.get_value(curr + self.NoUnS, ind)

            if pTF > pFF:
                pF = pTF * self.e_table.get_value(curr, ind)
            else:
                pF = pFF * self.e_table.get_value(curr, ind)

            prev = curr

            # Normalize P
            sum = pT + pF
            if sum == 0.0:
                P[0][i] = 0.5
            else:
                P[0][i] = pT / sum

            # Normalize S
            sum = pTF + pFF
            if sum == 0.0:
                S[0][i] = 0.0
            else:
                S[0][i] = pTF / sum

        # Backward-step
        P[1][length - 1] = 0.0
        prev = self.get_state(p5[length - 1], p3[length - 1])
        for i in range(length - 2, -1, -1):
            cur = self.get_state(p5[i], p3[i])
            ind = self.ind_table[self.get_index(p5[i], p3[i])]

            pTT = P[1][i + 1] * self.t_tabler.get_value(cur + self.NoUnS, prev + self.NoUnS)
            pTF = P[1][i + 1] * self.t_tabler.get_value(cur, prev + self.NoUnS)
            pFT = (1.0 - P[1][i + 1]) * self.t_tabler.get_value(cur + self.NoUnS, prev)
            pFF = (1.0 - P[1][i + 1]) * self.t_tabler.get_value(cur, prev)

            if pTT > pFT:
                pT = pTT * self.e_table.get_value(cur + self.NoUnS, ind)
            else:
                pT = pFT * self.e_table.get_value(cur + self.NoUnS, ind)

            if pTF > pFF:
                pF = pTF * self.e_table.get_value(cur, ind)
            else:
                pF = pFF * self.e_table.get_value(cur, ind)

            prev = cur

            # Normalize P
            sum = pT + pF
            if sum == 0.0:
                P[1][i] = 0.5
            else:
                P[1][i] = pT / sum

            # Normalize S
            sum = pTF + pFF
            if sum == 0.0:
                S[1][i] = 0.0
            else:
                S[1][i] = pTF / sum

        plot_bar(P[0], P[1], "1", "2", "../!back_up/miRMag/mirmag/3.png")
        plot_bar(S[0], S[1], "1", "2", "../!back_up/miRMag/mirmag/3.png")



        """




        // max(S1[]]) - begin position of the miRNA
        // max(S0[]]) - next position after the end of the miRNA
        // miRNA = [begin, end)
        // Length of the miRNAs without '-' is one of the {20,21,22,23,24} nt.

        // Cut the '-'-symbols
        std::string   branchPrime("");
        std::vector<double> signalPrime0;
        std::vector<double> signalPrime1;
        for (int i = 0; i < length; ++i)
        {
            if (branch[i] != '-')
            {
                branchPrime.push_back(branch[i]);
                signalPrime0.push_back(S[0][i]);
                signalPrime1.push_back(S[1][i]);
            }
        }

        // Check the length ... if less than MIN_MIRNA_LENGTH - return full branch.
        if (branchPrime.length() <= MIN_MIRNA_LENGTH)
        {
            if (o == 5)
            {
                return{ branchPrime, branchPrime };
            }
            else
            {
                return{ utilities::reverse(branchPrime), utilities::reverse(branchPrime) };
            }
        }

        // Determine the first maximum for the signalPrime0
        int bO = 0, eO = 0, bSO = 0, eSO = 0;
        std::vector<double> weigth = { 0.8, 0.9, 1, 0.9, 0.8 };
        


		// MiRNAs' ens's (in the stem-loop, not in the sequence!)
        // Optimal	
        int    tempInd = MIN_MIRNA_LENGTH;
		double tempMax = signalPrime0[tempInd];
		for (size_t i = tempInd; i < signalPrime0.size() ; ++i)
		{
			if ( signalPrime0[i] > tempMax)
			{
				tempMax = signalPrime0[i];
				tempInd = i;
			}
		}
        eO = tempInd;
		 
		// Sub-optimal
        if (eO != MIN_MIRNA_LENGTH) { tempInd = MIN_MIRNA_LENGTH; }
        else { tempInd = MIN_MIRNA_LENGTH + 1; }
		tempMax = signalPrime0[tempInd];
        for (size_t i = tempInd; i < signalPrime0.size(); ++i)
        {
            if (signalPrime0[i] > tempMax && (i != eO)  && (i != eO - 1) && (i != eO + 1))
            {
                tempMax = signalPrime0[i];
                tempInd = i;
            }
        }
        eSO = tempInd;









		// MiRNAs' begins's (in the stem-loop, not in the sequence!) - [ eO - MAX_MIRNA_LENGTH, e0 - MIN_MIRNA_LENGTH ]
        // Optimal
        tempInd = std::max(eO - MAX_MIRNA_LENGTH, 0);
        tempMax = signalPrime1[tempInd];
        for (size_t i = tempInd; i <= eO - MIN_MIRNA_LENGTH; ++i)
        {
            if ( signalPrime1[i] > tempMax)
            {
                tempMax = signalPrime1[i];
                tempInd = i;
            }
        }
        bO = tempInd;

        // Sub-optimal
        tempInd = std::max(eSO - MAX_MIRNA_LENGTH, 0);
        tempMax = signalPrime1[tempInd];
        for (size_t i = tempInd; i <= eSO - MIN_MIRNA_LENGTH; ++i)
        {
            if ( signalPrime1[i] > tempMax)
            {
                tempMax = signalPrime1[i];
                tempInd = i;
            }
        }
        bSO = tempInd;








        // Final result
        if (o == 5)
        {
            return { branchPrime.substr(bO, eO - 2 - bO), branchPrime.substr(bSO, eSO - 2 - bSO) };
        }
        else
        {
            return { utilities::reverse(branchPrime.substr(bO, eO - 2 - bO)), utilities::reverse(branchPrime.substr(bSO, eSO - 2 - bSO)) };
        }
    }
        """


if __name__ == "__main__":
    hp5s = get_hairpin5_objects("datasets/miRBase/rel.22.1/!Converted/miRNA.human.str").values()

    mhmm = MHMM()
    mhmm.training_model_by_file(f"datasets/miRBase/rel.22.1/!Converted/miRNA.human.str", "hairpin5")
    mhmm.classify_mirnas_by_model(5,
                                  "uccugu--ccgcaccucAGUGGAUGUAUGCCAUGAUGAUAagauauca",
                                  "uggacaugggcguggAAUCGACUACAUGUGG-GCCACUauccuaaag-")


