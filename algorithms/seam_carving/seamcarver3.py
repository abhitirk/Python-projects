import skimage
from pylab import *
from skimage import filters
from skimage import img_as_float, data, io
import Image

# returns a W x H array of floats, the energy at each pixel in img.
def gradient_energy(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    # Calculating the gradients of each band independently
    R_x = skimage.filters.sobel_h(R)
    R_y = skimage.filters.sobel_v(R)
    G_x = skimage.filters.sobel_h(G)
    G_y = skimage.filters.sobel_v(G)
    B_x = skimage.filters.sobel_h(B)
    B_y = skimage.filters.sobel_v(B)
    # Adding R_x and G_x values first
    sum_RGx = np.add(np.square(R_x), np.square(G_x))
    # Adding B to the computed R_x and G_x sum to give the horizontal gradient
    gradient_x = np.add(sum_RGx, np.square(B_x))
    sum_RGy = np.add(np.square(R_y), np.square(G_y))
    # Adding B_y to the computed R_y and G_y sum to give the vertical gradient
    gradient_y = np.add(sum_RGy, np.square(B_y))
    # Sum of the horizontal and vertical gradients = Gradient energy
    gradient_energy = gradient_x + gradient_y
    return gradient_energy
    pass

# Finds an optimal seam and Computes an array of H integers, for each row return the column of the seam.
def find_seam(img):
    h, w = img.shape[:2]
    # min_energy_sum = matrix used  compute the seam by considering minimum energy sums along the image
    min_energy_sum = np.zeros(shape=(h, w), dtype=float)
    # The path matrix stores the directions to be followed along each pixel to make the seam
    path = [[None for x in range(w)]for x in range(h)]
    grad = gradient_energy(img)
    np.copyto(min_energy_sum, grad)
    #applying dynamic programming approach to find seam
    for i in range(1, h):
        for j in range(1, w - 1):
            # Boundary condition to ensure the traversal does not go beyond the leftmost extreme of image
            if j == 1:
                if min_energy_sum[i - 1, j + 1] < min_energy_sum[i - 1, j]:
                    path[i][j] = "R" # Points to upper right pixel
                min_energy_sum[i][j] = min_energy_sum[i][j] + min(min_energy_sum[i - 1][j], min_energy_sum[i - 1][j + 1])
            # Boundary condition to ensure the traversal does not go beyond the rightmost extreme of image
            if j == w - 2:
                if min_energy_sum[i - 1, j - 1] < min_energy_sum[i - 1, j]:
                    path[i][j] = "L" # Points to upper left pixel
                min_energy_sum[i][j] = min_energy_sum[i][j] + min(min_energy_sum[i - 1][j - 1], min_energy_sum[i - 1][j])
            else:
                # To be executed if boundary condition does not apply to instance
                if min_energy_sum[i - 1, j - 1] < min_energy_sum[i - 1, j] and min_energy_sum[i - 1, j - 1] < min_energy_sum[i - 1, j + 1]:
                    path[i][j] = "L" # Points to upper left pixel
                elif min_energy_sum[i - 1, j + 1] < min_energy_sum[i - 1, j] and min_energy_sum[i - 1, j + 1] < min_energy_sum[i - 1, j - 1]:
                    path[i][j] = "R" # Points to upper right pixel
                min_energy_sum[i][j] += min(min_energy_sum[i - 1][j - 1], min_energy_sum[i - 1][j],
                                  min_energy_sum[i - 1][j + 1])

    # Finding bottom-most column value with minimum computed energy sum:

    min_energy = inf
    for i in range(1, w - 1):
        if  min_energy > min_energy_sum[h - 1][i]:
            min_energy = min_energy_sum[h - 1, i]
            column_val = i
    # This value (h-1, index) are the co-ordinates where seam starts

    # Initializing array of H indices to be returned
    seam = [None for x in range(h)]
    #  width_cursor - A temporary variable that indicates the column to be stored at row i
    width_cursor = column_val
    for i in range(h - 1, -1, -1): # Start from bottom-most row
        seam[i] = width_cursor # Column value stored at i-th row
        if path[i][width_cursor] == "L":
            # Decrement cursor by 1 when path points to left
            # Column value has to be decreased by 1 to move to the left column
            width_cursor -= 1
        elif path[i][width_cursor] == "R":
            # Increment cursor by 1 when path points to right
            # Column value has to be increased by 1 to move to the right column
            width_cursor += 1
    return seam
    pass

# Visualization of the seam
def plot_seam(img, seam):
    h, w = img.shape[:2]
    #Paint every column index at seam for every row
    for i in range(0, h):
        seam_column = seam[i]
        img[i, seam_column][0] = 255
        img[i, seam_column][1] = 255
        img[i, seam_column][2] = 0
    # Return image with seam
    return img
    pass

# Modify img in-place and returns a W-1 x H x 3 slice.
def remove_seam(img, seam):
    h, w = img.shape[:2]
    #Align every column following seam[i] by 1 step for every row
    for i in range(0, h):
        for j in range(seam[i], w - 1):
            img[i][j] = img[i][j+1]
    # Truncate the right-most extraneous column to produce a W - 1 by H image
    img = delete(img,-1,1)
    return img

def main():
    img = imread('sample3.png')
    img = img_as_float(img)
    h = img.shape[0]
    w = img.shape[1]
    z = img.shape[2]
    while True:
        n = int(raw_input("Enter the PERCENTAGE (%) of width reduction (1-99):"))
        if n > 99 or n < 1:
            print "Please enter a value between 99 and 1."
        else:
            break
    w_reduction = (n * w)/100
    print "Number of seams to be removed: %d" % w_reduction
    gradmatrix = gradient_energy(img)
    img_plot = np.zeros(shape=(h, w - (w_reduction - 1), z), dtype=float)
    for x in range(0, w_reduction):
       print "Calculating and removing seam : %d" %(x+1)
       seam = find_seam(img)
       img = plot_seam(img, seam)
       if x == w_reduction - 1:
           np.copyto(img_plot, img)
       img = remove_seam(img, seam)

    gray()
    subplot(1, 1, 1)
    imshow(img)
    title("COMPRESSED IMAGE")
    figure("SEAM AND GRADIENT")
    subplot(2, 2, 1)
    imshow(gradmatrix)
    title("DUAL GRADIENT ENERGY")
    subplot(2, 2, 2)
    imshow(img_plot)
    title("LAST SEAM REMOVED")
    show()
    imsave('Last_Seam_Plot.png', img_plot)
    imsave('image-compressed.png', img)

if __name__ == "__main__":
    main()