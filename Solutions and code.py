%% PART 1

% % Params (alternative set)
% G  = 2;          % unitless
% R  = 10e3;       % 10 kΩ
% C  = 10e-9;      % 10 nF
% R2 = 20e3;       % 20 kΩ
% R3 = 5e3;        % 5 kΩ
% W  = R*C;

%% Params (chosen set for +10 dB at w = 600*pi)
G  = 600*pi;   % unitless
R  = 1;        % normalized
C  = 1;        % normalized
R2 = 1;        % normalized
R3 = pi;       % normalized
W  = R*C;

%% Define systems

% H3(s)
H3 = tf([-1, 0, 0], [1, (G*R2)/(W*R3), (G/W)^2]);
H3.Name = 'H3';

% H2(s)
H2 = tf([0, -G, 0], [W, (R2*G)/R3, G^2/W]);
H2.Name = 'H2';

% H1(s)
H1 = tf([0, 0, -G^2], [W^2, (G*W*R2)/R3, G^2]);
H1.Name = 'H1';

%% Pole–Zero plot (all on one figure)
figure('Name','Pole–Zero Map');
pzmap(H1, H2, H3);
grid on;
title('Pole–Zero Map');
legend('H1','H2','H3','Location','best');

%% Impulse responses
figure('Name','Impulse Responses');
impulse(H1, H2, H3);
grid on;
legend('H1','H2','H3','Location','best');
title('Impulse Response of H1, H2, H3');
xlabel('Time (s)');
ylabel('Amplitude');

%% Bode plots
figure('Name','Bode Plots');
bode(H1, H2, H3);
grid on;
legend('H1','H2','H3','Location','best');
title('Bode Plot of H1, H2, H3');

% (Extra Bode call – kept as in original code)
bode(H1, H2, H3);

%% Uppgift 7
% För att få +10 dB vid w = 600*pi:
% ---> sätt t.ex. G = 600*pi, R2/R3 = 1/pi

n_min = 1;
n_max = 50;
L     = 1/200;
h     = 1;

% Funktion som tar ett skalärt t och returnerar Fourier-summan
% av de n_max första termerna
fourier_sum = @(t) 2*h/pi * sum( (1./(n_min:n_max)) .* sin((n_min:n_max)*pi*t/L) );

% Tidsarray
t = 0:0.0001:0.1;

% Beräkna f(t) för varje t
f = arrayfun(fourier_sum, t);

figure;
plot(t, f);
title('Fourierserie-signal');
xlabel('Tid (s)');
ylabel('Amplitude');
grid on;

figure;
lsim(H1, f, t);
title('Svar från H1 på Fourierserie-signal');
xlabel('Tid (s)');
ylabel('Amplitude');
grid on;


%% PART 2
%% Chebyshev I low-pass: specification setup (done on paper)

% --- Specs
wp = 2*pi*8e3;                 % rad/s, passband edge
ws = 2*pi*16e3;                % rad/s, stopband edge
Rp = 3;                        % dB, passband ripple (±3 dB)
Rs = 20*log10(4096);           % dB, stopband attenuation (~72.24 dB)
% (These are in dB because cheb* functions use dB specs)


%% Finding the lowest-order filters and plotting their responses

% --- Minimum order and design (Butterworth, analog)
[N1, wc]    = buttord(wp, ws, Rp, Rs, 's');
[num1,den1] = butter(N1, wc, 's');
% N1 = 13 (from earlier calculation)

% --- Minimum order and design (Chebyshev I, analog)
[N2, Wp2]   = cheb1ord(wp, ws, Rp, Rs, 's');
[num2,den2] = cheby1(N2, Rp, Wp2, 's');
% N2 = 7

% --- Minimum order and design (Chebyshev II, analog)
[N3, Wp3]   = cheb2ord(wp, ws, Rp, Rs, 's');
[num3,den3] = cheby2(N3, Rp, Wp3, 's');
% N3 = 7

% I therefore select a Chebyshev I filter --------------------------
H_cheby1 = tf(num2, den2);

figure;
bode(H_cheby1); grid on;
title('Bode Plot of Selected Chebyshev I LP Filter');

% Extra: Bode plot with handle
h = bodeplot(H_cheby1); grid on; %#ok<NASGU>


%% Superposition of sine waves (continuous-time signal, then sampling)
% Useful components + one interference tone

A1 = 1;           % V, amplitude of main sines (<= 1)
A  = 0.15;        % V, amplitude of interference (<= 1)

f1 = 1000;        % Hz, sine 1 (in useful band)
f2 = 6000;        % Hz, sine 2 (in useful band)
f3 = 15000;       % Hz, interference tone (> 11 kHz)

fs = 24e3;        % Hz, sampling rate

% Time vector: short, dense window
t = 0:1/fs:5e-3;

% Continuous-time composite signal
x_ct = A1*sin(2*pi*f1*t) + A1*sin(2*pi*f2*t) + A*sin(2*pi*f3*t);

figure;
plot(t, x_ct, 'LineWidth', 1.2);
grid on;
xlabel('Time (s)');
ylabel('Amplitude (V)');
title('x_{ct}(t) = Sum of Useful + Interference Tones');


%% Simulate analog filter response

y_ct = lsim(H_cheby1, x_ct, t);

figure;
plot(t, y_ct, 'LineWidth', 1.2);
grid on;
xlabel('Time (s)');
ylabel('Amplitude (V)');
title('AA Filter Output y_{ct}(t)');


%% Sampling (here: use all samples as discrete-time signal)

x_dt = y_ct(1:1:end);
t_dt = t(1:1:end);

figure;
stem(t_dt, x_dt, 'filled');
grid on;
xlabel('Time (s)');
ylabel('Amplitude (V)');
title('Sampled Sequence x[n]');


%% FFT and amplitude spectrum

N = length(x_dt);
X = fft(x_dt);
f = (0:N-1)*(fs/N);

mag = abs(X);
mag = mag / max(mag);   % normalize so max peak = 1

figure;
plot(f, mag);
grid on;
xlim([0 fs/2]);
xlabel('Frequency (Hz)');
ylabel('Normalized |X(f)|');
title('Magnitude Spectrum of Sampled Signal (max = 1)');

