from philosopher import Philosopher, dining_philosophers


def test_prevents_deadlock():
    """ Test that deadlock does not occur if each philosopher is holding exactly one fork.
    """
