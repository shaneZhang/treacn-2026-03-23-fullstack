#!/usr/bin/env python3
"""
Compatibility patch for pkg_resources with Python 3.13+
"""
import pkgutil

# Add missing ImpImporter alias for Python 3.13+ compatibility
if not hasattr(pkgutil, 'ImpImporter'):
    # In Python 3.13, ImpImporter was removed, use zipimporter as a fallback
    # or create a dummy class to avoid import errors
    class _DummyImpImporter:
        def __init__(self, *args, **kwargs):
            pass
    
    pkgutil.ImpImporter = _DummyImpImporter
