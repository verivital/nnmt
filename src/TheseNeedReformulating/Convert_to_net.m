%% Convert neural networks saved as struct to net objects 
% clc;clear
%%  Load the neural network file
% load('SingleCarPlant'); %all variables from file are loaded into workspace
% network_file = SingleCarPlant; 

%% Parameters of the network
nl = double(network_file.number_of_layers); % # of layers
ni = double(network_file.number_of_inputs); % # of inputs
no = double(network_file.number_of_outputs); % # of outputs

%% Transform names of activations function to its corresponding name in MATLAB
act = erase(string(network_file.activation_fcns)," "); %transform to strings

for i = 1:nl
    if act(i) == "relu" %ReLU activation function
        lystype{i} = 'poslin'; 
    elseif act(i) == "linear" %Linear Activation function
        lystype{i} = 'purelin';
    elseif act(i) == "sigmoid" %Sigmoid activation function
        lystype{i} = 'logsig';
    elseif act(i) == "tanh" %Hyperbolic tangent activation function
        lystype{i} = 'tansig';
    elseif act(i) == "relu1" %Saturation linear function from 0 to 1
        lystype{i} = 'satlin';
    elseif act(i) == "relu2" %Saturation linear function from -1 to 1
        lystype{i} = 'satlins';
    else
        disp("The activation function of layer "+i+" is currently not supported");
    end
end     

%% Create and define feedforward network
net = feedforwardnet(double(network_file.layer_sizes(1:(end-1))));
net.inputs{1}.processFcns = {}; %Remove preprocessing functions in the inputs and outputs
net.outputs{nl}.processFcns = {};

%% Transfer functions
for i = 1:nl
    net.layers{i}.size = length(network_file.b{1,i});
    %net.layers{i}.transferFcn = 'poslin'; %poslin = relu
    net.layers{i}.transferFcn = lystype{i}; %poslin = relu
    length(network_file.b{1,i});
end

%% Weights matrics
net.inputs{1}.size = ni;
for i = 1:nl-1
    net.LW{i+1,i} = double(network_file.W{i+1});
end
net.IW{1,1} = double(network_file.W{1});

%% Bias matrices
for i =1:nl
    net.b{i} = double(network_file.b{i});
end

%% Save files
%savefile = 'ControllerCartPole.mat';
%save(savefile,'net');

%% Generate simulink file
% gensim(net)