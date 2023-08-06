# -*- coding: utf-8 -*-
import os,sys, pickle
from collections import OrderedDict
from functools import partial
from pathlib import Path
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

#################################################################################################
def test_all():
  test1()
  test2()
  test4()
  # test3()


def test1():
  from utilmy.deeplearning.ttorch import util_model

  model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained = True)

  # Register a recorder to the 4th layer of the features part of AlexNet
  # Conv2d(64, 192, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2))
  # and record the output of the layer during the forward pass
  layer = list(model.features.named_children())[3][1]
  recorder = util_model.model_LayerRecorder(layer, record_output = True, backward = False)
  data = torch.rand(64, 3, 224, 224)
  output = model(data)
  print(recorder.recording)#tensor of shape (64, 192, 27, 27)
  recorder.close()#remove the recorder

  # Record input to the layer during the forward pass
  recorder = util_model.model_LayerRecorder(layer, record_input = True, backward = False)
  data = torch.rand(64, 3, 224, 224)
  output = model(data)
  print(recorder.recording)#tensor of shape (64, 64, 27, 27)
  recorder.close()#remove the recorder

  # Register a recorder to the 4th layer of the features part of AlexNet
  # MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
  # and record the output of the layer in the bacward pass
  layer = list(model.features.named_children())[2][1]
  # Record output to the layer during the backward pass
  recorder = util_model.model_LayerRecorder(layer, record_output = True, backward = True)
  data = torch.rand(64, 3, 224, 224)
  output = model(data)
  loss = torch.nn.CrossEntropyLoss()
  labels = torch.randint(1000, (64,))#random labels just to compute a bacward pass
  l = loss(output, labels)
  l.backward()
  print(recorder.recording[0])#tensor of shape (64, 64, 27, 27)
  recorder.close()#remove the recorder

  # Register a recorder to the 4th layer of the features part of AlexNet
  # Conv2d(64, 192, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2))
  # and record the parameters of the layer in the forward pass
  layer = list(model.features.named_children())[3][1]
  recorder = util_model.model_LayerRecorder(layer, record_params = True, backward = False)
  data = torch.rand(64, 3, 224, 224)
  output = model(data)
  print(recorder.recording)#list of tensors of shape (192, 64, 5, 5) (weights) (192,) (biases)
  recorder.close()#remove the recorder

  # A custom function can also be passed to the recorder and perform arbitrary
  # operations. In the example below, the custom function prints the kwargs that
  # are passed along with the custon function and also return 1 (stored in the recorder)
  def custom_fn(*args, **kwargs):#signature of any custom fn
      print('custom called')
      for k,v in kwargs.items():
          print('\nkey argument:', k)
          print('\nvalue argument:', v)
      return 1

  recorder = util_model.model_LayerRecorder(layer,
                                            backward = False,
                                            custom_fn = custom_fn,
                                            print_value = 5)
  data = torch.rand(64, 3, 224, 224)
  output = model(data)
  print(recorder.recording)#list of tensors of shape (192, 64, 5, 5) (weights) (192,) (biases)
  recorder.close()#remove the recorder

  # Record output to the layer during the forward pass and store it in folder
  layer = list(model.features.named_children())[3][1]
  recorder = util_model.model_LayerRecorder(
      layer,
      record_params = True,
      backward = False,
      save_to = './test_recorder'#create the folder before running this example!
  )
  for _ in range(5):#5 passes e.g. batches, thus 5 stored "recorded" tensors
      data = torch.rand(64, 3, 224, 224)
      output = model(data)
  recorder.close()#remove the recorder



