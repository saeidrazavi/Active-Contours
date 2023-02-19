import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import filters
import os
import moviepy.video.io.ImageSequenceClip
import sys
from skimage.filters import threshold_yen

# -------------------------


def plots(x, y, img, n):

    image3 = np.copy(img)

    color = (0, 255, 0)
    for i in range(0, n):
        if(i != 99):
            start_point = (int(y[i]), int(x[i]))
            end_point = (int(y[i+1]), int(x[i+1]))
        if(i == 99):
            start_point = (int(y[99]), int(x[99]))
            end_point = (int(y[0]), int(x[0]))

        image3 = cv2.line(image3, start_point, end_point, color, 3)

    color = (255, 0, 0)

    for i in range(0, n):
        center_coordinates = (int(y[i]), int(x[i]))
        image3 = cv2.circle(
            image3, center_coordinates, 2, color, 2)

    image3 = cv2.cvtColor(image3, cv2.COLOR_RGB2BGR)
    return image3

# ----------------------------


def decoder(num):
    x_m = 0
    y_m = 0
    if(num == 0):
        x_m = -1
        y_m = -1
    if(num == 1):
        x_m = -1
        y_m = 0
    if(num == 2):
        x_m = -1
        y_m = 1
    if(num == 3):
        x_m = 0
        y_m = -1
    if(num == 4):
        x_m = 0
        y_m = 0
    if(num == 5):
        x_m = 0
        y_m = 1
    if(num == 6):
        x_m = 1
        y_m = -1
    if(num == 7):
        x_m = 1
        y_m = 0
    if(num == 8):
        x_m = 1
        y_m = 1
    return x_m, y_m
# ----------------------------


def gradian(matrix):

    grad = cv2.Canny(matrix, 100, 200)
    grad = filters.gaussian(grad, 9)
    thresh_min = threshold_yen(grad)
    condition = (grad > thresh_min)
    grad *= condition
    grad /= np.max(grad)

    return -grad


# ------------------


def find_best_iteration(gradian_min, x_cor, y_cor, img: np.ndarray, cost_matrix):

    index_x_matrix = np.zeros([100, 9])
    index_y_matrix = np.zeros([100, 9])
    number_matrix = np.ones([100, 9])*4

    cost_matrix_copy = np.copy(cost_matrix[0, :])

    cost_matrix[0, :] = 0

    x_roll = np.roll(x_cor, 1)
    y_roll = np.roll(y_cor, 1)

    d = np.mean(np.sqrt(((x_cor-x_roll)**2+(y_cor-y_roll)**2)))
    x_center = np.mean(x_cor)
    y_center = np.mean(y_cor)
    l = np.mean(np.sqrt(((x_cor-x_center)**2+(y_cor-y_center)**2)))

    number_of_centers = 100
    for g in range(1, number_of_centers):
        x_instant = x_cor[g]
        y_instant = y_cor[g]

        for gg in range(0, 9):

            x_m1, y_m1 = decoder(gg)

            for ggg in range(0, 9):

                x_m2, y_m2 = decoder(ggg)
                ex_temp = \
                    (gradian_min[int(x_instant+x_m1), int(y_instant+y_m1)])
                inter_temp1 = (
                    ((x_instant+x_m1-(x_cor[g-1]+x_m2))**2+(y_instant+y_m1-(y_cor[g-1]+y_m2))**2)-d)**2

                inter_temp2 = (
                    ((x_instant+x_m1-(x_center))**2+(y_instant+y_m1-(y_center))**2)-1/2*l)**2

                inter_temp2 *= 2/((np.exp(20*(-ex_temp)))+1)

                total = 10**(-5)*inter_temp1+10**(-6)*inter_temp2 + \
                    10*ex_temp+cost_matrix[g-1, ggg]
                if total < cost_matrix[g, gg]:
                    cost_matrix[g, gg] = total
                    number_matrix[g, gg] = ggg
                    index_x_matrix[g, gg] = x_m2
                    index_y_matrix[g, gg] = y_m2

    # make it closed loop

    x_instant = x_cor[0]
    y_instant = y_cor[0]
    cost_matrix[0, :] = cost_matrix_copy

    c = 0
    for gg in range(0, 9):
        x_m1, y_m1 = decoder(gg)

        for ggg in range(0, 9):

            x_m2, y_m2 = decoder(ggg)
            ex_temp = \
                (gradian_min[int(x_instant+x_m1), int(y_instant+y_m1)])
            inter_temp1 = (
                ((x_instant+x_m1-(x_cor[99]+x_m2))**2+(y_instant+y_m1-(y_cor[99]+y_m2))**2)-d)**2

            inter_temp2 = (
                ((x_instant+x_m1-(x_center))**2+(y_instant+y_m1-(y_center))**2)-1/2*l)**2

            inter_temp2 *= 2/((np.exp(20*(-ex_temp)))+1)

            total = 10**(-5)*inter_temp1+10**(-6)*inter_temp2 + \
                10*ex_temp+cost_matrix[99, ggg]

            if total <= cost_matrix[0, gg]:
                c += 1
                cost_matrix[0, gg] = total
                index_x_matrix[0, gg] = x_m2
                index_y_matrix[0, gg] = y_m2
                number_matrix[0, gg] = ggg
    if(c >= 1):
        indice = np.where(cost_matrix[0, :] == min(cost_matrix[0, :]))[0][0]
    elif(c == 0):
        indice = 4
    x_m, y_m = decoder(indice)
    number = number_matrix[0, indice]

    x_cor[0] = x_m+x_cor[0]
    y_cor[0] = y_m+y_cor[0]

    for m in range(99, 0, -1):
        if(m == 99):
            x_m, y_m = decoder(number)
            x_cor[m] = x_m+x_cor[m]
            y_cor[m] = y_m+y_cor[m]
            number = number_matrix[int(m), int(number)]

        else:

            x_m, y_m = decoder(number)
            x_cor[int(m)] = x_m+x_cor[int(m)]
            y_cor[int(m)] = y_m+y_cor[int(m)]
            number = number_matrix[int(m), int(number)]

    return x_cor, y_cor, cost_matrix


