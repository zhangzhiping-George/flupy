'''
class LookingGlass:
    def __enter__(self):
        import sys
        self.orig_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'AJJJBALL' 

    def reverse_write(self, text):
        self.orig_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        import sys 
        sys.stdout.write = self.orig_write
        if exc_type is ZeroDivisionError: 
            print('Do Not divde by zero')
            return True

import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys

    orig_write = sys.stdout.write
    def reverse_write(text):
        # replace sys.stdout write() a little tricky
        orig_write(text[::-1]) 

    sys.stdout.write = reverse_write

    yield 'ASDLLL'
    sys.stdout.write = orig_write

'''
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys

    orig_write = sys.stdout.write
    def reverse_write(text):
        # replace sys.stdout write() a little tricky
        orig_write(text[::-1]) 

    sys.stdout.write = reverse_write

    try:
        yield 'ASDLLL'
    except ZeroDivisionError:
        print('exception gotch')
    finally:
        sys.stdout.write = orig_write

