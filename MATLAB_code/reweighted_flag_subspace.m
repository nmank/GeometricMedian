function [median_subspace,perp_line] = reweighted_flag_subspace(data,labels,label_names,epsilon,init, opt_type)
    mdian = zeros(3,2);
    for i=1:2
        [mdian(:,i),err,weights,ii,init_pt,y] = reweighted_flag(data(:,i,:),labels,label_names,epsilon,init, opt_type) 
    end 
    [Q,R] = qr(mdian);
    median_subspace = Q(:,1:2);
    perp_line = Q(:,3);
end