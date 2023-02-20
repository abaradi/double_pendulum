import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# The masses and lengths of the pendulum system
m1, m2, L1, L2, g = 1, 1, 1, 1, 9.81

# Returns a set of ODEs that describe the pendulum's behaviour


def deriv(y_list, t, L1, L2, m1, m2):
    theta_1, theta_2, omega_1, omega_2 = y_list

    c, s = np.cos(theta_1-theta_2), np.sin(theta_1-theta_2)

    theta_1dot = omega_1
    theta_2dot = omega_2
    omega_1dot = (m2*g*np.sin(theta_2)*c - m2*s*(L1*omega_1**2*c + L2*omega_2**2) -
                  (m1+m2)*g*np.sin(theta_1)) / (L1 * (m1 + m2*s**2))
    omega_2dot = ((m1+m2)*(L1*omega_1**2*s - g*np.sin(theta_2) + g*np.sin(theta_1)*c) +
                  m2*L2*omega_2**2*s*c) / (L2 * (m1 + m2*s**2))
    return theta_1dot, theta_2dot, omega_1dot, omega_2dot


# Time Span of the animation (seconds)

t_0 = 0.00
t_max = 30
dt = 0.04
t = np.arange(t_0, t_max, dt)

# Initial Conditions: theta_1, theta2, dtheta_1/dt, dtheta_2/dt
y0 = np.array([2*np.pi/5, 3*np.pi/4, 0, 0])


# Integrate the ODEs to get the solution

y = odeint(deriv, y0, t, args=(L1, L2, m1, m2))


# Extract theta_1(t) and theta_2(t) from the solution

theta_1, theta_2 = y[:, 0], y[:, 1]

# Converting the cartesian coordinates of the masses

x1 = L1 * np.sin(theta_1)
y1 = -L1 * np.cos(theta_1)
x2 = x1 + L2 * np.sin(theta_2)
y2 = y1 - L2 * np.cos(theta_2)

# Making the the figure

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-L1-L2,
                                                    L1+L2), ylim=(-L1-L2, L1+L2), title='Double Pendulum')
ax.grid()
line, = ax.plot([], [], 'o-', lw=2)
time_template = 'Time = %.1fs'
time_text = ax.text(-1.9, 1.65, '')


# Initializing the animation with empty data

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


# The animating function

def animate(i):
    x = [0, x1[i], x2[i]]
    y = [0, y1[i], y2[i]]
    line.set_data(x, y)
    time_text.set_text(time_template % (i * dt))
    return line, time_text


# Animation Settings

i = np.arange(0, len(t))
anim = animation.FuncAnimation(fig, animate, i,
                               interval=1, blit=False, repeat=False, init_func=init)
# Showing the animation

plt.show()
'''
# Saving the animation

writervideo = animation.FFMpegWriter(fps=24.5, bitrate=-1)

plt.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\unive\\Downloads\\Programs\\ffmpeg-4.3.1-win64-static\\bin\\ffmpeg.exe'

anim.save('Double Pendulum.mp4', writer=writervideo)
'''
# Plotting theta1 and theta2 vs time

fig = plt.figure(figsize=(8.5, 11))
for i in range(1, 3):
    ax = fig.add_subplot(2, 1, i)
    ax.set_ylabel(r'$\theta \ (rad)$')
    ax.set_xlabel(r'Time (s)')
    ax.set_facecolor('#212946')
    ax.tick_params(labelsize='small')
    ax.grid(b=True, which='both', axis='both', color='#2A3459')
    if i == 1:
        ax.plot(t, theta_1, label=r'$\theta_{1}$')
    else:
        ax.plot(t, theta_2, label=r'$\theta_{2}$')
    ax.legend(fontsize='x-small', shadow=True)

plt.show()
fig.savefig("Angle vs Time.pdf")
