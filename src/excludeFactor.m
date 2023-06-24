function estimates = excludeFactor(A,b,columns)
    estimates = zeros( size(A,1), numel(columns) );
    for i = 1:numel(columns)
        c = columns(i);
        Adim = [ A(:,1:c-1) A(:,c+1:end) ];
        bdim = [ b(1:c-1); b(c+1:end) ];
        estimates(:,i) = -(Adim * bdim) ./ A(:,c) ;
    end
end