import numpy as np
from random import randrange
import numpy.random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

'''
# Generate some test data
x = np.random.randn(8873)
y = np.random.randn(8873)

heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.show()
'''

GRID_SIZE = 50

def generateHeatmap(size, show=False):
    # Create a numpy array to store the heatmap
    heatmap = np.zeros((size, size))

    # Choose the coordinates of the hot point
    x = np.random.randint(size/4, size*3/4)
    y = np.random.randint(size/4, size*3/4)

    # Create arrays of x and y coordinates for each point in the heatmap
    x_coords, y_coords = np.meshgrid(range(size), range(size))

    # Calculate the distances between each point and the hot point
    distances = np.sqrt((x_coords - x)**2 + (y_coords - y)**2)

    # Create a smooth heat distribution around the hot point
    sigma = np.sqrt(size)
    heatmap = np.exp(-((distances**2)/(2*sigma**2)))

    # Normalize the heatmap so that the maximum value is 1
    heatmap /= np.max(heatmap)

    # Add some noise to the heatmap
    noise_std = size**0.4 / 100
    noise = np.random.normal(loc=0, scale=noise_std, size=(size, size))
    heatmap += noise

    # Clip the heatmap values to the range [0, 1]
    heatmap = np.clip(heatmap, 0, 1)

    # Map the heatmap values to RGB values using the 'hot' colormap
    cmap = mcolors.ListedColormap(plt.cm.hot(np.linspace(0, 1, 256)))
    rgba_heatmap = cmap(heatmap)

    if show:
        for x in range(0, GRID_SIZE, 8):
            for y in range(0, GRID_SIZE, 8):
                print(f"Color at ({x}, {y}): {getColor(heatmap[x][y])}")

        # Display the heatmap using matplotlib
        plt.imshow(heatmap, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.show()

        # Create a second plot to display the RGB values of the heatmap
        fig, ax = plt.subplots()
        ax.imshow(rgba_heatmap, interpolation='nearest')
        ax.set_title('RGB Values')
        plt.show()

    return heatmap

def getColor(heatValue):
    # Define the colormap and normalization function
    cmap = plt.get_cmap('hot')
    norm = mcolors.Normalize(vmin=0, vmax=1)
    
    # Convert the normalized heat value to an RGB color
    color = cmap(heatValue)
    
    # Convert the RGB color to a hex color code
    hex_color: mcolors.rgb2hex = mcolors.rgb2hex(color)
    
    return hex_color


if __name__ == "__main__":
    heatmap = generateHeatmap(GRID_SIZE, show=True)
    
