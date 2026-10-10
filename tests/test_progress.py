import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from progress import build, validate, TZ, instant
from publish_progress import publish

FIXED = '2026-09-17T12:00:00Z'


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.run_git('init', '-b', 'main')
        self.run_git('config', 'user.email', 'test@example.com')
        self.run_git('config', 'user.name', 'Fixture')
        self.config = {'challengeStartedAt': '2026-03-01', 'acceptedOnlyConfirmed': True, 'commitPolicies': {}}
        self.commit('Initialize', {'README.md': 'fixture'})

    def run_git(self, *args, env=None):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], env=env, encoding='utf-8', stderr=subprocess.STDOUT).strip()

    def path(self, problem='alpha', number=0):
        return f'Data Structures & Algorithms/{problem}/submission-{number}.py'

    def commit(self, message, files, stamp='2026-03-08T07:00:00Z'):
        for name, content in files.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if content is None:
                path.unlink()
            else:
                path.write_text(content, encoding='utf-8')
        self.run_git('add', '.')
        self.run_git('commit', '--allow-empty', '-m', message, env={**os.environ, 'GIT_AUTHOR_DATE': stamp, 'GIT_COMMITTER_DATE': stamp})
        return self.run_git('rev-parse', 'HEAD')

    def add(self, problem='alpha', number=0, stamp='2026-03-08T07:00:00Z'):
        return self.commit(f'Add: {problem} - submission-{number}', {self.path(problem, number): f'print({number})'}, stamp)

    def snapshot(self, metadata=None):
        return build(self.repo, 'HEAD', self.config, metadata or {}, FIXED)[0]

    def test_one_and_unknown_metadata(self):
        self.add()
        s = self.snapshot()
        self.assertEqual(s['summary']['distinctProblems'], 1)
        self.assertEqual(s['summary']['difficulty']['Unknown'], 1)
        self.assertIsNone(s['recentSubmissions'][0]['difficulty'])
        self.assertIsNone(s['recentSubmissions'][0]['topics'])
        self.assertEqual(s['recentSubmissions'][0]['links'], {})
        validate(s)

    def test_repeats_multiple_problems_and_streaks(self):
        for p, n, d in [('alpha', 0, 8), ('alpha', 1, 9), ('beta', 0, 9), ('alpha', 2, 11)]:
            self.add(p, n, f'2026-03-{d:02}T12:00:00Z')
        s = self.snapshot()
        self.assertEqual(s['summary']['distinctProblems'], 2)
        self.assertEqual(s['dailyActivity']['2026-03-09'], {'submissions': 2, 'distinctProblems': 2})
        self.assertEqual(s['challenge'], {'completedDays': 3, 'longestStreak': 2, 'lastCompletedDate': '2026-03-11', 'streakEndingOnLastCompletedDate': 1})
        self.config['challengeStartedAt'] = '2026-03-10'
        self.assertEqual(self.snapshot()['challenge']['completedDays'], 1)
        self.config['challengeStartedAt'] = '2026-09-16'
        self.assertEqual(self.snapshot()['challenge']['longestStreak'], 0)
        self.config['challengeStartedAt'] = None
        self.assertIsNone(self.snapshot()['challenge'])

    def test_same_day_repeated_problem(self):
        self.add()
        self.add(number=1)
        self.assertEqual(self.snapshot()['dailyActivity']['2026-03-08'], {'submissions': 2, 'distinctProblems': 1})

    def test_multiple_files_with_evidence(self):
        self.commit('Add: alpha - submission-0\n\nAdd: beta - submission-0', {self.path(): 'a', self.path('beta'): 'b'})
        self.assertEqual(self.snapshot()['summary']['submissions'], 2)

    def test_edits_deletion_rename_and_readdition(self):
        self.add()
        self.commit('Edit solution', {self.path(): 'updated'})
        self.commit('Rename', {self.path(): None, self.path('beta'): 'updated'})
        self.commit('Delete', {self.path('beta'): None})
        self.add()
        self.add('beta')
        s = self.snapshot()
        self.assertEqual(s['summary']['submissions'], 1)
        self.assertEqual(s['summary']['distinctProblems'], 1)

    def test_merge_traverses_side_branch_once(self):
        self.run_git('checkout', '-b', 'side')
        self.add()
        self.run_git('checkout', 'main')
        self.commit('Housekeeping', {'README.md': 'changed'})
        self.run_git('merge', '--no-ff', 'side', '-m', 'Merge side')
        self.assertEqual(self.snapshot()['summary']['submissions'], 1)

    def test_housekeeping_and_unsupported_course_and_empty_history(self):
        self.commit('Housekeeping', {'README.md': 'changed', 'Python For Beginners/foo/submission-0.py': 'code'})
        s = self.snapshot()
        self.assertEqual(s['summary']['submissions'], 0)
        self.assertEqual(s['recentSubmissions'], [])
        self.assertIsNone(s['challenge']['lastCompletedDate'])

    def test_midnight_and_dst(self):
        cases = [('2026-03-08T04:59:59Z', '2026-03-07', -5), ('2026-03-08T05:00:00Z', '2026-03-08', -5),
                 ('2026-03-08T06:59:59Z', '2026-03-08', -5), ('2026-03-08T07:00:00Z', '2026-03-08', -4),
                 ('2026-11-01T05:59:59Z', '2026-11-01', -4), ('2026-11-01T06:00:00Z', '2026-11-01', -5),
                 ('2026-07-01T03:59:59Z', '2026-06-30', -4), ('2026-07-01T04:00:00Z', '2026-07-01', -4)]
        for n, (stamp, day, offset) in enumerate(cases):
            with self.subTest(stamp=stamp):
                self.add(number=n, stamp=stamp)
                local = instant(stamp).astimezone(TZ)
                self.assertEqual(local.date().isoformat(), day)
                self.assertEqual(local.utcoffset().total_seconds(), offset * 3600)
        self.assertEqual(self.snapshot()['summary']['activeDays'], 5)

    def test_bulk_requires_policy_and_supports_exclusions_overrides(self):
        sha = self.commit('Bulk sync: 2 submissions', {self.path(): 'a', self.path('beta'): 'b'})
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            self.snapshot()
        policy = {'mode': 'undated', 'reason': 'Original dates unavailable'}
        self.config['commitPolicies'][sha] = policy
        self.assertEqual(self.snapshot()['summary']['undatedSubmissions'], 2)
        self.assertEqual(self.snapshot()['dailyActivity'], {})
        policy['mode'] = 'exclude'
        self.assertEqual(self.snapshot()['summary']['submissions'], 0)
        policy['mode'] = 'dated'
        with self.assertRaisesRegex(ValueError, 'original timestamps'):
            self.snapshot()
        policy.update(mode='dated', timestamps={self.path(): '2026-03-01T15:00:00Z', self.path('beta'): '2026-03-02T15:00:00Z'})
        self.assertEqual(list(self.snapshot()['dailyActivity']), ['2026-03-01', '2026-03-02'])

    def test_ambiguous_and_malformed(self):
        self.commit('Housekeeping', {self.path(): 'a'})
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            self.snapshot()

    def test_malformed_path(self):
        self.commit('Add: alpha - submission-0', {'Data Structures & Algorithms/alpha/answer.py': 'a'})
        with self.assertRaisesRegex(ValueError, 'Unsupported submission path'):
            self.snapshot()

    def test_determinism_metadata_and_schema_rejection(self):
        self.add()
        metadata = {'alpha': {'title': 'Reviewed title', 'difficulty': 'Hard', 'topics': ['Graph']}}
        s = self.snapshot(metadata)
        self.assertEqual(json.dumps(s), json.dumps(self.snapshot(metadata)))
        self.assertEqual(s['summary']['difficulty']['Hard'], 1)
        bad = copy.deepcopy(s)
        bad['summary']['submissions'] = 99
        with self.assertRaises(ValueError):
            validate(bad)
        with self.assertRaises(ValueError):
            self.snapshot({'alpha': {'difficulty': 'easy'}})

    def test_recent_ten_and_extension_identity(self):
        for n in range(12):
            self.add(number=n)
        self.commit('Add: alpha - submission-0', {'Data Structures & Algorithms/alpha/submission-0.cpp': 'a'})
        s = self.snapshot()
        self.assertEqual(s['summary']['submissions'], 12)
        self.assertEqual(len(s['recentSubmissions']), 10)

    def test_merge_only_addition_fails(self):
        self.run_git('checkout', '-b', 'side')
        self.commit('Side housekeeping', {'side.txt': 'a'})
        self.run_git('checkout', 'main')
        self.commit('Main housekeeping', {'main.txt': 'a'})
        self.run_git('merge', '--no-ff', '--no-commit', 'side')
        self.commit('Merge with extra solution', {self.path(): 'code'})
        with self.assertRaisesRegex(ValueError, 'Merge-only'):
            self.snapshot()

    def test_bad_config_and_shallow_history(self):
        self.config['challengeStartedAt'] = '09/16/26'
        with self.assertRaises(ValueError):
            self.snapshot()
        self.config['challengeStartedAt'] = None
        self.config['commitPolicies']['f' * 40] = {'mode': 'exclude', 'reason': 'typo'}
        with self.assertRaisesRegex(ValueError, 'not in source history'):
            self.snapshot()
        with tempfile.TemporaryDirectory() as destination:
            subprocess.run(['git', 'clone', '--depth=1', self.repo.as_uri(), destination], check=True, capture_output=True)
            self.config['commitPolicies'] = {}
            with self.assertRaisesRegex(ValueError, 'Full Git history'):
                build(destination, 'HEAD', self.config, {})

    def prepare_remote(self):
        remote = tempfile.TemporaryDirectory()
        self.addCleanup(remote.cleanup)
        subprocess.run(['git', 'init', '--bare', remote.name], check=True, capture_output=True)
        self.run_git('remote', 'add', 'origin', remote.name)
        self.run_git('push', 'origin', 'main')
        output = Path(remote.name) / 'input.json'
        return output

    def publish_snapshot(self, output, snapshot):
        output.write_text(json.dumps(snapshot), encoding='utf-8')
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            publish(str(output))
        finally:
            os.chdir(previous)

    def test_publisher_creation_update_and_stale_skip(self):
        self.add()
        output = self.prepare_remote()
        original_main = self.run_git('rev-parse', 'HEAD')
        self.publish_snapshot(output, self.snapshot())
        self.run_git('fetch', 'origin', 'dashboard-data')
        first = self.run_git('rev-parse', 'FETCH_HEAD')
        self.assertEqual(self.run_git('ls-tree', '-r', '--name-only', first), 'progress.json')
        self.assertEqual(self.run_git('rev-parse', 'HEAD'), original_main)
        stale = self.snapshot()
        self.add(number=1)
        self.run_git('push', 'origin', 'main')
        self.publish_snapshot(output, stale)
        self.assertTrue(self.run_git('ls-remote', 'origin', 'dashboard-data').startswith(first))
        self.publish_snapshot(output, self.snapshot())
        self.run_git('fetch', 'origin', 'dashboard-data')
        second = self.run_git('rev-parse', 'FETCH_HEAD')
        self.assertEqual(self.run_git('rev-parse', second + '^'), first)
        invalid = self.snapshot()
        invalid['summary']['submissions'] = 0
        with self.assertRaises(ValueError):
            self.publish_snapshot(output, invalid)
        self.assertTrue(self.run_git('ls-remote', 'origin', 'dashboard-data').startswith(second))

    def test_publisher_concurrent_writer_fails_without_overwrite(self):
        self.add()
        output = self.prepare_remote()
        self.publish_snapshot(output, self.snapshot())
        self.run_git('fetch', 'origin', 'dashboard-data')
        first = self.run_git('rev-parse', 'FETCH_HEAD')
        import publish_progress
        original_command = publish_progress.command
        competing = []

        def race(*args, **kwargs):
            if args[0] == 'push':
                tree = self.run_git('rev-parse', first + '^{tree}')
                other = self.run_git('commit-tree', tree, '-p', first, '-m', 'Competing update')
                self.run_git('push', 'origin', other + ':refs/heads/dashboard-data')
                competing.append(other)
            return original_command(*args, **kwargs)

        with patch.object(publish_progress, 'command', side_effect=race):
            with self.assertRaises(subprocess.CalledProcessError):
                self.publish_snapshot(output, self.snapshot())
        self.assertTrue(self.run_git('ls-remote', 'origin', 'dashboard-data').startswith(competing[0]))


if __name__ == '__main__':
    unittest.main()
