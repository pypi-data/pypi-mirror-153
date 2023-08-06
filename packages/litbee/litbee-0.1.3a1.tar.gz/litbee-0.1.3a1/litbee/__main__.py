"""Run streamlit run app.py from __main__.py."""
# pylint: disable=no-value-for-parameter
import sys

from pathlib import Path
from streamlit import cli

app = Path(__file__).with_name("app.py")
assert app.is_file, f"{app} does not exist or is not a file."

sys.argv = ["streamlit", "run", app]
sys.exit(cli.main())
