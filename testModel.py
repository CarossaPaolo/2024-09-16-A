from model.modello import Model

model = Model()
model.buildGraph(37, -87, "disk")
print(model.getInfoGraph())

bestPath, bestPathVal = model.buildPath()
print(f"best valore: {bestPathVal}")
for n in bestPath:
    print(f"{n.Name} (density: {n.getDesita():.4f})")
