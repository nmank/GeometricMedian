function [mean_point,err, weights,ii,init_pt,y] = karcher_mean(data,labels,label_names,epsilon,init, opt_type)
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
    Y = x{1}; %initialize at a datapoint
end
init_pt = Y;
    
for i=1:p
    if isequal(Y,x{i})
        fprintf('warning: flag mean is a data point'); 
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
tY = ones(3,1);
while norm(tY) >= epsilon

    %Compute tangents
    tangents = [];
    for i=1:p

        [V,U,Z,C,S] = gsvd(Y'*x{i},(eye(3) - Y*Y')*x{i});

        Theta = real(diag(acos(diag(C))));

        %fix this
        tangents(:,i) = U(:,1:k)*Theta*V';
        %for a sphere = calc_dist(x{i},Y,opt_type)*(x{i} - x{i}'*Y*Y)/norm(x{i} - x{i}'*Y*Y);
    end

    %mean of the tangents
    tY = sum(tangents,2)/p;

    %exp it back
    [U,S,V] = svd(tY);
    Y = [Y*V, U(:,1:k)]*[cos(S(1)); sin(S(1))]*V';

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

mean_point = Y;

end
