from .          import _player, _animal, _oikad
from .classType import ByteFlag


Player = _player.Permission()

# animal
Cat = _animal._cat.Permission()

# oikad
Pain       = _oikad._pain      .Permission()
Unrest     = _oikad._unrest    .Permission()
Resentment = _oikad._resentment.Permission()

ByteFlag.package()

del _player, _animal, _oikad