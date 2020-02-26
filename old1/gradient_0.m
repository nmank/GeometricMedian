num_points = 100;
epsilon = .00001;
[data,labels,label_names] = sphere_data(num_points);


p = length(label_names);
[n,pk] = size(data);
k = pk/p;


x = {};
X = zeros(n,pk);
for i=1:p
    [Q,R] = qr(data(:,1+k*(i-1):k*i));
    x{i} = Q(:,1:k);
    X(:,1+k*(i-1):k*i) = Q(:,1:k);
end

%loop this



Y0 = zeros(n,k);
%[Yall,S,V] = svd(X);
%Y = Yall(:,1:k);
Y = [1/sqrt(18);1/sqrt(18);4/sqrt(18)] %initialization

ii = 1;
err = [];
y = [];
y(:,ii) = Y;
while k-trace((Y0'*Y)*(Y0'*Y)') >= epsilon
%for ii = 1:100
    Y0 = Y;
    A = zeros(3,3);
    for i=1:num_points
        for j=1:num_points
            if i ~= j
                A = A + X(:,i)*X(:,j)';
            end
        end
    end
    Y = .1*(inv(A)*Y0*Y0'*A*Y0);
    Y = Y/norm(Y);
    err(ii) = k-trace((Y0'*Y)*(Y0'*Y)');
    ii = ii+ 1; 
    y(:,ii) = Y;
end

median_point = Y;

figure
sphere
hold on
plot3(data(1,:),data(2,:),data(3,:),'.')

%plot3(-median_point(1),-median_point(2),-median_point(3),'.','MarkerSize', 20)
plot3(y(1,:),y(2,:),y(3,:),'.','MarkerSize', 20)


