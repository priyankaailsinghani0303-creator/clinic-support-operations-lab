import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class WorkbenchUITests(unittest.TestCase):
    def test_calendar_workflow_and_invalid_closure(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'workbench.py')).run()
        self.assertFalse(app.exception)
        app.button(key='FormSubmitter:new_case-Create synthetic ticket').click().run()
        self.assertFalse(app.exception)
        # A reviewer cannot close a ticket merely by writing a summary.
        action = next(x for x in app.selectbox if x.label == 'Record type')
        action.select('Resolve')
        app.text_area[0].set_value('Premature closure')
        app.button(key='FormSubmitter:communication_1-Record action').click().run()
        self.assertTrue(app.error)
        app.text_input[0].set_value('Demo Agent')
        app.button(key='FormSubmitter:owner_1-Accept ownership').click().run()
        next(x for x in app.selectbox if x.label == 'Record type').select('Record response')
        app.text_area[0].set_value('Please check the date, provider and facility. Avoid a duplicate booking.')
        app.button(key='FormSubmitter:communication_1-Record action').click().run()
        for key in ['1_Booking record', '1_Current view', 'fix_1', 'verify_1']:
            app.button(key=key).click().run()
            self.assertFalse(app.exception)
        next(x for x in app.selectbox if x.label == 'Record type').select('Record simulated customer confirmation')
        app.text_area[0].set_value('Role-play: I can see the original appointment.')
        app.button(key='FormSubmitter:communication_1-Record action').click().run()
        next(x for x in app.selectbox if x.label == 'Record type').select('Resolve')
        app.text_area[0].set_value('Verified one original appointment in All Facilities.')
        app.button(key='FormSubmitter:communication_1-Record action').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Resolved' in x.value for x in app.subheader))

if __name__ == '__main__':
    unittest.main()
