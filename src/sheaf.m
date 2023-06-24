function [erates, edelta, actrates] = sheaf(predictions, measurements, eqns)
    deltapred = eqns*predictions'; %This gives the change in metabolites we expect, given rate predictions
    eqnextended = eqns; 
    actrates = pinv(eqns)*measurements'; %This gives the rates we expect, assuming our predictions and using metabolite measurements
    erates = predictions' - actrates;
    edelta = deltapred - measurements';
end