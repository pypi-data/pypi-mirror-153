#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8 ff=unix ft=python ts=4 sw=4 sts=4 si et
"""
pip-licenses

MIT License

Copyright (c) 2018 raimon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#
# Modified to be used within the eric-ide project.
#
# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

import argparse
import codecs
import glob
import json
import os
import sys
from collections import Counter
from email import message_from_string
from email.parser import FeedParser
from enum import Enum, auto
from typing import List, Optional, Sequence, Text


def get_installed_distributions(local_only=True, user_only=False):
    try:
        from pip._internal.metadata import get_environment
    except ImportError:
        # For backward compatibility with pip version 20.3.4
        from pip._internal.utils import misc
        return misc.get_installed_distributions(
            local_only=local_only,
            user_only=user_only
        )
    else:
        from pip._internal.utils.compat import stdlib_pkgs
        dists = get_environment(None).iter_installed_distributions(
            local_only=local_only,
            user_only=user_only,
            skip=stdlib_pkgs,
            include_editables=True,
            editables_only=False,
        )
        return [d._dist for d in dists]


__pkgname__ = 'pip-licenses'
__version__ = '3.5.4'
__author__ = 'raimon'
__license__ = 'MIT'
__summary__ = ('Dump the software license list of '
               'Python packages installed with pip.')
__url__ = 'https://github.com/raimon49/pip-licenses'


FIELD_NAMES = (
    'Name',
    'Version',
    'License',
    'LicenseFile',
    'LicenseText',
    'NoticeFile',
    'NoticeText',
    'Author',
    'Description',
    'URL',
)


DEFAULT_OUTPUT_FIELDS = (
    'Name',
    'Version',
)


SUMMARY_OUTPUT_FIELDS = (
    'Count',
    'License',
)


METADATA_KEYS = (
    'home-page',
    'author',
    'license',
    'summary',
    'license_classifier',
)

# Mapping of FIELD_NAMES to METADATA_KEYS where they differ by more than case
FIELDS_TO_METADATA_KEYS = {
    'URL': 'home-page',
    'Description': 'summary',
    'License-Metadata': 'license',
    'License-Classifier': 'license_classifier',
}


SYSTEM_PACKAGES = (
    __pkgname__,
    'pip',
    'setuptools',
    'wheel',
)

LICENSE_UNKNOWN = 'UNKNOWN'


def get_packages(args: "CustomNamespace"):

    def get_pkg_included_file(pkg, file_names):
        """
        Attempt to find the package's included file on disk and return the
        tuple (included_file_path, included_file_contents).
        """
        included_file = LICENSE_UNKNOWN
        included_text = LICENSE_UNKNOWN
        pkg_dirname = "{}-{}.dist-info".format(
            pkg.project_name.replace("-", "_"), pkg.version)
        patterns = []
        [patterns.extend(sorted(glob.glob(os.path.join(pkg.location,
                                                       pkg_dirname,
                                                       f))))
         for f in file_names]
        for test_file in patterns:
            if os.path.exists(test_file) and not os.path.isdir(test_file):
                included_file = test_file
                with open(test_file, encoding='utf-8',
                          errors='backslashreplace') as included_file_handle:
                    included_text = included_file_handle.read()
                break
        return (included_file, included_text)

    def get_pkg_info(pkg):
        (license_file, license_text) = get_pkg_included_file(
            pkg,
            ('LICENSE*', 'LICENCE*', 'COPYING*')
        )
        (notice_file, notice_text) = get_pkg_included_file(
            pkg,
            ('NOTICE*',)
        )
        pkg_info = {
            'name': pkg.project_name,
            'version': pkg.version,
            'namever': str(pkg),
            'licensefile': license_file,
            'licensetext': license_text,
            'noticefile': notice_file,
            'noticetext': notice_text,
        }
        metadata = None
        if pkg.has_metadata('METADATA'):
            metadata = pkg.get_metadata('METADATA')

        if pkg.has_metadata('PKG-INFO') and metadata is None:
            metadata = pkg.get_metadata('PKG-INFO')

        if metadata is None:
            for key in METADATA_KEYS:
                pkg_info[key] = LICENSE_UNKNOWN

            return pkg_info

        feed_parser = FeedParser()
        feed_parser.feed(metadata)
        parsed_metadata = feed_parser.close()

        for key in METADATA_KEYS:
            pkg_info[key] = parsed_metadata.get(key, LICENSE_UNKNOWN)

        if metadata is not None:
            message = message_from_string(metadata)
            pkg_info['license_classifier'] = \
                find_license_from_classifier(message)

        if args.filter_strings:
            for k in pkg_info:
                if isinstance(pkg_info[k], list):
                    for i, item in enumerate(pkg_info[k]):
                        pkg_info[k][i] = item. \
                            encode(args.filter_code_page, errors="ignore"). \
                            decode(args.filter_code_page)
                else:
                    pkg_info[k] = pkg_info[k]. \
                        encode(args.filter_code_page, errors="ignore"). \
                        decode(args.filter_code_page)

        return pkg_info

    pkgs = get_installed_distributions(
        local_only=args.local_only,
        user_only=args.user_only,
    )
    ignore_pkgs_as_lower = [pkg.lower() for pkg in args.ignore_packages]
    pkgs_as_lower = [pkg.lower() for pkg in args.packages]

    fail_on_licenses = set()
    if args.fail_on:
        fail_on_licenses = set(map(str.strip, args.fail_on.split(";")))

    allow_only_licenses = set()
    if args.allow_only:
        allow_only_licenses = set(map(str.strip, args.allow_only.split(";")))

    for pkg in pkgs:
        pkg_name = pkg.project_name

        if pkg_name.lower() in ignore_pkgs_as_lower:
            continue

        if pkgs_as_lower and pkg_name.lower() not in pkgs_as_lower:
            continue

        if not args.with_system and pkg_name in SYSTEM_PACKAGES:
            continue

        pkg_info = get_pkg_info(pkg)

        license_names = select_license_by_source(
            args.from_,
            pkg_info['license_classifier'],
            pkg_info['license'])

        if fail_on_licenses:
            failed_licenses = license_names.intersection(fail_on_licenses)
            if failed_licenses:
                sys.stderr.write(
                    "fail-on license {} was found for package "
                    "{}:{}".format(
                        '; '.join(sorted(failed_licenses)),
                        pkg_info['name'],
                        pkg_info['version'])
                )
                sys.exit(1)

        if allow_only_licenses:
            uncommon_licenses = license_names.difference(allow_only_licenses)
            if len(uncommon_licenses) == len(license_names):
                sys.stderr.write(
                    "license {} not in allow-only licenses was found"
                    " for package {}:{}".format(
                        '; '.join(sorted(uncommon_licenses)),
                        pkg_info['name'],
                        pkg_info['version'])
                )
                sys.exit(1)

        yield pkg_info


def create_licenses_list(
        args: "CustomNamespace", output_fields=DEFAULT_OUTPUT_FIELDS):
    
    licenses = []
    for pkg in get_packages(args):
        row = {}
        for field in output_fields:
            if field == 'License':
                license_set = select_license_by_source(
                    args.from_, pkg['license_classifier'], pkg['license'])
                license_str = '; '.join(sorted(license_set))
                row[field] = license_str
            elif field == 'License-Classifier':
                row[field] = ('; '.join(sorted(pkg['license_classifier']))
                           or LICENSE_UNKNOWN)
            elif field.lower() in pkg:
                row[field] = pkg[field.lower()]
            else:
                row[field] = pkg[FIELDS_TO_METADATA_KEYS[field]]
        licenses.append(row)

    return licenses


def create_summary_list(args: "CustomNamespace"):
    counts = Counter(
        '; '.join(sorted(select_license_by_source(
            args.from_, pkg['license_classifier'], pkg['license'])))
        for pkg in get_packages(args))

    licenses = []
    for license, count in counts.items():
        licenses.append({
            "Count": count,
            "License": license,
        })
    
    return licenses


def find_license_from_classifier(message):
    licenses = []
    for k, v in message.items():
        if k == 'Classifier' and v.startswith('License'):
            license = v.split(' :: ')[-1]

            # Through the declaration of 'Classifier: License :: OSI Approved'
            if license != 'OSI Approved':
                licenses.append(license)

    return licenses


def select_license_by_source(from_source, license_classifier, license_meta):
    license_classifier_set = set(license_classifier) or {LICENSE_UNKNOWN}
    if (from_source == FromArg.CLASSIFIER or
            from_source == FromArg.MIXED and len(license_classifier) > 0):
        return license_classifier_set
    else:
        return {license_meta}


def get_output_fields(args: "CustomNamespace"):
    if args.summary:
        return list(SUMMARY_OUTPUT_FIELDS)

    output_fields = list(DEFAULT_OUTPUT_FIELDS)

    if args.from_ == FromArg.ALL:
        output_fields.append('License-Metadata')
        output_fields.append('License-Classifier')
    else:
        output_fields.append('License')

    if args.with_authors:
        output_fields.append('Author')

    if args.with_urls:
        output_fields.append('URL')

    if args.with_description:
        output_fields.append('Description')

    if args.with_license_file:
        if not args.no_license_path:
            output_fields.append('LicenseFile')

        output_fields.append('LicenseText')

        if args.with_notice_file:
            output_fields.append('NoticeText')
            if not args.no_license_path:
                output_fields.append('NoticeFile')

    return output_fields


def create_output_string(args: "CustomNamespace"):
    output_fields = get_output_fields(args)

    if args.summary:
        licenses = create_summary_list(args)
    else:
        licenses = create_licenses_list(args, output_fields)
    
    return json.dumps(licenses)


class CustomHelpFormatter(argparse.HelpFormatter):  # pragma: no cover
    def __init__(
        self, prog: Text, indent_increment: int = 2,
        max_help_position: int = 24, width: Optional[int] = None
    ) -> None:
        max_help_position = 30
        super().__init__(
            prog, indent_increment=indent_increment,
            max_help_position=max_help_position, width=width)

    def _format_action(self, action: argparse.Action) -> str:
        flag_indent_argument: bool = False
        text = self._expand_help(action)
        separator_pos = text[:3].find('|')
        if separator_pos != -1 and 'I' in text[:separator_pos]:
            self._indent()
            flag_indent_argument = True
        help_str = super()._format_action(action)
        if flag_indent_argument:
            self._dedent()
        return help_str

    def _expand_help(self, action: argparse.Action) -> str:
        if isinstance(action.default, Enum):
            default_value = enum_key_to_value(action.default)
            return self._get_help_string(action) % {'default': default_value}
        return super()._expand_help(action)

    def _split_lines(self, text: Text, width: int) -> List[str]:
        separator_pos = text[:3].find('|')
        if separator_pos != -1:
            flag_splitlines: bool = 'R' in text[:separator_pos]
            text = text[separator_pos + 1:]
            if flag_splitlines:
                return text.splitlines()
        return super()._split_lines(text, width)


class CustomNamespace(argparse.Namespace):
    from_: "FromArg"
    order: "OrderArg"
    summary: bool
    local_only: bool
    user_only:bool
    output_file: str
    ignore_packages: List[str]
    packages: List[str]
    with_system: bool
    with_authors: bool
    with_urls: bool
    with_description: bool
    with_license_file: bool
    no_license_path: bool
    with_notice_file: bool
    filter_strings: bool
    filter_code_page: str
    fail_on: Optional[str]
    allow_only: Optional[str]


class CompatibleArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args: Optional[Sequence[Text]] = None,
                   namespace: CustomNamespace = None) -> CustomNamespace:
        args = super().parse_args(args, namespace)
        self._verify_args(args)
        return args

    def _verify_args(self, args: CustomNamespace):
        if args.with_license_file is False and (
                args.no_license_path is True or
                args.with_notice_file is True):
            self.error(
                "'--no-license-path' and '--with-notice-file' require "
                "the '--with-license-file' option to be set")
        if args.filter_strings is False and \
                args.filter_code_page != 'latin1':
            self.error(
                "'--filter-code-page' requires the '--filter-strings' "
                "option to be set")
        try:
            codecs.lookup(args.filter_code_page)
        except LookupError:
            self.error(
                "invalid code page '%s' given for '--filter-code-page, "
                "check https://docs.python.org/3/library/codecs.html"
                "#standard-encodings for valid code pages"
                % args.filter_code_page)


class NoValueEnum(Enum):
    def __repr__(self):  # pragma: no cover
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class FromArg(NoValueEnum):
    META = M = auto()
    CLASSIFIER = C = auto()
    MIXED = MIX = auto()
    ALL = auto()


class OrderArg(NoValueEnum):
    COUNT = C = auto()
    LICENSE = L = auto()
    NAME = N = auto()
    AUTHOR = A = auto()
    URL = U = auto()


def value_to_enum_key(value: str) -> str:
    return value.replace('-', '_').upper()


def enum_key_to_value(enum_key: Enum) -> str:
    return enum_key.name.replace('_', '-').lower()


def choices_from_enum(enum_cls: NoValueEnum) -> List[str]:
    return [key.replace('_', '-').lower()
            for key in enum_cls.__members__.keys()]


MAP_DEST_TO_ENUM = {
    'from_': FromArg,
    'order': OrderArg,
}


class SelectAction(argparse.Action):
    def __call__(
        self, parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Text,
        option_string: Optional[Text] = None,
    ) -> None:
        enum_cls = MAP_DEST_TO_ENUM[self.dest]
        values = value_to_enum_key(values)
        setattr(namespace, self.dest, getattr(enum_cls, values))


def create_parser():
    parser = CompatibleArgumentParser(
        description=__summary__,
        formatter_class=CustomHelpFormatter)

    common_options = parser.add_argument_group('Common options')
    format_options = parser.add_argument_group('Format options')
    verify_options = parser.add_argument_group('Verify options')

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + __version__)

    common_options.add_argument(
        '--from',
        dest='from_',
        action=SelectAction, type=str,
        default=FromArg.MIXED, metavar='SOURCE',
        choices=choices_from_enum(FromArg),
        help='R|where to find license information\n'
             '"meta", "classifier, "mixed", "all"\n'
             '(default: %(default)s)')
    common_options.add_argument(
        '-o', '--order',
        action=SelectAction, type=str,
        default=OrderArg.NAME, metavar='COL',
        choices=choices_from_enum(OrderArg),
        help='R|order by column\n'
             '"name", "license", "author", "url"\n'
             '(default: %(default)s)')
    common_options.add_argument(
        '--summary',
        action='store_true',
        default=False,
        help='dump summary of each license')
    common_options.add_argument(
        '--output-file',
        action='store', type=str,
        help='save license list to file')
    common_options.add_argument(
        '-i', '--ignore-packages',
        action='store', type=str,
        nargs='+', metavar='PKG',
        default=[],
        help='ignore package name in dumped list')
    common_options.add_argument(
        '-p', '--packages',
        action='store', type=str,
        nargs='+', metavar='PKG',
        default=[],
        help='only include selected packages in output')
    common_options.add_argument(
        '--local-only',
        action='store_true',
        default=False,
        help='include only local packages')
    common_options.add_argument(
        '--user-only',
        action='store_true',
        default=False,
        help='include only packages of the user site dir')
    
    format_options.add_argument(
        '-s', '--with-system',
        action='store_true',
        default=False,
        help='dump with system packages')
    format_options.add_argument(
        '-a', '--with-authors',
        action='store_true',
        default=False,
        help='dump with package authors')
    format_options.add_argument(
        '-u', '--with-urls',
        action='store_true',
        default=False,
        help='dump with package urls')
    format_options.add_argument(
        '-d', '--with-description',
        action='store_true',
        default=False,
        help='dump with short package description')
    format_options.add_argument(
        '-l', '--with-license-file',
        action='store_true',
        default=False,
        help='dump with location of license file and '
             'contents, most useful with JSON output')
    format_options.add_argument(
        '--no-license-path',
        action='store_true',
        default=False,
        help='I|when specified together with option -l, '
             'suppress location of license file output')
    format_options.add_argument(
        '--with-notice-file',
        action='store_true',
        default=False,
        help='I|when specified together with option -l, '
             'dump with location of license file and contents')
    format_options.add_argument(
        '--filter-strings',
        action="store_true",
        default=False,
        help='filter input according to code page')
    format_options.add_argument(
        '--filter-code-page',
        action="store", type=str,
        default="latin1",
        metavar="CODE",
        help='I|specify code page for filtering '
             '(default: %(default)s)')

    verify_options.add_argument(
        '--fail-on',
        action='store', type=str,
        default=None,
        help='fail (exit with code 1) on the first occurrence '
             'of the licenses of the semicolon-separated list')
    verify_options.add_argument(
        '--allow-only',
        action='store', type=str,
        default=None,
        help='fail (exit with code 1) on the first occurrence '
             'of the licenses not in the semicolon-separated list')

    return parser


def main():  # pragma: no cover
    parser = create_parser()
    args = parser.parse_args()

    output_string = create_output_string(args)

    print(output_string)


if __name__ == '__main__':  # pragma: no cover
    main()