def test2():
        import torch
        from utilmy.deeplearning.ttorch import util_model

        model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained = True)

        # Freeze all parameters
        util_model.model_freezeparams(model,
                                      freeze = True)

        # Unfreeze all parameters
        util_model.model_freezeparams(model,
                                      freeze = False)

        # Freeze specific parameters by naming them
        params_to_freeze = ['features.0.weight', 'classifier.1.weight']
        util_model.model_freezeparams(model,
                                      params_to_freeze = params_to_freeze,
                                      freeze = True)

        # Unfreeze specific parameters by naming them
        params_to_freeze = ['features.0.weight', 'classifier.1.weight']
        util_model.model_freezeparams(model,
                                      params_to_freeze = params_to_freeze,
                                      freeze = False)


        model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained = True)

        # Get all parameters
        params_values, params_names, req_grad = util_model.model_getparams(model)

        # Get only a subset of parameters by passing a list of named parameters
        params_to_get = ['features.0.weight', 'classifier.1.weight']
        params_values, params_names, req_grad = util_model.model_getparams(model,
                                                                           params_to_get = params_to_get)



        model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained = True)

        # Delete the last layer of the classifier of the AlexNet model
        model.classifier = util_model.model_layers_delete(model.classifier, del_ids = [6])

        # Delete the last linear layer of an Elman RNN
        simple_rnn = nn.Sequential(
            nn.RNN(2,
                100,
                1,
                batch_first = True),
            nn.Linear(100, 10),
        )

        simple_rnn = util_model.model_layers_delete(simple_rnn, del_ids = [1])




        model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained = True)

        # Delete the last layer of the classifier of the AlexNet model
        model.classifier = util_model.model_layers_delete(model.classifier, del_ids = [6])

        # Add back to the model the deleted layer
        module = {
                'name': '6',
                'position': 6,
                'module': nn.Linear(in_features = 4096, out_features = 1000, bias = True)
                }

        model.classifier = util_model.model_layers_add(model.classifier, modules = [module])



def test3():
    import matplotlib.pyplot as plt
    import numpy as np
    import torch
    import torchvision
    import torchvision.transforms as transforms

    from utilmy.deeplearning.ttorch import util_model

    #Load pretrained AlexNet and CIFAR
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    batch_size = 32
    testset = torchvision.datasets.CIFAR10(root = './CIFAR_torchvision',
                                          train = False,
                                          download = True,
                                          transform = transform)
    testloader = torch.utils.data.DataLoader(testset,
                                            batch_size = batch_size,
                                            shuffle = True)
    # Assign a recorder to a layer of AlexNet:
    # here: MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
    model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained = True)
    layer = list(model.features.named_children())[5][1]
    recorder = util_model.model_LayerRecorder(layer, record_output = True, backward = False)

    #Grab a batch and pass it through the model
    X,Y = next(iter(testloader))
    out = model(X)

    # Compute similarity of representations in selected layer for images in batch
    rec = recorder.recording.detach().clone()
    rec = rec.reshape(batch_size, -1)
    sim = np.corrcoef(rec.numpy())
    plt.imshow(sim)
    plt.colorbar()


def test4():
   class_label_dict =  {'gender': 2,'season': 4,'age':5 }  ##5 n_unique_label
   layers_dim=[512, 256]

   batch_size       = 64
   X       = torch.rand(batch_size, 512)
   y_true  = { 'gender': torch.rand(batch_size, 2),
               'season': torch.rand(batch_size, 4) ,
               'age':    torch.rand(batch_size, 5) }

   model  = MultiClassMultiLabel_Head(layers_dim = layers_dim, class_label_dict = class_label_dict)
   y_pred = model(X)
   loss = model.get_loss(y_pred, y_true)




#################################################################################################
################ Model tooling ##################################################################
def model_getparams(model, params_to_get = None, detach = True):
    '''Extracts the parameters, names, and 'requires gradient' status from  model
    Docs::

        Input
        -----
        model: class instance based on the base class torch.nn.Module

        params_to_get: list of str, default=None, specifying the names of the
            parameters to be extracted
            If None, then all parameters and names of parameters from the model
            will be extracted

        detach: bool, default True, detach the tensor from the computational graph

        Output
        ------
        params_name: list, contaning one str for each extracted parameter

        params_values: list, containg one tensor corresponding to each
            parameter.
            NOTE: The tensor is detached from the computation graph

        req_grad: list, containing one Boolean variable for each parameter
            denoting the requires_grad status of the tensor/parameter
            of the model
    '''
    params_names = []
    params_values = []
    req_grad = []
    for name, param in zip(model.named_parameters(), model.parameters()):
        if params_to_get is not None:
            if name[0] in params_to_get:
                params_names.append(name[0])
                if detach is True:
                    params_values.append(param.detach().clone())
                elif detach is False:
                    params_values.append(param.clone())
                req_grad.append(param.requires_grad)
        else:
            params_names.append(name[0])
            if detach is True:
                params_values.append(param.detach().clone())
            elif detach is False:
                params_values.append(param.clone())
            req_grad.append(param.requires_grad)

    return params_values, params_names, req_grad


