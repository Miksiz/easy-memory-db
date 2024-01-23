import operator

class DatabaseException(BaseException):
  pass

class DatabaseRollbackException(DatabaseException):
  pass

class DatabaseCommitException(DatabaseException):
  pass

class Database:
  def __init__(self):
    self.data = {}
    self.previous_states = []

  def set(self, name: str, value: str) -> None:
    self.data[name] = value
  
  def get(self, name: str) -> str:
    return self.data.get(name, 'NULL')

  def unset(self, name: str) -> None:
    self.data.pop(name, None)
  
  def counts(self, value: str) -> int:
    return operator.countOf(self.data.values(), value)
  
  def find(self, value: str) -> list[str]:
    return [k for k, v in self.data.items() if v == value]
  
  def start_transaction(self):
    self.previous_states.append(self.data.copy())

  def commit_transaction(self):
    try:
      self.previous_states.pop()
    except IndexError:
      raise DatabaseCommitException('No active transaction to commit')
  
  def rollback_transaction(self):
    try:
      self.data = self.previous_states.pop()
    except IndexError:
      raise DatabaseRollbackException('No previous state to rollback to')
