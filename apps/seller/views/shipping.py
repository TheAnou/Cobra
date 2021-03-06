from math import ceil as roundUp
from apps.seller.models import ShippingOption


def calculateShippingCost(weight, shipping_option, ship_to_country):
  shipping_cost = 9999
  rates = {}

  if (ship_to_country == 'US' and
      int(weight) <= 500 and
      shipping_option.name == 'Envelope'):
    rates = [
      (20, 33),
      (40, 51.5),
      (70, 59),
      (80, 66.5),
      (100, 74),
      (149, 113),
      (200, 128.6),
      (250, 151),
      (300, 197),
      (350, 219),
      (400, 159.6),
      (450, 171),
      (500, 178.5),
    ]

  elif ship_to_country == 'US': # Package shipping_option
    rates = [
      (1000, 202),
      (2000, 290),
      (3000, 376),
      (4000, 463),
      (5000, 550),
      (6000, 638),
      (7000, 726),
      (8000, 815),
      (9000, 904),
      (10000, 993),
      (11000, 1082),
      (12000, 1171),
      (13000, 1251),
      (14000, 1350),
      (15000, 1440),
      (16000, 1530),
      (17000, 1690),
      (18000, 1709),
      (19000, 1799),
      (20000, 1889),
      (21000, 1991),
      (22000, 2081),
      (23000, 2172),
      (24000, 2262),
      (25000, 2352),
      (26000, 2443),
      (27000, 2533),
      (28000, 2624),
      (29000, 2714),
      (30000, 2804),
      (31000, 3787),
      (32000, 3898),
      (33000, 4010),
      (34000, 4122),
      (35000, 4233),
      (36000, 4345),
      (37000, 4457),
      (38000, 4568),
      (39000, 4680),
      (40000, 4792),
      (41000, 4904),
      (42000, 5015),
      (43000, 5127),
      (44000, 5239),
      (45000, 5350),
      (46000, 5462),
      (47000, 5574),
      (48000, 5685),
      (49000, 5797),
      (50000, 5909),
      (51000, 6020),
      (52000, 6132),
      (53000, 6244),
      (54000, 6355),
      (55000, 6467),
      (56000, 6579),
      (57000, 6690),
      (58000, 6802),
      (59000, 6914),
      (60000, 7025),
      (61000, 7137),
      (62000, 7249),
      (63000, 7360),
      (64000, 7472),
      (65000, 7584),
      (66000, 7686),
      (67000, 7807),
      (68000, 7919),
      (69000, 8031),
      (70000, 8142),
    ]

  elif ship_to_country == 'MA': # Package shipping_option
    rates = [
      (20, 20),
      (50, 23),
      (100, 27),
      (250, 33),
      (500, 38),
      (1000, 46),
      (2000, 47),
      (3000, 48),
      (4000, 49),
      (5000, 50),
      (6000, 57),
      (7000, 58),
      (8000, 59),
      (9000, 60),
      (10000, 61),
      (11000, 69),
      (12000, 70),
      (13000, 71),
      (15000, 73),
      (16000, 80),
      (17000, 81),
      (18000, 82),
      (19000, 83),
      (20000, 84),
      (21000, 91),
      (22000, 92),
      (23000, 93),
      (24000, 94),
      (25000, 95),
      (26000, 102),
      (27000, 103),
      (28000, 104),
      (29000, 105),
      (30000, 106),
      (31000, 113),
      (32000, 114.8),
      (33000, 116.6),
      (34000, 118.4),
      (35000, 120.2),
      (36000, 122),
      (37000, 123.8),
      (38000, 125.6),
      (39000, 127.4),
      (40000, 129.2),
      (41000, 131),
      (42000, 132.8),
      (43000, 134.6),
      (44000, 136.4),
      (45000, 138.2),
      (46000, 140),
      (47000, 141.8),
      (48000, 143.6),
      (49000, 145.4),
      (50000, 147.2),
      (51000, 149),
      (52000, 150.8),
      (53000, 152.5),
      (54000, 154.4),
      (55000, 156.2),
      (56000, 158),
      (57000, 159.8),
      (58000, 161.6),
      (59000, 163.4),
      (60000, 165.2),
      (61000, 167),
      (62000, 168.8),
      (63000, 170.6),
      (64000, 172.4),
      (65000, 174.2),
      (66000, 176),
      (67000, 177.8),
      (68000, 179.6),
      (69000, 182),
      (70000, 183.2),
    ]


  for (weight_limit, cost) in rates:
    if int(weight) <= weight_limit: # and float(cost) < shipping_cost:
      shipping_cost = float(cost)
      break

  return int(roundUp(shipping_cost))
