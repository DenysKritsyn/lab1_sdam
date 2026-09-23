import tkinter as tk
import collections
import matplotlib.pyplot as plt
import tkinter.messagebox as messagebox
from itertools import accumulate
from tkinter import messagebox
from parameters.average import getAverage
from parameters.median import getMedian
from parameters.mode import getMode, NoModeError
from parameters.scope import getScope
from parameters.math_expectation import getMathExpectation
from parameters.dispersion import getDispersion
from parameters.standard_deviation import getStandardDeviation
from parameters.modified_dispersion import getModifiedDispersion
from parameters.modified_standard_deviation import getModifiedStandardDeviation
from parameters.variation import getVariation
from parameters.initial_statistical_moment import getInitialStatisticalMoment
from parameters.central_statistical_moment import getCentralStatisticalMoment
from parameters.asymmetry import getAsymmetry
from parameters.excess import getExcess

def estimate_parameters():
    raw_data = entry_series.get()
    try:
        # Numbers can be separated by spaces or commas
        clean_data = raw_data.replace(',', ' ')
        num_series = [float(x) for x in clean_data.split()]
        
        if not num_series:
            messagebox.showwarning("Warning", "Please enter at least one number.")
            return

        # Compute characteristics
        avg = getAverage(num_series)
        med = getMedian(num_series)
        scope = getScope(num_series)
        m_exp = getMathExpectation(num_series)
        disp = getDispersion(num_series)
        mod_disp = getModifiedDispersion(num_series)
        mod_std_dev = getModifiedStandardDeviation(num_series)
        init_moment_2 = getInitialStatisticalMoment(2, num_series)
        cent_moment_2 = getCentralStatisticalMoment(2, num_series)
        std_dev = getStandardDeviation(num_series)
        
        # Check if mode is possible
        try:
            mod = getMode(num_series)
        except NoModeError:
            mod = "No Mode (all numbers are unique)"

        # Handle potential division by zero
        if std_dev == 0:
            var = "Error (Math Expectation = 0)"
            asym = "Error (Standard Deviation = 0)"
            exc = "Error (Standard Deviation = 0)"
        else:
            var = round(getVariation(num_series), 4)
            asym = round(getAsymmetry(num_series), 4)
            exc = round(getExcess(num_series), 4)

        # Display results
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        
        results = [
            f"Average: {avg}",
            f"Median: {med}",
            f"Mode: {mod}",
            f"Scope (Range): {scope}",
            f"Math Expectation: {m_exp}",
            f"Dispersion: {disp}",
            f"Standard Deviation: {std_dev}",
            f"Modified Dispersion: {mod_disp}",
            f"Modified Standard Deviation: {mod_std_dev}",
            f"Variation (%): {var}",
            f"Initial Statistical Moment (k=2): {init_moment_2}",
            f"Central Statistical Moment (k=2): {cent_moment_2}",
            f"Asymmetry: {asym}",
            f"Excess: {exc}",
        ]
        
        result_text.insert(tk.END, "\n\n".join(results))
        result_text.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please use only numbers separated by spaces or commas.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Modify graphic, making him 'step alike'
def make_step_tuple(base_tuple):
    """
    Transforms standard coordinates into two separate sets of lines for ECDF:
    solid horizontal lines and dashed vertical jumps.
    """
    idx, X, F_x, color, title, ylabel = base_tuple
    x_horiz, y_horiz = [], []
    x_vert, y_vert = [], []
    x_hollow, y_hollow = [], []
    offset = (X[-1] - X[0]) * 0.1 if len(X) > 1 else 1.0
    x_horiz.extend([X[0] - offset, X[0], float('nan')])
    y_horiz.extend([0, 0, float('nan')])
    prev_f_x = 0
    for i in range(len(X)):
        current_x = X[i]
        current_f_x = F_x[i]
        x_hollow.append(current_x)
        y_hollow.append(prev_f_x)
        x_vert.extend([current_x, current_x, float('nan')])
        y_vert.extend([prev_f_x, current_f_x, float('nan')])
        next_x = X[i+1] if i < len(X) - 1 else X[-1] + offset
        x_horiz.extend([current_x, next_x, float('nan')])
        y_horiz.extend([current_f_x, current_f_x, float('nan')])
        prev_f_x = current_f_x
    return (idx, (x_horiz, x_vert, x_hollow), (y_horiz, y_vert, y_hollow), color, title, ylabel)

def plot_polygons():
    raw_data = entry_series.get()
    try:
        clean_data = raw_data.replace(',', ' ')
        num_series = [float(x) for x in clean_data.split()]
        
        if not num_series:
            messagebox.showwarning("Warning", "Please enter at least one number.")
            return

        # N: Total sample size
        N = len(num_series) 
        
        # X: Sorted list of unique variants
        counts = collections.Counter(num_series)
        X = sorted(counts.keys()) 
        
        # n: List of absolute frequencies
        n = [counts[x_i] for x_i in X]
        
        # p_star: List of relative frequencies
        p_star = [n_i / N for n_i in n]
        
        fig, axs = plt.subplots(2, 1, figsize=(15, 12))
        fig.canvas.manager.set_window_title('Statistical Polygons (Discrete)')
        axs = axs.flatten() 

        plot_configs = [
            (0, X, n,      'blue',   'Frequency Polygon',          'Absolute Frequency (n_i)'),
            (1, X, p_star, 'green',  'Relative Frequency Polygon', 'Relative Frequency (p_i*)'),
        ]

        for idx, x_data, y_data, color, title, ylabel in plot_configs:
            ax = axs[idx]
            ax.plot(x_data, y_data, marker='o', linestyle='-', color=color)
            ax.set_title(title)
            ax.set_xlabel('Variants (X)')
            ax.set_ylabel(ylabel)
            ax.grid(True, linestyle='--', alpha=0.5)
            
            # Exact coordinate values on axes
            ax.set_xticks(X)
            ax.set_xticklabels([str(round(x, 2)) for x in X], fontsize=8)
            y_ticks = sorted(list(set(y_data)))
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(round(y, 3)) for y in y_ticks], fontsize=8)

        plt.tight_layout(pad=3.0, h_pad=8.0)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting: {str(e)}")

