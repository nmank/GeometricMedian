%data parameters
num_points = 100;

%number of extra pts
num_extra = 100

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

%chordal median
[cmedn,err,weights,ii,init_pt,y] = reweighted_flag(data(:,1:total),labels(1:total),label_names(1:total),epsilon,init,'chord');

%geodesic median
[gmedn,err,weights,ii,init_pt,y] = reweighted_flag(data(:,1:total),labels(1:total),label_names(1:total),epsilon,init,'geodi');

%chordal mean
[Yall,S,V] = svd(data(:,1:total));
cmn = Yall(:,1)/norm(Yall(:,1));

%karcher
[kmn,err, weights,ii,init_pt,y] = karcher_mean(data(:,1:total),labels(1:total),label_names(1:total), epsilon,'rand', opt_type);

%plots
figure
hold on
xlim([-1,1])
ylim([-1,1])
for i=1:total
   plot([0,data(1,i),-data(1,i)],[0,data(2,i),-data(2,i)],'k')
end   

%chordal median
p1 = plot([0,cmedn(1),-cmedn(1)],[0,cmedn(2),-cmedn(2)],'r','LineWidth',5)

%geodesic median
p2 = plot([0,gmedn(1),-gmedn(1)],[0,gmedn(2),-gmedn(2)],'m','LineWidth',4)

%chordal mean
p3 = plot([0,cmn(1),-cmn(1)],[0,cmn(2),-cmn(2)],'b','LineWidth',3)

%karcher mean
p4 = plot([0,kmn(1),-kmn(1)],[0,kmn(2),-kmn(2)],'y','LineWidth',2)


legend([p1;p2;p3;p4],'Chordal Median','Geodesic Median','Flag Mean','Karcher Mean')

num_it = 1000000;
[err1, sp_pts,vtx_err] = opt_space(data,labels,label_names,num_it,opt_type);

scatter(sp_pts(1,:),sp_pts(2,:),ones(num_it+1,1)*10,exp(-err1),'filled');

    