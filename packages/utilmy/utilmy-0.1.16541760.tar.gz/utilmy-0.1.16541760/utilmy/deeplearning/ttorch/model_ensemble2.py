# -*- coding: utf-8 -*-
""" utils for model merge
Doc::

        import utilmy.deeplearning.ttorch.model_ensemble as me
        me.test1()
        me.help()

        https://discuss.pytorch.org/t/combining-trained-models-in-pytorch/28383/45

        https://discuss.pytorch.org/t/merging-3-models/66230/3

        Issue wthen reloading jupyte
                import library.Child
                reload(library)
                import library.Child

Code::

        if ARG.MODE == 'mode1':
            ARG.MODEL_INFO.TYPE = 'dataonly' 
            train_config                     = Box({})
            train_config.LR                  = 0.001
            train_config.DEVICE              = 'cpu'
            train_config.BATCH_SIZE          = 32
            train_config.EPOCHS              = 1
            train_config.EARLY_STOPPING_THLD = 10
            train_config.VALID_FREQ          = 1
            train_config.SAVE_FILENAME       = './model.pt'
            train_config.TRAIN_RATIO         = 0.7


        #### SEPARATE the models completetly, and create duplicate
        ### modelA  ########################################################
        model_ft = models.resnet18(pretrained=True)
        embA_dim = int(model_ft.fc.in_features)  ###

        ARG.modelA               = Box()   #MODEL_TASK
        ARG.modelA.name          = 'resnet18'
        ARG.modelA.nn_model      = model_ft
        ARG.modelA.layer_emb_id          = 'fc'
        ARG.modelA.architect     = [ embA_dim]  ### head s
        ARG.modelA.dataset       = Box()
        ARG.modelA.dataset.dirin = "/"
        ARG.modelA.dataset.coly  = 'ytarget'
        modelA = modelA_create(ARG.modelA)
        

        ### modelB  ########################################################
        model_ft = models.resnet50(pretrained=True)
        embB_dim = int(model_ft.fc.in_features)

        ARG.modelB               = Box()   
        ARG.modelB.name          = 'resnet50'
        ARG.modelB.nn_model      = model_ft
        ARG.modelB.layer_emb_id          = 'fc'
        ARG.modelB.architect     = [embB_dim ]   ### head size
        ARG.modelB.dataset       = Box()
        ARG.modelB.dataset.dirin = "/"
        ARG.modelB.dataset.coly  = 'ytarget'
        modelB = modelB_create(ARG.modelB )

        
        ### merge_model  ###################################################
        ARG.merge_model           = Box()
        ARG.merge_model.name      = 'modelmerge1'
        ARG.merge_model.architect = { 'layers_dim': [ 200, 32, 1 ] }

        ARG.merge_model.architect.merge_type= 'cat'

        ARG.merge_model.dataset       = Box()
        ARG.merge_model.dataset.dirin = "/"
        ARG.merge_model.dataset.coly = 'ytarget'
        ARG.merge_model.train_config  = train_config
        model = MergeModel_create(ARG, modelB=modelB, modelA=modelA)


        #### Run Model   ###################################################
        # load_DataFrame = modelB_create.load_DataFrame   
        # prepro_dataset = modelB_create.prepro_dataset
        model.build()        
        model.training(load_DataFrame, prepro_dataset) 
        inputs = torch.randn((1,5)).to(model.device)
        outputs = model.predict(inputs)


TODO :
    make get_embedding works


"""
import os, random, numpy as np, pandas as pd ;from box import Box
from copy import deepcopy
import copy, collections
from abc import abstractmethod

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import torchvision
from torchvision import transforms, datasets, models
#############################################################################################
from utilmy import log

##############################################################################################
def help():
    """function help
    """
    from utilmy import help_create
    ss =  help_create(__file__)
    log(ss)



##############################################################################################
def test_all():
    test1()
    test2a()
    test2b()
    test2c()
    test2d()



def test1():    
    """     
    """    
    from box import Box ; from copy import deepcopy
    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = Box()


    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    def load_DataFrame():
        return df

    prepro_dataset = None 
    

    ##################################################################
    if ARG.MODE == 'mode1':
        ARG.MODEL_INFO.TYPE = 'dataonly' 
        #train_config
        train_config                     = Box({})
        train_config.LR                  = 0.001
        train_config.SEED                = 42
        train_config.DEVICE              = 'cpu'
        train_config.BATCH_SIZE          = 32
        train_config.EPOCHS              = 1
        train_config.EARLY_STOPPING_THLD = 10
        train_config.VALID_FREQ          = 1
        train_config.SAVE_FILENAME       = './model.pt'
        train_config.TRAIN_RATIO         = 0.7
        train_config.VAL_RATIO           = 0.2
        train_config.TEST_RATIO          = 0.1

    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ########################################################
    ARG.modelA               = Box()   #MODEL_TASK
    ARG.modelA.name          = 'modelA1'
    ARG.modelA.nn_model      = None        
    ARG.modelA.architect     = [ 5, 100, 16 ]
    ARG.modelA.dataset       = Box()
    ARG.modelA.nn_model      = None
    ARG.modelA.layer_emb_id  = ""
    ARG.modelA.dataset.dirin = "/"
    ARG.modelA.dataset.coly  = 'ytarget'
    modelA = modelA_create(ARG.modelA)


    ### modelB  ########################################################
    ARG.modelB               = Box()   
    ARG.modelB.name          = 'modelB1'
    ARG.modelB.nn_model      = None
    ARG.modelB.architect     = [5,100,16]
    ARG.modelB.dataset       = Box()
    ARG.modelB.nn_model      = None
    ARG.modelB.layer_emb_id  = ""
    ARG.modelB.dataset.dirin = "/"
    ARG.modelB.dataset.coly  = 'ytarget'
    modelB = modelB_create(ARG.modelB )

    
    ### merge_model  ###################################################
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'
    #ARG.merge_model.architect = { 'layers_dim': [ 200, 32, 1 ] }
    #ARG.merge_model.architect.merge_type= 'cat'

    ARG.merge_model.architect = {}
    ARG.merge_model.architect.input_dim        =  200
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [100, 32]
    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]

    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    modelC = None
    model_create_list = [modelA, modelB, modelC]
    model = model = MergeModel_create(ARG, model_create_list)

    #### Run Model   ###################################################
    model.build()        
    model.training(load_DataFrame, prepro_dataset) 
    model.save_weight('ztmp/model_x5.pt') 
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,5)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)

