import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Define time points for every hour (original data)
time_hours = np.arange(0, 24, 1)  # 24 hours, one data point per hour

# Generate a basic CGM-like pattern with a baseline and moderate volatility
baseline = 120  # Mid-range baseline for glucose level
volatility = 10  # Degree of fluctuation around baseline
glucose_levels = baseline + np.random.normal(0, volatility, time_hours.shape)

# Introduce smoother, gradual spikes for post-meal glucose increases
spike_hours = [7, 12, 18]  # Common times for meals (breakfast, lunch, dinner)
spike_magnitude = 30  # Spike magnitude to simulate meal response
for hour in spike_hours:
    # Spread each spike over a few hours for a gradual effect
    glucose_levels[hour-1:hour+2] += np.linspace(0, spike_magnitude, 3)

# Add gentle dips to simulate periods of low glucose
dip_hours = [3, 15]  # Times that might represent overnight and afternoon lows
dip_magnitude = 15  # Dip magnitude to simulate glucose drops
for hour in dip_hours:
    # Spread each dip over a few hours for a gradual effect
    glucose_levels[hour-1:hour+2] -= np.linspace(0, dip_magnitude, 3)

# Add specific points to exceed the target boundaries
glucose_levels[5] = 65  # A dip below 70 mg/dl
glucose_levels[19] = 185  # A spike above 180 mg/dl

# Interpolate to add points every 5 minutes
# Define a new time range with 5-minute intervals (288 points for 24 hours)
time_5min = np.linspace(0, 23, 288)  # Each hour has 12 five-minute intervals

# Interpolation function
interp_func = interp1d(time_hours, glucose_levels, kind='cubic')
glucose_levels_5min = interp_func(time_5min)

# Plotting the data with CGM target boundaries and shaded area
plt.figure(figsize=(12, 6))
plt.plot(time_5min, glucose_levels_5min, label='CGM Reading (mock data)', color='blue')

# Add boundary lines for 180 mg/dl and 70 mg/dl
plt.axhline(y=180, color='red', linestyle='--', linewidth=1.5, label='Upper Boundary (180 mg/dl)')
plt.axhline(y=70, color='red', linestyle='--', linewidth=1.5, label='Lower Boundary (70 mg/dl)')

# Add a light green shaded area between the boundary lines
plt.fill_between(time_5min, 70, 180, color='lightgreen', alpha=0.3)

# Additional plot settings
plt.title("Simulated CGM Sensor Data Over 24 Hours with Boundary Exceedance", pad=20)
plt.xlabel("Time (hours)", labelpad=15)
plt.ylabel("Blood Glucose Level (mg/dl)", labelpad=15)
plt.ylim(60, 190)
plt.grid(True)

# Set the y-axis ticks to only show 70 and 180 mg/dl
plt.yticks([70, 180])

# Box off the plot by setting limits and removing extra space
plt.xlim(0, 23)  # Set x-axis to cut off at 24 hours (from 0 to 23)
plt.gca().spines['top'].set_visible(False)  # Remove top border
plt.gca().spines['right'].set_visible(False)  # Remove right border
plt.gca().spines['left'].set_linewidth(1.5)  # Increase left border width
plt.gca().spines['bottom'].set_linewidth(1.5)  # Increase bottom border width

# Add a legend
plt.legend()

# Show the plot
plt.show()
