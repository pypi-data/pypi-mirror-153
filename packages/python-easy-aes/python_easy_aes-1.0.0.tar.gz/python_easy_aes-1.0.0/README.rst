===============
python-easy_aes
===============


.. image:: https://img.shields.io/pypi/v/python_easy_aes.svg
        :target: https://pypi.python.org/pypi/python_easy_aes


Easily encrypt/decrypt files/texts using AES. 
This library takes care of everything under the hood, including nist compliance, recommended settings, etc. 
So you can just plug and play.


* Free software: MIT license
* Documentation: https://python-easy-aes.readthedocs.io.


Features
--------

Encrypt messages/files
* Encrypt files using PBKDF2 and SHA-256 (NSA recommendation. Better known as level 8 security)
* Encrypt files using Scrypt (Industry and CISCO recommendation. Better known as level 9 security)
Decrypt them
No need to worry about the salt, the iv, etc.

Credits
-------
This package was coded in it\'s entirety by Aria Bagheri. But you can always contribute if you want! Just fork the project, have a go at it, and then submit a pull request!
Special thanks to all developers at pycryptodome, those that helped develop AES 256, and our protectors at NSA and CISCO for their recommendation guidelines. Without their amazing work, this project would not be here!
