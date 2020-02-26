function [alpha,X] = weight(x,Y0,opt_type)
    p = length(x);
    X = zeros(3,p);
    alpha = [];
    if opt_type == 'chord'
        for i=1:p
            alpha(i) = sqrt(1/sin(acos(abs(x{i}'*Y0)))); 
            X(:,i) = alpha(i)*x{i};
        end
    elseif opt_type == 'geodi' 
        for i=1:p
            alpha(i) = 1/sqrt((sin(abs(acos(x{i}'*Y0)))*abs(x{i}'*Y0))); 
            X(:,i) = alpha(i)*x{i};
        end
    elseif opt_type == 'geods'
        for i=1:p
            alpha(i) = abs(acos(x{i}'*Y0))/sqrt(1-(x{i}'*Y0)^4); 
            X(:,i) = alpha(i)*x{i};
        end  
    else
        sprintf('UNUSABLE WEIGHT TYPE')
    end
end