import json
import tempfile
import unittest
from pathlib import Path
from workbench_core import Workbench, SCENARIOS, clock

START = '2026-11-13T09:00:00+00:00'
LATER = '2026-11-13T09:10:00+00:00'
DEADLINE = '2026-11-13T10:00:00+00:00'

class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'test.sqlite'
        self.w = Workbench(self.path)

    def prepare(self, scenario):
        i = self.w.create(scenario, 'High', now=START)
        self.w.act(i, 'Accept ownership', owner='Demo Agent', deadline=DEADLINE, now=LATER)
        self.w.act(i, 'Record response', text='Checking scope; next update at 10 UTC.', now=LATER)
        for check in SCENARIOS[scenario]['checks']:
            self.w.act(i, check, now=LATER)
        return i

    def test_all_scenarios_close_only_after_verification_and_confirmation(self):
        for scenario, spec in SCENARIOS.items():
            with self.subTest(scenario=scenario):
                i = self.prepare(scenario)
                with self.assertRaises(ValueError):
                    self.w.act(i, 'Resolve', text='done', now=LATER)
                self.w.act(i, spec['fix'], now=LATER)
                self.w.act(i, 'Verify workflow', now=LATER)
                with self.assertRaises(ValueError):
                    self.w.act(i, 'Resolve', text='done', now=LATER)
                self.w.act(i, 'Record simulated customer confirmation', text='Role-play: workflow visible.', now=LATER)
                result = self.w.act(i, 'Resolve', text='Synthetic workflow verified.', now=LATER)
                self.assertEqual(result['status'], 'Resolved')
                self.assertIsNone(result['next_update'])
                self.assertIn(spec['verification'], self.w.report(i))

    def test_uninvestigated_fix_and_premature_verification_blocked(self):
        i = self.w.create('Payments', 'High', now=START)
        for action in [SCENARIOS['Payments']['fix'], 'Verify workflow']:
            with self.assertRaises(ValueError):
                self.w.act(i, action, now=LATER)
        self.assertEqual(len(self.w.events(i)), 1)

    def test_reopen_preserves_history_and_invalidates_verification(self):
        i = self.prepare('Calendar')
        for action in [SCENARIOS['Calendar']['fix'], 'Verify workflow', 'Record simulated customer confirmation', 'Resolve']:
            self.w.act(i, action, text='Synthetic evidence', now=LATER)
        before = len(self.w.events(i))
        with self.assertRaises(ValueError):
            self.w.act(i, 'Record response', text='new', now=LATER)
        t = self.w.act(i, 'Reopen', text='Role-play recurrence', now=LATER)
        self.assertEqual(t['status'], 'Open')
        self.assertEqual(t['verified'], 0)
        self.assertIsNone(t['resolved'])
        self.assertEqual(len(self.w.events(i)), before+1)

    def test_ownership_and_response_validation(self):
        i = self.w.create('Messaging', 'Medium', now=START)
        with self.assertRaises(ValueError):
            self.w.act(i, 'Record response', text='hi', now=LATER)
        with self.assertRaises(ValueError):
            self.w.act(i, 'Accept ownership', owner='Demo', deadline=START, now=LATER)
        self.w.act(i, 'Accept ownership', owner='Demo', deadline=DEADLINE, now=LATER)
        with self.assertRaises(ValueError):
            self.w.act(i, 'Record response', text='', now=LATER)

    def test_escalation_retains_owner_and_storage_persists(self):
        i = self.prepare('Payments')
        self.w.act(i, 'Record escalation', text='Payments: compare platform and processor; next check at 10 UTC.', now=LATER)
        other = Workbench(self.path)
        self.assertEqual(other.get(i)['owner'], 'Demo Agent')
        self.assertEqual(other.get(i)['status'], 'Escalated')
        self.assertIn('acceptance has not been recorded', other.report(i))

    def test_clocks_distinguish_pending_overdue_and_completed(self):
        self.assertEqual(clock(START, None, 15, LATER)['state'], 'Pending')
        self.assertEqual(clock(START, None, 10, LATER)['state'], 'At risk')
        self.assertEqual(clock(START, None, 9, LATER)['state'], 'Overdue')
        self.assertEqual(clock(START, LATER, 10, DEADLINE)['state'], 'Met')
        self.assertEqual(clock(START, LATER, 9, DEADLINE)['state'], 'Breached')

    def test_invalid_and_backdated_events_do_not_mutate(self):
        i = self.prepare('Calendar')
        before = len(self.w.events(i))
        with self.assertRaises(ValueError):
            self.w.act(i, 'Current view', now=START)
        self.assertEqual(len(self.w.events(i)), before)
        with self.assertRaises(ValueError):
            self.w.create('Unknown', 'High', now=START)
        with self.assertRaises(ValueError):
            clock(START, None, 15, '2026-11-13T08:00:00+00:00')

if __name__ == '__main__':
    unittest.main()
