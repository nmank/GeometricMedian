function er = calc_error(x,Y,p,opt_type)
    er = 0;
    if opt_type == 'chord'
        for i=1:p
            er = er + real(sin(acos(abs(x{i}'*Y))));
        end
    elseif opt_type == 'chors'
        for i=1:p
            er = er + real(sin(acos(abs(x{i}'*Y))))^2;
        end
    elseif opt_type == 'geodi' 
        for i=1:p
            er = er + acos(abs(x{i}'*Y));
        end
    elseif opt_type == 'geods'
        for i=1:p
            er = er + acos(abs(x{i}'*Y))^2;
        end
    else
        sprintf('UNUSABLE WEIGHT TYPE')
    end
end