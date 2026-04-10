import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

initial_amp = 1.0
initial_freq = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_cov = 0.1
initial_cutoff = 0.1

t = np.linspace(0, 10, 1000)
current_noise = np.random.normal(initial_noise_mean, np.sqrt(initial_noise_cov), len(t))

def harmonic_with_noise(t, amplitude, frequency, phase, show_noise):
    y_pure = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return (y_pure + current_noise, y_pure) if show_noise else (y_pure, y_pure)

def apply_filter(data, cutoff):
    try:
        b, a = butter(3, cutoff, btype='low', analog=False)
        return filtfilt(b, a, data)
    except: return data

fig, ax = plt.subplots(figsize=(10, 9))
plt.subplots_adjust(left=0.1, bottom=0.45, top=0.92) 

y_noisy, y_pure = harmonic_with_noise(t, initial_amp, initial_freq, initial_phase, True)
y_filtered = apply_filter(y_noisy, initial_cutoff)

line_pure, = ax.plot(t, y_pure, label='Чиста гармоніка', color='green', lw=1.5, alpha=0.7)
line_noisy, = ax.plot(t, y_noisy, label='Зашумлений сигнал', color='blue', lw=1, alpha=0.5)
line_filtered, = ax.plot(t, y_filtered, label='Відфільтрований сигнал', color='red', lw=2)

ax.set_ylim(-5, 5)
ax.legend(loc='upper right')
ax.set_title("Гармоніка з шумом та фільтрацією")

ax_color = 'lightgoldenrodyellow'
s_amp = Slider(plt.axes([0.15, 0.35, 0.3, 0.03], facecolor=ax_color), 'Амплітуда', 0.1, 5.0, valinit=initial_amp)
s_freq = Slider(plt.axes([0.15, 0.30, 0.3, 0.03], facecolor=ax_color), 'Частота', 0.1, 5.0, valinit=initial_freq)
s_phase = Slider(plt.axes([0.15, 0.25, 0.3, 0.03], facecolor=ax_color), 'Фаза', 0, 2*np.pi, valinit=initial_phase)

s_n_mean = Slider(plt.axes([0.6, 0.35, 0.3, 0.03], facecolor=ax_color), 'Сер. шум', -1.0, 1.0, valinit=initial_noise_mean)
s_n_cov = Slider(plt.axes([0.6, 0.30, 0.3, 0.03], facecolor=ax_color), 'Дисп. шуму', 0.0, 1.0, valinit=initial_noise_cov)
s_filter = Slider(plt.axes([0.6, 0.25, 0.3, 0.03], facecolor=ax_color), 'Фільтр', 0.01, 0.5, valinit=initial_cutoff)

rax = plt.axes([0.15, 0.13, 0.3, 0.08], facecolor='#f0f0f0')
check = CheckButtons(rax, ('Показати шум', 'Показати фільтр'), (True, True))

btn_res = Button(plt.axes([0.8, 0.13, 0.1, 0.05]), 'Reset', color='#ff9999')

def update(val):
    global current_noise
    if s_n_mean.val != update.last_n[0] or s_n_cov.val != update.last_n[1]:
        current_noise = np.random.normal(s_n_mean.val, np.sqrt(s_n_cov.val), len(t))
        update.last_n = (s_n_mean.val, s_n_cov.val)
    
    y_n, y_p = harmonic_with_noise(t, s_amp.val, s_freq.val, s_phase.val, check.get_status()[0])
    line_pure.set_ydata(y_p)
    line_noisy.set_ydata(y_n); line_noisy.set_visible(check.get_status()[0])
    
    y_f = apply_filter(y_n, s_filter.val)
    line_filtered.set_ydata(y_f); line_filtered.set_visible(check.get_status()[1])
    fig.canvas.draw_idle()

update.last_n = (initial_noise_mean, initial_noise_cov)
for s in [s_amp, s_freq, s_phase, s_n_mean, s_n_cov, s_filter]: s.on_changed(update)
check.on_clicked(update)

def reset(e):
    for s in [s_amp, s_freq, s_phase, s_n_mean, s_n_cov, s_filter]: s.reset()
btn_res.on_clicked(reset)

instruction_text = (
    "ІНСТРУКЦІЯ:\n"
    "- Слайдери дають можливість змінювати бажані параметри.\n"
    "- Також ви можете показувати/приховувати шуми та фільтри відповідною кнопкою.\n"
    "- Кнопка Reset скидає всі параметри до початкових значень."
)

fig.text(0.5, 0.01, instruction_text, 
         fontsize=9, 
         color='#333333',
         ha='center', 
         va='bottom',
         bbox=dict(facecolor='white', edgecolor='#cccccc', boxstyle='round,pad=0.3'))

plt.show()