def test2a():    
    """     
    """    
    from box import Box ; from copy import deepcopy
    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = Box()


    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    def load_DataFrame():
        return df

    prepro_dataset = None 
    

    ##################################################################
    if ARG.MODE == 'mode1':
        ARG.MODEL_INFO.TYPE = 'dataonly' 
        #train_config
        train_config                     = Box({})
        train_config.LR                  = 0.001
        train_config.SEED                = 42
        train_config.DEVICE              = 'cpu'
        train_config.BATCH_SIZE          = 32
        train_config.EPOCHS              = 1
        train_config.EARLY_STOPPING_THLD = 10
        train_config.VALID_FREQ          = 1
        train_config.SAVE_FILENAME       = './model.pt'
        train_config.TRAIN_RATIO         = 0.7
        train_config.VAL_RATIO           = 0.2
        train_config.TEST_RATIO          = 0.1


    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ########################################################
    ARG.modelA               = Box()   #MODEL_TASK
    ARG.modelA.name          = 'modelA1'
    ARG.modelA.architect     = [ 5, 100, 16 ]
    ARG.modelA.dataset       = Box()
    ARG.modelA.nn_model      = None
    ARG.modelA.layer_emb_id          = ""
    ARG.modelA.dataset.dirin = "/"
    ARG.modelA.dataset.coly  = 'ytarget'
    ARG.modelA.seed          = 42
    modelA = modelA_create(ARG.modelA)


    ### modelB  ########################################################
    ARG.modelB               = Box()
    ARG.modelB.name         = 'modelB1'
    ARG.modelB.architect     = [5,100,16]
    ARG.modelB.dataset       = Box()
    ARG.modelB.nn_model      = None
    ARG.modelB.layer_emb_id          = ""
    ARG.modelB.dataset.dirin = "/"
    ARG.modelB.dataset.coly  = 'ytarget'
    ARG.modelB.seed          = 42
    modelB = modelB_create(ARG.modelB )

    ### merge_model  ###################################################
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'
    ARG.merge_model.seed      = 42
    ARG.merge_model.architect = {}
    ARG.merge_model.architect.input_dim        =  200
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [100, 32]
    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]


    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    modelC = None
    model_create_list = [modelA, modelB, modelC]
    model = model = MergeModel_create(ARG, model_create_list)


    #### Run Model   ###################################################
    # load_DataFrame = modelB_create.load_DataFrame   
    # prepro_dataset = modelB_create.prepro_dataset
    model.build()        
    model.training(load_DataFrame, prepro_dataset) 

    model.save_weight('ztmp/model_x5.pt') 
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,5)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)

def test2b():    
    """     
    """    
    from box import Box ; from copy import deepcopy
    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = Box()


    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    ###########################

    def load_DataFrame():
        return df  

    ##################################################################
    if ARG.MODE == 'mode1':
        ARG.MODEL_INFO.TYPE = 'dataonly' 
        #train_config
        train_config                     = Box({})
        train_config.LR                  = 0.001
        train_config.SEED                = 42
        train_config.DEVICE              = 'cpu'
        train_config.BATCH_SIZE          = 32
        train_config.EPOCHS              = 1
        train_config.EARLY_STOPPING_THLD = 10
        train_config.VALID_FREQ          = 1
        train_config.SAVE_FILENAME       = './model.pt'
        train_config.TRAIN_RATIO         = 0.7
        train_config.VAL_RATIO           = 0.2
        train_config.TEST_RATIO          = 0.1

    def prepro_dataset(self,df:pd.DataFrame=None):
        trainx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        trainy = torch.rand(train_config.BATCH_SIZE)
        validx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        validy = torch.rand(train_config.BATCH_SIZE)
        testx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        testy = torch.rand(train_config.BATCH_SIZE)
        return (trainx, trainy,validx,validy,testx,testy)

    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ########################################################
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA               = Box()   #MODEL_TASK
    ARG.modelA.name          = 'resnet18'
    ARG.modelA.nn_model      = model_ft
    ARG.modelA.layer_emb_id  = 'fc'
    ARG.modelA.architect     = [ embA_dim]  ### head s
    ARG.modelA.dataset       = Box()
    ARG.modelA.dataset.dirin = "/"
    ARG.modelA.dataset.coly  = 'ytarget'
    modelA = modelA_create(ARG.modelA)
    
    #model_ft.fc = modelA
    ### modelB  ########################################################
    model_ft = models.resnet50(pretrained=True)
    embB_dim = model_ft.fc.in_features

    ARG.modelB               = Box()   
    ARG.modelB.name          = 'resnet50'
    ARG.modelB.nn_model      = model_ft
    ARG.modelB.layer_emb_id  = 'fc'
    ARG.modelB.architect     = [embB_dim ]   ### head size
    ARG.modelB.dataset       = Box()
    ARG.modelB.dataset.dirin = "/"
    ARG.modelB.dataset.coly  = 'ytarget'
    modelB = modelB_create(ARG.modelB )

    
    ### merge_model  ###################################################
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'
    #ARG.merge_model.architect = { 'layers_dim': [ embA_dim + embB_dim, 32, 1 ] }
    #ARG.merge_model.architect.merge_type= 'cat'
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [512, 32]
    ARG.merge_model.architect.merge_custom     = None

    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]
    ARG.merge_model.architect.head_custom      = None

    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly  = 'ytarget'
    ARG.merge_model.train_config  = train_config
    modelC = None
    model_create_list = [modelA, modelB, modelC]
    model = MergeModel_create(ARG, model_create_list)

    #### Run Model   ###################################################
    # load_DataFrame = modelB_create.load_DataFrame   
    # prepro_dataset = modelB_create.prepro_dataset
    model.build()
    model.training(load_DataFrame, prepro_dataset) 

    model.save_weight('ztmp/model_x5.pt') 
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,224,224)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)

