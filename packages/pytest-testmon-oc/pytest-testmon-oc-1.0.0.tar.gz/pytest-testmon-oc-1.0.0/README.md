# Testmon OC

This is a pytest plug-in fork from [testmon](https://testmon.org).
Testmon OC only tests affected by recent changes. 
Not re-run for test failed before.

## Quickstart

    pip install pytest-testmon

    # build the dependency database and save it to .testmondata
    pytest --testmon

    # change some of your code (with test coverage)

    # only run tests affected by recent changes
    pytest --testmon

To learn more about different options you can use with testmon, please
head to [testmon.org](https://testmon.org)
