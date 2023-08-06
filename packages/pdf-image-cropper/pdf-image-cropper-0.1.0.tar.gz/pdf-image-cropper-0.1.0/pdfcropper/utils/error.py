class ErrorHandler:
    def __init__(self, error='ignore'):
        self.error = error
    
    def send(self, error_type, msg):
        if self.error == 'ignore':
            pass
        elif self.error == 'print':
            print(msg)
        else:
            raise error_type(msg)