import pytest

from hbayes.bayesian_optimization import Queue


@pytest.mark.unittest
def test_add():
    queue = Queue()

    assert len(queue) == 0
    assert queue.empty

    queue.add(1)
    assert len(queue) == 1

    queue.add(1)
    assert len(queue) == 2

    queue.add(2)
    assert len(queue) == 3


@pytest.mark.unittest
def test_queue():
    queue = Queue()

    with pytest.raises(StopIteration):
        next(queue)

    queue.add(1)
    queue.add(2)
    queue.add(3)

    assert len(queue) == 3
    assert not queue.empty

    assert next(queue) == 1
    assert len(queue) == 2

    assert next(queue) == 2
    assert next(queue) == 3
    assert len(queue) == 0


if __name__ == '__main__':
    r"""
    CommandLine:
        python test/test_observer.py
    """
    pytest.main([__file__])
