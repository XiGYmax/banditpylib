from typing import List, Tuple, Set, Optional

import numpy as np

from banditpylib.bandits import search_best_assortment, Reward, search, \
    local_search_best_assortment
from .utils import OrdinaryMNLLearner


class EpsGreedy(OrdinaryMNLLearner):
  r"""Epsilon-Greedy policy

  With probability :math:`\frac{\epsilon}{t}` do uniform sampling and with the
  remaining probability serve the assortment with the maximum empirical reward.
  """
  def __init__(self,
               revenues: np.ndarray,
               horizon: int,
               reward: Reward,
               card_limit=np.inf,
               name=None,
               use_local_search=False,
               random_neighbors=10,
               eps=1.0):
    """
    Args:
      revenues: product revenues
      horizon: total number of time steps
      reward: reward the learner wants to maximize
      card_limit: cardinality constraint
      name: alias name
      use_local_search: whether to use local search for searching the best
        assortment
      random_neighbors: number of random neighbors to look up if local search is
        used
      eps: epsilon
    """
    super().__init__(
        revenues=revenues,
        horizon=horizon,
        reward=reward,
        card_limit=card_limit,
        name=name,
        use_local_search=use_local_search,
        random_neighbors=random_neighbors)
    if eps <= 0:
      raise Exception('Epsilon %.2f in %s is no greater than 0!' % \
          (eps, self.__name))
    self.__eps = eps

  def _name(self) -> str:
    """
    Returns:
      default learner name
    """
    return 'epsilon_greedy'

  def reset(self):
    """Reset the learner

    .. warning::
      This function should be called before the start of the game.
    """
    # current time step
    self.__time = 1
    # current episode
    self.__episode = 1
    # number of episodes a product is served until the current episode
    # (exclusive)
    self.__serving_episodes = np.zeros(self.product_num() + 1)
    # number of times the customer chooses a product until the current time
    # (exclusive)
    self.__customer_choices = np.zeros(self.product_num() + 1)
    self.__last_actions = None
    self.__last_feedback = None

  def em_preference_params(self) -> np.ndarray:
    """
    Returns:
      empirical estimate of preference parameters
    """
    # unbiased estimate of preference parameters
    unbiased_est = self.__customer_choices / self.__serving_episodes
    unbiased_est[np.isnan(unbiased_est)] = 1
    unbiased_est = np.minimum(unbiased_est, 1)
    return unbiased_est

  def select_ramdom_assort(self) -> Set[int]:
    assortments: List[Set[int]] = []
    search(assortments=assortments,
           product_num=self.product_num(),
           next_product_id=1,
           assortment=set(),
           card_limit=self.card_limit())
    # pylint: disable=no-member
    return assortments[int(np.random.randint(0, len(assortments)))]

  def actions(self, context=None) -> Optional[List[Tuple[Set[int], int]]]:
    """
    Returns:
      assortments to serve
    """
    del context
    if self.__time > self.horizon():
      self.__last_actions = None
    else:
      # check if last observation is not a non-purchase
      if self.__last_feedback and self.__last_feedback[0][1][0] != 0:
        return self.__last_actions
      # When a non-purchase observation happens, a new episode is started and
      # a new assortment to be served is calculated

      # pylint: disable=no-member
      # with probability eps/t, randomly select an assortment to serve
      if np.random.random() <= self.__eps / self.__time:
        self.__last_actions = [(self.select_ramdom_assort(), 1)]
        return self.__last_actions

      self.reward.set_preference_params(self.em_preference_params())
      # calculate assortment with the maximum reward using optimistic
      # preference parameters
      if self.use_local_search:
        _, best_assortment = local_search_best_assortment(
            reward=self.reward,
            random_neighbors=self.random_neighbors,
            card_limit=self.card_limit(),
            init_assortment=(
                self.__last_actions[0][0] if self.__last_actions else None))
      else:
        _, best_assortment = search_best_assortment(
            reward=self.reward, card_limit=self.card_limit())
      self.__last_actions = [(best_assortment, 1)]
    return self.__last_actions

  def update(self, feedback: List[Tuple[np.ndarray, List[int]]]):
    """Learner update

    Args:
      feedback: feedback returned by the bandit environment by executing
        :func:`actions`
    """
    self.__customer_choices[feedback[0][1][0]] += 1
    self.__last_feedback = feedback
    self.__time += 1
    if feedback[0][1][0] == 0:
      for product_id in self.__last_actions[0][0]:
        self.__serving_episodes[product_id] += 1
      self.__episode += 1
