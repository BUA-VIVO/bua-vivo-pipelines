from mongoengine import *

def clusterNameFormatter(nameraw):
    if nameraw.lower() == 'neurocure':
        return 'NeuroCure'
    elif nameraw in ['nc','NC','neuro cure','Neuro cure', 'neuro Cure','Neuro Cure']:
        return 'NeuroCure'
    elif nameraw.lower() == 'matters of activity':
        return 'Matters of Activity'
    elif nameraw in ['moa','MoA','MOA','mattersofactivity','mattersOfActivity','MattersOfActivity','Mattersofactivity']:
        return 'Matters of Activity'
    elif nameraw.lower() == 'science of intelligence':
        return 'Science of Intelligence'
    elif nameraw in ['scioi','SCIoI','SCIOI', 'ScienceofIntelligence','ScienceOfIntelligence','scienceofintelligence','Scienceofintelligence']:
        return 'Science of Intelligence'
    else:
        return nameraw

def updateOwnership(db,cluster):
    obj = db[0]
    owner = obj.flag_owner
    if cluster.__name__() not in owner: 
        owner.append(cluster.__name__())
        obj.flag_owner = owner
        obj.save()



    
