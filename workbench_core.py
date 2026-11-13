"""Synthetic support workbench. Standard-library domain and SQLite storage."""
import json
import sqlite3
from datetime import datetime, timezone

TARGETS = {"Urgent": (15, 120), "High": (30, 240), "Medium": (120, 480), "Low": (240, 1440)}
SCENARIOS = {
    "Calendar": {
        "report": "A booked appointment is missing from the calendar.",
        "expected": "The existing appointment is visible in the correct facility view.",
        "checks": {"Booking record": "Appointment DEMO-101 exists, confirmed, at 08:00 UTC; facility North; provider Demo Provider.",
                   "Current view": "Calendar date and provider match. Facility filter is South; appointment belongs to North."},
        "fix": "Select All Facilities",
        "verification": "DEMO-101 is visible at 08:00 UTC. Booking count remains 1; no duplicate created.",
        "classification": "Configuration",
        "article": "Check date, provider and facility filters before creating another booking. Verify the original record.",
    },
    "Payments": {
        "report": "Checkout showed an error. Should the clinic retry the payment?",
        "expected": "The platform shows the processor's confirmed transaction state.",
        "checks": {"Processor status": "Sandbox transaction DEMO-PAY-201: succeeded; amount USD 100; attempts 1.",
                   "Platform status": "Local status is pending after a simulated callback delay. Processor confirms success."},
        "fix": "Refresh sandbox transaction status",
        "verification": "Platform and processor both show succeeded. Attempts remain 1; no second charge simulated.",
        "classification": "Integration state",
        "article": "Check the original transaction state before retrying. An uncertain platform result does not establish a failed charge.",
    },
    "Messaging": {
        "report": "An appointment reminder was not delivered.",
        "expected": "An eligible reminder is queued and its delivery result is recorded.",
        "checks": {"Reminder configuration": "Synthetic SMS reminder enabled; test appointment eligible; scheduled send time reached.",
                   "Delivery log": "Sandbox job DEMO-SMS-301 suppressed: test recipient has no consent recorded. No provider send attempted."},
        "fix": "Test with consented synthetic recipient",
        "verification": "A new synthetic recipient with consent recorded before scheduling receives a simulator-delivered test reminder. Original consent unchanged.",
        "classification": "Configuration",
        "article": "Separate eligibility, queueing and delivery. Check consent and suppression status; do not bypass an original recipient's preferences.",
    },
}

def utcnow():
    return datetime.now(timezone.utc).isoformat()