def test2c():    
    """     
    """    
    from box import Box ; from copy import deepcopy

    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = Box()


    ####################################################################
    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    def load_DataFrame():
        return df  

    def prepro_dataset(self,df:pd.DataFrame=None):
        trainx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        trainy = torch.rand(train_config.BATCH_SIZE)
        validx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        validy = torch.rand(train_config.BATCH_SIZE)
        testx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        testy = torch.rand(train_config.BATCH_SIZE)
        return (trainx, trainy,validx,validy,testx,testy)


    ##################################################################
    train_config                     = Box({})
    if ARG.MODE == 'mode1':
        ARG.MODEL_INFO.TYPE = 'dataonly' 
        #train_config
        train_config.LR                  = 0.001
        train_config.SEED                = 42
        train_config.DEVICE              = 'cpu'
        train_config.BATCH_SIZE          = 4
        train_config.EPOCHS              = 1
        train_config.EARLY_STOPPING_THLD = 10
        train_config.VALID_FREQ          = 1
        train_config.SAVE_FILENAME       = './model.pt'
        train_config.TRAIN_RATIO         = 0.7
        train_config.VAL_RATIO           = 0.2
        train_config.TEST_RATIO          = 0.1


    #### SEPARATE the models completetly, and create duplicate
    
    ### modelA  ########################################################
    model_ft = models.resnet18(pretrained=True)
    embA_dim = int(model_ft.fc.in_features)  ###

    ARG.modelA               = Box()   #MODEL_TASK
    ARG.modelA.name          = 'resnet18'
    ARG.modelA.nn_model      = model_ft
    ARG.modelA.layer_emb_id          = 'fc'
    ARG.modelA.architect     = [ embA_dim]  ### head s
    ARG.modelA.dataset       = Box()
    ARG.modelA.dataset.dirin = "/"
    ARG.modelA.dataset.coly  = 'ytarget'
    modelA = modelA_create(ARG.modelA)
    


    ### modelB  ########################################################
    model_ft = models.resnet50(pretrained=True)
    embB_dim = int(model_ft.fc.in_features)

    ARG.modelB               = Box()   
    ARG.modelB.name          = 'resnet50'
    ARG.modelB.nn_model      = model_ft
    ARG.modelB.layer_emb_id          = 'fc'
    ARG.modelB.architect     = [embB_dim ]   ### head size
    ARG.modelB.dataset       = Box()
    ARG.modelB.dataset.dirin = "/"
    ARG.modelB.dataset.coly  = 'ytarget'
    modelB = modelB_create(ARG.modelB )


    # ### modelC  ########################################################
    embC_dim                 = 0
    model_ft                 = models.vgg11(pretrained=True)
    embC_dim                 = int(model_ft.classifier[-1].in_features)
    ARG.modelC               = Box()   
    ARG.modelC.name          = 'resnet50'
    ARG.modelC.nn_model      = model_ft
    ARG.modelC.layer_emb_id          = 'fc'
    ARG.modelC.architect     = [ embC_dim ]   ### head size
    ARG.modelC.dataset       = Box()
    ARG.modelC.dataset.dirin = "/"
    ARG.modelC.dataset.coly  = 'ytarget'
    modelC = modelC_create(ARG.modelC )



    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY  : because it's merge
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'

    #ARG.merge_model.architect = { 'layers_dim': [ embA_dim + embB_dim + embC_dim, 32, 1 ] }
    #ARG.merge_model.architect.merge_type= 'cat'
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim + embC_dim
    
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [512, 32]
    ARG.merge_model.architect.merge_custom     = None

    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]
    ARG.merge_model.architect.head_custom      = None


    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    model_create_list = [modelA, modelB, modelC]
    model = model = MergeModel_create(ARG, model_create_list)
    #### Run Model   ###################################################
    # load_DataFrame = modelB_create.load_DataFrame   
    # prepro_dataset = modelB_create.prepro_dataset
    model.build()
    model.training(load_DataFrame, prepro_dataset) 

    model.save_weight('ztmp/model_x5.pt') 
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,224,224)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)

