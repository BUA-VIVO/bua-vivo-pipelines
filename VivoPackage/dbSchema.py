from mongoengine import *

class Cluster(DynamicDocument):
    name = StringField(required=True)
    
class ClusterVCard(DynamicDocument):
    name = StringField(required=True)

class Person(DynamicDocument):
    name = StringField(required=True)
    
class Project(DynamicDocument):
    name = StringField(required=True)

class Publication(DynamicDocument):
    name = StringField(required=True)
    
class Journal(DynamicDocument):
    name = StringField(required=True)

class MembershipRole(DynamicDocument):
    name = StringField(required=True)
    
class Authorship(DynamicDocument):
    name = StringField(required=True)
    
class VCard(DynamicDocument):
    name = StringField(required=True)
    
class VCardName(DynamicDocument):
    name = StringField(required=True)
    
class Year(DynamicDocument):
    name = StringField(required=True)

class Position(DynamicDocument):
    name = StringField(required=True)
