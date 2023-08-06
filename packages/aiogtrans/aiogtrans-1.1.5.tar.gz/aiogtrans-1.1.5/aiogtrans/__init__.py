"""
Free Google Translate API for Python. Translates totally free of charge.

Forked by _Leg3ndary after original project was abandoned.

Licensed Under MIT
------------------

Copyright (c) 2022 Ben Z

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""

__all__ = ("HttpXTranslator", "AiohttpTranslator")

# Client
from aiogtrans.httpxclient import HttpXTranslator
from aiogtrans.aiohttpclient import AiohttpTranslator

# Constants
from aiogtrans.constants import LANGCODES, LANGUAGES

# Models for typehinting
from aiogtrans.models import Translated, Detected
