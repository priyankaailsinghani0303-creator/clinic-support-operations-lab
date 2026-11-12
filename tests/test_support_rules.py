import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support_rules import calculate_sla, route_ticket, simulation_status

BASE = Path(__file__).resolve().parents[1]

class SupportRulesTests(unittest.TestCase):
    def setUp(self):
        self.tickets = pd.DataFrame([{'ticket_id': 'X', 'priority': 'Urgent'}])
        self.policy = pd.DataFrame([{'priority': 'Urgent', 'first_response_minutes': 15}])
        self.times = pd.DataFrame([{'ticket_id': 'X', 'created_at': '2026-11-12T09:00:00Z', 'first_responded_at': '2026-11-12T09:15:00Z'}])

    def status(self, times=None, policy=None):
        return calculate_sla(self.tickets, self.times if times is None else times, self.policy if policy is None else policy).iloc[0]['SLA Status']

    def test_boundary_and_timezone(self):
        self.assertEqual(self.status(), 'Met')
        self.times.loc[0, 'first_responded_at'] = '2026-11-12T13:15:01+04:00'
        self.assertEqual(self.status(), 'Breached')
        self.times.loc[0, 'first_responded_at'] = '2026-11-12 09:15:00'
        self.assertEqual(self.status(), 'Met')

    def test_missing_and_invalid_history(self):
        self.assertEqual(self.status(self.times.iloc[:0]), 'Creation Time Missing/Invalid')
        for value, expected in [('', 'Response Not Recorded'), ('bad', 'Invalid Response Timestamp'), ('2026-11-12T08:59:00Z', 'Invalid Response Timestamp')]:
            with self.subTest(value=value):
                self.times.loc[0, 'first_responded_at'] = value
                self.assertEqual(self.status(), expected)
        self.times.loc[0, 'created_at'] = 'bad'
        self.assertEqual(self.status(), 'Creation Time Missing/Invalid')

    def test_duplicate_and_invalid_policy(self):
        self.assertEqual(self.status(pd.concat([self.times, self.times])), 'Duplicate Timestamp Records')
        self.assertEqual(self.status(policy=pd.concat([self.policy, self.policy])), 'Policy Missing/Invalid')
        for target in [0, -1, float('inf'), 'bad']:
            with self.subTest(target=target):
                policy = pd.DataFrame([{'priority': 'Urgent', 'first_response_minutes': target}])
                self.assertEqual(self.status(policy=policy), 'Policy Missing/Invalid')

    def test_normalization_and_unique_tickets(self):
        self.tickets.loc[0, 'priority'] = ' urgent '
        self.assertEqual(self.status(), 'Met')
        with self.assertRaises(ValueError):
            calculate_sla(pd.concat([self.tickets, self.tickets]), self.times, self.policy)

    def test_routing(self):
        for category, team in [('Booking', 'Platform Support'), (' payments ', 'Platform Support'), ('Messaging', 'Platform Support'), ('Account', 'Account Support'), ('Other', 'General Support'), ('Unknown', 'General Support')]:
            with self.subTest(category=category):
                routed = route_ticket({'ticket_id': 'X', 'issue_type': category, 'priority': 'High'})
                self.assertEqual(routed['suggested_initial_team'], team)

    def test_risk_thresholds(self):
        for elapsed, expected in [(11.9, 'ON TRACK'), (12, 'AT RISK'), (15, 'AT RISK'), (15.01, 'BREACHED')]:
            self.assertEqual(simulation_status(elapsed, 15), expected)

    def test_repository_sample(self):
        result = calculate_sla(*(pd.read_csv(BASE / f) for f in ['tickets.csv', 'ticket_timestamps.csv', 'sla_policy.csv']))
        self.assertEqual(result['SLA Status'].tolist(), ['Met', 'Breached', 'Creation Time Missing/Invalid'])
        valid = result['SLA Status'].isin(['Met', 'Breached'])
        self.assertEqual(result['SLA Status'].eq('Met').sum() / valid.sum(), .5)

if __name__ == '__main__':
    unittest.main()
