# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0

__version__ = '0.3.1'


import re
import coverage

from coverage import env
from coverage.misc import join_regex


class ExcludeUntilPlugin(coverage.plugin.CoveragePlugin):

    def __init__(self, options):
        super(ExcludeUntilPlugin, self).__init__()
        if 'marker' in options:
            self._marker = options['marker']
        else:
            self._marker = '# = exclude above lines ='

    def marker(self):
        return self._marker


def patched_lines_matching(self, *regexes):
    """Find the lines matching one of a list of regexes.

    Returns a set of line numbers, the lines that contain a match for one
    of the regexes in `regexes`.  The entire line needn't match, just a
    part of it.

    """
    combined = join_regex(regexes)
    if env.PYVERSION[0] < 3:
        combined = combined.decode("utf8")

    exclude_until_marker = ''
    if 'ExcludeUntilPlugin' in combined:
        plugin_match = re.search('\(\?\:ExcludeUntilPlugin([^\)]+)\)', combined)
        if plugin_match:
            exclude_until_marker = plugin_match.group(1)
        combined = combined.replace('ExcludeUntilPlugin', '')
    regex_c = re.compile(combined)
    matches = set()
    for i, line_text in enumerate(self.lines, start=1):
        match = regex_c.search(line_text)
        if match:
            if exclude_until_marker and match.group(0) == exclude_until_marker:
                matches.update(range(1, i))
            else:
                matches.add(i)

    return matches


def patched_get_data(self):
    """Get the collected data.

    Also warn about various problems collecting data.

    Returns a :class:`coverage.CoverageData`, the collected coverage data.

    .. versionadded:: 4.0

    """
    self._init()
    self._init_data(suffix=None)
    self._post_init()

    plugin_name = 'exclude_until_coverage_plugin.ExcludeUntilPlugin'
    if plugin_name in self._plugins.names:
        exclude_until_plugin = self._plugins.get(plugin_name)
        exclude_until_marker = 'ExcludeUntilPlugin{0}'.format(exclude_until_plugin.marker())
        if exclude_until_marker not in self.config.exclude_list:
            self.config.exclude_list.append(exclude_until_marker)

    if self._collector and self._collector.flush_data():
        self._post_save_work()

    return self._data


coverage.control.Coverage.get_data = patched_get_data
coverage.parser.PythonParser.lines_matching = patched_lines_matching
