# Created by matveyev at 15.02.2021

from PyQt5 import QtCore

PLOT_COLORS = [(255, 0, 0),
               (255, 170, 0),
               (255, 85, 0),
               (170, 0, 0),
               (85, 170, 127),
               (0, 170, 0),
               (85, 170, 255),
               (85, 0, 255),
               (0, 0, 127),
               (82, 190, 128),
               (229, 152, 102),
               (116, 176, 255),
               (0, 85, 127),
               (85, 85, 127),
               (187, 143, 206),
               (244, 208, 63),
               (70, 70, 70),
               (170, 85, 255),
               (170, 0, 0),
               (0, 85, 0)]


CROSSHAIR_CURSOR = {"line_style": {"color": (20, 144, 255),
                                   "style": QtCore.Qt.DotLine},
                    "text_style": {"color": (255, 255, 255),
                                   "fill": (30, 144, 255, 170),
                                   "font": ("Arial", 14)},}
DISTANCE_MEASUREMENT = {"vertical_line": {"color": (30, 144, 255),
                                          "style": QtCore.Qt.DashLine},
                        "horizontal_line": {"color": (30, 144, 255),
                                            "style": QtCore.Qt.SolidLine},
                        "text_style": {"color": (255, 255, 255),
                                       "font": ("Arial", 12),
                                       "fill": (30, 144, 255, 170)},
                        "arrow_style": {"tipAngle": 45, "baseAngle": 10, "headLen": 10,
                                        "tailLen": None, "pen": (30, 144, 255), "brush": (30, 144, 255)}}

FIT_STYLES = [{"color": "#ee2222", "style": QtCore.Qt.DashLine},
              {"color": "#22ee22", "style": QtCore.Qt.DashLine},
              {"color": "#2222ee", "style": QtCore.Qt.DashLine},
             ]