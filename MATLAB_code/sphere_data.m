function [data,labels,label_names] = sphere_data(num_points,regular,circle,angle,frame)


if frame == 6
    labels = [1:6];
    label_names = labels;
    
    alph = 1/sqrt(5);
    data(:,1)= [0;0;1];
    data(:,2)= [sqrt(1-alph^2);0;alph];
    data(:,3)= [alph*sqrt((1-alph)/(1+alph)),sqrt((1+2*alph)*(1-alph)/(1+alph)),alph];
    data(:,4)= [alph*sqrt((1-alph)/(1+alph)),-sqrt((1+2*alph)*(1-alph)/(1+alph)),alph];
    data(:,5)= [-alph*sqrt((1+alph)/(1-alph)),sqrt((1-2*alph)*(1+alph)/(1-alph)),alph];
    data(:,6)= [-alph*sqrt((1+alph)/(1-alph)),-sqrt((1-2*alph)*(1+alph)/(1-alph)),alph];;
elseif frame == 7
    F = [-0.8660357512091325,
            0.0883105669356131,
            0.4921212466406468,
0.0917774516007844,
-0.1799110941824524,
-0.9793921061391798,
-0.7023471350867070,
-0.7089146224380025,
0.0644093155458075,
0.7600602784346310,
0.1194328703772649,
0.6387833456026533,
0.0550351361953868,
-0.9068946631296984,
-0.4177477753032638,
-0.7058933355778055,
0.6819619170332442,
-0.1914224190192523,
-0.0509403365791145,
-0.6991512258168202,
0.7131568169400361]
    for i=1:7
        for j=1:3
            data(j,i) = F((i-1)*3+j);
        end
        if data(3,i)<0
            data(:,i) = -data(:,i);
        end
    end
    labels = [1:7];
    label_names = labels;
elseif frame == 8
    F = [-0.5206331422670317,
0.0582793469182117,
-0.8517890870960626,
0.9152524348564197,
0.3661143368365520,
0.1681465814464479,
-0.8585122514737608,
0.4707641694864390,
-0.2033170204316341,
-0.7257435503194911,
0.3160248630503207,
0.6110847609813932,
-0.3183584979996931,
-0.9461763764444925,
-0.0582934937171339,
0.1842536974911826,
-0.7830235607990399,
0.5940746402552631,
-0.6115411009213358,
-0.5156358203084005,
0.6001143080270654,
0.0366529324169408,
0.6240048129275264,
0.7805604114919755];
    for i=1:8
        for j=1:3
            data(j,i) = F((i-1)*3+j);
        end
        if data(3,i)<0
            data(:,i) = -data(:,i);
        end
    end
    labels = [1:8];
    label_names = labels;

else
    labels = [1:num_points];
    label_names = labels;
    
    if circle
        %theta = pi*ones(num_points,1)/4;
        theta = angle*ones(num_points,1);
    else 
        theta = pi*rand(num_points,1)/4;
    end

    if regular
        phi = 2*pi*[1:num_points]/num_points;
    else
        %phi = 2*pi*rand(num_points,1);
        phi = 2*pi*normrnd(0,.2,[num_points]);
    end




    data = zeros(3,num_points);
    for i=1:num_points
        data(1,i) = sin(theta(i))*cos(phi(i));
        data(2,i) = sin(theta(i))*sin(phi(i));
        data(3,i) = cos(theta(i));
    end

    % data = zeros(3,num_points);
    % data(:,1) = [.1;.1;.1]/norm([.1;.1;.1]);
    % data(:,2) = [-.1;.2;.1]/norm([-.1;.2;.1]);
    % data(:,3) = [.3;-.1;.1]/norm([.3;-.1;.1]);
end

end