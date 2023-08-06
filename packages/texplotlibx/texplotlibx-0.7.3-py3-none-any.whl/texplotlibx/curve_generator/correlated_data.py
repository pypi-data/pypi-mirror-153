from .curve_generator import _tpl_curve_generator


class _tpl_curve_generator_correlated_data(_tpl_curve_generator):
  _identifiers = (
    "correlated data",
    "lines and points",
    "lines + points",
    "pointslines"
  )

  def _get_draw(self):
    color = "=%s" % self.curve.color.get_value() if self.curve.color.get_value() is not None else ""
    return "draw%s," % color
