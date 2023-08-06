from typing import Any

_session: Any = None


def rememberSession(clientSession: Any):
  global _session
  _session = clientSession


def anyAuthenticatedSession():
  global _session
  if _session and _session.isAuthenticated():
    return _session
  else:
    return None
