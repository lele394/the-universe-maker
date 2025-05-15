import framework as fr

# print(fr.Star(10, "O"))
# print(fr.Star(10, "B"))
# print(fr.Star(10, "A"))
# print(fr.Star(10, "F"))
# print(fr.Star(10, "G"))
# print(fr.Star(10, "K"))
# print(fr.Star(1, "M"))

# fr.Planet(2, 1, planet_type="Gas")

# ss = fr.StarSystem(1, name="HIP-2234")
# ss.generate(7)
# # print(ss)
# ss.display()

# try:
#     obj = ss.get_object(input("\n> "))
#     print(obj)

# except ValueError:
#     pass




















# action = "load"

# if action == "create":
#     universe = fr.Universe()
#     universe.generate(200, 1.0)
#     universe.info()
#     ss2 = universe.systems[next(iter(universe.systems))]
#     ss2.display()
#     p2 = ss2.get_object(ss2.name+"-I")

#     # Save
#     import pickle
#     with open("universe.pkl", "wb") as f:
#         pickle.dump(universe, f)





# elif action == "load":
#     import pickle
#     with open("universe.pkl", "rb") as f:
#         universe2 = pickle.load(f)
#         universe2.info()
#     ss2 = universe2.systems[next(iter(universe2.systems))]
#     ss2.display()
    # p2 = ss2.get_object(ss2.name+"-I")








# keys_list = list(universe.systems.keys())

# ss = universe.systems[keys_list[0]]
# ss.display()
# p = ss.get_object(ss.name+"-I")
# print(p)
# universe.systems[keys_list[1]].display()
# universe.systems[keys_list[-1]].display()



# import sys
# # size = sys.getsizeof(universe)
# # print(f"In-memory size: {size} bytes")







# # with open("universe.pkl", "wb") as f:
# #     pickle.dump(universe, f)

# print()
# print()
# print()
# print()
# print()
# print()

# with open("universe.pkl", "rb") as f:
#     universe2 = pickle.load(f)

# universe2.info()
# # size = sys.getsizeof(universe2)
# # print(f"In-memory size: {size} bytes")



# ss2 = universe2.systems[next(iter(universe2.systems))]
# ss2.display()
# p2 = ss2.get_object(ss2.name+"-I")
# print(p2)















universe = fr.Universe()
universe.generate(3, 1.0)
universe.info()

keys_list = list(universe.systems.keys())
ss1 = universe.systems[keys_list[0]]
ss2 = universe.systems[keys_list[1]]
print()
print()
print()
ss1.display()
# ss2.display()
print()
print()
print()

p1 = ss1.get_object(ss1.name+"-I")
p2 = ss2.get_object(ss2.name+"-I")

ship_stats = {
    "name": "SOME SHIP",
    "type": "frigate",
}

ship = fr.Ship(5, ship_stats, p1)
ss1.display()
ss2.display()
print()

ship.move(p2)

print()
print()
print()
print()
print()



ss1.display()
ss2.display()
