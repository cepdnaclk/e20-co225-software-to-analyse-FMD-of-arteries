import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours

# Initialize a list to store points
points = []

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def draw_and_measure(image, point1, point2, color, text):
    # Draw circles at the points
    cv2.circle(image, point1, 5, color, -1)
    cv2.circle(image, point2, 5, color, -1)
    # Draw a line between the points
    cv2.line(image, point1, point2, color, 2)
    # Annotate the distance
    (mX, mY) = midpoint(point1, point2)
    cv2.putText(image, text, (int(mX), int(mY - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

def click_event(event, x, y, flags, param):
    global points, image_copy, image

    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the point
        points.append((x, y))
        # Draw a circle at the clicked point
        cv2.circle(image_copy, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Image", image_copy)

        # When two points are selected, draw the rectangle and calculate the area
        if len(points) == 2:
            cv2.rectangle(image_copy, points[0], points[1], (0, 255, 0), 2)
            cv2.imshow("Image", image_copy)
            calculate_area_and_diameter(points[0], points[1])
            points = []  # Reset the points list

def calculate_area_and_diameter(pt1, pt2):
    global image_copy, image

    x1, y1 = pt1
    x2, y2 = pt2

    # Ensure the points are ordered correctly
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))

    roi = edged[y1:y2, x1:x2]

    # Find contours in the region of interest
    cnts = cv2.findContours(roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < 100:
            continue

        # Get the minimum area bounding box and order the points
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)

        # Calculate the area of the contour
        area = cv2.contourArea(c)

        # Approximate the diameter (assuming circular cross-section)
        diameter = np.sqrt(4 * area / np.pi)

        # Print the calculated area and diameter
        print(f"Contour Area: {area:.2f} pixels")
        print(f"Approximate Diameter: {diameter:.2f} pixels")

        # Annotate the image with the diameter
        cv2.drawContours(image_copy, [box.astype("int") + [x1, y1]], -1, (0, 255, 0), 2)

        # Draw and label the diameter using the height of the bounding box
        (tl, tr, br, bl) = box
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        height = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        diameter_text = "{:.1f} pixels".format(height)

        draw_and_measure(image_copy, (int(tlblX) + x1, int(tlblY) + y1), (int(trbrX) + x1, int(trbrY) + y1), (255, 255, 255), diameter_text)

    # Show the image with annotations
    cv2.imshow("Image", image_copy)

# Load the image and preprocess it
image = cv2.imread('Photos/test.jpg')
image_copy = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# Edge detection
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# Show the image and set the mouse callback
cv2.imshow("Image", image_copy)
cv2.setMouseCallback("Image", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
