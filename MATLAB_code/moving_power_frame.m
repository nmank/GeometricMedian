%data parameters
num_points = 4;
circ = true; %placed on the origin
%angle = 2*pi/9; %angle for the circle from the origin in the direction of the z axis
reg = true; %regular spacing
frame = 1; %set this to 6 for point frame data
filename = 'chor_opt_4.gif';

%generate the data
mu = 1-(3-1)*num_points/(3*(num_points-1));
[ F, coh ] = troppaltproj_sp( num_points, 1, 3, mu );
labels = [1:num_points];
label_names = labels;
data = F;

for ii=1:100
    opt_type = .5+ii*.01;
    
    %something to check the parameter space
    h = figure('Visible', 'off');
    set(h,'visible','off')
    num_it = 100000;
    [err1, sp_pts,vtx_err] = opt_space(data,labels,label_names,num_it,opt_type);
    scatter3(sp_pts(1,:),sp_pts(2,:),sp_pts(3,:),ones(num_it+1,1)*10,exp(-err1),'filled');
    hold on
    %data
    scatter3(data(1,:),data(2,:),data(3,:)+.02,ones(num_points,1)*50,'k','filled')
    title(string(opt_type))
    view([0,90]);
    
    % Capture the plot as an image 
    frame1 = getframe(h); 
    im = frame2im(frame1); 
    [imind,cm] = rgb2ind(im,256); 
    
    % Write to the GIF File 
    if ii == 1 
        imwrite(imind,cm,filename,'gif', 'Loopcount',inf); 
    else 
        imwrite(imind,cm,filename,'gif','WriteMode','append'); 
    end 
end


    