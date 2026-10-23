PERSONAS = {
    "Script Kiddie": {"paths": ["/admin", "/login"], "delay": 1},
    "Stealthy": {"paths": ["/robots.txt", "/env"], "delay": 5},
    "APTx": {"paths": ["/config"], "delay": 3},
}
if __name__ == "__main__":
    for name, data in PERSONAS.items():
        print(f"{name} attacks {data['paths']} with {data['delay']}s delay")