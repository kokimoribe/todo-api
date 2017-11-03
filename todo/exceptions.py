"""Exceptions are defined here"""


class NotFoundError(Exception):
    """Exception for HTTP Not Found error"""
    status_code = 404

    def to_dict(self):
        """Convert exception to dictionary representation"""
        return {'error': str(self), 'status': self.status_code}


class UnauthorizedError(Exception):
    """Exception for HTTP Unauthorized error"""
    status_code = 401

    def to_dict(self):
        """Convert exception to dictionary representation"""
        return {'error': str(self), 'status': self.status_code}