def model_freezeparams(model,  params_to_freeze = None,  freeze = True):
    '''Freeze or unfreeze the parametrs of a model
    Docs::

        Input
        -----
        model:  class instance based on the base class torch.nn.Module

        params_to_freeze: list of str specifying the names of the params to be
            frozen or unfrozen

        freeze: bool, default True, specifying the freeze or
            unfreeze of model params

        Output
        ------
        model: class instance based on the base class torch.nn.Module with changed
            requires_grad param for the anmes params in params_to_freeze
            (freeze = requires_grad is False unfreeze = requires_grad is True)
    '''
    for name, param in zip(model.named_parameters(), model.parameters()):
        if params_to_freeze is not None:
            if name[0] in params_to_freeze:
                param.requires_grad = True if freeze is False else False
        else:
            param.requires_grad = True if freeze is False else False


def model_layers_delete(model, del_ids = []):
    '''Delete layers from model

    Input
    -----
    model: model to be modified

    del_ids: list, default [], of int the modules/layers
        that will be deleted
        NOTE: 0, 1... denotes the 1st, 2nd etc layer

    Output
    ------
    model: model with deleted modules/layers that is an instance of
        torch.nn.modules.container.Sequential
    '''
    children = [c for i,c in enumerate(model.named_children()) if i not in del_ids]
    model = torch.nn.Sequential(
        OrderedDict(children)
    )

    return model


def model_layers_add(model, modules = []):
    '''Add layers/modules to torch.nn.modules.container.Sequential

    Input
    -----
    model: instance of class of base class torch.nn.Module

    modules: list of dict
        each dict has key:value pairs

        {
        'name': str
        'position': int
        'module': torch.nn.Module
        }

        with:
            name: str, name to be added in the nn.modules.container.Sequential

            position: int, [0,..N], with N>0, also -1, where N the total
            nr of modules in the torch.nn.modules.container.Sequential
            -1 denotes the module that will be appended at the end

            module: torch.nn.Module

    Output
    ------
    model: model with added modules/layers that is an instance of
        torch.nn.modules.container.Sequential
    '''
    all_positions = [m['position'] for m in modules]
    current_children = [c for c in model.named_children()]
    children = []
    children_idx = 0
    iterations = len(current_children) + len(all_positions)
    if -1 in all_positions: iterations -= 1
    for i in range(iterations):
        if i not in all_positions:
            children.append(current_children[children_idx])
            children_idx += 1
        else:
            idx = all_positions.index(i)
            d = modules[idx]
            children.append((d['name'], d['module']))
    if -1 in all_positions:
        idx = all_positions.index(-1)
        d = modules[idx]
        children.append((d['name'], d['module']))

    model = torch.nn.Sequential(
        OrderedDict(children)
    )

    return model


def model_layers_getall(model):
    '''
    Get all the children (layers) from a model, even the ones that are nested

    Input
    -----
    model: class instance based on the base class torch.nn.Module

    Output
    ------
    all_layers: list of all layers of the model

    Adapted from:
    https://stackoverflow.com/questions/54846905/pytorch-get-all-layers-of-model
    '''
    children = list(model.children())
    all_layers = []
    if not children:#if model has no children model is last child
        return model
    else:
       # Look for children from children to the last child
       for child in children:
            try:
                all_layers.extend(model_layers_getall(child))
            except TypeError:
                all_layers.append(model_layers_getall(child))

    return all_layers



