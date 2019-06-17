if __name__ == "__main__":
    exit()


def line(p1, p2):
    """
    finds a coefficients of a slope that fits two given points
    :param p1: 1st point that lies on a slope
    :param p2: 2nd point that lies on a slope
    :return: coefficients of a slope
    """
    a = (p1[1] - p2[1])
    b = (p2[0] - p1[0])
    c = (p1[0]*p2[1] - p2[0]*p1[1])
    return a, b, -c


def line_to_line(l_a, l_b):
    """
    Checks for a collision between two infinite slopes
    :param l_a: 1st slope
    :param l_b: 2nd slope
    :return: Collision Point if collision occurred, False otherwise
    """
    d = l_a[0] * l_b[1] - l_a[1] * l_b[0]
    dx = l_a[2] * l_b[1] - l_a[1] * l_b[2]
    dy = l_a[0] * l_b[2] - l_a[2] * l_b[0]
    if dx == dy:
        x = dx
        y = dy
        return x, y
    elif d != 0:
        x = dx / d
        y = dy / d
        return x, y
    else:
        return None


def segments_collision(p1a, p1b, p2a, p2b):
    """
    Checks for collision between two segments
    :param p1a: 1st segment starting point
    :param p1b: 1st segment ending point
    :param p2a: 2nd segment starting point
    :param p2b: 2nd segment ending point
    :return: True if collision occurred, False otherwise
    """
    l1 = line(p1a, p1b)
    l2 = line(p2a, p2b)
    outcome = line_to_line(l1, l2)
    if outcome is None:
        return False
    else:
        x, y = outcome
        if (p1a[0] > x and p1b[0] > x) \
                or (p1a[0] < x and p1b[0] < x) \
                or (p1a[1] > y and p1b[1] > y) \
                or (p1a[1] < y and p1b[1] < y) \
                or (p2a[0] > x and p2b[0] > x) \
                or (p2a[0] < x and p2b[0] < x) \
                or (p2a[1] > y and p2b[1] > y) \
                or (p2a[1] < y and p2b[1] < y):
            return False
        else:
            return True


def polygon_to_polygon(pol_a, pol_b):
    """
    Checks collision between two polygons
    :param pol_a: 1st polygon
    :param pol_b: 2nd polygon
    :return: True if collision occurred, False otherwise
    """
    pol_a.append(pol_a[0])
    pol_b.append(pol_b[0])
    for i in range(1, len(pol_a)):
        p1a = pol_a[i - 1]
        p1b = pol_a[i]
        for j in range(1, len(pol_b)):
            p2a = pol_b[j - 1]
            p2b = pol_b[j]
            if segments_collision(p1a, p1b, p2a, p2b):
                return True
    return False


def rect_to_rect(rect_a, rect_b):
    """
    Checks if two rectangular objects are colliding:
    :param rect_a: (left,up, right,down) bounds of a rectangle
    :param rect_b: (left,up, right,down) bounds of a rectangle
    :return: True if collision occurred, False if not
    """
    return not (rect_b[0] > rect_a[2]
                or rect_b[2] < rect_a[0]
                or rect_b[1] > rect_a[3]
                or rect_b[3] < rect_a[1])


def point_to_polygon(pos, vertices, point):
    """
    Checks if a given point lies inside a polygon by splitting it into triangles
    :param pos: center point of a polygon
    :param vertices: vertices of a polygon
    :param point: point to check collision with
    :return: True if collision occurred, False otherwise
    """
    if len(vertices) == 2:
        return line_to_line(line(vertices[0], vertices[1]), line(point, point))
    elif len(vertices) == 1:
        return vertices[0] is point
    for i in range(1, len(vertices)):
        x1, y1 = pos
        x2, y2 = vertices[i - 1]
        x3, y3 = vertices[i]
        x, y = point
        area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        area_a = abs(x * (y2 - y3) + x2 * (y3 - y) + x3 * (y - y2))
        area_b = abs(x1 * (y - y3) + x * (y3 - y1) + x3 * (y1 - y))
        area_c = abs(x1 * (y2 - y) + x2 * (y - y1) + x * (y1 - y2))
        if area - 0.1 < area_a + area_b + area_c < area + 0.1:
            return True
    return False