def plot_curves():
    raw_data = entry_series.get()
    try:
        clean_data = raw_data.replace(',', ' ')
        num_series = [float(x) for x in clean_data.split()]
        
        if not num_series:
            messagebox.showwarning("Warning", "Please enter at least one number.")
            return

        N = len(num_series) 
        counts = collections.Counter(num_series)
        X = sorted(counts.keys()) 
        n = [counts[x_i] for x_i in X]
        m = list(accumulate(n))
        
        # F_x: Empirical distribution function
        F_x = [m_i / N for m_i in m]

        fig, axs = plt.subplots(3, 1, figsize=(15, 18))
        fig.canvas.manager.set_window_title('Statistical Curves (Discrete)')
        axs = axs.flatten() 

        plot_configs = [
            (0, X, m,   'red',    'Cumulative Frequency Curve',      'Cumulative Frequency (m_i)'),
            (1, X, F_x, 'orange', 'Cumulative Relative Freq. Curve', 'Cumulative Rel. Frequency (m_i / N)'),
            make_step_tuple((2, X, F_x, 'purple', 'Empirical Distribution Function, F*(x)', 'F*(x)'))
        ]

        for idx, x_data, y_data, color, title, ylabel in plot_configs:
            ax = axs[idx]
            
            # Specially for 3rd graph
            if idx == 2:
                x_h, x_v, x_hol = x_data
                y_h, y_v, y_hol = y_data
                
                ax.plot(x_h, y_h, linestyle='-', color=color)
                ax.plot(x_v, y_v, linestyle='--', color=color, alpha=0.5)
                ax.plot(X, F_x, 'o', color=color, alpha=0.5)
                ax.plot(x_hol, y_hol, 'o', markerfacecolor='white', markeredgecolor=color)
            else:
                ax.plot(x_data, y_data, marker='o', linestyle='-', color=color)
            
            ax.set_title(title)
            ax.set_xlabel('Variants (X)')
            ax.set_ylabel(ylabel)
            ax.grid(True, linestyle='--', alpha=0.5)
            
            # Exact coordinate values on axes
            ax.set_xticks(X)
            ax.set_xticklabels([str(round(x, 2)) for x in X], fontsize=8)
            
            if idx == 2:
                y_ticks = sorted(list(set([0] + F_x)))
            else:
                y_ticks = sorted(list(set(y_data)))
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(round(y, 3)) for y in y_ticks], fontsize=8)

        plt.tight_layout(pad=3.0, h_pad=8.0)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting: {str(e)}")

# Create main window
root = tk.Tk()
root.title("Statistical Parameters Estimator (Lab 1)")
root.geometry("600x700")
root.configure(padx=20, pady=20, bg="#f5f5f5")

# Header
tk.Label(root, text="Discrete Series Characteristics Calculation", font=("Helvetica", 16, "bold"), bg="#f5f5f5").pack(pady=(0, 20))

# Input field
tk.Label(root, text="Enter numerical values (separated by space or comma):", font=("Arial", 11), bg="#f5f5f5").pack(anchor="w")
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="X:", font=("Arial", 14), bg="#f5f5f5").pack(side=tk.LEFT, padx=(0, 5))

entry_series = tk.Entry(input_frame, font=("Arial", 14), width=50)
entry_series.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry_series.insert(0, "0.14 0.25 0.31 0.57 0.65 0.78 0.42 0.47 0.60 0.91") # Default test data (my variant from laboratory task)

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#f5f5f5")
buttons_frame.pack(pady=20)

btn_estimate = tk.Button(buttons_frame, text="Estimate", font=("Arial", 13, "bold"), bg="#4CAF50", fg="white", cursor="hand2", command=estimate_parameters)
btn_estimate.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

btn_polygons = tk.Button(buttons_frame, text="Show Polygons", font=("Arial", 13, "bold"), bg="#2196F3", fg="white", cursor="hand2", command=plot_polygons)
btn_polygons.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

btn_curves = tk.Button(buttons_frame, text="Show Curves", font=("Arial", 13, "bold"), bg="#FF9800", fg="white", cursor="hand2", command=plot_curves)
btn_curves.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

# Text area for results
tk.Label(root, text="Results:", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(anchor="w")
result_text = tk.Text(root, font=("Consolas", 12), height=20, state=tk.DISABLED, bg="#ffffff", relief=tk.GROOVE, borderwidth=2)
result_text.pack(fill=tk.BOTH, expand=True, pady=5)

root.mainloop()