# -------------------------------
# read image
image = cv2.imread('tasbih.jpg')
image = np.array(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
img = np.copy(image)
plt.imshow(img)


# getting boarders of contour (should be distribute uniformly)
plt.title('choose 6-15 points "all around " the tasbih .\n please choose it all around the object(not just one side)!\nafter choose press ENTER')
points = plt.ginput(0, 0)
plt.close()
points = np.uint(np.array((points)))
x_cor = np.array(points[:, 1])
y_cor = np.array(points[:, 0])


# -------------

x_center = np.mean(x_cor)  # center of circle (x)
y_center = np.mean(y_cor)  # center of circle (y)

# ------------

y_max = max(abs(y_cor-y_center))  # radius in y axis
x_max = max(abs(x_cor-x_center))  # radius in x axis


deg = np.linspace(0, 2 * np.pi, 100)  # to select vertices unifromly
x_new_cent = x_center + x_max * np.sin(deg)
y_new_cent = y_center + y_max * np.cos(deg)

first_image = plots(x_new_cent, y_new_cent, img, 100)
first_image = cv2.cvtColor(first_image, cv2.COLOR_BGR2RGB)
plt.imshow(first_image)
plt.title('close the window to continue the proccess')
plt.show()

gradian_minus = gradian(img)

# Create directory for frames to save
# -------------------------
dirName = 'pic'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory ", dirName,  " Created ")
except FileExistsError:
    print("Directory ", dirName,  " already exists")


file = sys.argv[0]
dirname = os.path.dirname(file)
dirname = dirname + '/' + 'pic'
path = dirname

# ---------------------------------

for f in range(0, 400):

    if(f == 0):
        cost = np.ones([100, 9])*np.inf
    x, y, cost = find_best_iteration(
        gradian_minus, x_new_cent, y_new_cent, image, cost)

    frame = plots(x, y, img, 100)

    cv2.imwrite(os.path.join(path, f'{f}.png'), frame)


image_folder = dirname
fps = 3
image_files = []

# make gif
for i in range(0, 400, 5):
    image_files.append(image_folder + '/' + str(i) + ".png")
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(
    image_files, fps=fps)
clip.write_videofile('contour.mp4')

frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
plt.imsave('res11.jpg', frame)
plt.imshow(frame)
plt.title('final_image')
plt.show()
