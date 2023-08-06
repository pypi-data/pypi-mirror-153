from torch_geometric.data import Data, Dataset, InMemoryDataset
class graph_dataset(InMemoryDataset):
    def __init__(self, data_list):
        super(graph_dataset, self).__init__('/tmp/graph_dataset')
        self.data, self.slices = self.collate(data_list)

# to load
import pickle
with open("data/pretrain_dataset_20220510.pickle", "rb") as fr:
    pretrain_dataset = pickle.load(fr)
with open("data/train_dataset_20220510.pickle", "rb") as fr:
    train_dataset = pickle.load(fr)
with open("data/validation_dataset_20220510.pickle", "rb") as fr:
    validation_dataset = pickle.load(fr)
with open("data/test_dataset_20220510.pickle", "rb") as fr:
    test_dataset = pickle.load(fr)

data = train_dataset[0]
print(data)
print('=============================================================')

# Gather some statistics about the first graph.
print(f'Number of nodes: {data.num_nodes}')
print(f'Number of edges: {data.num_edges}')
print(f'Average node degree: {data.num_edges / data.num_nodes:.2f}')
print(f'Has isolated nodes: {data.has_isolated_nodes()}')
print(f'Has self-loops: {data.has_self_loops()}')
print(f'Is undirected: {data.is_undirected()}')

batch_size = 32

