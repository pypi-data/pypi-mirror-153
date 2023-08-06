from .curve_data import _tpl_curve_data
from .curve_generator.curve_generator import _tpl_curve_generator
from .curve_generator.get_generator import _get_generator


class _tpl_curve:
  def __init__(self, *args, **kwargs):
    self.__data = _tpl_curve_data(*args, **kwargs)
    self.__generator = _tpl_curve_generator(self.__data)

  def _set_plottype(self, plottype: str = 'xy'):
    gen_cls = _get_generator(plottype)
    if gen_cls is not None:
      self.__generator = gen_cls(self.__data)

  def _get_addplot_code(self):
    return self.__generator._get_addplot_code()
