# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
"""Exclude Until Coverage Plugin"""
from .exclude_until import ExcludeUntilPlugin


def coverage_init(reg, options):
    reg.add_file_tracer(ExcludeUntilPlugin(options))
