Dollop
=======

Dollop is a Python library for splitting up iterables into smaller portions 🥣.

Dollop preserves type, so dolloping a string yields substrings, dolloping a tuple yields subtuples, etc.


Installation
------------

.. code-block:: bash

   pip install dollop


Usage
-----

Here are some quick examples on how to use Dollop!

.. code-block:: python

    from dollop import serve

    for serving in serve('Dolloping all day long', serving_size=6):
        print(serving)

    for serving in serve((1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89), n_servings=4):
        print(serving)

Output:

.. code-block:: bash

    Dollop
    ing al
    l day 
    long
    (1, 1, 2)
    (3, 5, 8)
    (13, 21, 34)
    (55, 89)

