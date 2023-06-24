% metabolic reactions
% 1 : A --> B 
% 2 : B --> C + D
%
%    [ r1 r2  A  B  C  D]
eA = [ -1  0 -1  0  0  0];
eB = [  1 -1  0 -1  0  0];
eC = [  0  1  0  0 -1  0];
eD = [  0  1  0  0  0 -1];

E = [eA; eB; eC; eD;];

%              [ r1 r2  A  B  C  D]
measurements = [ 1  2   3  4  5  6]';
excludeFactor(E,measurements,1:size(E,2))