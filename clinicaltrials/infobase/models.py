from django.db import models

from datetime import datetime

class Item(models.Model):
    key = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(self, index=True)
    revision = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=datetime.now, index=True)
    updated = models.DateTimeField(null=True, blank=True, index=True)
    
    def save(self):
        if self.id:
            self.updated = datetime.now()

    def __getattr__(self, attr_name):
        ''' get named datum of current version '''

        res = Datum.objects.filter(thing=self, key=attr_name, revision=self.revision)
        
    def __setattr__(self, attr_name, value):
        ''' set named datum '''
        next_revision = self.revision + 1
        other_attrs = Attribute.objects.filter(thing=self,revision=self.revision).exclude(key=attr_name)
        other_attrs.update(revision=next_revision)
        self.revision = next_revision
        self.save()
        Attribute.objects.create(thing=self, revision=next_revision, key=attr_name)

DATATYPES = ('text', 'int', 'float', 'date', 'reference')
DATATYPES = zip(DATATYPES, DATATYPES)

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
LEN_DATE_FORMAT = len(datetime.now().strftime(DATE_FORMAT))

class Attribute(models.Model):
    thing = models.ForeignKey(Thing)
    revision = models.PositiveIntegerField()
    key = models.CharField(max_length=255, index=True)
    value = models.TextField()
    datatype = models.CharField(max_length=16, choices=DATATYPES)
    created = models.DateTimeField(default=datetime.now, index=True)
    
    class Meta:
        unique_together = ('thing', 'revision')
        order_with_respect_to = 'thing'
    
    @classmethod    
    def store(cls, thing, revision, key, value, datatype=None):
        if datatype is None:
            if isinstance(value, str):
                raise TypeError('Strings must be converted to Unicode for storage')
            elif isinstance(value, unicode):
                datatype = 'text'
                value = value.encode('utf-8')
            elif isinstance(value, (int, long)):
                datatype = 'int'
                value = str(value)
            elif isinstance(value, datetime):
                datatype = 'date'
                value = value.strftime(DATE_FORMAT)
            elif isinstance(value, Item):
                if id is None:
                    raise TypeError('Items must be saved before assignment as an Attribute')
                datatype = 'reference'
                value = value.id
        cls.objects.create(thing=thing, revision=revision, key=key, value=value, 
                           datatype=datatype)
                
    def get_value(self):
        if self.datatype == 'text':
            return self.value.decode('utf-8')
        elif self.datatype == 'int':
            return int(self.value)
        elif self.datatype == 'float':
            return float(self, value)
        elif self.datatype == 'date':
            return datetime.strptime(self.value[:LEN_DATE_FORMAT], DATE_FORMAT)
        elif self.datatype == 'reference':
            return Item.objects.get(id=int(self.value))
        else:
            raise ValueError('Unknown datatype "%s" (%s:%s)' % (self.datatype, self.key, self.value))
            
class Version(models.Model):
    thing = models.ForeignKey(Thing, index=True)
    revision = models.PositiveIntegerField(index=True)
    author = models.ForeignKey(User, null=True)
    comment = models.TextField()
    created = models.DateTimeField(default=datetime.now, index=True)
    
    class Meta:
        unique_together = ('thing', 'revision')
        
