% Function for calculation of AR Coefficients
%calculating Caps R for all blocks of data
function [coeffs] = estimateARcoeffs(data, model_order)
% calculating small r
    for i = 1:model_order
        r(i) = sum(data((model_order + 1) : ...
            length(data)) .* data((model_order + 1 - i) : ...
            (length(data) - i)));
    end

% calculating Caps R

    for i = 1:model_order
        for j = 1:model_order
            R(i, j) = sum(data((model_order + 1 - i) : ...
                length(data) - i) .* data((model_order + 1 - j) ...
                : (length(data) - j)));
        end
    end

% Calculating coefficient_A

    coeffs = -inv(R) * transpose(r);

end