%data parameters
num_points = 3;
circ = true; %placed on the origin
%angle = 2*pi/9; %angle for the circle from the origin in the direction of the z axis
reg = true; %regular spacing
frame = 1; %set this to 6 for point frame data
opt_type = 'chord';

special_angle = 0;
for ii=1:100
    angle = ii*(pi/2)/100;
    %generate the data
    [data,labels,label_names] = sphere_data(num_points,reg,circ,angle,frame);

    %something to check the parameter space
    num_it = 100000;
    [err1, sp_pts,vtx_err] = opt_space(data,labels,label_names,num_it,opt_type);
    miner = min(err1);
    
    if (miner>=vtx_err(1)) && (special_angle == 0)
        special_angle = angle;
    end
end

%special angles for each opt type and number of points
%CAUTION: ERR1 is the set of all errors for 100000 randomly spaced points,
%so this might not be that accurate!
% opt type, num_pts, angle
% chord, 3, 0.628318530717959 almost pi/5
% chord, 4, 0.738274273593601>pi/5
% geodi, 3, 1.240929098167968>pi/3
% geodi, 4, 0.926769832808989>pi/4


    