#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Python 3.13+ compatibility patch for pkg_resources
import pkgutil
if not hasattr(pkgutil, 'ImpImporter'):
    # Create a dummy class for compatibility with older packages
    class _DummyImpImporter:
        def __init__(self, *args, **kwargs):
            pass
    pkgutil.ImpImporter = _DummyImpImporter


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QTribe.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
