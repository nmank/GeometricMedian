function er = calc_error(x,Y,p,opt_type)
    er = 0;
    if opt_type == 'chord'
        for i=1:p
            cos_theta = abs(x{i}'*Y);
            if abs(x{i}'*Y)< -1
                theta = pi;
            elseif abs(x{i}'*Y)>1
                theta = 0;
            else
                theta = acos(cos_theta);
            end
            er = er + sin(theta);
        end
    elseif opt_type == 'chors'
        for i=1:p
            cos_theta = abs(x{i}'*Y);
            if abs(x{i}'*Y)< -1
                theta = pi;
            elseif abs(x{i}'*Y)>1
                theta = 0;
            else
                theta = acos(cos_theta);
            end
            er = er + real(sin(theta))^2;
        end
    elseif opt_type == 'geodi' 
        for i=1:p
            cos_theta = abs(x{i}'*Y);
            if abs(x{i}'*Y)< -1
                theta = pi;
            elseif abs(x{i}'*Y)>1
                theta = 0;
            else
                theta = acos(cos_theta);
            end
            er = er + theta;
        end
    elseif opt_type == 'geods'
        cos_theta = abs(x{i}'*Y);
            if abs(x{i}'*Y)< -1
                theta = pi;
            elseif abs(x{i}'*Y)>1
                theta = 0;
            else
                theta = acos(cos_theta);
            end
        for i=1:p
            er = er + theta^2;
        end
    elseif isstr(opt_type) == 0
        for i=1:p
            cos_theta = abs(x{i}'*Y);
            if abs(x{i}'*Y)< -1
                theta = pi;
            elseif abs(x{i}'*Y)>1
                theta = 0;
            else
                theta = acos(cos_theta);
            end
            er = er + (real(sin(theta))^2)^opt_type;
        end
    else
        sprintf('UNUSABLE WEIGHT TYPE')
    end
end