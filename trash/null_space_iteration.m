function [median_point,err, weights,ii,init_pt,y] = null_space_iteration(data,labels,label_names,epsilon,init,alpha)
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
    Y = Yall(:,1:k);
end
init_pt = Y;
    



ii = 1;
err = [];
weights = [];
y = [];
y(:,1) = Y;
while k - trace((Y0'*Y)*(Y0'*Y)') >= epsilon
%for ii = 1:5
    Y0 = Y;
    X = zeros(n,pk);
    weight = [];
    er = 0;
    Fy = 0;
    for i=1:p
        Fy = Fy + (-x{i}*x{i}')/sin(acos(abs(x{i}'*Y0)));
    end
    Yall = null(Fy);
    Fy
    rank(Fy)
    Y = Yall(:,1);
    for i=1:p
        er = er + sin(acos(abs(x{i}'*Y)));
    end
    err(ii) = er
    y(:,ii+1) = Y;
    ii = ii+ 1;
end


median_point = Y;

end


%imshow(reshape(10*median_point, 28,28),'InitialMagnification', 3200)