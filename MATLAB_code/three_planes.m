function [planes,lines,labels,label_names] = three_planes(angle)

labels = [1:3];
label_names = labels;

theta = angle*ones(3,1);
phi = 2*pi*[1:3]/3;

planes = [];
for i=1:3
    lines(:,i) = [sin(theta(i))*cos(phi(i)); sin(theta(i))*sin(phi(i)); cos(theta(i))];
    x = [lines(:,i),rand(3,1),rand(3,1)];
    [Q,R] = qr(x);
    planes(:,:,i) = Q(:,2:3);
end

end