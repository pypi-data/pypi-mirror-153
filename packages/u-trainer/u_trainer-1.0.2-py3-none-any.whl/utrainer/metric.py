# -*- coding: utf8 -*-
#
from abc import ABC, abstractmethod
from typing import Dict


class Metric(ABC):

    @abstractmethod
    def step(self, inputs):
        raise NotImplementedError

    @abstractmethod
    def score(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def report(self) -> Dict:
        raise NotImplementedError
