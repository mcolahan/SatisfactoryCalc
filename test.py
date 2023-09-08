import satisfactory_calc as sc

if __name__ == "__main__":
    phase2_prods = {
        "Versatile Framework":	20,
        "Automated Wiring":	5,
        "Steel Beam": 10 ,
        "Steel Pipe": 10,
        "Encased Industrial Beam": 10,
        "Motor": 10,
        "Rotor": 5,
        "Stator": 5,
        "Modular Frame": 20,
    }

    alt_recipes = [
        'Alternate: Steel Screw',
        'Alternate: Steel Rotor'
    ]

    phase2 = sc.Factory(phase2_prods, alt_recipes=alt_recipes)
    phase2.calculate()
    phase2.draw("graph.png")

