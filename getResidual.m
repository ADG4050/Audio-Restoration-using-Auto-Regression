% Function for generation of residual over all the blocks
function [residual] = getResidual(data, coeffs)
    data = data - mean(data);
    residual = filter([1 coeffs], 1, data);
end