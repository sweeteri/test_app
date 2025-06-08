from shapely.geometry import Point, Polygon

stock_polygon = Polygon([(30, 10), (40, 40), (20, 40), (10, 20), (30, 10)])

def is_inside_stock(x, y):
    point = Point(x, y)
    return stock_polygon.contains(point) or stock_polygon.touches(point)
