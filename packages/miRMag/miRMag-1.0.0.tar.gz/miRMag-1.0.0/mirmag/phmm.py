#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

from mirmag.logger import get_logger
from mirmag.matrix import Matrix
from mirmag.stemloop import Hairpin3
from mirmag.utils import get_hairpin5_objects, get_hairpin3_objects, get_hairpindb_objects


logger = get_logger(logger_name="phmm", log_to_console=True)


class PHMM:
    """ Class to describe pre-miRNA sequences. Based on the Hidden Markov Model.
        Class contains methods to train the model and to classify the putative pre-miRNA.

    Parameters
    ----------
    file_name : str
        The name of the file with the training dataset.

    file_type : str
        The type of the input data: Hairpin5 or Hairpin3 or HairpinDB.

    model_type : int
        The type of the model: with begin state (type 1) OR without begin state (type 2, preferred).

    Returns
    -------
    PHMM object : object
        The HMM-object to classify pre-miRNAs.
    """

    def __init__(self):
        """ Model structure: States {S(optional), A, C, G, U/T, -} and observations {Helix/T, Loop/F}. """
        self.t_table = Matrix(m=6, n=6)     # Initial transition table [6 x 6]
        self.e_table = Matrix(m=6, n=2)     # Initial emission table [6 x 2]
        self.model_type = 2                 # Initial model type (without begin and end states)

    def training_model_by_file(self, file_name: str, file_type: str, model_type: int = 2) -> None:
        """ Выполнить обучение СММ по данным из файла. Данные могут быть в Hairpin5, Hairpinp3 или HairpinDB-форматах.

        :param file_name: Файл с данными для обучения.
        :param file_type: Тип данных в файле для обучения. Строка "hairpin5", "hairpin3" или "hairpindb".
        :param model_type: Тип модели - 1 (с начальным состоянием), 2 (без начального состояния, предпочтительный).
        :return: None.
        """

        self.model_type = model_type

        if file_type.lower() == "hairpin5":
            premirnas = [Hairpin3(hp5=hp5) for hp5 in get_hairpin5_objects(file_name).values()]
        elif file_type.lower() == "hairpin3":
            premirnas = get_hairpin3_objects(file_name).values()
        elif file_type.lower() == "hairpindb":
            premirnas = [Hairpin3(hpdb=hpdb) for hpdb in get_hairpindb_objects(file_name).values()]
        else:
            raise Exception(f"Incorrect file type. File: {file_name}, type: {file_type}, model: {model_type}.")

        for hp3 in premirnas:
            sequence = hp3.get_p5() + hp3.get_p3()[::-1]
            structure = hp3.get_str() + hp3.get_str()[::-1]

            if self.model_type == 1:
                """ Вариант модели 1: У модели ЕСТЬ стартовое состояние 0, НЕТ конечного состояния. 
                    Направление перехода: из curr_state в next_state, в next_state порождается символ.
                """
                curr_state = 0  # Begin/Initial state of the model
                for index in range(len(sequence)):
                    next_state = self.get_state(sequence[index])
                    self.t_table.inc_value(curr_state, next_state)
                    self.e_table.inc_value(next_state, self.get_index(structure[index]))
                    curr_state = next_state

            elif self.model_type == 2:
                """ Вариант модели 2 (предпочтительный): У модели НЕТ стартового состояния, НЕТ конечного состояния. 
                    Направление перехода: из curr_state в next_state, в curr_state порождается символ.
                """
                for index in range(0, len(sequence) - 1):
                    curr_state = self.get_state(sequence[index])
                    next_state = self.get_state(sequence[index + 1])
                    self.t_table.inc_value(curr_state, next_state)
                    self.e_table.inc_value(curr_state, self.get_index(structure[index]))
                self.e_table.inc_value(self.get_state(sequence[-1]), self.get_index(structure[-1]))

            else:
                raise Exception(f"Incorrect type of model. File: {file_name}, type: {file_type}, model: {model_type}.")

        # Нормировка таблиц СММ
        self.t_table.normalize(partial=False)
        self.e_table.normalize(partial=True)

    def training_model_by_dataset(self) -> None:
        """ TODO: заполнить таблицы СММ данными после процесса обучения. """
        self.t_table = Matrix()
        self.e_table = Matrix()
        self.model_type = 2

    def classify_hairpin_by_model(self, hp3: Hairpin3, threshold: float) -> (bool, float):
        """ Классификация кандидата Пре-миРНК соотвественно заданному порогу.
            Чем задается больше значение порога - тем больше предсказывается кандидатов (т.к. log10).

        :param hp3: Putative precursor in Hairpin3-format.
        :param threshold: Threshold.
        :return: Classification status (True / False) and precursor score accordingly to the model.
        """

        sequence = hp3.get_p5() + hp3.get_p3()[::-1]
        structure = hp3.get_str() + hp3.get_str()[::-1]

        score = 0.0

        if self.model_type == 1:
            """ Вариант предсказания по модели #1 (с начальным состоянием). """
            curr_state = 0
            for index in range(len(sequence)):
                next_state = self.get_state(sequence[index])
                score += math.log10(self.t_table.get_value(curr_state, next_state))
                score += math.log10(self.e_table.get_value(next_state, self.get_index(structure[index])))
                curr_state = next_state

        elif self.model_type == 2:
            """ Вариант предсказания по модели #2 (без начального состояния, предпочтительный). """
            for index in range(0, len(sequence) - 1):
                curr_state = self.get_state(sequence[index])
                next_state = self.get_state(sequence[index + 1])
                score += math.log10(self.t_table.get_value(curr_state, next_state))
                score += math.log10(self.e_table.get_value(curr_state, self.get_index(structure[index])))
            score += math.log10(self.e_table.get_value(self.get_state(sequence[-1]), self.get_index(structure[-1])))

        else:
            raise Exception(f"Incorrect model type. Type: {self.model_type}.")

        # Проверка score соответственно заданному порогу
        score = (-1) * score / len(hp3.get_p5())
        return (True, score) if score <= threshold else (False, score)

    @staticmethod
    def get_state(c):
        if c in "aA":
            return 1
        elif c in "uUtT":
            return 2
        elif c in "gG":
            return 3
        elif c in "cC":
            return 4
        elif c in "-":
            return 5
        else:
            return 5    #//!< Wrong symbols, return to X state >!// #

    @staticmethod
    def get_index(c):
        return int(c == "|")

    def __str__(self):
        return f"Матрица переходов между состояниями:\n{self.t_table}\n\nМатрица порождения элементов:\n{self.e_table}"


if __name__ == "__main__":
    """ Examples / Use cases. """

    # Training
    phmm = PHMM()
    phmm.training_model_by_file(file_name="datasets/miRBase/rel.22.1/miRNA.str", file_type="hairpin5", model_type=2)
    print(phmm)

    # Validate
    putative_premirnas = get_hairpin5_objects(file_name="datasets/miRBase/rel.22.1/miRNA.str")
    for hp5 in putative_premirnas.values():
        hp3 = Hairpin3(hp5=hp5)
        print(phmm.classify_hairpin_by_model(hp3=hp3, threshold=1.79))
