function Fy = calc_gradient(x,Y0,opt_type,n,p)
    Fy = zeros(n,1);
    if opt_type == 'chord'
        for i=1:p
            if isinf(1/real(sin(acos(x{i}'*Y0)))) ~= true
                Fy = Fy + (-x{i}*x{i}'*Y0)/real(sin(acos(abs(x{i}'*Y0))));  
            end
        end     
    elseif opt_type == 'geodi'
        for i=1:p
            if isinf(1/(sin(acos(x{i}'*Y0))*x{i}'*Y0)) ~= true
                Fy = Fy + (-x{i}*x{i}'*Y0)/(sin(acos(x{i}'*Y0))*x{i}'*Y0);  
            end
        end  
    elseif opt_type == 'geods'
        for i=1:p
            if isinf(1/real(sin(acos(x{i}'*Y0)))) ~= true
                Fy = Fy + (-x{i}*x{i}'*Y0)*acos((Y0'*x{i})^2)/(sqrt(1-(Y0'*x{i})^4));  
            end
        end  
    else 
        print('INVALID OPT TYPE')
    end

end