def parse(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError("Use timezone-aware timestamps")
    return result.astimezone(timezone.utc)

def clock(created, completed, target, now):
    elapsed = (parse(completed or now) - parse(created)).total_seconds() / 60
    if elapsed < 0:
        raise ValueError("Timestamp precedes creation")
    if completed:
        state = "Met" if elapsed <= target else "Breached"
    else:
        state = "Overdue" if elapsed > target else "At risk" if elapsed >= .8 * target else "Pending"
    return {"minutes": round(elapsed, 2), "target": target, "state": state}

class Workbench:
    def __init__(self, path):
        self.path = str(path)
        with self.connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS tickets (
              id INTEGER PRIMARY KEY, scenario TEXT NOT NULL, priority TEXT NOT NULL,
              created TEXT NOT NULL, responded TEXT, resolved TEXT, status TEXT NOT NULL DEFAULT 'Open',
              owner TEXT NOT NULL DEFAULT '', next_update TEXT,
              findings TEXT NOT NULL DEFAULT '{}', fixed INTEGER NOT NULL DEFAULT 0,
              verified INTEGER NOT NULL DEFAULT 0, customer_confirmed INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS events (
              id INTEGER PRIMARY KEY, ticket_id INTEGER NOT NULL REFERENCES tickets(id),
              at TEXT NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL);
            """)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        return db

    def tickets(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM tickets ORDER BY id DESC")]

    def get(self, ticket_id):
        with self.connect() as db:
            row = db.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
        if row is None:
            raise ValueError("Ticket does not exist")
        return dict(row)

    def events(self, ticket_id):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM events WHERE ticket_id=? ORDER BY id", (ticket_id,))]

    def create(self, scenario, priority, now=None):
        if scenario not in SCENARIOS or priority not in TARGETS:
            raise ValueError("Unknown scenario or priority")
        at = now or utcnow()
        parse(at)
        with self.connect() as db:
            ticket_id = db.execute("INSERT INTO tickets(scenario,priority,created) VALUES(?,?,?)", (scenario, priority, at)).lastrowid
            db.execute("INSERT INTO events(ticket_id,at,kind,body) VALUES(?,?,?,?)", (ticket_id, at, "Created", SCENARIOS[scenario]["report"]))
        return ticket_id

    def act(self, ticket_id, action, text='', owner='', deadline=None, now=None):
        at = now or utcnow()
        parse(at)
        # Serialize each read/validate/write operation to avoid stale state transitions.
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
            if row is None:
                raise ValueError("Ticket does not exist")
            t = dict(row)
            if parse(at) < parse(t['created']):
                raise ValueError("Action precedes ticket creation")
            last = db.execute("SELECT at FROM events WHERE ticket_id=? ORDER BY id DESC LIMIT 1", (ticket_id,)).fetchone()
            if last and parse(at) < parse(last['at']):
                raise ValueError("Action precedes latest recorded event")
            s = SCENARIOS[t['scenario']]
            findings = json.loads(t['findings'])
            updates = {}
            body = text.strip()
            if t['status'] == 'Resolved' and action != 'Reopen':
                raise ValueError("Reopen the ticket before making changes")
            if action == 'Accept ownership':
                if not owner.strip() or not deadline or parse(deadline) <= parse(at):
                    raise ValueError("Provide an owner and a future update deadline")
                updates = {'owner': owner.strip(), 'next_update': deadline}
                body = f"{owner.strip()} accepted ownership. Next update: {deadline}"
            elif action == 'Record response':
                if not body:
                    raise ValueError("Write the customer response")
                if not t['owner']:
                    raise ValueError("Accept ownership first")
                updates = {'responded': t['responded'] or at}
            elif action in s['checks']:
                findings[action] = s['checks'][action]
                updates = {'findings': json.dumps(findings)}
                body = s['checks'][action]
            elif action == s['fix']:
                if set(findings) != set(s['checks']):
                    raise ValueError("Complete both evidence checks before applying the simulated action")
                updates = {'fixed': 1, 'verified': 0, 'customer_confirmed': 0}
                body = f"Simulator action: {s['fix']}. No external service was contacted."
            elif action == 'Verify workflow':
                if not t['fixed']:
                    raise ValueError("Apply the simulated action first")
                updates = {'verified': 1}
                body = s['verification']
            elif action == 'Record simulated customer confirmation':
                if not t['verified'] or not body:
                    raise ValueError("Verify the workflow and record the simulated confirmation")
                updates = {'customer_confirmed': 1}
            elif action == 'Resolve':
                if not all([t['owner'], t['responded'], t['verified'], t['customer_confirmed'], body]):
                    raise ValueError("Closure requires owner, response, verification, simulated confirmation and summary")
                updates = {'status': 'Resolved', 'resolved': at, 'next_update': None}
            elif action == 'Reopen':
                if t['status'] != 'Resolved' or not body:
                    raise ValueError("Only a resolved ticket can reopen; provide a reason")
                updates = {'status': 'Open', 'resolved': None, 'fixed': 0, 'verified': 0, 'customer_confirmed': 0}
            elif action == 'Record escalation':
                if not t['owner'] or not body:
                    raise ValueError("Accept ownership and provide a receiving team, evidence, question and next action")
                updates = {'status': 'Escalated'}
                body += "\nSupport owner retained; receiving-team acceptance has not been recorded."
            else:
                raise ValueError("Unknown action")
            if updates:
                sql = ','.join(f'{key}=?' for key in updates)
                db.execute(f'UPDATE tickets SET {sql} WHERE id=?', (*updates.values(), ticket_id))
            db.execute("INSERT INTO events(ticket_id,at,kind,body) VALUES(?,?,?,?)", (ticket_id, at, action, body))
        return self.get(ticket_id)

    def report(self, ticket_id):
        t = self.get(ticket_id)
        s = SCENARIOS[t['scenario']]
        lines = [f"# Synthetic ticket S{ticket_id:03d} — {t['scenario']}",
                 "SIMULATOR OUTPUT: not a customer outcome or external platform investigation.",
                 f"Status: {t['status']} | Owner: {t['owner'] or 'Unassigned'}",
                 f"Expected: {s['expected']}", f"Reported: {s['report']}",
                 f"Created: {t['created']} | First response: {t['responded']} | Resolved: {t['resolved']}",
                 f"Next update: {t['next_update']}", "## Recorded events"]
        for e in self.events(ticket_id):
            lines.append(f"- {e['at']} | {e['kind']}: {e['body']}")
        return '\n\n'.join(lines)
