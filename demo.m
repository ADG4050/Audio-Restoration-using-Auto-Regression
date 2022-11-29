clear all
close all

tic
% reading the real and degraded file and storing the degraded sampled
% version in audio input with Fs as sample frequency.
[og, fs] = audioread('clean.wav');
[audinp, Fs] = audioread("degraded.wav");

% plotting the input audio.
figure(1); 
plot(audinp); 
title('Audio input');
ylabel('Amplitude'), xlabel('Time(secs)');


% taking only the left handle of the audio as both left and righ coloumn
% of the audio are same.
input = audinp(:, 1);

% initialising the parameters
fram_dur = 1; % Frame duration of each block
model_order = 15;

% If input audio size is to be changed 
% time  = ''; % replace '' with desired time in seconds
% input = input(1 : (time * 1000));


% normalising the data by considering model order = 3.
new_input = input((model_order + 1):length(input));
% Norm_input = new_input;
Norm_input = (new_input - mean(new_input)); %./ std(new_input);
figure(2); 
plot(Norm_input); 
title('Normalised input');
ylabel('Amplitude'), xlabel('Time(secs)');


% distributing the input data to mutliple blocks of data
fram_size = round(fram_dur * Fs); 
N = length(Norm_input);
No_of_frames = floor(N / fram_size); % Individual block size
temp = 0;
for j = 1:No_of_frames
    blocks(j, :) = Norm_input(temp + 1 : temp + fram_size);
    temp = temp + fram_size;
end


% calculation of AR Coefficients (Function declaration in seperate file)
for i = 1:No_of_frames
    [coeffs(i, :)] = estimateARcoeffs(blocks(i, :), model_order);
end

% calculation of residual using function (Function declaration in 
% seperate file)
for i = 1:No_of_frames
    res(i, :) = getResidual(blocks(i, :), coeffs(i, :));
end

% Accumulation of residual all over blocks for plotting 
Res = reshape(res', 1, []);
figure(3); 
plot(Res); 
title('Residual signal');
ylabel('Amplitude'), xlabel('Time(secs)');

% Applying threshold for the residual blocks
thres_res = res;
for i = 1:No_of_frames
    for j = 1:fram_size
        if (abs(thres_res(i, j)) >= 0.25)
            thres_res(i, j) = 1;
        else
            thres_res(i, j) = 0;
        end
    end
end

% Accumulation of clicks all over blocks for plotting 
Thres_res = reshape(thres_res', 1, []);
figure(4);
plot(Thres_res); 
title('All clicks');
ylabel('Amplitude'), xlabel('Time(secs)');

% Interpolation process for the signal restoration(Function declaration 
% in seperate file)
for i = 1:No_of_frames
    [restored(i, :)] = interpolateAR(blocks(i, :), thres_res(i, :), ...
        fram_size, model_order, coeffs(i, :), new_input);
end

% Accumulation of restored values all over blocks for plotting 
Restored = reshape(restored', 1, []);
% figure(5);
% subplot(2, 1, 1);
% plot(new_input), title('degraded signal');
% subplot(2, 1, 2);
% plot(Restored), title('restored signal');


% Calculation of Mean square error
mse_input1 = input(1:(fram_size * No_of_frames)); %degraded signal
mse_input2 = Restored; % restored signal
mse_input3 = og(1:(fram_size * No_of_frames)); %real signal

% mse between real and restored signal
mse = sum((mse_input3' - mse_input2) .^ 2) / (fram_size * Fs); 


% FINAL PLOT
figure(5);
subplot(3, 1, 1);
plot(mse_input3), title('original signal');
ylabel('Amplitude'), xlabel('Time(secs)');
subplot(3, 1, 2);
plot(mse_input1), title('degraded signal');
ylabel('Amplitude'), xlabel('Time(secs)');
subplot(3, 1, 3);
plot(Restored), title('Restored signal');
ylabel('Amplitude'), xlabel('Time(secs)');

 
toc
% Exporting the restored audio clip (uncomment it)
%audiowrite('output.wav', Restored, Fs);

% No of clicks detected in the Degraded Signal
a = 0;
for i = 1:length(Thres_res)
    if(Thres_res(i) == 1)
        a = a + 1;
    end
end 

b = find(Thres_res == 1); %index of degradation














