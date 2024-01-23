from typing import Optional
from database import Database, DatabaseException
import re

class InterpreterParseException(BaseException):
  pass

class Interpreter:
  argument_pattern = re.compile(r'^\s*?(\S+)(?:\s*$|\s+(.+?)\s*$)') # Паттерн для получения первого аргумента команды без пробелов

  def __init__(self):
    self.db = Database()

  def get_next_argument(self, line: str) -> (str, str):
    '''
    Функция получает слудующий аргумент из строки line, отделенный пробелами
    Возвращает (argument, rest_of_line)
    '''
    m = self.argument_pattern.search(line)
    if m:
      return (m[1], m[2] if m[2] else '')
    else:
      return ('', '')

  value_arg_commands = {'FIND', 'COUNTS'}
  name_arg_commands = {'GET', 'UNSET'}
  no_arg_commands = {'END', 'BEGIN', 'COMMIT', 'ROLLBACK'}
  def process_command(self, line: str) -> Optional[str]:
    command, line = self.get_next_argument(line)
    name, value = (None, None)

    if command == 'SET':
      name, value = self.get_next_argument(line)
      if not name: raise InterpreterParseException('Variable name not specified')
      if not value: raise InterpreterParseException('Value not specified')
    if command in self.value_arg_commands:
      value = line
      if not value: raise InterpreterParseException('Value not specified')
    elif command in self.name_arg_commands:
      name, line = self.get_next_argument(line)
      if not name: raise InterpreterParseException('Variable name not specified')
      if line: raise InterpreterParseException('Extra data after variable name specified')
    elif command in self.no_arg_commands:
      if line: raise InterpreterParseException('Extra data after command')

    match command:
      case 'SET':
        return self.db.set(name, value)
      case 'GET':
        return self.db.get(name)
      case 'UNSET':
        return self.db.unset(name)
      case 'COUNTS':
        return str(self.db.counts(value))
      case 'FIND':
        return ', '.join(self.db.find(value))
      case 'END':
        exit(0)
      case 'BEGIN':
        return self.db.start_transaction()
      case 'COMMIT':
        return self.db.commit_transaction()
      case 'ROLLBACK':
        return self.db.rollback_transaction()
      case _:
        raise InterpreterParseException('This command does not exist')

  def run_command(self, line: str) -> Optional[str]:
    try:
      result = self.process_command(line)
    except InterpreterParseException as e:
      result = f'Parse error: {e}'
    except DatabaseException as e:
      result = f'Command error: {e}'
    except SystemExit:
      raise
    except BaseException as e:
      result = f'Program error: {e}'
    return result

  def run(self) -> None:
    while True:
      try:
        line = input('> ')
      except EOFError:
        break
      out_line = self.run_command(line)
      if out_line is not None:
        print(out_line)