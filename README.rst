rqtree
======

stupidly inefficient grayscale image compression using quadtrees and elementary
statistics knowledge. the idea is that you take a square ``n * n`` matrix of
darkness values and supply a target standard deviation (call this ``s``). The
algorithm is simple::

    ┌───┬───┬───────┐
    │   │   │       │
    ├───┼─┬─┤       │
    │   ├─┼─┤       │
    ├─┬─┼─┼─┼─┬─┬───┤
    ├─┼─┼─┼─┼─┼─┤   │
    ├─┴─┼─┴─┼─┼─┼───┤
    │   │   ├─┼─┤   │
    └───┴───┴─┴─┴───┘

- if the standard deviation of all the darkness values within an ``x * x`` region
  is ``<= s``, then the ``x * x`` region will be represented using the arithmetic
  mean of the values.

- else, the ``x * x`` region is partitioned into 4 ``x/2 * x/2`` regions and
  step 1 is repeated on this region. eventually you may in the worst case end
  up with a quadtree of maximum depth of around ``log2(n)``.

- said quadtree can then be traversed and the image will be the result of
  recursively joining the nodes of the quadtree together. said result can
  also be scaled up or down, so it can also be used as a bad scalable
  graphics thing.

todo
----

- clean up code
- actually implement this
