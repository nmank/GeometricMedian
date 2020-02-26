function [median_point,err, weights,ii,init_pt] = subspace_geom_median(data,labels,label_names,epsilon,init)
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
    [Q,R] = qr(data(:,1+k*(i-1):k*i));
    x{i} = Q(:,1:k);
    %x{i} = data(:,1+k*(i-1):k*i);
    %X(:,1+k*(i-1):k*i) = data(:,1+k*(i-1):k*i);
    X(:,1+k*(i-1):k*i) = Q(:,1:k);
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
while k - trace((Y0'*Y)*(Y0'*Y)') >= epsilon
%for ii = 1:5
    Y0 = Y;
    X = zeros(n,pk);
    weight = [];
    er = 0;
    for i=1:p
        er = er + sum(acos(diag(x{i}'*Y)));
        num = 1/(k-trace((x{i}'*Y)*(x{i}'*Y)'));
%         denom = 0;
%         for j=1:p
%             denom = denom + 1/(k-trace((x{j}'*Y)*(x{j}'*Y)'));
%         end
%         alpha = num/denom;
        alpha = num;
        X(:,1+k*(i-1):k*i) = alpha*x{i};
        weight(i) = alpha;
    end
    [Yall,S,V] = svd(X);
    Y = Yall(:,1:k);
    err(ii) = er
    weights(ii,:) = weight;
    ii = ii+ 1;
end


median_point = Y;

end


%imshow(reshape(10*median_point, 28,28),'InitialMagnification', 3200)