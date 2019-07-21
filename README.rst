Company matching
================

Introduction
------------

Company matching is a Python module made to match companies' names and is distributed under the MIT license. Sometimes we receive files from customers where the names of the companies appear in different forms. We must then try to find matches to simplify processing.

Installation
------------

pip install company-matching

Example
-------

.. code-block:: python

   from companymatching.DefaultMatching import DefaultMatching

   def similar_names(self, lhs, rhs):
     name_matching = DefaultMatching()
     result = name_matching.match(lhs, rhs)
     return result.score > 80

Concept
-------

This module is built like a pipeline. You define the different steps your candidates will go through in order to detect possible matches and the level of false positives you want to obtain.

By default, here are all the steps that are performed:
 - Normalization of unicode characters and suppression of accents.
 - Deletion of meaningless characters.
 - Character management of '.' or '&' misplaced.
 - Strict comparison using Levenshtein distance.
 - Test for the presence of initials.
 - Categorization of the token in the company name according to whether it is an abbreviation of a legal form (corp.), a legal form (limited liability company) or a common word (eg: tree, piano).
 - Correspondence of the abbreviation and the long form of the legal forms.
 - Comparison of legal forms.
 - Correspondence of the '&' with 'and'.
 - Correspondence of abbreviations of known words (eg: pvt - private).
 - Comparison of words (with typography using Levenshtein distance).

You have 3 types of steps that you can put in your pipeline which are derived from the mixin present in `base.py`:

Normalizer
^^^^^^^^^^

They have for definition:

.. code-block:: python

   def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):

The default behaviour consists to return the `lhs` and `rhs` unchanged. This is used to apply a treatment on company names such as removing accents for example.

Comparer
^^^^^^^^

They have for definition:

.. code-block:: python
   
   def compare(self, lhs, rhs, original_lhs, original_rhs, **parameters):

The default behaviour consists to return `None` if no matching was possible. This allows a comparison function to be applied to the current state of company names, such as the Levenshtein distance. If it looks like a match, it produces a `MatchingResult` which is made of a score and additional arguments depending on which step the match was made.

Matcher
^^^^^^^

They have for default behaviour:

.. code-block:: python

   def match(self, lhs, rhs, original_lhs, original_rhs, **parameters):
      new_lhs, new_rhs = self.normalize(lhs, rhs, original_lhs, original_rhs, **parameters)
      return self.compare(new_lhs, new_rhs, original_lhs, original_rhs, **parameters), new_lhs, new_rhs

The aim consists to apply first the normalization process of the current step and, then, the comparison according to this step. Finally, it returns a result of the `compare` function and the normalized string to the next step. One needs to use this mixin in particular if they don't want the result of the normalization to be kept and passed through the next step.

The different steps are applied until any of these `compare` produce a `MatchingResult` (something different than None). Each step owns a special member variable called: `additional_flag` which can be used to mark by which step the result went through, like "Translation" for instance. Depending on the country of the companies' names, you could chose the steps to apply.

Depending on your needs, you must thus construct a pipeline with the different steps that you want. By default, the steps try many different things which may be time consuming.
The pipeline can also be configured through the default parameters or on demand by giving additional arguments to the matching function.

Results
-------

By default, the results may have those flags (which can be combined):
 - Abbreviation: A common abbreviation was used in one company name but not in the other one. Like "Test brothers" and "Test bros".
 - Additional: When the number of legal forms do not match. Like "Test limited corporation" and "Test ltd".
 - Exact: Common words have no typography within. Like "Test LLC" and "Test limited liability corporation".
 - Initials: Initials were present. Like "TT" and "Test Test".
 - Shorthand: If the long form of the entity legal forms were present in the other one as abbreviations. Like "Test LLC" and "Test limited liability corporation".
 - Synonym: Some "same" legal forms may have different abbreviations. In Belgium, "SA" and "NV" have the same meaning, same goes with corp, co, at the international ...
 - Translation: If the name could be matched if the translation was applied.
 - Transliteration: If the name could be matched if the transliteration was applied.
 - Typography: Common words have at least one typography within. Like "Tast LLC" and "Test limited liability corporation".

License
-------

Distributed under MIT license. Written by `Youri Hubaut <https://github.com/Gawaboumga>`__.
