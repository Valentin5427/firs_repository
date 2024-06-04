#coding=utf-8

import unittest
import validictory
from dpframe.tech.json import schema

class JSONSchemaTestCase(unittest.TestCase):

    def testTaskSchema(self):
        validictory.validate(schema.AGENT_TASK, schema.CORE, required_by_default=False)
        self.assertTrue(True)

    def testAgentSettingsSchema(self):
        validictory.validate(schema.AGENT_SETTINGS, schema.CORE, required_by_default=False)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()