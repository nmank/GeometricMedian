% Write MNIST data to csv file
load mnist_all.mat

digits = 0:9;
d = length(digits);

set = 'train';

% Convert training data
for i = 1:d
    digit = digits(i);
    var_name = strcat(set,num2str(digit));
    var = eval(var_name);
    data = double(var);
    filename = strcat(set,num2str(digit),'.csv');
    csvwrite(filename,data)
end

set = 'test';

% Convert training data
for i = 1:d
    digit = digits(i);
    var_name = strcat(set,num2str(digit));
    var = eval(var_name);
    data = double(var);
    filename = strcat(set,num2str(digit),'.csv');
    csvwrite(filename,data)
end