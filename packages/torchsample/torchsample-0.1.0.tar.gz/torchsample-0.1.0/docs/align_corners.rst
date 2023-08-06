About Align Corners
===================

This serves to be a brief, but complete writeup on explaining what
``align_corners`` actually is, how it impacts interpolation, and
when we should set it or not. Unless otherwise specified,
``align_corners`` refers to PyTorch code.

TL;DR:  ``align_corners=False`` in pytorch is proper and generally better.


History
^^^^^^^
There's an `excellent writeup`_ by `@hollance`_ that explains the history
of ``align_corners`` in various frameworks. In summary:

1. **BAD:** TensorFlowV1 implemented bilinear resizing incorrect. When doubling
   resolution, this results in an image that shifts up one pixel and left
   one pixel. This also repeats the final row and column.
2. **So-so:** TensorFlow attempted to fix this in a backwards compatible way if
   the caller sets ``align_corners=True``. This implementation, unfortunately, is
   also incorrect. The distance between successive pixels depends on the size
   of the image. Intuitively, the distance between pixels should be fixed.
   PyTorch uses this semi-bugged implementation when ``align_corners=True``.
3. **GOOD:** PyTorch's ``align_corners=False`` is actually **different** from
   TensorFlow's. This is the "proper" way to bilinearly resize an image.


Explanation
^^^^^^^^^^^

The linked articles are in the context of resizing images, but I'm going
to present a pytorch example in the context of normalized coordinates to bring
it all together.

Consider a 2 pixel wide, 1 pixel tall image.
The left pixel has intensity value 100, and the right pixel has intensity value 200.
The value of a pixel is considered as a point at it's center, ``X``.

.. code-block::

                align_corners=False
     +-------------------+-------------------+
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |         X         |         X         |
     |    Value: 100     |    Value: 200     |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     +-------------------+-------------------+
    -1       -0.5        0        0.5        1   Norm. Coords.


                align_corners=True
     +-------------------+-------------------+
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |         X         |         X         |
     |    Value: 100     |    Value: 200     |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     +-------------------+-------------------+
             -1          0         1             Norm. Coords.


* ``align_corners=False`` coordinate system starts at the
  **left side** of the left-most pixel, and has it end at the
  **right side** of the right-most pixel.
* ``align_corners=True`` coordinate system starts at the
  **center** of the left-most pixel, and has it end at the
  **center** of the right-most pixel.

For ``align_corners=False``, what border values is it interpolating between?
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PyTorch has a ``padding_mode`` argument for querying border pixels. By
default, ``padding_mode="zeros"``, meaning that there's a border of
pixels with value ``0`` around the image. For example, sampling this
image at normalized coordinates ``(-1, -1)`` will sample the top
left corner of the left pixel. Due to bilinear interpolation with the
surrounding zero-padding, the resulting value would be ``1/4`` the
pixel's value; i.e. ``25``.

That sounds bad.
""""""""""""""""
`Probably, it is an actively researched topic`_.
In ``torchsample`` we change the default to ``padding_mode="border"``,
meaning that the padding has the same value as it's neighboring valid
pixel value.
With this padding mode, sampling at ``(-1, -1)`` would result in the full value ``100``.
The resulting sampled image/featuremap looks how one would expect it to look.



.. _@hollance: https://github.com/hollance
.. _Probably, it is an actively researched topic: https://arxiv.org/pdf/2010.02178.pdf
.. _excellent writeup: https://machinethink.net/blog/coreml-upsampling/
