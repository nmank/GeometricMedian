function [median_point,err, weights,ii,init_pt,y] = karcher_median(data,labels,label_names,epsilon,init, opt_type)
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

    %run weiszfield on the tangents
    error = 1;
    tolerance = .0001;
    tY = tangents(:,1);
    while error > tolerance
        XYdist = []
        for i=1:p
            if norm(tangents(:,i)-tY) ~= 0
                XYdist(i) = 1/norm(tangents(:,i)-tY);
            end
        end
        tY = sum(tangents*XYdist'/sum(XYdist),2);
        error = calc_error(x,Y,p,opt_type);
    end

    %exp it back
    [U,S,V] = svd(tY);
    Y = [Y*V, U(:,1:k)]*[diag(cos(diag(S))); diag(sin(diag(S)))]*V';

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