class model_LayerRecorder():
    '''Get input, output or parameters to a module/layer by registering forward or backward hooks
    Docs ::

        module: a module of a class in torch.nn.modules

        record_input: bool, default False, deciding if input to module will be
            recorded

        record_output: bool, default False, deciding if output to module will be
            recorded

        record_params: bool, default False, deciding if params of module will be
            recorded

        params_to_get: list of str, default None, specifying the parameters to be
            recorded from the module (if None all parameters are recorded)
            NOTE: meaningful only if record_params

        backward: bool, default False, deciding if a forward or backward hook
            will be registered and the recprding will be performed accordingly

        custom_fn: function, default None, to be executed in the forward or backward
            pass.

            It must have the following signature:

            custom_fn(module, output, input, **kwars)

            with kwars optional

            The signature follows the signature of functions to be registered
            in hooks. See for more details:
            https://pytorch.org/docs/stable/generated/torch.nn.modules.module.register_module_forward_hook.html

         save_to: str, default None, specifying a path to a folder for all recordings
             to be saved.
             NOTE: recodrings are saved with filename: recording_0, recording_1, recording_N

         **kwargs: if keyword args are specified they will be passed as to the
             custom_fn


        The attribute recording contains the output, input or params of a module
    '''
    def __init__(self,
                 module,
                 record_input = False,
                 record_output = False,
                 record_params = False,
                 params_to_get = None,
                 backward = False,
                 custom_fn = None,
                 save_to = None,
                 **kwargs):
        self.params_to_get = params_to_get
        self.kwargs = kwargs if kwargs else None
        if save_to:
            self.counter = 0#if path is specified, keep a counter
            self.save_to = save_to
        if record_input is True:
            fn = partial(self._fn_in_out_params, record_what = 'input')
        elif record_output is True:
            fn = partial(self._fn_in_out_params, record_what = 'output')
        elif record_params is True:
            fn = partial(self._fn_in_out_params, record_what = 'params')

        if custom_fn is not None:
            fn = self._custom_wrapper
            self.custom_fn = custom_fn

        if backward is False:
            self.hook = module.register_forward_hook(fn)
        elif backward is True:
            self.hook = module.register_full_backward_hook(fn)

    def _fn_in_out_params(self, module, input, output, record_what = None):
        att = getattr(self, 'save_to', None)
        if att is None:
            if record_what == 'input':
                self.recording = input
            elif record_what == 'output':
                self.recording = output
            elif record_what == 'params':
                params = model_getparams(module, params_to_get = self.params_to_get)[0]
                self.recording = params
        else:
            name = 'recording_' + str(self.counter)
            filename = Path(self.save_to) / name
            self.counter += 1

            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as handle:
                if record_what == 'input':
                    pickle.dump(input, handle, protocol = pickle.HIGHEST_PROTOCOL)
                elif record_what == 'output':
                    pickle.dump(output, handle, protocol = pickle.HIGHEST_PROTOCOL)
                elif record_what == 'params':
                    params = model_getparams(module, params_to_get = self.params_to_get)[0]
                    pickle.dump(params, handle, protocol = pickle.HIGHEST_PROTOCOL)

    def _custom_wrapper(self, module, input, output):
        if self.kwargs:
            res = self.custom_fn(module, input, output, **self.kwargs)
        else:
            res = self.custom_fn(module, input, output)
        att = getattr(self, 'save_to', None)
        if res and att is None:
            self.recording = res
        elif res and att:
            name = 'recording_' + str(self.counter)
            filename = Path(self.save_to) / name
            self.counter += 1
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as handle:
                pickle.dump(res, handle, protocol = pickle.HIGHEST_PROTOCOL)

    def close(self):
        self.hook.remove()
        att = getattr(self, 'counter', None)
        if att: self.counter = 0


class model_getlayer():
    """ Get a specific layer for embedding output
    Doc::

        model = models.resnet50()
        layerI= model_getlayer(model, pos_layer=-1)

        ### Forward pass
        Xin = torch.randn(4, 3, 224, 224)
        print( model(Xin) )

        print('emb')
        Xemb = layerI.output
        print(Xemb.shape)
        print(Xemb)

    """
    def __init__(self, network, backward=False, pos_layer=-2):
        self.layers = []
        self.get_layers_in_order(network)
        self.last_layer = self.layers[pos_layer]
        self.hook       = self.last_layer.register_forward_hook(self.hook_fn)

    def hook_fn(self, module1, input, output):
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




##################################################################################################
########### Gradient Checks ######################################################################
def model_is_gradient_needed(net_model):
        kk = 0
        for param1 in net_model.parameters():
            if kk > 5 : break
            kk = kk + 1
            # torch.testing.assert_close(param1.data, param2.data)
            if(param1.requires_grad==True):
                 return True
        return False


