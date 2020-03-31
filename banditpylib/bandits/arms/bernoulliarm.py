import numpy as np

from .utils import Arm


class BernoulliArm(Arm):
  """Class for Bernoulli arm

  .. inheritance-diagram:: BernoulliArm
    :parts: 1
  """

  def __init__(self, mean):
    """
    Args:
      mean (float): mean
    """
    self.__mean = mean

  @property
  def mean(self):
    return self.__mean

  def pull(self, pulls=1):
    return np.random.binomial(1, self.__mean, pulls)
