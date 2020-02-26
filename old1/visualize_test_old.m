num_points = 3;
opt_type = 'chors';
epsilon_flag = .0001; 
epsilon_grad = .000001; 
alpha = .02;
reg = true;
circ = true;
angle = 2*pi/9;
init = 'rando';
[data,labels,label_names] = sphere_data(num_points,reg,circ,angle);

%[sm,errs,weights,ii,init_pt] = subspace_geom_median(data,labels,label_names,epsilon,init);
[fm,errf,weights,ii,init_pt,yf] = flag_adopted(data,labels,label_names,epsilon_flag,init);
[gd,errg,ii,init_pt,yg, norm_gradient] = grad_desc(data,labels,label_names,epsilon_grad,init,alpha);
[gs,errgs,weights,ii,init_pt,ygs] = geodesic_squared(data,labels,label_names,epsilon_flag,init);
[gsn,errgsn,weights,ii,init_pt,ygsn] = geodesic_not_squared(data,labels,label_names,epsilon_flag,init);
%[gr,errr,ii,init_pt,yr] = greedy(data,labels,label_names,epsilon,init,alpha);


%errs(end)
errf(end)
errg(end)
errgs(end)
errgsn(end)
%errr(end)


%plot error
figure
hold on
plot(real(errf))
plot(real(errg))
plot(real(errgs))
plot(real(errgsn))

% 
% dist_to_init = [];
% for i=1:num_points
%     dist_to_init(i)= real(sin(acos(abs(data(:,i)'*init_pt))));
% end
% [junk,argmin_d] = min(dist_to_init);
% closest_to_init = data(:,argmin_d);


%something to check the parameter space
figure
num_it = 10000;
[err, y] = opt_space(data,labels,label_names,num_it,opt_type);
scatter3(y(1,:),y(2,:),y(3,:),ones(10001,1)*10,exp(-err));
hold on
scatter3(data(1,:),data(2,:),data(3,:),ones(num_points,1)*50,'k','filled')

%data and solutions
plot3(data(1,:),data(2,:),data(3,:),'.','MarkerSize', 30,'Color','b')
%closest to init
%plot3(closest_to_init(1),closest_to_init(2),closest_to_init(3),'.','MarkerSize', 60)
if gd(3)< 0 
    plot3(-gd(1),-gd(2),-gd(3),'.','MarkerSize', 40,'Color','r')
else
    plot3(gd(1),gd(2),gd(3),'.','MarkerSize', 40,'Color','r')
end
if fm(3)<0
    plot3(-fm(1),-fm(2),-fm(3),'.','MarkerSize', 40,'Color','k')
else
    plot3(fm(1),fm(2),fm(3),'.','MarkerSize', 40,'Color','k')
end
%plot3(-gr(1),-gr(2),-gr(3),'.','MarkerSize', 40,'Color','k')


%initial_point
plot3(init_pt(1),init_pt(2),init_pt(3),'x','Color','b','MarkerSize', 20)
if yf(3,1) < 0
    plot3(-yf(1,:),-yf(2,:),-yf(3,:),'.','MarkerSize', 10,'Color','k')
else
    plot3(yf(1,:),yf(2,:),yf(3,:),'.','MarkerSize', 10,'Color','k')
end
   
if yg(3,1) < 0
    plot3(-yg(1,:),-yg(2,:),-yg(3,:),'.','MarkerSize', 10,'Color','r')
else
    plot3(yg(1,:),yg(2,:),yg(3,:),'.','MarkerSize', 10,'Color','r')
end






% [median_point,err,weights,ii,init_pt,y] = good_test(data,labels,label_names,epsilon,init);
% 
% plot3(median_point(1),median_point(2),median_point(3),'o','MarkerSize', 20,'Color','k')
%figure
% hold on
% sphere
% plot3(median_point(1),median_point(2),median_point(3),'.','MarkerSize', 40,'Color','r')
% plot3(data(1,:),data(2,:),data(3,:),'.','MarkerSize', 30,'Color','b')
% 
% %initial_point
% plot3(init_pt(1),init_pt(2),init_pt(3),'x','Color','b','MarkerSize', 20)
% 
% plot3(y(1,:),y(2,:),y(3,:),'.','MarkerSize', 10,'Color','r')

    