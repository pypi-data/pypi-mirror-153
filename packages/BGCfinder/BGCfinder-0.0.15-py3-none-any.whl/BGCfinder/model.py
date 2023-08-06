import numpy as np
from tqdm import tqdm
import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import Linear
from torch_geometric.nn import GINEConv
from torch_geometric.nn import global_add_pool



class GINEConv_pretrain(torch.nn.Module):
    def __init__(self, num_hidden= 6, num_node_features=10, num_edge_features=4, out_channels=6, p=0.5, n_layers=3):
        super().__init__()
         # parameters
        self.num_node_features = num_node_features
        self.num_edge_features = num_edge_features
        self.num_hidden = num_hidden
        self.out_channels = out_channels
        self.n_layers = n_layers
        self.layers = nn.ModuleList()
        self.p = p
        
        # model structure 
        in_channels = self.num_node_features 
        for i in range(self.n_layers):
        	self.layers.append(GINEConv(nn.Linear(in_channels, self.num_hidden)))
        	in_channels = self.num_hidden
        
        self.edge_convert1 = Linear(self.num_edge_features, self.num_node_features)
        self.edge_convert2 = Linear(self.num_node_features, self.num_hidden)
        
        self.lin_out1 = Linear(self.num_hidden, self.num_hidden)
        self.lin_out2 = Linear(self.num_hidden, self.out_channels)
        
    def forward(self, data):
        in_channels = self.num_node_features 
        for i in range(self.n_layers):
        	self.layers.append(GINEConv(nn.Linear(in_channels, self.num_hidden)))
        	in_channels = self.num_hidden
        
        self.edge_convert1 = Linear(self.num_edge_features, self.num_node_features)
        self.edge_convert2 = Linear(self.num_node_features, self.num_hidden)
        
        self.lin_out1 = Linear(self.num_hidden, self.num_hidden)
        self.lin_out2 = Linear(self.num_hidden, self.out_channels)
        
    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        
        edge_attr = self.edge_convert1(edge_attr) # edge_dim : num_edge_features -> num_node_features
        x = self.layers[0](x, edge_index, edge_attr)
        x = F.elu(x)
        
        edge_attr = self.edge_convert2(edge_attr) # edge_dim : num_node_features -> num_hidden
        x = self.layers[1](x, edge_index, edge_attr)
        x = F.elu(x)     
        
        if (self.n_layers>=2):
            for i in range(2,self.n_layers):
                x = self.layers[i](x, edge_index, edge_attr)
                x = F.elu(x)
                
        x = self.lin_out1(x)
        x = F.dropout(x, p=self.p, training=self.training)
        x = self.lin_out2(x)
        
        return x
            
class GINEConv_train(torch.nn.Module):
    def __init__(self, pretrain_model, out_channels=2):
        super().__init__()
        # parameters
        self.num_node_features = pretrain_model.num_node_features
        self.num_edge_features = pretrain_model.num_edge_features
        self.num_hidden = pretrain_model.num_hidden
        self.out_channels = out_channels
        self.n_layers = pretrain_model.n_layers
        self.layers = pretrain_model.layers
        self.p = pretrain_model.p
    
        self.edge_convert1 = pretrain_model.edge_convert1
        self.edge_convert2 = pretrain_model.edge_convert2
    
        self.lin_out1 = Linear(self.num_hidden, self.num_hidden)
        self.lin_out2 = Linear(self.num_hidden, self.out_channels)
        #self.sigmoid = nn.Sigmoid()
        
    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        
        edge_attr = self.edge_convert1(edge_attr) # edge_dim : num_edge_features -> num_node_features
        x = self.layers[0](x, edge_index, edge_attr)
        x = F.elu(x)
        
        edge_attr = self.edge_convert2(edge_attr) # edge_dim : num_node_features -> num_hidden
        x = self.layers[1](x, edge_index, edge_attr)
        x = F.elu(x)     
        
        if (self.n_layers>=2):
            for i in range(2,self.n_layers):
                x = self.layers[i](x, edge_index, edge_attr)
                x = F.elu(x)
                
        x = global_add_pool(x, batch)
        x = self.lin_out1(x)
        x = F.dropout(x, p=self.p, training=self.training)
        x = self.lin_out2(x)
        
        return x

def model_prediction(model, loader, device, positive_label_position=1):
    '''
    Argument
        loader : (pytorch data loader)
        positive_label_position : the position of positive label. 
            For example, positive label position is 0 in the case of y= [True, False] 
    '''
    model.eval()
    proteinID = [] # to export proteinID
    y_probability = np.array([])
    y_pred = np.array([])
    for batch in tqdm(loader):
        batch = batch.to(device)
        out = model(batch).to(device)
        pred = out.argmax(dim=1).to(device)
        proteinID += batch.name
        
        # ROC
        probability = nn.Softmax(dim=1)(out).cpu() #convert into probility
        probability = torch.index_select(probability, 1, torch.tensor([positive_label_position])).cpu() # to select only postiive case [0: no, 1: selected]
        y_probability = np.append(y_probability, probability.cpu().detach().numpy()) # to convert into numpy
        del probability
        y_pred = np.append(y_pred, pred.cpu().detach().numpy())
        
    return proteinID, y_probability, y_pred
    
