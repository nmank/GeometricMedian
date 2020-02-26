function [data, labels, label_names] = load_mnist(digits, sample_num, set)
% [data, labels] = load_mnist(digits, sample_num, set)
% Load data from the MNIST handwritten numbers data set
% Input: digits = vector of desired digits (0-9)
% Input: sample_num = scalar or vector of desired number of samples from
%   each class; if vector need length(sample_num)==length(digits)
% Input: set = 'train' or 'test'
% Output: data = matrix of MNIST data, column major, selected randomly
% Output: labels = digit labels for each point in data
% Output: label_names = cell of strings specifying digits for each class

d = length(digits);
if length(sample_num)==1
    sample_num = repmat(sample_num,1,d);
else if length(sample_num)~=d
        fprintf('Incorrect number of sample sizes specified')
        return
    end
end 

load('mnist_all.mat')

data = [];
labels = [];

% Collect data
for i = 1:d
    digit = digits(i);
    var_name = strcat(set,num2str(digit));
    var = eval(var_name);
    smpl = datasample(var,sample_num(i),1,'Replace',false);
    data = [data; double(smpl)];
    labels = [labels digit*ones(1,sample_num(i))];
    label_names{i} = num2str(digit);
end
data = data';