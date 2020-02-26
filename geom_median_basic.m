function [median_point,err, weights,ii] = geom_median_basic(data,labels,label_names,epsilon)
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
    x{i} = data(:,1+k*(i-1):k*i)
    X(:,1+k*(i-1):k*i) = data(:,1+k*(i-1):k*i)
    %X(:,1+k*(i-1):k*i) = Q(:,1:k);
end

%loop this



Y = sum(X)/p;
%[Yall,S,V] = svd(X);
%Y = Yall(:,1:k);
%Y = [1/sqrt(18);4/sqrt(18);1/sqrt(18)] %random initialization
Y0 = [0;0;0];
ii = 1;
err = [];
weights = [];
while (norm(Y0-Y)) >= epsilon
%for ii = 1:100
    Y0 = Y;
    Y = zeros(n,k);
    weight = [];
    for i=1:p
        num = 1/(norm(x{i}-Y0));
        denom = 0;
        for j=1:p
            denom = denom + 1/(norm(x{j}-Y0));
        end
        alpha = num/denom;
        Y = Y+alpha*x{i};
        weight(i) = alpha;
    end
    err(ii) = (norm(Y0-Y));
    weights(ii,:) = weight;
    ii = ii+ 1;
end


median_point = Y(:,1);

end
%imshow(reshape(10*median_point, 28,28),'InitialMagnification', 3200)