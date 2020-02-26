
%angle = acos(1/sqrt(3));
angle = 2*pi/9; %angle for the circle from the origin in the direction of the z axis

%choose the distance in the optimization problem
%chord = chordal
%chors = chordal squared
%geodi = geodesic
%geods = geodesic squared
opt_type = 'chord';

epsilon = .000001; %convergence criteria (squared sine of angles between consecutive iterations)
init = 'rando'; %algorithm initialization (start at flag mean if not 'random')

%generate the data
[data,lines, labels,label_names] = three_planes(angle);

%compute the sln to opt problem via flag
%check 'robustness' by running 100 trials and plotting each entry in the
%solution
itr = []
itr_line = []
for i=1:1000
    [itr(:,:,i),itr_line(:,i)] = reweighted_flag_subspace(data,labels,label_names,epsilon,init,opt_type);
end

hold on
scatter([1:1000],abs(itr(1,2,:)),'.')
scatter([1:1000],abs(itr(2,2,:)),'.')
scatter([1:1000],abs(itr(3,2,:)),'.')
title('Median Subspace Entries in Second Column Vector')
ylabel('Entry Value')
xlabel('Iteration')
legend('Row 1','Row 2','Row 3')

hold off

hold on
[x y] = meshgrid(-10:1:10);
for i=1:10
    z = (itr_line(1,i)*x + itr_line(2,i)*y)/itr_line(3,i);
    surf(x,y,z);
end

for i=1:3
    z = (lines(1,i)*x + lines(2,i)*y)/lines(3,i);
    surf(x,y,z);
end