from torch_geometric.loader import DataLoader
pretrain_loader = DataLoader(pretrain_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
validation_loader = DataLoader(validation_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True, drop_last=True)

for step, data in enumerate(train_loader):
    print(f'Step {step + 1}:')
    print('=======')
    print(f'Number of graphs in the current batch: {data.num_graphs}')
    print(data)
    break

del step
del data

###################################################################
def slack_alarm(message):
    """
    message : string
    """
    import os
    from slack import WebClient
    from slack.errors import SlackApiError

    SLACK_API_TOKEN = 'xoxb-3456243383942-3465240022692-nQxw8PlFwhcywqhYlzO3jqmX'
    client = WebClient(token=SLACK_API_TOKEN)

    try:
        response = client.chat_postMessage(channel='#deep-learning',text=message)
        assert response["message"]["text"] == message

        #filepath="./tmp.txt"
        #response = client.files_upload(channels='#random', file=filepath)
        #assert response["file"]  # the uploaded file
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

def pretrain_gpu(loader, mode='train', device='cuda'):
    '''
    mode
        train : normal training setting
        overfit_single_batch : to overfit a model with a single batch
    '''
    model.train()
    loss_all = 0
    correct, validation_correct, test_correct = 0, 0, 0#to calculate an accuracy
    num_training, num_validation, num_test = 0, 0, 0 #to calculate an accuracy
    #criterion = torch.nn.CrossEntropyLoss()
    criterion = nn.CrossEntropyLoss() #nn.CrossEntropyLoss()

    for idx, batch in enumerate(loader):
        batch = batch.to(device)
        y = torch.argmax(batch.y.reshape(-1,6).type(torch.float), dim=1).to(device)
        optimizer.zero_grad() #initialization

        out = model(batch).to(device)
        loss = criterion(out[batch.train_mask], y[batch.train_mask])  # Tensor. Compute the loss. 
        loss.backward()
        loss_all += loss.item() * batch.num_graphs # loss.item() : the loss in float type
        optimizer.step()  # to update the parameters

        # to measure train accuracy
        pred = out.argmax(dim=1)
        correct += int((pred[batch.train_mask] == y[batch.train_mask]).sum())  # Check against ground-truth labels.
        num_training += y[batch.train_mask].size(dim=0)
        
        
        model.eval()
        # validaiton and test accuracy
        validation_correct += int((pred[batch.validation_mask] == y[batch.validation_mask]).sum())
        num_validation += y[batch.validation_mask].size(dim=0)
        test_correct += int((pred[batch.test_mask] == y[batch.test_mask]).sum())
        num_test += y[batch.test_mask].size(dim=0)
        
        if mode == 'overfit_single_batch' :
            break
    
    accuracy = correct / num_training
    validation_accuracy = validation_correct / num_validation        
    test_accuracy = test_correct / num_test        
    return loss_all / len(loader.dataset), accuracy, validation_accuracy, test_accuracy

def pretrain_all_sample(device, total_num_epoch, running_num_epoch, tf_board_directory, model_save_directory, slack_message=False):
    '''
    Parameters:
        total_num_epoch : the total number of epoch that have run
        running_num_epoch : the number of epoch that run in this time

    '''
    #################################################################################
    # load modules and set parameters
    from torch.utils.tensorboard import SummaryWriter
    writer = SummaryWriter(tf_board_directory)
        ## logdir=./python/run/GAT_Net/run_02

    if (total_num_epoch < 0 or running_num_epoch <= 0):
        import sys
        sys.exit("Check the number of epoch. It is incorrect")

    # optimizer = torch.optim.Adam(model.parameters(), lr=3e-6, weight_decay=0.95)
    # scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',factor=0.7, patience=50, min_lr=1e-8)

    #################################################################################
    #running code
    import time
    total_time_start = time.time() # to measure time
    best_validation_error = None
    for epoch in range(1, running_num_epoch+1):
        epoch_time_start = time.time() # to measure time
        lr = scheduler.optimizer.param_groups[0]['lr']
        loss, train_accuracy, validation_accuracy, test_accuracy = pretrain_gpu()

        # to save the metrics
        if best_validation_error is None or validation_accuracy <= best_validation_error:
            best_validation_error = validation_accuracy
        total_num_epoch = total_num_epoch + 1
        epoch_time_end = time.time() # to measure time    
        writer.add_scalar('loss in train', loss, total_num_epoch) #tensorboard
        writer.add_scalar('train accuracy', train_accuracy, total_num_epoch) #tensorboard
        writer.add_scalar('validation accuracy', validation_accuracy, total_num_epoch) #tensorboard    
        writer.add_scalar('test accuracy', test_accuracy, total_num_epoch) #tensorboard
        writer.add_scalar('learning rate', lr, total_num_epoch) #tensorboard
        # print(f'ToTal Epoch: {total_num_epoch:03d}, LR: {lr:7f}, Loss: {loss:.7f}, '
        #       f'Val MAE: {validation_error:.7f}, Test MAE: {test_error:.7f}, Time: {epoch_time_end - epoch_time_start}')

        # to send message
        if slack_message:
            slack_alarm('[Life3 JupyterNotebook] : ' + str(epoch) + ' / ' + str(running_num_epoch) + '\ntrain accuracy: ' + str(train_accuracy) + '\nvalidation_accuracy: ' + str(validation_accuracy) + '\ntest_accuracy: ' + str(test_accuracy))
            

    total_time_finish = time.time() # to measure time
    print(f'Done. Total running Time: {total_time_finish - total_time_start}')
    writer.close() #tensorboard : if close() is not declared, the writer does not save any valeus.

    # model save
    torch.save({
            'epoch': total_num_epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, model_save_directory)
    print('total number of epoches : ', total_num_epoch)
    print("-------------------------done------------------------------")


def train_gpu(loader, mode='train', device='cuda'):
    '''
    Parameters
        loader : data loader (pytorch)
        mode
            train : normal training setting
            overfit_single_batch : to overfit a model with a single batch
        device
            'cpu'
            'cuda'
    Global variable
        model
    '''
    model.train()
    loss_all = 0
    correct=0 #to calculate an accuracy
    num_training=0 #to calculate an accuracy
    #criterion = torch.nn.CrossEntropyLoss()
    criterion = nn.CrossEntropyLoss() #nn.CrossEntropyLoss()
    
    for idx, batch in enumerate(loader):
        batch = batch.to(device)
        y = torch.argmax(batch.y.reshape(-1,2).type(torch.float), dim=1).to(device)
        optimizer.zero_grad() #initialization
        out = model(batch).to(device)
        loss = criterion(out, y)  # Tensor. Compute the loss. 
        loss.backward()
        loss_all += loss.item() * batch.num_graphs # loss.item() : the loss in float type
        optimizer.step()  # to update the parameters

        # to measure accuracy
        pred = out.argmax(dim=1)
        correct += int((pred == y).sum())  # Check against ground-truth labels.
        num_training += y.size(dim=0)
        
        
        if mode == 'overfit_single_batch' :
            break
    
    accuracy = correct / num_training        
    return loss_all / len(loader.dataset), accuracy 

def test_gpu(loader):
    from torch import nn 
    
    model.eval()
    criterion = torch.nn.CrossEntropyLoss()
    #error = 0.0
    correct = 0
    num_test = 0 # to measure accuracy
    
    for batch in loader:
        #print(batch)
        batch = batch.to(device)
        out = model(batch).to(device)
        pred = out.argmax(dim=1).to(device)
        
        #y = batch.y.reshape(-1,2).type(torch.float).argmax(dim=1)
        y = torch.argmax(batch.y.reshape(-1,2).type(torch.float), dim=1).to(device)
        num_test += y.size(dim=0)
        correct += int((pred == y).sum())
    accuracy = correct / num_test      
        #error += (model(batch) * std - y * std).abs().sum().item()  # MAE
    return correct / len(loader.dataset)

def test_gpu_roc(loader, positive_label_position=0):
    '''
    Argument
        loader : (pytorch data loader)
        positive_label_position : the position of positive label. 
            For example, positive label position is 0 in the case of y= [True, False] 
    '''
    from torch import nn 
    import numpy as np
    
    model.eval()
    criterion = torch.nn.CrossEntropyLoss()
    #error = 0.0
    correct = 0
    num_test = 0 # to measure accuracy
    proteinID = [] # to export proteinID
    # for ROC 
    roc_y_probability = np.array([])
    roc_y_true = np.array([])
    metric_pred = np.array([])
    for batch in loader:
        #print(batch)
        batch = batch.to(device)
        out = model(batch).to(device)
        pred = out.argmax(dim=1).to(device)
        
        y = torch.argmax(batch.y.reshape(-1,2).type(torch.float), dim=1).to(device)
        proteinID += batch.name
        num_test += y.size(dim=0)
        correct += int((pred == y).sum())
        
        # ROC
        probability = nn.Softmax(dim=1)(out).cpu() #convert into probility
        probability = torch.index_select(probability, 1, torch.tensor([positive_label_position])).cpu() # to select only postiive case [0: no, 1: selected]
        roc_y_probability = np.append(roc_y_probability, probability.cpu().detach().numpy()) # to convert into numpy
        del probability
        roc_y_true = np.append(roc_y_true, y.cpu().detach().numpy())
        metric_pred = np.append(metric_pred, pred.cpu().detach().numpy())
        
    accuracy = correct / num_test      
        #error += (model(batch) * std - y * std).abs().sum().item()  # MAE
    return correct / len(loader.dataset), roc_y_probability, roc_y_true, proteinID, metric_pred

def roc_curve_plot(roc_y_probability, roc_y_true, positive_label=1):
    '''
    This function will plot ROC curve
    -------
    PARAMETERS:
        roc_y_probability :  np.array that contains the probability of positive case. 
                        e.g. np.array([0.1, 0.4, 0.35, 0.8]) 
        roc_y_true : np.array that labels True case as 1 and False case as 0. 
                        e.g. np.array([0, 0, 1, 1])
        positive_label : The label of the positive class. Only applied to binary y_true. 
                    For multilabel-indicator y_true, pos_label is fixed to 1.
    
    REFERENCE:
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html
    '''
    

    from sklearn import metrics
    import matplotlib.pyplot as plt

    fpr, tpr, thresholds = metrics.roc_curve(roc_y_true, roc_y_probability, positive_label)
    roc_auc = metrics.auc(fpr, tpr)
    
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

    return fpr, tpr, thresholds


def train_all_sample(device, total_num_epoch, running_num_epoch, train_loader, tf_board_directory, model_save_directory, best_model_save_directory=None, slack_message=False):
    '''
    Parameters:
        total_num_epoch : the total number of epoch that have run
        running_num_epoch : the number of epoch that run in this time
        train_loader : train_loader
        tf_board_directory
        model_save_directory : save directory to save the final model
        best_model_save_directory : [optional] save directory to save the best model (best validation accuracy)
    '''
    #################################################################################
    # load modules and set parameters
    from torch.utils.tensorboard import SummaryWriter
    writer = SummaryWriter(tf_board_directory)
        ## logdir=./python/run/GAT_Net/run_02

    if (total_num_epoch < 0 or running_num_epoch <= 0):
        import sys
        sys.exit("Check the number of epoch. It is incorrect")

    # optimizer = torch.optim.Adam(model.parameters(), lr=3e-6, weight_decay=0.95)
    # scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',factor=0.7, patience=50, min_lr=1e-8)

    #################################################################################
    #running code
    import time
    total_time_start = time.time() # to measure time
    best_validation_accuracy = None
    for epoch in range(1, running_num_epoch+1):
        epoch_time_start = time.time() # to measure time
        lr = scheduler.optimizer.param_groups[0]['lr']
        loss, train_accuracy = train_gpu(train_loader)
        validation_accuracy = test_gpu(validation_loader)
        scheduler.step(validation_accuracy)

        # to save the metrics and model
        if best_validation_accuracy is None or validation_accuracy >= best_validation_accuracy:
            best_validation_accuracy = validation_accuracy
            if not(best_model_save_directory is None):            
                torch.save({
                'epoch': total_num_epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
                }, best_model_save_directory)
        test_accuracy = test_gpu(test_loader)
        total_num_epoch = total_num_epoch + 1
        epoch_time_end = time.time() # to measure time    
        writer.add_scalar('loss in train', loss, total_num_epoch) #tensorboard
        writer.add_scalar('train accuracy', train_accuracy, total_num_epoch) #tensorboard
        writer.add_scalar('validation accuracy', validation_accuracy, total_num_epoch) #tensorboard    
        writer.add_scalar('test accuracy', test_accuracy, total_num_epoch) #tensorboard
        writer.add_scalar('learning rate', lr, total_num_epoch) #tensorboard
        # print(f'ToTal Epoch: {total_num_epoch:03d}, LR: {lr:7f}, Loss: {loss:.7f}, '
        #       f'Val MAE: {validation_error:.7f}, Test MAE: {test_error:.7f}, Time: {epoch_time_end - epoch_time_start}')

        # to send message
        if slack_message:
            slack_alarm('[Life3 JupyterNotebook] : ' + str(epoch) + ' / ' + str(running_num_epoch) + '\ntrain accuracy: ' + str(train_accuracy) + '\nvalidation_accuracy: ' + str(validation_accuracy) + '\ntest_accuracy: ' + str(test_accuracy))
            

    total_time_finish = time.time() # to measure time
    print(f'Done. Total running Time: {total_time_finish - total_time_start}')
    writer.close() #tensorboard : if close() is not declared, the writer does not save any valeus.

    # model save
    torch.save({
            'epoch': total_num_epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, model_save_directory)
    print('total number of epoches : ', total_num_epoch)
    print("-------------------------done------------------------------")

#####################################################################################

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
        in_channels = self.num_node_features #initial input
        for i in range(self.n_layers):
            self.layers.append(GINEConv(nn.Linear(in_channels, self.num_hidden)))
            in_channels = self.num_hidden
        
        self.edge_convert1 = Linear(self.num_edge_features, self.num_node_features)
        self.edge_convert2 = Linear(self.num_node_features, self.num_hidden)
        
        self.lin_out1 = Linear(self.num_hidden, self.num_hidden)
        self.lin_out2 = Linear(self.num_hidden, self.out_channels)
        
    def forward(self, data):
        # model structure 
        in_channels = self.num_node_features #initial input
        for i in range(self.n_layers):
            self.layers.append(GINEConv(nn.Linear(in_channels, self.num_hidden)))
            in_channels = self.num_hidden
        
        self.edge_convert1 = Linear(self.num_edge_features, self.num_node_features)
        self.edge_convert2 = Linear(self.num_node_features, self.num_hidden)
        
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
                
        x = self.lin_out1(x)
        x = F.dropout(x, p=self.p, training=self.training)
        x = self.lin_out2(x)
        # x = self.sigmoid(x)
        # x = nn.Softmax(dim=1)(x) # to convert into probability
        
        return x
            #[batch_size = 32, output_channels = 2]

# # CPU --> GPU
# #device = torch.device('cpu')
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = GINEConv_pretrain(num_hidden= 30, num_node_features=pretrain_dataset.num_node_features, num_edge_features=pretrain_dataset.num_edge_features, n_layers=150).to(device)
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
# scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',factor=0.8, patience=5, min_lr=0.00001)

# print(device)
# print('-------------')
# print(model)

# pretrain_all_sample(device='cuda', 
#     total_num_epoch=0, 
#     running_num_epoch=20, 
#     tf_board_directory='run/GINEConv_pretrain/run_5_GINEConv_6_pretrain', 
#     model_save_directory='model/GINEConv_pretrain/run_5_GINEConv_6_pretrain',
#     slack_message=True)

# pretrain_model = model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
pretrain_model = GINEConv_pretrain(num_hidden= 15, num_node_features=pretrain_dataset.num_node_features, num_edge_features=pretrain_dataset.num_edge_features, n_layers=150).to(device)
optimizer = torch.optim.RMSprop(pretrain_model.parameters(), lr=0.0015334791245047435)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',factor=0.8, patience=5, min_lr=0.0001)
#optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
PATH = 'model/GINEConv_pretrain/run_2'

checkpoint = torch.load(PATH)
pretrain_model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']

import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import Linear
from torch_geometric.nn import GINEConv
from torch_geometric.nn import global_add_pool

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
        
        # model structure 
#         in_channels = self.num_node_features #initial input
#         for i in range(self.n_layers):
#           self.layers.append(GINEConv(nn.Linear(in_channels, self.num_hidden)))
#           in_channels = self.num_hidden
        
#         self.edge_convert1 = Linear(self.num_edge_features, self.num_node_features)
#         self.edge_convert2 = Linear(self.num_node_features, self.num_hidden)
        
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
                
        x = global_add_pool(x, batch) # [batch_size, hidden_channels]
        # x = global_mean_pool(x, batch)  # [batch_size, hidden_channels]
        x = self.lin_out1(x)
        x = F.dropout(x, p=self.p, training=self.training)
        x = self.lin_out2(x)
        # x = self.sigmoid(x)
        # x = nn.Softmax(dim=1)(x) # to convert into probability
        
        return x
            #[batch_size = 32, output_channels = 2]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GINEConv_train(pretrain_model=pretrain_model, out_channels=2).to(device)
model.n_layers = 100
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',factor=0.8, patience=5, min_lr=0.0001)

print(device)
print('-------------')
print(model)
           
train_all_sample(device='cuda', 
    total_num_epoch=0, 
    running_num_epoch=150, 
    train_loader=train_loader, 
    tf_board_directory='tfboard/GINEConv/run_21', 
    model_save_directory='model/GINEConv/run_21', 
    best_model_save_directory='model/GINEConv/run_21_best',
    slack_message=True)
