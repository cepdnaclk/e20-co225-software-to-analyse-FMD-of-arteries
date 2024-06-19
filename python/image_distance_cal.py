import cv2
import numpy as np
from scipy.spatial import distance as dist
import csv

#store the points and distances
points = []
distances = []

def click_event(event, x, y, flags, param):
    global points, distances

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)#marks the point
        cv2.imshow("Image", image) #2nd use: Update the image display with new visual elements (like circles or lines) each time a mouse event occurs.

        # Once we have 2 points, calculate the distance
        if len(points) == 2:
            pt1, pt2 = points
            d = dist.euclidean(pt1, pt2)
            distances.append(d)
            cv2.line(image, pt1, pt2, (0, 255, 0), 2) #drawing line (uses B,G,R not RGB)
            cv2.putText(image, f"{d:.2f}px", (pt1[0], pt1[1] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)#text eka line eka uda
            #(pt1[0], pt1[1] - 10) offsets the text
            cv2.imshow("Image", image)
            print(f"Distance: {d:.2f} pixels")
            points = [] #empty the array

# Function to save distances to a CSV file
def save_distances_to_csv(distances, filename='distances.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Distance (pixels)'])
        for d in distances:
            writer.writerow([d])

# Insert image here
image = cv2.imread('img3.jpg') 

cv2.imshow("Image", image)#1st use: Display the initial image and set up the window for interaction.

cv2.setMouseCallback("Image", click_event)#whenever a mouse event (like a mouse click) occurs in that window,
#the specified callback function (click_event) will be called.

# used together in OpenCV applications to ensure proper termination of the program.
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the distances to a CSV file
save_distances_to_csv(distances)

