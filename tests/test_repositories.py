from unittest import TestCase

from versions.repositories import Repository, Pool
from versions.packages import Package


class TestRepository(TestCase):

    def test(self):
        packages = set([
            Package.parse('foo-1.0'),
            Package.parse('foo-2.0'),
            Package.parse('foo-3.0'),
            Package.parse('vim-7.4+perl.python'),
            Package.parse('vim-7.4+perl.ruby.python'),
            Package.parse('vim-6.0+perl.ruby.python'),
        ])
        repository = Repository(packages)
        self.assertEqual(repository.get('foo'), [
            Package.parse('foo-1.0'),
            Package.parse('foo-2.0'),
            Package.parse('foo-3.0'),
        ])
        self.assertEqual(repository.get('vim[ruby]>7'), [
            Package.parse('vim-7.4+perl.ruby.python'),
        ])


class TestPool(TestCase):

    def test(self):
        foo_repo = Repository(set([
            Package.parse('foo-1.0'),
            Package.parse('foo-2.0'),
            Package.parse('foo-3.0')]))
        vim_repo = Repository(set([
            Package.parse('vim-7.4+perl.python'),
            Package.parse('vim-7.4+perl.ruby.python'),
            Package.parse('vim-6.0+perl.ruby.python')]))
        pool = Pool([foo_repo, vim_repo])
        self.assertEqual(pool.get('foo'), [
            Package.parse('foo-1.0'),
            Package.parse('foo-2.0'),
            Package.parse('foo-3.0'),
        ])
        self.assertEqual(pool.get('vim[ruby]>7'), [
            Package.parse('vim-7.4+perl.ruby.python'),
        ])
