# coding: utf-8

import pkgutil
from pathlib import Path
from token import NAME
from tokenize import generate_tokens

from django.test import TestCase
from django.conf import settings


PY_FILE_EXTENSION = '*.py'

NO_QUALITY_CHECK_LINE_MARK = '# noqa'
NO_QUALITY_CHECK_FILE_MARK = '# smelly_tokens: noqa'


class SmellyTokensTestCase(object):

    _tokens = []

    def test_check_token_exists(self):
        errors = []
        for module_name in getattr(settings, 'SMELLY_TOKENS_APPLICATIONS', []):
            module = pkgutil.get_loader(module_name)
            module_dir = Path(module.get_filename()).parent

            excludes = getattr(settings, 'SMELLY_TOKENS_EXCLUDE_DIRS', [])

            for file in self._get_py_files(module_dir, excludes):
                if not any([
                    t in file.read_text()
                    for t in self._tokens
                ]):
                    continue
                for kind, token, start, _, whole in \
                        generate_tokens(file.open().readline):
                    if whole.startswith(NO_QUALITY_CHECK_FILE_MARK):
                        break
                    if whole.strip().endswith(NO_QUALITY_CHECK_LINE_MARK):
                        continue
                    if kind != NAME:
                        continue
                    if token in self._tokens:
                        errors.append("'{}' left at '{}', line {}".format(
                            token, file, start[0]))

        self.assertTrue(len(errors) == 0, '\n'.join(errors))

    def _get_py_files(self, module_dir, exclude_dirs=[]):
        excluded_dirs = [module_dir / e for e in exclude_dirs]
        for file in module_dir.rglob(PY_FILE_EXTENSION):
            if file.parent in excluded_dirs:
                continue
            yield file


class EvalTokenTestCase(SmellyTokensTestCase, TestCase):
    _tokens = ['eval']


class PdbTokenTestCase(SmellyTokensTestCase, TestCase):
    _tokens = ['pdb', 'ipdb']


class PrintTokenTestCase(SmellyTokensTestCase, TestCase):
    _tokens = ['print']
