function [median_point,err, weights,ii,init_pt,y] = reweighted_flag(data,labels,label_names,epsilon,init, opt_type)
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


Y0 = zeros(n,k);

if isequal(init,'random')
    y = rand(3,1); %random initialization
    Y = y/norm(y);
else
    [Yall,S,V] = svd(X);
    %Y = Yall(:,1:k);
    %perturb
    Y = Yall(:,1:k) + rand();
    Y = Y/norm(Y);
end
init_pt = Y;
    
for i=1:p
    if isequal(Y,x{i})
        sprintf('warning: flag mean is a data point'); 
    end
end


ii = 1;
err = [];
weights = [];
y = [];
y(:,ii) = Y;
er = calc_error(x,Y,p,opt_type);
err(ii) = er;
weights = [];
while sqrt(k - trace((Y0'*Y)*(Y0'*Y)')) >= epsilon
%while diffr > 0
%for ii = 1:100
    Y0 = Y;    
    [alpha,X] = weight(x,Y0,opt_type);
    weights(ii,:) = alpha;
    
    [Yall,S,V] = svd(X);
    Y = Yall(:,1);
    er = calc_error(x,Y,p,opt_type);
    ii = ii+ 1;
    err(ii) = er;
    if err(ii) > err(ii-1)
        Y = Y0;
        err(ii)= err(ii-1);
        y(:,ii) = Y;
        break
    end
    y(:,ii) = Y;
end


median_point = Y;

end


%imshow(reshape(10*median_point, 28,28),'InitialMagnification', 3200)