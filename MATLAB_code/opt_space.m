function [err, y, vertices_err] = opt_space(data,labels,label_names,num_it,opt_type)
% find the geometric median
% Input: data = matrix of MNIST data, column major, selected randomly
% Input: labels = digit labels for each point in data
% Input: label_names = cell of strings specifying digits for each class
% Input: epsilon = stop iterating when the secant distance between the current
% mean approximation and the previous one is less than epsilon
% Output: the geometric median



%p points on the Gr(k,n)
p = length(label_names);
[n,pk] = size(data);
k = pk/p;


x = {};
X = zeros(n,pk);
for i=1:p
    %[Q,R] = qr(data(:,1+k*(i-1):k*i));
    %x{i} = Q(:,1:k);
    x{i} = data(:,1+k*(i-1):k*i);
    X(:,1+k*(i-1):k*i) = data(:,1+k*(i-1):k*i);
    %X(:,1+k*(i-1):k*i) = Q(:,1:k);
end

if n == 3
    Y = [0;0;1];
else
    Y = [0;1];
end

ii = 1;
err = [];
er = calc_error(x,Y,p,opt_type);
err(ii) = er;
y(:,ii) = Y;


y = [];
y(:,1) = Y;
for ii = 1:num_it
    Y = y(:,1) + (2*rand(n,1)-1);
    Y = Y/norm(Y);
    Y(n) = abs(Y(n));
    er = calc_error(x,Y,p,opt_type);
    ii = ii+ 1;
    err(ii) = er;
    y(:,ii) = Y;  
end

vertices_err = [];
for i=1:p
    vertices_err(i) = calc_error(x,x{i},p,opt_type);
end


end


%imshow(reshape(10*median_point, 28,28),'InitialMagnification', 3200)