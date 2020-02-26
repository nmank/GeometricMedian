function [median_point,err, ii,init_pt,y,norm_gradient] = grad_desc(data,labels,label_names,epsilon,init,alpha)
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

%store the points in x and X
x = {};
X = zeros(n,pk);
for i=1:p
    x{i} = data(:,1+k*(i-1):k*i);
    X(:,1+k*(i-1):k*i) = data(:,1+k*(i-1):k*i);
end

%initialize the algorithm either randomly or at flag mean
Y0 = zeros(n,k);
if isequal(init,'random')
    y = rand(3,1); %random initialization
    Y = y/norm(y);
else
    [Yall,S,V] = svd(X);
    Y = Yall(:,1:k);
end
init_pt = Y;

%calculate the error of this initial point
ii = 1;
err = [];
er = 0;
for i=1:p
        er = er + abs(real(sin(acos(abs(x{i}'*Y)))));
end
err(ii) = er;
y(:,ii) = Y;

%perform gradient descent until the chordal distance between conecutive
%estimates is less than epsilon
y = [];
norm_gradient= [];
y(:,1) = Y;
while k - trace((Y0'*Y)*(Y0'*Y)') >= epsilon 
%for ii = 2:1000
    Y0 = Y;
    X = zeros(n,pk);
    %calculate gradient
    Fy = zeros(n,1);
    for i=1:p
        if isinf(1/real(sin(acos(x{i}'*Y0)))) ~= true
            Fy = Fy + (-x{i}*x{i}'*Y0)/real(sin(acos(abs(x{i}'*Y0))));
            %Fy = Fy + (-x{i}*x{i}'*Y0)/sqrt(1-Y0'*x{i}*x{i}'*Y0);
        end
    end
    if isinf(1/real(sin(acos(x{i}'*Y0)))) == true
        break
    end
    %project the gradient onto the tangent space
    G = (eye(3)-Y0*Y0')*Fy;
    norm_gradient(ii) = norm(G);
    %error check
    if sum(G) == 0 || any(isnan(G))
        Fy
        G
        break
    end
    %move to a point that is alpha along the geodesic at Y0 in the
    %direction of G
    [U,S,V] = svd(G);
    Y = Y0*V*cos(-alpha*S(1))*V'+U*[sin(-alpha*S(1));0;0]*V';
    er = 0;
    for i=1:p
        er = er + real(sin(acos(abs(x{i}'*Y))));
        %er = er + sqrt(1-Y'*x{i}*x{i}'*Y);
    end
   
    %add one to the iteration and save error and estimate
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