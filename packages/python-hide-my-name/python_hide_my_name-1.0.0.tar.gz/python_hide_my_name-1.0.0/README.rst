============
python-hide-my-name
============


.. image:: https://img.shields.io/pypi/v/python_hide_my_name.svg
        :target: https://pypi.python.org/pypi/python_hide_my_name


I know how much of a struggle it is to find working proxies. Even the best websites sometimes give you proxies that don't work! So I made python-hide-my-name.
Automatically finds proxies from hidemy.name, tests them, and only gives you the ones that actually work!


* Free software: MIT license
* Documentation: https://python-hide-my-name.readthedocs.io.


Features
--------

Tests a single proxy for you!
Fetches as many proxies as you want for you! (Multithreading applied here. So yes it's fast!)
Tests those proxies! (Multithreading applied here as well. A lot less IO bottleneck!)
Returns the ones that do work!

Credits
-------
This package was coded in it\'s entirety by Aria Bagheri. But you can always contribute if you want! Just fork the project, have your go at it, and then submit a pull request!
Special thanks to hidemy.name. Without their amazing work, this project would not be here!
It is worth mentioning that hidemy.name regularly removes broken proxies from their website and their website is constantly updated with new proxies thanks to their ingenious 'spider robot'.
But between their proxy check intervals, there are proxies breaking and it is simply not feasible for them to update evey second.
That's where this tool comes in handy.
