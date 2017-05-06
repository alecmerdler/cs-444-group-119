from philo import numPhilos, philos, forks, askWaiter, Philosopher, Fork


def test_prevents_deadlock():
    """ Test that deadlock does not occur if each philosopher is holding exactly one fork.
    """

    for i in range(0,numPhilos):
        philos.append(Philosopher(i))
        forks.append(Fork(i))

    # Lock all forks, causing deadlock
    for fork in forks:
        fork.lock.acquire(False)

    for philo in philos:
        philo.start()


test_prevents_deadlock()