from mongoengine import *

class Person(DynamicDocument):
    name = StringField(required=True)
    
class Project(DynamicDocument):
    name = StringField(required=True)

class Publication(DynamicDocument):
    name = StringField(required=True)

class MembershipRole(DynamicDocument):
    name = StringField(required=True)
    
class Authorship(DynamicDocument):
    name = StringField(required=True)