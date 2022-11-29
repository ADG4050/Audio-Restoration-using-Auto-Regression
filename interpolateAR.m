%function of interpoltion for signal restoration 
function [restored] = interpolateAR(datablock, thres_res, fram_size, ...
    model_order, coeffs, new_input)

% creation of A Matrix 

    A = zeros([(fram_size - model_order) fram_size]);
    for i = 1:fram_size - model_order
        int_coef = [flip(coeffs), 1];
        A(i, i:length(int_coef) + i - 1) = int_coef;
    end

% Creating Matrix Ak, Au out of A and yk.

    u_ind = find(thres_res == 1);
    k_ind = find(thres_res == 0);
    Ak = A(:, k_ind);
    Au = A(:, u_ind);
    yk = datablock(:, k_ind);
   
%unknown elements (yu) from matrix calculations 
    yu = (- (Au)' * Au) \ ((Au)' * Ak * (yk)');


% restored block
    for k = 1:length(yu)
        datablock(:, u_ind) = yu(k);  
    end

    restored = datablock;
    restored = (restored + mean(new_input)); %.* std(new_input));
end
