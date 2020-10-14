%data parameters
num_points = 100;

%number of extra pts
num_extra = 100;

%choose the distance in the optimization problem
%chord = chordal
%chors = chordal squared
%geodi = geodesic
%geods = geodesic squared
opt_type = 'chord';

epsilon = .0001; %convergence criteria (squared sine of angles between consecutive iterations)
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

total = num_points + num_extra


num_it = 10000;
[err1, sp_pts,vtx_err] = opt_space(data(:,1:total),labels(1:total),label_names(1:total),num_it,opt_type);




%chordal median
[cmedn,err,weights,ii,init_pt,y] = reweighted_flag(data(:,1:total),labels(1:total),label_names(1:total),epsilon,init,opt_type);



figure
hold on
xlim([-1,1])
ylim([-1,1])
for i=1:total
   plot([0,data(1,i),-data(1,i)],[0,data(2,i),-data(2,i)],'k')
end 

%chordal median
p1 = plot([0,cmedn(1),-cmedn(1)],[0,cmedn(2),-cmedn(2)],'r','LineWidth',5)

scatter(sp_pts(1,:),sp_pts(2,:),ones(num_it+1,1)*10,exp(-err1),'filled');

