# 暂不使用
from django.db.models import ManyToManyField, DateTimeField, ForeignKey


def my_model_to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
  
            value = f.value_from_object(self)
       
            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, ManyToManyField):
                value = [ i.id for i in value ] if self.pk else None
                
            if isinstance(f, ForeignKey):
                print(self.user)
                # value = [ data for data in self.user ] if self.pk else None

            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

            data[f.name] = value

        return data