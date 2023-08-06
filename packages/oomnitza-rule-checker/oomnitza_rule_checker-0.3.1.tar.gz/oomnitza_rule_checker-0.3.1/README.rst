=====================
Oomnitza Rule Checker
=====================

Package contains reusable logic to check Oomnitza begin criteria for objects.

The ``check_rules`` handler used to check that the given document corresponds
to the given rules, e.g. matches them.


.. code-block:: python

    given_result = check_rules(
        {
            "rules": [],
            "groupOp": "and",
            "groups": [
                {
                    "groupOp": "and",
                    "rules": [
                        {
                            "op": "cn",
                            "data": "CC1UH",
                            "field": "ASSETS.serial_number",
                        }
                    ],
                    "groups": [],
                },
            ],
        },
        document={
            "equipment_id": "ad2c2ab54adb481c8436d6238838813a",
            "assigned_to": "2e84e8e99431411a84f2339bd02cacb0",
            "serial_number": "C02CC1UHMD6T1",
            "model": "MacBookPro16,1",
        },
        changed_values=None,
        object_type="dontcare",
    )

    assert given_result, "serial number matches"


The ``check_rule_by_op`` handler used to check that the given values satisfy
the specified operator, e.g. equal, begins_with, less_or_equal, etc.


.. code-block:: python

    assert check_rule_by_op(Op.LESS_OR_EQUAL, "1", "2")
    assert check_rule_by_op(Op.HAS_BEEN_CHANGED, "before", "after")
    assert not check_rule_by_op(Op.ENDS_WITH, "aaa", "b")


Development
-----------

Install package with or without test dependencies.

.. code-block:: shell

    python3 -m venv .venv
    source .venv/bin/activate
    pip install oomnitza_rule_checker
    pip install -e .[tests]


Feel free to write additional tests to cover the new changes and run test
suite.

.. code-block:: shell

    pytest


Distribution
------------


Build and upload the package to the PyPi repository.

.. code-block:: shell

    python setup.py sdist register upload

