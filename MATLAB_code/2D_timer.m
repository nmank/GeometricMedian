%data parameters
num_points = 100;

%number of extra pts
num_extra = 10
%choose the distance in the optimization problem
%chord = chordal
%chors = chordal squared
%geodi = geodesic
%geods = geodesic squared
opt_type = 'chord';

epsilon = .00001; %convergence criteria (squared sine of angles between consecutive iterations)
init = 'ran'; %algorithm initialization (start at flag mean if not 'random')

%generate the data
data = zeros(2,num_points*2);
for i=1:num_points
    theta = pi/2+(rand()-.5)*.3;
    data(:,i) = [cos(theta);sin(theta)];
end

for i=num_points+1:num_points*2
    theta = 3*pi/4+(rand()-.5)*.3;
    data(:,i) = [cos(theta);sin(theta)];
end

    
labels = [1:num_points*2];
label_names = labels;

%compute the sln to opt problem via flag
%medn = the solution
%err = error at each iteration
%weights = weights at each iteration
%ii = number of iteratioms
%init_pt = starting point
%point at each iteration (y(1) = init_pt)

total = num_points + num_extra


cmedn_time = [];
gmedn_time = [];
kmn_time = [];

for i = 1:100
    
    %chordal median
    cmedn = @() reweighted_flag(data(:,1:total),labels(1:total),label_names(1:total),epsilon,init,'chord');


    %geodesic median
    gmedn = @() reweighted_flag(data(:,1:total),labels(1:total),label_names(1:total),epsilon,init,'geodi');

    %chordal mean
    % [Yall,S,V] = svd(data(:,1:total));
    % cmn = Yall(:,1)/norm(Yall(:,1));

    %karcher
    kmn = @() karcher_mean(data(:,1:total),labels(1:total),label_names(1:total), epsilon,'rand', opt_type);

    cmedn_time(i) = timeit(cmedn);

    gmedn_time(i) = timeit(gmedn);

    kmn_time(i) = timeit(kmn);
    
    disp('iteration')
    i
    
end

disp('-----------------------')
disp('-----------------------')
disp('Chordal Median')
mean(cmedn_time)
std(cmedn_time)
disp('-----------------------')
disp('Geodesic Median')
mean(gmedn_time)
std(gmedn_time)
disp('-----------------------')
disp('Karcher Mean')
mean(kmn_time)
std(kmn_time)
