%data parameters
num_points = 11;
circ = true; %placed on the origin
angle = acos(1/sqrt(3));
%angle = 2*pi/9; %angle for the circle from the origin in the direction of the z axis
reg = true; %regular spacing
frame = 1; %set this to 6 for point frame data
num_samples = 1000

%choose the distance in the optimization problem
%chord = chordal
%chors = chordal squared
%geodi = geodesic
%geods = geodesic squared
opt_type = 'geodi';

epsilon = .000001; %convergence criteria (squared sine of angles between consecutive iterations)
init = 'random'; %algorithm initialization (start at flag mean if not 'random')

%generate the data
N = num_points-1;
labels = [1:num_points];
label_names = labels;
theta = pi*rand(N,1)/4;
phi = 2*pi*normrnd(0,.2,[N]);
data = zeros(3,num_points);
for i=1:N
    data(1,i) = sin(theta(i))*cos(phi(i));
    data(2,i) = sin(theta(i))*sin(phi(i));
    data(3,i) = cos(theta(i));
end



%data
scatter3(data(1,1:N),data(2,1:N),data(3,1:N),ones(N,1)*50,'k','filled')
hold on

for ii=1:num_samples
    %randomize the N+1st point
    theta = pi*rand()/4;
    phi = 2*pi*normrnd(0,.2);
    data(1,num_points) = sin(theta)*cos(phi);
    data(2,num_points) = sin(theta)*sin(phi);
    data(3,num_points) = cos(theta);


    %compute the sln to opt problem via flag
    %medn = the solution
    %err = error at each iteration
    %weights = weights at each iteration
    %ii = number of iteratioms
    %init_pt = starting point
    %point at each iteration (y(1) = init_pt)
    [medn,err,weights,ii,init_pt,y] = reweighted_flag(data,labels,label_names,epsilon,init,opt_type);

    %bonus point
    %scatter3(data(1,num_points),data(2,num_points),data(3,num_points)+.02,20,'g','filled')

    %median
    if medn(3)<0
        scatter3(-medn(1),-medn(2),-medn(3), 1,'r','filled')
    else
        scatter3(medn(1),medn(2),medn(3), 1,'r','filled')
    end

    
    %mean
    if opt_type =='chord'
        X = zeros(3,num_points);
        for i=1:num_points
            X(:,1+(i-1):i) = data(:,1+(i-1):i);
        end
        [Yall,S,V] = svd(X);
        mn = Yall(:,1)/norm(Yall(:,1));
    elseif opt_type == 'geodi'
        [mn,err, weights,ii,init_pt,y] = karcher_mean(data,labels,label_names,epsilon,init, opt_type);
    else
        print('opt_type error')
    end
    if mn(3)<0
        scatter3(-mn(1),-mn(2),-mn(3)+.01, 1,'b','filled')
    else
        scatter3(mn(1),mn(2),mn(3)+.01, 1,'b','filled')
    end
end


    