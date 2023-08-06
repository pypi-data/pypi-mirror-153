========================
python-password-security
========================


.. image:: https://img.shields.io/pypi/v/python_password_security.svg
        :target: https://pypi.python.org/pypi/python_password_security


Helps you make sure your passwords follow [NSA's Network Infrastructure Security Guidance](https://media.defense.gov/2022/Mar/01/2002947139/-1/-1/0/CTR_NSA_NETWORK_INFRASTRUCTURE_SECURITY_GUIDANCE_20220301.PDF)

Note: This project is by no way, shape, or form involved with the NSA. It just took inspiration from their guidance.


* Free software: MIT license
* Documentation: https://python-password-security.readthedocs.io.


Features
--------

Checks if your password has been cracked before against a database of [11.8 billion breached passwords](https://haveibeenpwned.com/).
Checks if your password includes capital letters, lowercase letters, numbers, and special characters.
Checks if your password is a keyboard walk (hint: they are highly insecure and not smart at all!)
Allows you to disable any of the security measures if you like to take risks!

Credits
-------
This package was coded in it\'s entirety by Aria Bagheri. But you can always contribute if you want! Just fork the project, have your go at it, and then submit a pull request!
Special thanks to folks at haveibeenpwned.com, the FBI, and the NCA. Without their amazing work, this project would lack a good database of pwned passwords to check against.
Also, thanks to Rich Kelley for providing the open source community with the keyboard walk algorithm. While it still is a proof of concept, it saved me a lot of time, and tears.
