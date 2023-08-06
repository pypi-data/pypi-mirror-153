"""
Fast Queue (short fque) is a simplified version of the built in queue.Queue with basic functionality but higher
performance. Fast queue runs 10x faster than the standard queue implementation by relying on pythons builtin deque and
implementing just the minimum needed locks.

Author: Perry Technologies
"""
from fque.fque import Queue
