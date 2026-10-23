import time
import json
import argparse
import urllib.request
import urllib.error
from personas import PERSONAS

def run_attack(persona_name):
    if persona_name not in PERSONAS:
        print(f"Error: Persona '{persona_name}' not found.")
        print(f"Available personas: {list(PERSONAS.keys())}")
        return

    persona = PERSONAS[persona_name]
    paths = persona["paths"]
    delay = persona["delay"]

    print(f"--- Starting attack simulation as: {persona_name} ---")
    print(f"Delay between requests: {delay} seconds\n")

    for attempt, path in enumerate(paths, start=1):
        payload = {
            "path": path,
            "method": "GET",
            "ip": "192.168.1.100",
            "attempts": attempt
        }
        
        print(f"Sending attack to: {path} (Attempt {attempt})")
        
        # Prepare the request
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            "http://127.0.0.1:8000/event", 
            data=data, 
            headers={'Content-Type': 'application/json'}
        )

        try:
            # Send the request
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                print(f"Server response: {response_data}")
        except urllib.error.URLError as e:
            print(f"[!] Failed to reach server: {e.reason}")
        except Exception as e:
            print(f"[!] An error occurred: {e}")

        # Wait before the next attack
        time.sleep(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Honeypot Attacker Simulator")
    parser.add_argument("--persona", required=True, help="Choose: 'Script Kiddie', 'Stealthy', or 'APTx'")
    args = parser.parse_args()
    
    run_attack(args.persona)