from .curve_generator import _tpl_curve_generator
from .ybar import _tpl_curve_generator_ybar, _tpl_curve_generator_ybarinterval
from .lines import _tpl_curve_generator_lines
from .correlated_data import _tpl_curve_generator_correlated_data


__subclasses = (
  _tpl_curve_generator,
  _tpl_curve_generator_ybar,
  _tpl_curve_generator_ybarinterval,
  _tpl_curve_generator_lines,
  _tpl_curve_generator_correlated_data
)


def _get_generator(plottype: str):
  for sc in __subclasses:
    for identifier in sc._identifiers:
      if plottype.lower() == identifier.lower():
        return sc
  print(f"Cannot identify plottype \"{type}\". Keeping previous type (default: xy).")
  return None
