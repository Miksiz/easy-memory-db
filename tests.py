import unittest
from interpreter import Interpreter

class InterpreterTestCase(unittest.TestCase):
  def setUp(self):
    self.interpreter = Interpreter()

  def test_set_get_value(self):
    self.interpreter.run_command('SET A 100')
    res = self.interpreter.run_command('GET A')
    self.assertEqual(res, '100')
    res = self.interpreter.run_command('GET B')
    self.assertEqual(res, 'NULL')

  def test_wrong_command(self):
    res = self.interpreter.run_command('START SOMETHING')
    self.assertEqual(res, 'Parse error: This command does not exist')
    res = self.interpreter.run_command('GET A B')
    self.assertEqual(res, 'Parse error: Extra data after variable name specified')
  
  def test_transactions(self):
    self.interpreter.run_command('BEGIN')
    self.interpreter.run_command('SET A 10')
    self.interpreter.run_command('BEGIN')
    self.interpreter.run_command('SET A 20')
    self.interpreter.run_command('BEGIN')
    self.interpreter.run_command('SET A 30')
    res = self.interpreter.run_command('GET A')
    self.assertEqual(res, '30')
    self.interpreter.run_command('ROLLBACK')
    res = self.interpreter.run_command('GET A')
    self.assertEqual(res, '20')
    self.interpreter.run_command('COMMIT')
    res = self.interpreter.run_command('GET A')
    self.assertEqual(res, '20')
