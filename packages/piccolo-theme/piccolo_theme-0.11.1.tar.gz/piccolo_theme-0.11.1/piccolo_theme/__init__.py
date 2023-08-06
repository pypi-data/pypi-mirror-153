import os
import typing as t

if t.TYPE_CHECKING:
    from sphinx.application import Sphinx


__VERSION__ = "0.11.1"


def setup(app: 'Sphinx'):
    """
    :param app:
        Passed by Sphinx.

    """
    app.add_html_theme(
        "piccolo_theme", os.path.abspath(os.path.dirname(__file__))
    )