def plot_grad_flow(named_parameters):
    """
    Docs::

        Gradient flow check in Pytorch
        Check that the gradient flow is proper in the network by recording the average gradients per layer in every training iteration and then plotting them at the end. If the average gradients are zero in the initial layers of the network then probably your network is too deep for the gradient to flow.

        Usage
        loss = self.criterion(outputs, labels)
        loss.backward()
        plot_grad_flow(model.named_parameters()) # version 1
        # OR
        plot_grad_flow_v2(model.named_parameters()) # version 2
    """
    from matplotlib import pyplot as plt
    ave_grads = []
    layers = []
    for n, p in named_parameters:
        if(p.requires_grad) and ("bias" not in n):
            layers.append(n)
            ave_grads.append(p.grad.abs().mean())
    plt.plot(ave_grads, alpha=0.3, color="b")
    plt.hlines(0, 0, len(ave_grads)+1, linewidth=1, color="k" )
    plt.xticks(range(0,len(ave_grads), 1), layers, rotation="vertical")
    plt.xlim(xmin=0, xmax=len(ave_grads))
    plt.xlabel("Layers")
    plt.ylabel("average gradient")
    plt.title("Gradient flow")
    plt.grid(True)


def plot_grad_flow_v2(named_parameters):
    '''  Check Grad Flow
    Docs::

        Plots the gradients flowing through different layers in the net during training.
        Can be used for checking for possible gradient vanishing / exploding problems.

        Usage: Plug this function in Trainer class after loss.backwards() as
        "plot_grad_flow(self.model.named_parameters())" to visualize the gradient flow
    '''
    from matplotlib import pyplot as plt
    ave_grads = []
    max_grads= []
    layers = []
    for n, p in named_parameters:
        if(p.requires_grad) and ("bias" not in n):
            layers.append(n)
            ave_grads.append(p.grad.abs().mean())
            max_grads.append(p.grad.abs().max())
    plt.bar(np.arange(len(max_grads)), max_grads, alpha=0.1, lw=1, color="c")
    plt.bar(np.arange(len(max_grads)), ave_grads, alpha=0.1, lw=1, color="b")
    plt.hlines(0, 0, len(ave_grads)+1, lw=2, color="k" )
    plt.xticks(range(0,len(ave_grads), 1), layers, rotation="vertical")
    plt.xlim(left=0, right=len(ave_grads))
    plt.ylim(bottom = -0.001, top=0.02) # zoom in on the lower gradient regions
    plt.xlabel("Layers")
    plt.ylabel("average gradient")
    plt.title("Gradient flow")
    plt.grid(True)
    plt.legend([Line2D([0], [0], color="c", lw=4),
                Line2D([0], [0], color="b", lw=4),
                Line2D([0], [0], color="k", lw=4)], ['max-gradient', 'mean-gradient', 'zero-gradient'])






##################################################################################################
########### Computer vision ######################################################################
def vision_prediction_check():
    """ Tooling for Vision checks
    Docs::

            https://github.com/jacobgil/pytorch-grad-cam

            https://github.com/pytorch/captum

    """
    pass







###############################################################################################
########### Custom layer ######################################################################
class MultiClassMultiLabel_Head(nn.Module):
    """  Multi Class Multi Label head
    Docs::

        class_label_dict :  {'gender': 2,  'age' : 5}  ##5 n_unique_label

    """
    def __init__(self, layers_dim=[256,64],  class_label_dict=None, dropout=0, activation_custom=None,
                 use_first_head_only= None ):

        super().__init__()
        self.dropout     = nn.Dropout(dropout)
        self.activation  = nn.ReLU() if activation_custom is None else activation_custom
        self.use_first_head_only = use_first_head_only

        if self.use_first_head_only:
            for key,val in class_label_dict.items() :
              break
            self.class_label_dict = {key: val}
        else :
            self.class_label_dict = class_label_dict


        ########Common part #################################################################
        self.linear_list = []
        out_dimi = layers_dim[0]
        for i,dimi in enumerate(layers_dim[1:]) :
            # Layer 1
            in_dimi  = out_dimi
            out_dimi = layers_dim[i]
            self.linear_list.append(nn.Linear(in_features=in_dimi, out_features=out_dimi, bias=False) )

        dim_final = layers_dim[-1]
        self.linear_list = nn.Sequential(*self.linear_list)


        ########Multi-Class ################################################################
        self.head_task_dict = {}
        for classname, n_unique_label in class_label_dict.items():
            self.head_task_dict[classname] = []
            self.head_task_dict[classname].append(nn.Linear(dim_final, n_unique_label))
            self.head_task_dict[classname].append(nn.Linear(n_unique_label, 1))
            self.head_task_dict[classname] = nn.Sequential( *self.head_task_dict[classname])


        #########Multi-Class ################################################################
        #self.head_task_dict = {}
        #for classname, n_unique_label in class_label_dict.items():
        #    self.head_task_dict[classname] = nn.Linear(dim_final, n_unique_label)


    def forward(self, x):
        for lin_layer in self.linear_list:
           x = self.activation(lin_layer(self.dropout(x)))

        yout = {}
        for class_i in self.class_label_dict.keys():
            yout[class_i] = self.head_task_dict[class_i](x)
            if self.use_first_head_only:
               return yout[ class_i ]

        return yout


    def get_loss(self,ypred, ytrue, loss_calc_custom=None,
                 weights=None, sum_loss=True):
        """ Get losses

        """
        if loss_calc_custom is None :
           loss_calc_fun = nn.CrossEntropyLoss()
        else :
           loss_calc_fun = loss_calc_custom()

        loss_list = []
        for ypred_col, ytrue_col in zip(ypred, ytrue) :
           loss_list.append(loss_calc_fun(ypred_col, ytrue_col) )

        if sum_loss:
            weights = 1.0 / len(loss_list) * np.ones(len(loss_list))  if weights is None else weights
            lsum = 0.0
            for li in loss_list:
                lsum = lsum + weights[i]* li
            return lsum
        return loss_list




