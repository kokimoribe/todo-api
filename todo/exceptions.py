"""Exceptions are defined here"""


class NotFoundError(Exception):
    """Exception for Not Found error"""
    status_code = 404

    def to_dict(self):
        """Convert exception to dictionary representation"""
        return {'error': str(self), 'status': self.status_code}
