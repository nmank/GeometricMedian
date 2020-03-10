%data parameters
num_points = 3;
circ = true; %placed on the origin
angle = 2*pi/9; %angle for the circle from the origin in the direction of the z axis
reg = true; %regular spacing

%choose the distance in the optimization problem
%chord = chordal
%chors = chordal squared
%geodi = geodesic
%geods = geodesic squared
opt_type = 'chord';

epsilon = .000001; %convergence criteria (squared sine of angles between consecutive iterations)
init = 'rando'; %algorithm initialization (start at flag mean if not 'random')

%generate the data
mu = 1-(3-1)*num_points/(3*(num_points-1));
[ F, coh ] = troppaltproj_sp( num_points, 1, 3, mu );
labels = [1:num_points];
label_names = labels;
data = F;
%compute the sln to opt problem via flag
%avg = the solution
%err = error at each iteration
%weights = weights at each iteration
%ii = number of iteratioms
%init_pt = starting point
%point at each iteration (y(1) = init_pt)
[avg,err,weights,ii,init_pt,y] = reweighted_flag(data,labels,label_names,epsilon,init,opt_type);


%compute the sln to opt problem via gradient descent
epsilon_grad = .000001; %convergence criteria (squared sine of angles between consecutive iterations)
alpha = .02; %step size

%compute the sln to opt problem via gradient descent
%avg = the solution
%err = error at each iteration
%weights = weights at each iteration
%ii = number of iteratioms
%init_pt = starting point
%point at each iteration (y(1) = init_pt)
[gd,errg,iig,init_ptg,yg, norm_gradient] = grad_desc(data,labels,label_names,epsilon_grad,init,alpha,opt_type);


%print final error
err(end)
errg(end)


%plot error
figure
hold on
plot(real(err))
plot(real(errg))
title('Summed Chordal Distance from the Data')
xlabel('Iterations')
ylabel('Distance')
legend({'Iterated Flag Mean','Gradient Descent'},'Location','northeast')

%something to check the parameter space
figure
num_it = 1000000;
[err, sp_pts,vtx_err] = opt_space(data,labels,label_names,num_it,opt_type);
scatter3(sp_pts(1,:),sp_pts(2,:),sp_pts(3,:),ones(num_it+1,1)*10,exp(-err),'filled');
hold on
%data
scatter3(data(1,:),data(2,:),data(3,:)+.04,ones(num_points,1)*50,'k','filled')


%chordal (plotted as o)
%sln
if avg(3)<0
    scatter3(-avg(1),-avg(2),-avg(3)+.01, 30,'r','filled')
else
    scatter3(avg(1),avg(2),avg(3)+.01, 30,'r','filled')
end
%sln at each iteration
if y(3,1) < 0
    scatter3(-y(1,:),-y(2,:),-y(3,:)+.01, ones(ii,1)*10,'r','filled')
else
    scatter3(y(1,:),y(2,:),y(3,:)+.01, ones(ii,1)*10,'r','filled')
end

% %gradient descent (plotted as .)
% %sln
% if gd(3)< 0 
%     plot3(-gd(1),-gd(2),-gd(3),'.','MarkerSize', 40,'Color','r')
% else
%     plot3(gd(1),gd(2),gd(3),'.','MarkerSize', 40,'Color','r')
% end
% %sln at each iteration
% if yg(3,1) < 0
%     plot3(-yg(1,:),-yg(2,:),-yg(3,:),'.','MarkerSize', 10,'Color','r')
% else
%     plot3(yg(1,:),yg(2,:),yg(3,:),'.','MarkerSize', 10,'Color','r')
% end

%initial_point (plotted as x)
%plot3(init_pt(1),init_pt(2),init_pt(3),'x','Color','b','MarkerSize', 20)




    