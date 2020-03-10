function dst = calc_dist(x,y,opt_type)
    if opt_type == 'chord'
        dst = real(sin(acos(abs(x'*y))));
    elseif opt_type == 'chors'
        dst = real(sin(acos(abs(x'*y))))^2;
    elseif opt_type == 'geodi' 
        dst = acos(abs(x'*y));
    elseif opt_type == 'geods'
        dst = acos(abs(x'*y))^2;
    else
        print('UNUSABLE WEIGHT TYPE')
    end
end