def test2d():    
    """     
    """    
    from box import Box ; from copy import deepcopy
    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = Box()


####################################################################
    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)
    
    def load_DataFrame():
        return df  

    ##################################################################
    train_config                     = Box({})
    if ARG.MODE == 'mode1':
        ARG.MODEL_INFO.TYPE = 'dataonly' 
        #train_config                           = Box({})
        train_config.LR                        = 0.001
        train_config.SEED                      = 42
        train_config.DEVICE                    = 'cpu'
        train_config.BATCH_SIZE                = 64
        train_config.EPOCHS                    = 1
        train_config.EARLY_STOPPING_THLD       = 10
        train_config.VALID_FREQ                = 1
        train_config.SAVE_FILENAME             = './model.pt'
        train_config.TRAIN_RATIO               = 0.7
        train_config.VAL_RATIO                 = 0.2
        train_config.TEST_RATIO                = 0.1

    def test_dataset_f_mnist(samples=100):
        """function test_dataset_f_mnist
        """
        # Generate the transformations
        train_list_transforms = [transforms.ToTensor(),transforms.Lambda(lambda x: x.repeat(3, 1, 1))]
        train_dataset = datasets.FashionMNIST(root="data",train=True,
                                              transform=transforms.Compose(train_list_transforms),download=True)
        
        #sampling the requred no. of samples from dataset 
        dataset = torch.utils.data.Subset(train_dataset, np.arange(samples))
        data_smpls    = []
        trgt_smpls    = []
        for data, targets in dataset:
            data_smpls.append(data)
            trgt_smpls.append(targets)

        #Converting list to tensor format
        data_smpls,trgt_smpl = torch.stack(data_smpls),torch.Tensor(trgt_smpls) 

        train_ratio = train_config.TRAIN_RATIO
        test_ratio  = train_config.TEST_RATIO
        val_ratio   = train_config.VAL_RATIO
        
        train_X, test_X, train_y, test_y = train_test_split(data_smpls,  trgt_smpl,  test_size=1 - train_ratio)
        valid_X, test_X, valid_y, test_y = train_test_split(test_X, test_y, test_size= test_ratio / (test_ratio + val_ratio))
        return (train_X, train_y, valid_X, valid_y, test_X , test_y)

    def prepro_dataset(self,df:pd.DataFrame=None):
        train_X ,train_y,valid_X ,valid_y,test_X, test_y = test_dataset_f_mnist(samples=100)
        return train_X ,train_y,valid_X ,valid_y,test_X,test_y

    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ########################################################
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA               = Box()   #MODEL_TASK
    ARG.modelA.name          = 'resnet18'
    ARG.modelA.nn_model      = model_ft
    ARG.modelA.layer_emb_id  = 'fc'
    ARG.modelA.architect     = [ embA_dim]  ### head s
    ARG.modelA.dataset       = Box()
    ARG.modelA.dataset.dirin = "/"
    ARG.modelA.dataset.coly  = 'ytarget'
    modelA = modelA_create(ARG.modelA)
    
    ### modelB  ########################################################
    model_ft = models.resnet50(pretrained=True)
    embB_dim = int(model_ft.fc.in_features)

    ARG.modelB               = Box()   
    ARG.modelB.name          = 'resnet50'
    ARG.modelB.nn_model      = model_ft
    ARG.modelB.layer_emb_id  = 'fc'
    ARG.modelB.architect     = [embB_dim ]   ### head size
    ARG.modelB.dataset       = Box()
    ARG.modelB.dataset.dirin = "/"
    ARG.modelB.dataset.coly  = 'ytarget'
    modelB = modelB_create(ARG.modelB )

    # ### modelC  ########################################################
    embC_dim                 = 0
    model_ft                 = models.efficientnet_b0(pretrained=True)
    embC_dim                 = model_ft.classifier[1].in_features
    ARG.modelC               = Box()   
    ARG.modelC.name          = 'efficientnet_b0'
    ARG.modelC.nn_model      = model_ft
    ARG.modelC.layer_emb_id  = 'fc'
    ARG.modelC.architect     = [ embC_dim ]   ### head size
    ARG.modelC.dataset       = Box()
    ARG.modelC.dataset.dirin = "/"
    ARG.modelC.dataset.coly  = 'ytarget'
    modelC = modelC_create(ARG.modelC )


    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY  : because it's merge
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'
    #ARG.merge_model.architect = { 'layers_dim': [ embA_dim + embB_dim + embC_dim, 32, 1 ] }
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim + embC_dim

    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [1024, 768]
    ARG.merge_model.architect.merge_custom     = None

    ARG.merge_model.architect.head_layers_dim  = [128, 1]        
    ARG.merge_model.architect.head_custom      = None
  

    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    model_create_list = [modelA, modelB, modelC]
    model = MergeModel_create(ARG,model_create_list)

    #### Run Model   ###################################################
    model.build()
    model.training(load_DataFrame, prepro_dataset) 

    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)

