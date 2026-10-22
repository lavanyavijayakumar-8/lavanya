"""
Python 3.14 Compatibility Shim for Django 5.0 template context copying.
In Python 3.14, super().__copy__() on BaseContext returns an object without dicts attribute,
causing AttributeError in django.template.context.BaseContext.__copy__.
"""

try:
    import django.template.context as _ctx
    
    def _safe_context_copy(self):
        duplicate = object.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate
        
    _ctx.BaseContext.__copy__ = _safe_context_copy
except Exception:
    pass
