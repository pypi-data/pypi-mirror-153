###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import txaio

txaio.use_twisted()

from ._version import __version__  # noqa
from ._exception import InvalidConfigException  # noqa
from .common import address  # noqa
from .common import uint256, unpack_uint256, pack_uint256  # noqa
from .common import uint128, unpack_uint128, pack_uint128  # noqa
from .common import uint64, unpack_uint64, pack_uint64  # noqa
from . import meta, mrealm, xbr, xbrmm, xbrnetwork  # noqa
from . import globalschema, mrealmschema, cookiestore, realmstore  # noqa

__all__ = (
    '__version__',
    'meta',
    'mrealm',
    'cookiestore',
    'realmstore',
    'xbr',
    'xbrmm',
    'xbrnetwork',
    'address',
    'uint256',
    'pack_uint256',
    'unpack_uint256',
    'uint128',
    'pack_uint128',
    'unpack_uint128',
    'uint64',
    'pack_uint64',
    'unpack_uint64',
    'globalschema',
    'mrealmschema',
    'InvalidConfigException',
)
