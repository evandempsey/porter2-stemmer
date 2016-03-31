===============================
Porter2 Stemmer
===============================

.. image:: https://travis-ci.org/evandempsey/porter2-stemmer.svg
        :target: https://travis-ci.org/evandempsey/porter2-stemmer

.. image:: https://img.shields.io/pypi/v/porter2stemmer.svg
        :target: https://pypi.python.org/pypi/porter2stemmer


An implementation of the Porter2 English stemming algorithm.

* Free software: BSD license
* Documentation: http://porter2-stemmer.readthedocs.org/

What is stemming?
*****************

Stemming is a technique used in Natural Language Processing to reduce different inflected forms of words to a single
invariant root form. The root form is called the stem and may or may not be identical to the morphological root of the
word.

What is it good for?
********************

Lots of things, but query expansion in information retrieval is the canonical example. Let's say you are building a
search engine. If someone searches for "cat" it would be nice if they were shown documents that contained the word "cats"
too. Unless the query and document index are stemmed, that won't happen. Stemming can be thought of as a method to reduce
the specificity of queries in order to pull back more relevant results. As such, it involves a trade-off.

What type of stemmer is this?
*****************************

Porter2 is a suffix-stripping stemmer. It transforms words into stems by applying a deterministic sequence of
changes to the final portion of the word. Other stemmers work differently. They may, for instance, simply look up
the inflected form in a table and map it to a morphological root, or they may use a clustering approach to
map diverse forms to a centre form. Different approaches have different advantages and disadvantages.

How do I use it?
****************

Very simply. Import it, instantiate a stemmer, and away you go::

    from porter2stemmer import Porter2Stemmer
    stemmer = Porter2Stemmer()
    print(stemmer.stem('conspicuous'))