##############################################################################################
class model_getlayer():
    def __init__(self, network, backward=False, pos_layer=-2):
        self.layers = []
        self.get_layers_in_order(network)
        self.last_layer = self.layers[pos_layer]
        self.hook       = self.last_layer.register_forward_hook(self.hook_fn)

    def hook_fn(self, module, input, output):
        self.input = input
        self.output = output

    def close(self):
        self.hook.remove()

    def get_layers_in_order(self, network):
      if len(list(network.children())) == 0:
        self.layers.append(network)
        return
      for layer in network.children():
        self.get_layers_in_order(layer)


class model_template_MLP(torch.nn.Module):
    def __init__(self,layers_dim=[20,100,16]):
        super(modelA, self).__init__()
        self.layers_dim = layers_dim 
        self.output_dim = layers_dim[-1]
        # self.head_task = nn.Sequential()
        self.head_task = []
        input_dim = layers_dim[0]
        for layer_dim in layers_dim[:-1]:
            self.head_task.append(nn.Linear(input_dim, layer_dim))
            self.head_task.append(nn.ReLU())
            input_dim = layer_dim
        self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))   #####  Do not use Sigmoid 
        self.head_task = nn.Sequential(*self.head_task)

    def forward(self, x,**kwargs):
        return self.head_task(x)


##############################################################################################
class BaseModel(object):
    """This is BaseClass for model create

    Method:
        create_model : Initialize Model (torch.nn.Module)
        evaluate: 
        prepro_dataset:  (conver pandas.DataFrame to appropriate format)
        create_loss :   Initialize Loss Function 
        training:   starting training
        build: create model, loss, optimizer (call before training)
        train: equavilent to model.train() in pytorch (auto enable dropout,vv..vv..)
        eval: equavilent to model.eval() in pytorch (auto disable dropout,vv..vv..)
        device_setup: 
        load_DataFrame: read pandas
        load_weight: 
        save_weight: 
        predict : 
    """
    
    def __init__(self,arg):
        self.arg      = Box(arg)
        self._device  = self.device_setup(arg)
        self.losser   = None
        self.is_train = False
        
    @abstractmethod
    def create_model(self,) -> torch.nn.Module:
    #   raise NotImplementedError
        log("       model is building")
    @abstractmethod
    def evaluate(self):
        raise NotImplementedError

    @abstractmethod
    def prepro_dataset(self,csv) -> pd.DataFrame:
        raise NotImplementedError
    
    @abstractmethod
    def create_loss(self,) -> torch.nn.Module:
        log("       loss is building")
        # raise NotImplementedError

    @abstractmethod
    def training(self,):
        raise NotImplementedError

    @property
    def device(self,):
        return self._device
    
    @device.setter
    def device(self,value):
        if isinstance(value,torch.device):
          self._device = value
        elif isinstance(value,str):
          self._device = torch.device(value)
        else:
          raise TypeError("device must be str or torch.device")

    def build(self,):
        self.net       = self.create_model().to(self.device)
        self.loss_calc = self.create_loss().to(self.device)
        # self.loss_calc= 
        self.is_train = False
    
    def train(self): # equivalent model.train() in pytorch
        self.is_train = True
        self.net.train()

    def eval(self):     # equivalent model.eval() in pytorch
        self.is_train = False
        self.net.eval()

    def device_setup(self,arg):
        device = getattr(arg,'device','cpu')
        seed   = arg.seed if hasattr(arg,'seed') else 42
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

        if 'gpu' in device :
            try :
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
            except Exception as e:
                log(e)
                device = 'cpu'
        return device

    def load_DataFrame(self,path=None)-> pd.DataFrame:
        if path:
            log(f"reading csv from {path}")
            self.df = pd.read_csv(path,delimiter=';')
            return self.df
        if os.path.isfile(self.arg.dataset.path):
            log(f"reading csv from arg.DATASET.PATH :{self.arg.dataset.path}")
            self.df = pd.read_csv(self.arg.dataset.path,delimiter=';')
            return self.df
        else:
            import requests
            import io
            r = requests.get(self.arg.dataset.url)
            log(f"Reading csv from arg.DATASET.URL")
            if r.status_code ==200:
                self.df = pd.read_csv(io.BytesIO(r.content),delimiter=';')
            else:
                raise Exception("Can't read data, status_code: {r.status_code}")
            
            return self.df


    def load_weights(self, path):
        assert os.path.isfile(path),f"{path} does not exist"
        try:
          ckp = torch.load(path,map_location=self.device)
        except Exception as e:
          log(e)
          log(f"can't load the checkpoint from {path}")  
        if isinstance(ckp,collections.OrderedDict):
          self.net.load_state_dict(ckp)
        else:
          self.net.load_state_dict(ckp['state_dict'])
    
    def save_weight(self,path,meta_data=None):
      os.makedirs(os.path.dirname(path),exist_ok=True)
      ckp = {
          'state_dict':self.net.state_dict(),
      }
      if meta_data:
        if isinstance(meta_data,dict):
            ckp.update(meta_data)
        else:
            ckp.update({'meta_data':meta_data,})
            
        
      torch.save(ckp,path)

    def predict(self,x,**kwargs):
        # raise NotImplementedError
        output = self.net(x,**kwargs)
        return output 


