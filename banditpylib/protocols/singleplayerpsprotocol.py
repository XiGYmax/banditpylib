from absl import flags

import numpy as np

from .utils import Protocol

FLAGS = flags.FLAGS

__all__ = ['SinglePlayerPEProtocol']


class SinglePlayerPEProtocol(Protocol):
  """single player pure exploration protocol
  """

  def __init__(self, pars=None):
    pass

  @property
  def type(self):
    return 'SinglePlayerPEProtocol'

  def __one_trial_fixbudget(self):
    results = []
    for budget in self._pars['budgets']:
      self.__budget = budget

      ##########################################################################
      # initialization
      self._bandit.reset()
      self._player.reset(self._bandit, self.__budget)
      ##########################################################################

      self._player.learner_round()
      if self._bandit.tot_samples > budget:
        raise Exception(
            '%s uses more than the given budget!' % self._player.name)
      regret = getattr(self._bandit, self._regret_funcname)(
          getattr(self._player, self._rewards_funcname)())
      results.append(dict({self._player.name: [budget, regret]}))
    return results

  def __one_trial_fixconf(self):
    results = []
    for fail_prob in self._pars['fail_probs']:
      self.__fail_prob = fail_prob

      ##########################################################################
      # initialization
      self._bandit.reset()
      self._player.reset(self._bandit, self.__fail_prob)
      ##########################################################################

      self._player.learner_round()
      regret = getattr(self._bandit, self._regret_funcname)(
          getattr(self._player, self._rewards_funcname)())
      results.append(
          dict({self._player.name:
                [fail_prob, self._bandit.tot_samples, regret]}))
    return results

  def _one_trial(self, seed):
    np.random.seed(seed)
    if 'FixBudget' in self._player.goal:
      return self.__one_trial_fixbudget()
    return self.__one_trial_fixconf()
