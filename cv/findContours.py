import numpy as np


HOLE_BORDER = 1
OUTER_BORDER = 2


class Border:
    def __init__(self, seq_num, border_type):
        self.border_type = border_type
        self.seq_num = seq_num


class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    @property
    def coordinates(self):
        return [[self.col, self.row]]

    def setPoint(self, row, col):
        self.row = row
        self.col = col

    def stepCW(self, pivot):
        # clockwise step
        if self.col > pivot.col:
            self.setPoint(pivot.row + 1, pivot.col)
        elif self.col < pivot.col:
            self.setPoint(pivot.row - 1, pivot.col)
        elif self.row > pivot.row:
            self.setPoint(pivot.row, pivot.col - 1)
        elif self.row < pivot.row:
            self.setPoint(pivot.row, pivot.col + 1)

    def stepCCW(self, pivot):
        # counterclockwise step
        if self.col > pivot.col:
            self.setPoint(pivot.row - 1, pivot.col)
        elif self.col < pivot.col:
            self.setPoint(pivot.row + 1, pivot.col)
        elif self.row > pivot.row:
            self.setPoint(pivot.row, pivot.col + 1)
        elif self.row < pivot.row:
            self.setPoint(pivot.row, pivot.col - 1)

    def samePoint(self, p):
        return self.row == p.row and self.col == p.col

    def copy(self):
        return Point(self.row, self.col)


class Node:
    def __init__(self, parent, first_child, next_sibling, border):
        self.parent = parent
        self.first_child = first_child
        self.next_sibling = next_sibling
        self.border = border

    def reset(self):
        self.parent = -1
        self.first_child = -1
        self.next_sibling = -1


class Checked:
    def __init__(self, checked=[False] * 4):
        self._checked = checked

    def stepCCW(self, point, center):
        if point.col > center.col:
            loc = 0
        elif point.col < center.col:
            loc = 2
        elif point.row > center.row:
            loc = 1
        elif point.row < center.row:
            loc = 3
        else:
            raise Exception("Error: markExamined Failed")
        self._checked[loc] = True

    def setLocChecked(self, loc):
        self._checked[loc] = True

    def isExamined(self):
        return self._checked[0]


def isPixelOutOfBounds(point, numrows, numcols):
    return (
        point.col >= numcols or point.row >= numrows or point.col < 0 or point.row < 0
    )


def followBorder(image, row, col, p2, NBD, contours):
    numrows = len(image)
    numcols = len(image[0])
    current = Point(p2.row, p2.col)
    start = Point(row, col)
    point_storage = []

    while True:
        current.stepCW(start)
        if current.samePoint(p2):
            image[start.row][start.col] = -NBD.seq_num
            point_storage.append(start.coordinates)
            contours.append(point_storage)
            return image, contours
        if (
            not isPixelOutOfBounds(current, numrows, numcols)
            and image[current.row][current.col]
        ):
            break

    p1 = current
    p3 = start
    p2 = p1

    while True:
        current = p2.copy()
        checked = Checked()

        while True:
            checked.stepCCW(current, p3)
            current.stepCCW(p3)
            if (
                not isPixelOutOfBounds(current, numrows, numcols)
                and image[current.row][current.col]
            ):
                break

        p4 = current

        if (
            p3.col + 1 >= numcols or image[p3.row][p3.col + 1] == 0
        ) and checked.isExamined():
            image[p3.row][p3.col] = -NBD.seq_num
        elif p3.col + 1 < numcols and image[p3.row][p3.col] == 1:
            image[p3.row][p3.col] = NBD.seq_num

        point_storage.append(p3.coordinates)

        if p4.samePoint(start) and p3.samePoint(p1):
            contours.append(point_storage)
            return image, contours

        p2 = p3
        p3 = p4


def findContours(image):
    image = np.array(image, dtype="int16")
    image[image > 0] = 1

    numrows = len(image)
    numcols = len(image[0])
    LNBD = Border(1, HOLE_BORDER)
    NBD = Border(1, HOLE_BORDER)
    contours = []
    hierarchy = []
    temp_node = Node(-1, -1, -1, NBD)
    hierarchy.append(temp_node)
    p2 = Point(0, 0)
    is_border_start = False

    r = 0
    while r < numrows:
        LNBD.seq_num = 1
        LNBD.border_type = HOLE_BORDER

        c = 0
        while c < numcols:
            is_border_start = False
            if (image[r][c] == 1 and c - 1 < 0) or (
                image[r][c] == 1 and image[r][c - 1] == 0
            ):
                NBD.border_type = OUTER_BORDER
                NBD.seq_num += 1
                p2.setPoint(r, c - 1)
                is_border_start = True

            elif c + 1 < numcols and (image[r][c] >= 1 and image[r][c + 1] == 0):
                NBD.border_type = HOLE_BORDER
                NBD.seq_num += 1
                if image[r][c] > 1:
                    LNBD.seq_num = image[r][c]
                    LNBD.border_type = hierarchy[LNBD.seq_num - 1].border.border_type
                p2.setPoint(r, c + 1)
                is_border_start = True

            if is_border_start:
                temp_node.reset()
                if NBD.border_type == LNBD.border_type:
                    temp_node.parent = hierarchy[LNBD.seq_num - 1].parent
                    temp_node.next_sibling = hierarchy[temp_node.parent - 1].first_child
                    hierarchy[temp_node.parent - 1].first_child = NBD.seq_num
                    temp_node.border = NBD
                    hierarchy.append(temp_node)

                else:
                    if hierarchy[LNBD.seq_num - 1].first_child != -1:
                        temp_node.next_sibling = hierarchy[LNBD.seq_num - 1].first_child

                    temp_node.parent = LNBD.seq_num
                    hierarchy[LNBD.seq_num - 1].first_child = NBD.seq_num
                    temp_node.border = NBD
                    hierarchy.append(temp_node)

                image, contours = followBorder(image, r, c, p2, NBD, contours)

            if abs(image[r][c]) > 1:
                LNBD.seq_num = abs(image[r][c])
                LNBD.border_type = hierarchy[LNBD.seq_num - 1].border.border_type

            c += 1
        r += 1

    return contours, hierarchy


def printHierarchy(hierarchy):
    for i in range(len(hierarchy)):
        print(
            i + 1,
            ":: parent: ",
            hierarchy[i].parent,
            " first child: ",
            hierarchy[i].first_child,
            " next sibling: ",
            hierarchy[i].next_sibling,
        )


def printContours(contours):
    for i in range(len(contours)):
        for j in range(len(contours[i])):
            print((contours[i][j].row, contours[i][j].col), end=" ")
        print()