class MergeModel_create(BaseModel):
    """
    """
    def __init__(self,arg:dict=None, model_create_list = None):
        """
        """
        super(MergeModel_create,self).__init__(arg)
        self.models_list = []
        if(len(model_create_list)!=0):
            for i in range(len(model_create_list)):
                if model_create_list[i] is not None:
                    self.models_list.append(model_create_list[i])

        #To handle if all models are selected as None
        if len(self.models_list)==0 or len(model_create_list)==0:
            raise Exception("No models are selected for embeddings")


    def create_model(self,):
        super(MergeModel_create,self).create_model()
        models_list           = self.models_list

        self.input_dim        = self.arg.merge_model.architect.input_dim

        self.merge_type =      self.arg.merge_model.get('merge_type','cat')
        self.merge_layers_dim= self.arg.merge_model.architect.get('merge_layers_dim', [1024, 768] )    
        self.merge_custom=     self.arg.merge_model.architect.get('merge_custom', None)

        self.head_layers_dim=  self.arg.merge_model.architect.get('head_layers_dim', [512, 128, 10] )
        self.head_custom=      self.arg.merge_model.architect.get('head_custom', None)


        class Modelmerge(torch.nn.Module):
            def __init__(self, models_list=None,
                         input_dim = 1200,  ### embA + embB + embC
                         merge_type       = 'cat',
                         merge_layers_dim = [1024, 768],
                         merge_custom     = None,
                         head_layers_dim  = [512, 128, 10],  ## 10 classe
                         head_custom      = None
                         ):
                super(Modelmerge, self).__init__()

                self.merge_type = merge_type ### merge type
                self.input_dim  = input_dim
                # assert head_layers_dim[0] == merge_layers_dim[-1]

                #### Create instance of each model   ############################
                self.model_nets = []
                for i in range(len(models_list)):
                    if(models_list[i] is not None):
                        self.model_nets.append(models_list[i])
                        self.model_nets[i] = copy.deepcopy(models_list[i].net)
                        self.model_nets[i].load_state_dict(models_list[i].net.state_dict())

                ##### Merge    #################################################
                if merge_custom is None :   ### Default merge
                    self.merge_task = []
                    input_dim = self.input_dim
                    for layer_dim in merge_layers_dim[1:-1]:
                        self.merge_task.append(nn.Linear(input_dim, layer_dim))
                        self.merge_task.append(nn.ReLU())
                        input_dim = layer_dim
                    self.merge_task.append(nn.Linear(input_dim, merge_layers_dim[-1]))

                    ##### MLP merge task
                    self.merge_task = nn.Sequential(*self.merge_task)
                else:
                    self.merge_task = merge_custom

                ##### Head Task   #############################################
                if head_custom is None :   ### Default head
                    self.head_task = []
                    input_dim = merge_layers_dim[-1]
                    for layer_dim in head_layers_dim[0:-1]:
                        self.head_task.append(nn.Linear(input_dim, layer_dim))
                        self.head_task.append(nn.ReLU())
                        input_dim = layer_dim
                    self.head_task.append(nn.Linear(input_dim, head_layers_dim[-1]))

                    ###### Not good in model due to compute errors, keep into Losss
                    # self.head_task.append(nn.Sigmoid())  #### output layer

                    ##### MLP Head task
                    self.head_task = nn.Sequential(*self.head_task)
                else:
                    self.head_task = head_custom
                

            def forward(self, x,**kw):
                z1 = self.forward_merge(x, **kw)
                z2 = self.head_task(z1)
                return z2    # predict absolute values


            def forward_merge(self, x,**kw):
                # merge: cat or add
                alpha = kw.get('alpha',0) # default only use YpredA
                scale = kw.get('scale',1)

                ## with torch.no_grad():
                embV = []
                for model in self.model_nets:
                    if model is not None:
                        emb = model.get_embedding(x)
                        emb = torch_norm_l2(emb)
                        embV.append(emb)

                ###### Concatenerate   #############################
                if self.merge_type == 'cat_combine':
                    z = torch.cat((alpha*embV[1], (1-alpha)*embV[0]), dim=-1)

                elif self.merge_type == 'cat':
                    ### May need scale
                    z = torch.cat(embV, dim=-1)

                merge_emb = self.merge_task(z)
                return merge_emb


            def get_embedding(self, x,**kw):
                z1 = self.forward_merge(x, **kw)
                return z1
        return Modelmerge(models_list,
                          input_dim        = self.input_dim,  ### embA + embB + embC
                          merge_type=        self.merge_type,
                          merge_layers_dim = self.merge_layers_dim,
                          merge_custom=      self.merge_custom,
                          head_layers_dim=   self.head_layers_dim,  ## 10 classe
                          head_custom=       self.head_custom,
                          )


    def build(self):
        # super(MergeModel_create,self).build()
        
        for i in range(len(self.models_list)):
            log("model:{}".format(i))
            self.models_list[i].build() if self.models_list[i] is not None else None

        log("MergeModel:")
        self.net       = self.create_model().to(self.device)
        self.loss_calc = self.create_loss()#.to(self.device)

        #### BE cacreful to include all the params if COmbine loss.
        #### Here, only head_task
        self.optimizer = torch.optim.Adam(self.net.head_task.parameters())
        
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode='min', factor=0.5, patience=5, 
                         verbose=True, threshold=0.0001, threshold_mode='rel', cooldown=0, min_lr=0, eps=1e-08)
        #self.optimizer = torch.optim.Adam(self.head_task )


        #### Freeze modelA, modelB, to stop gradients.
        self.freeze_all()


    def freeze_all(self,):
        for i in range(len(self.models_list)):
            if(self.models_list[i] is not None):
                for param in self.models_list[i].net.parameters():
                        param.requires_grad = False           

    def unfreeze_all(self,):
        for i in range(len(self.models_list)):
            if(self.models_list[i] is not None):
                for param in self.models_list[i].net.parameters():
                        param.requires_grad = True 

    def create_loss(self,):
        """ Simple Head task loss
           1) Only Head task loss : Classfieri head  ### Baseline
           Stop the gradient or not in modelA and modelB.
            embA_d = embA.detach()  ### Stop the gradient
            modelA_loss(x_a, embA)        
        """
        super(MergeModel_create,self).create_loss()
        loss =  torch.nn.BCEWithLogitsLoss()
        return loss
        

    def prepro_dataset(self,df:pd.DataFrame=None):
        if df is None:              
            df = self.df     # if there is no dataframe feeded , get df from model itself

        coly = 'y'
        y    = df[coly].values
        X    = df.drop([coly], axis=1).values
        nsamples = X.shape[0]

        ##### Split   #########################################################################
        seed= 42 
        train_ratio = self.arg.merge_model.train_config.TRAIN_RATIO
        test_ratio  = self.arg.merge_model.train_config.TEST_RATIO
        val_ratio   = self.arg.merge_model.train_config.TEST_RATIO
        train_X, test_X, train_y, test_y = train_test_split(X,  y,  test_size=1 - train_ratio, random_state=seed)
        valid_X, test_X, valid_y, test_y = train_test_split(test_X, test_y, test_size= test_ratio / (test_ratio + val_ratio), random_state=seed)
        return (train_X, train_y, valid_X,  valid_y, test_X,  test_y, )
        

    def training(self,load_DataFrame=None,prepro_dataset=None):
        """ Train Loop
        Docs:

             # training with load_DataFrame and prepro_data function or default funtion in self.method

        """
       
        batch_size = self.arg.merge_model.train_config.BATCH_SIZE
        EPOCHS     = self.arg.merge_model.train_config.EPOCHS
        path_save  = self.arg.merge_model.train_config.SAVE_FILENAME

        df = load_DataFrame() if load_DataFrame else self.load_DataFrame()
        if prepro_dataset:
            train_X, train_y, valid_X,  valid_y, test_X,  test_y  = prepro_dataset(self,df)
        else:
            train_X, train_y, valid_X,  valid_y, test_X,  test_y = self.prepro_dataset(df)  

        train_loader, valid_loader, test_loader =  dataloader_create(train_X, train_y, valid_X,  valid_y,
                                                                    test_X,  test_y,
                                                                    device=self.device, batch_size=batch_size)
                
        for epoch in range(1,EPOCHS+1):
            self.train()
            loss_train = 0
            with torch.autograd.set_detect_anomaly(True): 
                for inputs,targets in train_loader:                    
                    self.optimizer.zero_grad()

                    predict = self.predict(inputs)
                    predict = torch.reshape(predict,(predict.shape[0],))
                    loss    = self.loss_calc(predict, targets)
                    # loss.grad
                    loss.backward()
                    self.optimizer.step()
                    loss_train += loss * inputs.size(0)
                loss_train /= len(train_loader.dataset) # mean on dataset

            ##### Evaluation #######################################
            loss_val = 0
            self.eval()
            with torch.no_grad():
                for inputs,targets in valid_loader:
                    predict = self.predict(inputs)
                    predict = torch.reshape(predict,(predict.shape[0],))
                    self.optimizer.zero_grad()
                    loss = self.loss_calc(predict,targets)                    
                    loss_val += loss * inputs.size(0)
            loss_val /= len(valid_loader.dataset) # mean on dataset
            
            self.save_weight(  path = path_save, meta_data = { 'epoch' : epoch, 'loss_train': loss_train, 'loss_val': loss_val, } )