class LSTM(nn.Module):
  def __init__(self, input_size, hidden_size, num_layers, num_classes, dropout):
    super(LSTM, self).__init__()
    self.num_layers = num_layers
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.num_classes = num_classes
    self.dropout = dropout

    self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers,
                        dropout = self.dropout, batch_first=True)
    self.fc = nn.Linear(self.hidden_size, self.num_classes)

  def forward(self, x):
    h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
    c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
    out, _ = self.lstm(x, (h0,c0))
    out = out[:,-1,:]
    out = self.fc(out)
    return out



class SequenceReshaper(nn.Module):
    def __init__(self, from_ = 'vision'):
        super(SequenceReshaper,self).__init__()
        self.from_ = from_

    def forward(self, x):
        if self.from_ == 'vision':
            x = x[:,0,:,:]
            x = x.squeeze()
            return x
        else:
            return x


###############################################################################################
########### Custom element ####################################################################
class SmeLU(torch.nn.Module):
    """
    This class implements the Smooth ReLU (SmeLU) activation function proposed in:
    https://arxiv.org/pdf/2202.06499.pdf


    Example :
        def main() -> None:
            # Init figures
            fig, ax = plt.subplots(1, 1)
            fig_grad, ax_grad = plt.subplots(1, 1)
            # Iterate over some beta values
            for beta in [0.5, 1., 2., 3., 4.]:
                # Init SemLU
                smelu: SmeLU = SmeLU(beta=beta)
                # Make input
                input: torch.Tensor = torch.linspace(-6, 6, 1000, requires_grad=True)
                # Get activations
                output: torch.Tensor = smelu(input)
                # Compute gradients
                output.sum().backward()
                # Plot activation and gradients
                ax.plot(input.detach(), output.detach(), label=str(beta))
                ax_grad.plot(input.detach(), input.grad.detach(), label=str(beta))
            # Show legend, title and grid
            ax.legend()
            ax_grad.legend()
            ax.set_title("SemLU")
            ax_grad.set_title("SemLU gradient")
            ax.grid()
            ax_grad.grid()
            # Show plots
            plt.show()

    """

    def __init__(self, beta: float = 2.) -> None:
        """
        Constructor method.
        beta (float): Beta value if the SmeLU activation function. Default 2.
        """
        # Call super constructor
        super(SmeLU, self).__init__()
        # Check beta
        assert beta >= 0., f"Beta must be equal or larger than zero. beta={beta} given."
        # Save parameter
        self.beta: float = beta

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        input (torch.Tensor): Tensor of any shape
        :return (torch.Tensor): Output activation tensor of the same shape as the input tensor
        """
        output: torch.Tensor = torch.where(input >= self.beta, input,
                                           torch.tensor([0.], device=input.device, dtype=input.dtype))
        output: torch.Tensor = torch.where(torch.abs(input) <= self.beta,
                                           ((input + self.beta) ** 2) / (4. * self.beta), output)
        return output











###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()





