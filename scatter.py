# AI generated. I don't like working with matplotlib for realtime stuff

import matplotlib.pyplot as plt
import numpy as np

class RealtimeScatterPlot:
    """
    A class to manage and update a Matplotlib scatter plot in real time.
    The plot updates without blocking the main program execution.
    This MVP version requires the user to provide data as complex numbers,
    plotting the real part on the x-axis and the imaginary part on the y-axis.
    """
    def __init__(self, complex_data, x_range=None, y_range=None):
        """
        Initializes the scatter plot with user-provided complex data.

        Args:
            complex_data (array-like): Initial list or array of complex numbers.
            x_range (tuple, optional): A tuple (min, max) defining the x-axis limits.
                                       If None, limits are determined from the real parts of data.
            y_range (tuple, optional): A tuple (min, max) defining the y-axis limits.
                                       If None, limits are determined from the imaginary parts of data.
        """
        self.complex_data = np.array(complex_data, dtype=complex)
        self.x_data = np.real(self.complex_data)
        self.y_data = np.imag(self.complex_data)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.scatter = None # To hold the scatter plot object

        # Set axis limits based on data or provided ranges
        if x_range:
            self.ax.set_xlim(x_range[0], x_range[1])
        else:
            self.ax.set_xlim(np.min(self.x_data) - 1, np.max(self.x_data) + 1)

        if y_range:
            self.ax.set_ylim(y_range[0], y_range[1])
        else:
            self.ax.set_ylim(np.min(self.y_data) - 1, np.max(self.y_data) + 1)

        self.ax.set_title("Real-time Scatter Plot (Complex Data)")
        self.ax.set_xlabel("Real Part (X-axis)")
        self.ax.set_ylabel("Imaginary Part (Y-axis)")
        self.ax.grid(True)

        # Create the initial scatter plot
        self.scatter = self.ax.scatter(self.x_data, self.y_data, c='blue', alpha=0.7)

        # Enable interactive mode for real-time updates
        plt.ion()
        plt.show(block=False) # Show the plot without blocking

    def update_plot(self, new_complex_data, append=True):
        """
        Updates the scatter plot with new user-provided complex data.

        Args:
            new_complex_data (array-like): New list or array of complex numbers
                                           to add or replace.
            append (bool): If True, new points are appended to existing data.
                           If False, the plot is reset with only the new data.
        """
        new_complex_data = np.array(new_complex_data, dtype=complex)
        new_x = np.real(new_complex_data)
        new_y = np.imag(new_complex_data)

        if append:
            self.complex_data = np.append(self.complex_data, new_complex_data)
            self.x_data = np.append(self.x_data, new_x)
            self.y_data = np.append(self.y_data, new_y)
        else:
            self.complex_data = new_complex_data
            self.x_data = new_x
            self.y_data = new_y

        # Update the data in the scatter plot object
        self.scatter.set_offsets(np.c_[self.x_data, self.y_data])

        # Autoscale the view if data goes beyond limits (optional, uncomment if needed)
        self.ax.relim()
        self.ax.autoscale_view()

        # Redraw the canvas and process events
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events() # Process events to update the display
        #plt.pause(0.001) # Short pause to allow GUI events to be processed


    def close_plot(self):
        """Closes the plot window."""
        plt.close(self.fig)
