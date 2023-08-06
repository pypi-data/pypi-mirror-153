
"""



utilmy/deeplearning/ttorch/model_ensemble.py
-------------------------functions----------------------
dataloader_create(train_X = None, train_y = None, valid_X = None, valid_y = None, test_X = None, test_y = None, device = 'cpu', batch_size = 16, )
device_setup(arg, device = 'cpu', seed = 67)
get_embedding()
help()
prepro_dataset_custom(df:pd.DataFrame)
test1()
test2a()
test2b()
test2c()
test2d()
test_all()
torch_norm_l2(X)

-------------------------methods----------------------
BaseModel.__init__(self, arg)
BaseModel.build(self, )
BaseModel.create_loss(self, )
BaseModel.create_model(self, )
BaseModel.device(self, )
BaseModel.device(self, )
BaseModel.device_setup(self, arg)
BaseModel.eval(self)
BaseModel.evaluate(self)
BaseModel.load_DataFrame(self, path = None)
BaseModel.load_weights(self, path)
BaseModel.predict(self, x, **kwargs)
BaseModel.prepro_dataset(self, csv)
BaseModel.save_weight(self, path, meta_data = None)
BaseModel.train(self)
BaseModel.training(self, )
MergeModel_create.__init__(self, arg:dict = None, modelA = None, modelB = None, modelC = None)
MergeModel_create.build(self)
MergeModel_create.create_loss(self, )
MergeModel_create.create_model(self, )
MergeModel_create.freeze_all(self, )
MergeModel_create.prepro_dataset(self, df:pd.DataFrame = None)
MergeModel_create.training(self, load_DataFrame = None, prepro_dataset = None)
MergeModel_create.unfreeze_all(self, )
modelA_create.__init__(self, arg)
modelA_create.create_loss(self, loss_fun = None)
modelA_create.create_model(self, modelA_nn:torch.nn.Module = None)
modelB_create.__init__(self, arg)
modelB_create.create_loss(self)
modelB_create.create_model(self)
modelC_create.__init__(self, arg)
modelC_create.create_loss(self)
modelC_create.create_model(self)
model_getlayer.__init__(self, network, backward = False, pos_layer = -2)
model_getlayer.close(self)
model_getlayer.get_layers_in_order(self, network)
model_getlayer.hook_fn(self, module, input, output)
model_template_MLP.__init__(self, layers_dim = [20, 100, 16])
model_template_MLP.forward(self, x, **kwargs)


"""