###################################################################
class model_create(BaseModel):
    """ modelA
    """
    def __init__(self,arg):
        super(model_create,self).__init__(arg)

    def create_model(self, modelA_nn:torch.nn.Module=None):
        super(model_create,self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id      = self.arg.layer_emb_id

        #if not modelA_nn: return modelA_nn

        ### Default version
        class modelA(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  ):   
                super(modelA, self).__init__()
                self.head_task = []
                self.layer_id  = layer_id  ##flag meaning ????  layer 

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #setattr(self.nn_model_base, self.layer_id, self.head_task)  #### head 
                    self.head_task = self.nn_model_base
                    return 

                ###### Normal MLP Head   #########################################
                self.layers_dim = layers_dim 
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()

                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)


            def forward(self, x,**kwargs):
                return self.head_task(x)


            def get_embedding(self, x,**kwargs):
                layer_l2= model_getlayer(self.head_task, pos_layer=-2)
                embA = self.forward(x)
                embA = layer_l2.output.squeeze()
                return embA

        return modelA(layers_dim, nn_model_base, layer_id)

    def create_loss(self, loss_fun=None) -> torch.nn.Module:
        super(model_create,self).create_loss()
        if not loss_fun : loss_fun
        return torch.nn.BCELoss()


class modelA_create(BaseModel):
    """ modelA
    """
    def __init__(self,arg):
        super(modelA_create,self).__init__(arg)

    def create_model(self, modelA_nn:torch.nn.Module=None):
        super(modelA_create,self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id      = self.arg.layer_emb_id

        #if not modelA_nn: return modelA_nn

        ### Default version
        class modelA(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  ):   
                super(modelA, self).__init__()
                self.head_task = []
                self.layer_id  = layer_id  ##flag meaning ????  layer 

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #setattr(self.nn_model_base, self.layer_id, self.head_task)  #### head 
                    self.head_task = self.nn_model_base
                    return 

                ###### Normal MLP Head   #########################################
                self.layers_dim = layers_dim 
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()

                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)


            def forward(self, x,**kwargs):
                return self.head_task(x)


            def get_embedding(self, x,**kwargs):
                layer_l2= model_getlayer(self.head_task, pos_layer=-2)
                embA = self.forward(x)
                embA = layer_l2.output.squeeze()
                return embA

        return modelA(layers_dim, nn_model_base, layer_id)

    def create_loss(self, loss_fun=None) -> torch.nn.Module:
        super(modelA_create,self).create_loss()
        if not loss_fun : loss_fun
        return torch.nn.BCELoss()


