from mongo.mongoPipelineForEntities import importEntities
from mongo.mongoPipelineForRelations import importRelations
from ClusterScripts.moaSetup import MattersOfActivity
from ClusterScripts.NeuroCure import NeuroCure
from ClusterScripts.SCIOI import SCIoI

if __name__ == '__main__':

    # load Cluster
    moa = MattersOfActivity()
    nc = NeuroCure()
    sci = SCIoI()

    # Define Clusters to import into MongoDB
    importList = [moa,nc,sci]

    # Run Pipelines
    print('MAIN-RUN: importEntities')
    importEntities(importList)
    print('MAIN-RUN: importRelations')
    importRelations(importList)
