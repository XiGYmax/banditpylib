from typing import List, Tuple, Optional

import math
import numpy as np

from banditpylib.arms import PseudoArm
from .utils import OrdinaryFBBAILearner


class SR(OrdinaryFBBAILearner):
  """Successive rejects policy :cite:`audibert2010best`"""
  def __init__(self, arm_num: int, budget: int, name: str = None):
    """
    Args:
      arm_num: number of arms
      budget: total number of pulls
      name: alias name
    """
    super().__init__(arm_num=arm_num, budget=budget, name=name)
    # calculate bar_log_K
    self.__bar_log_K = 0.5 + sum([1/i for i in range(2, self.arm_num() + 1)])
    if (budget - arm_num) < arm_num * self.__bar_log_K:
      raise Exception('Budget is too small.')

  def _name(self) -> str:
    """
    Returns:
      default learner name
    """
    return 'sr'

  def reset(self):
    """Reset the learner

    .. warning::
      This function should be called before the start of the game.
    """
    self.__pseudo_arms = [PseudoArm() for arm_id in range(self.arm_num())]
    # calculate pulls_per_round
    self.__pulls_per_round = [-1]
    nk = [0]
    for k in range(1, self.arm_num()):
      nk.append(
          math.ceil(1 / self.__bar_log_K * (self.budget() - self.arm_num()) /
                    (self.arm_num() + 1 - k)))
      self.__pulls_per_round.append(nk[k] - nk[k - 1])
    self.__active_arms = set(range(self.arm_num()))
    self.__budget_left = self.budget()
    self.__best_arm = None
    # current round
    self.__round = 1

  def actions(self, context=None) -> Optional[List[Tuple[int, int]]]:
    """
    Args:
      context: context of the ordinary bandit which should be `None`

    Returns:
      arms to pull
    """
    del context
    if self.__round >= self.arm_num():
      self.__last_actions = None
    else:
      if self.__round < self.arm_num() - 1:
        self.__last_actions = [(arm_id, self.__pulls_per_round[self.__round])
                               for arm_id in self.__active_arms]
      else:
        # use up the left budget when there are only two arms left
        pulls = [self.__budget_left // 2]
        pulls.append(self.__budget_left - pulls[0])
        self.__last_actions = [(list(self.__active_arms)[i], pulls[i])
                               for i in range(2)]
    return self.__last_actions

  def update(self, feedback: List[Tuple[Optional[np.ndarray], None]]):
    """Learner update

    Args:
      feedback: feedback returned by the bandit environment by executing
        :func:`actions`
    """
    for (ind, (rewards, _)) in enumerate(feedback):
      if rewards is not None:
        self.__pseudo_arms[self.__last_actions[ind][0]].update(rewards)
        self.__budget_left -= len(rewards)
    # remove the arm with the least mean
    arm_id_to_remove = min([(arm_id, self.__pseudo_arms[arm_id].em_mean)
                            for arm_id in self.__active_arms],
                           key=lambda x: x[1])[0]
    self.__active_arms.remove(arm_id_to_remove)
    if self.__round == self.arm_num() - 1:
      self.__best_arm = list(self.__active_arms)[0]
    self.__round += 1

  def best_arm(self) -> int:
    """
    Returns:
      best arm identified by the learner
    """
    if self.__best_arm is None:
      raise Exception('%s: I don\'t have an answer yet!' % self.name)
    return self.__best_arm
