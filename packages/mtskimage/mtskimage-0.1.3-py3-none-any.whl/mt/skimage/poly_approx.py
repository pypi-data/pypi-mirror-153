'''Approximates a polygon with an axis-aligned rectangle.'''


from mt.geo2d.rect import Rect
import numpy as _np
import scipy.ndimage as _sn
import skimage.transform.integral as _sti
import skimage.draw as _sd
import scipy.spatial as _ss


__all__ = ['poly2rect']


def tl_int(img, x, y):
    if x < 0 or y < 0:
        return 0
    x = int(x)
    y = int(y)
    if y >= img.shape[0]: # height
        y = img.shape[0]-1
    if x >= img.shape[1]: # width
        x = img.shape[1]-1
    return img[y,x]

def rect_sum(img, r):
    return tl_int(img, r.max_x, r.max_y) + tl_int(img, r.min_x-1, r.min_y-1) - tl_int(img, r.max_x, r.min_y-1) - tl_int(img, r.min_x-1, r.max_y)

def rect_perimeter(img, r):
    return (rect_sum(img, r) - rect_sum(img, Rect(min_x=r.min_x+1, min_y=r.min_y+1, max_x=r.max_x-1, max_y=r.max_y-1))) / ((r.max_x + r.max_y - r.min_x - r.min_y)*2)


def poly2rect(poly):
    '''Approximates a polygon with an axis-aligned rectangle by minimising the mean of point-to-polygon distances of all points on the rectangle.

    Parameters
    ----------
        poly : numpy.array
            a list of 2D points forming a single polygon

    Returns
    -------
        rect : mt.geo.rect.Rect
            a 2D rectangle with integer coordinates

    '''
    if len(poly.shape) != 2 or poly.shape[1] != 2:
        raise ValueError("Only accepting a numpy array of shape (:,2) as a polygon. Receiving shape {}".format(poly.shape))

    # preparation
    poly = poly.astype(_np.int32) # make the coordinates integer
    N = poly.shape[0]
    tl = poly.min(axis=0)
    br = poly.max(axis=0)

    # special cases
    if N == 0:
        return Rect()
    if N <= 2 or tl[0] >= br[0] or tl[1] >= br[1]:
        return Rect(min_x=tl[0], min_y=tl[1], max_x=br[0], max_y=br[1])

    # convexify if necessary
    if N > 3:
        poly = poly[_ss.ConvexHull(poly).vertices]
        N = poly.shape[0]
        tl = poly.min(axis=0)
        br = poly.max(axis=0)

    # draw polygon perimeter
    w, h = (br-tl)+1
    poly -= tl # to make poly non-negative coordinates
    buf = _np.ones((h, w), dtype=_np.uint8)
    rr, cc = _sd.polygon_perimeter(poly[:,1], poly[:,0], shape=buf.shape, clip=True)
    buf[rr,cc] = 0

    # compute distance transform
    edt = _sn.distance_transform_edt(buf)

    # compute the integral image
    img = _sti.integral_image(edt)

    # optimise
    r0 = Rect(min_x=0, min_y=0, max_x=w-1, max_y=h-1)
    loss0 = rect_perimeter(img, r0)
    dirty = True
    while dirty:
        dirty = False

        # top
        if r0.min_y+1 < r0.max_y:
            r = Rect(min_x=r0.min_x, min_y=r0.min_y+1, max_x=r0.max_x, max_y=r0.max_y)
            loss = rect_perimeter(img, r)
            if loss < loss0:
                r0 = r
                loss0 = loss
                dirty = True

        # left
        if r0.min_x+1 < r0.max_x:
            r = Rect(min_x=r0.min_x+1, min_y=r0.min_y, max_x=r0.max_x, max_y=r0.max_y)
            loss = rect_perimeter(img, r)
            if loss < loss0:
                r0 = r
                loss0 = loss
                dirty = True

        # bottom
        if r0.min_y+1 < r0.max_y:
            r = Rect(min_x=r0.min_x, min_y=r0.min_y, max_x=r0.max_x, max_y=r0.max_y-1)
            loss = rect_perimeter(img, r)
            if loss < loss0:
                r0 = r
                loss0 = loss
                dirty = True

        # right
        if r0.min_x+1 < r0.max_x:
            r = Rect(min_x=r0.min_x, min_y=r0.min_y, max_x=r0.max_x-1, max_y=r0.max_y)
            loss = rect_perimeter(img, r)
            if loss < loss0:
                r0 = r
                loss0 = loss
                dirty = True

    return Rect(min_x=r0.min_x+tl[0], min_y=r0.min_y+tl[1], max_x=r0.max_x+tl[0], max_y=r0.max_y+tl[1])
