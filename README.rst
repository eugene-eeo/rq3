rq3
===

stupidly inefficient grayscale image smoothing using quadtrees and elementary
statistics knowledge. the idea is that you take an ``m * n`` matrix of darkness
values and supply a target standard deviation (call this ``s``). The algorithm
is simple:

.. image:: media/quadtree.png

- if the standard deviation of all the darkness values within an ``x * y``
  region ``<= s``, said region will be represented using the arithmetic mean
  of the values.

- else, the ``x * y`` region is partitioned into 4 ``x/2 * y/2`` regions and
  step 1 is repeated on this region. eventually you may in the worst case end
  up with a quadtree of maximum depth of around ``log2(n) + 1``.

- said quadtree can then be traversed and the image will be the result of
  recursively joining the nodes of the quadtree together.

todo
----

- clean up code
- test against different distributions
- different heurestics instead of just stdev
- maybe use random partitioning