class modelB_create(BaseModel):
    """ modelB Creatio 
    """
    def __init__(self,arg):
        super(modelB_create,self).__init__(arg)
        self.nn_model_base = arg.nn_model

    def create_model(self):
        super(modelB_create,self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id        = self.arg.layer_emb_id
        
        class modelB(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  )   :
                super(modelB, self).__init__()                
                self.head_task = [None]
                self.layer_id    = layer_id

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #### Adding head task on top of 
                    ## setattr(self.nn_model_base, self.layer_id, self.head_task)
                    self.head_task = self.nn_model_base
                    return 

                ###### Normal MLP Head   #########################################
                self.head_task = []
                self.layers_dim = layers_dim 
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()
                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)

            def forward(self, x,**kwargs):
                return self.head_task(x)

            def get_embedding(self,x, **kwargs):
                layer_l2= model_getlayer(self.head_task, pos_layer=-2)
                embB = self.forward(x)
                embB = layer_l2.output.squeeze()
                return embB
        return modelB(layers_dim, nn_model_base, layer_id )
        

    def create_loss(self) -> torch.nn.Module:
        super(modelB_create,self).create_loss()
        return torch.nn.BCELoss()


class modelC_create(BaseModel):
    """ modelC Creatio 
    """
    def __init__(self,arg):
        super(modelC_create,self).__init__(arg)
        self.nn_model_base = arg.nn_model

    def create_model(self):
        super(modelC_create,self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id        = self.arg.layer_emb_id
        
        class modelC(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  )   :
                super(modelC, self).__init__()                
                self.head_task = [None]
                self.layer_id    = layer_id

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #### Adding head task on top of 
                    ## setattr(self.nn_model_base, self.layer_id, self.head_task)
                    self.head_task = self.nn_model_base
                    return 

                ###### Normal MLP Head   #########################################
                self.head_task = []
                self.layers_dim = layers_dim 
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()
                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)

            def forward(self, x,**kwargs):
                return self.head_task(x)

            def get_embedding(self,x, **kwargs):
                layer_l2= model_getlayer(self.head_task, pos_layer=-2)
                embC = self.forward(x)
                embC = layer_l2.output.squeeze()
                return embC
        return modelC(layers_dim, nn_model_base, layer_id )

    def create_loss(self) -> torch.nn.Module:
        super(modelC_create,self).create_loss()
        return torch.nn.BCELoss()



#################################################################################################
def device_setup(arg, device='cpu', seed=67):
    """function device_setup        
    """
    device = arg.get('device', device)
    seed   = arg.get('seed', seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if 'gpu' in device :
        try :
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        except Exception as e:
            log(e)
            device = 'cpu'
    return device


def dataloader_create(train_X=None, train_y=None, valid_X=None, valid_y=None, test_X=None, test_y=None,  
                            device='cpu', batch_size=16,)->torch.utils.data.DataLoader:
    """function dataloader_create
    Args:
        train_X:   
        train_y:   
        valid_X:   
        valid_y:   
        test_X:   
        test_y:   
        arg:   
    Returns:
        
    """
    train_loader, valid_loader, test_loader = None, None, None

    if train_X is not None :
        train_X, train_y = torch.tensor(train_X, dtype=torch.float32, device=device), torch.tensor(train_y, dtype=torch.float32, device=device)
        train_loader = DataLoader(TensorDataset(train_X, train_y), batch_size=batch_size, shuffle=True,drop_last=True)
        log("data size", len(train_X) )

    if valid_X is not None :
        valid_X, valid_y = torch.tensor(valid_X, dtype=torch.float32, device=device), torch.tensor(valid_y, dtype=torch.float32, device=device)
        valid_loader = DataLoader(TensorDataset(valid_X, valid_y), batch_size=valid_X.shape[0])
        log("data size", len(valid_X)  )

    if test_X  is not None :
        test_X, test_y   = torch.tensor(test_X,  dtype=torch.float32, device=device), torch.tensor(test_y, dtype=torch.float32, device=device)
        test_loader  = DataLoader(TensorDataset(test_X, test_y), batch_size=test_X.shape[0])
        log("data size:", len(test_X) )

    return train_loader, valid_loader, test_loader


def torch_norm_l2(X):
    """
    normalize the torch  tensor X by L2 norm.
    """
    X_norm = torch.norm(X, p=2, dim=1, keepdim=True)
    X_norm = X / X_norm
    return X_norm


###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()