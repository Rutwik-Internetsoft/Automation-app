from fastapi import FastAPI, HTTPException
import subprocess
import platform
import yaml
import os
from urllib.parse import unquote
from fastapi.responses import StreamingResponse


app = FastAPI()

def execute_test(command):
    """Run a test command and return real-time logs."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")

    def stream_logs():
        for line in iter(process.stdout.readline, ''):
            yield line  # Stream each line as it's generated

        stderr_output = process.stderr.read()
        if stderr_output:
            yield f"\n❌ ERROR:\n{stderr_output}"

        process.wait()

    return StreamingResponse(stream_logs(), media_type="text/event-stream")


@app.get("/start-allure")
def start_allure():
    """Start Allure server and return the report URL."""
    try:
        subprocess.Popen(["allure", "serve", "Automation-logic/allure-results", "-p", "5052"], shell=True)
        return {"url": "http://127.0.0.1:5052/"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/get-allure-url")
def get_allure_url():
    """Return the URL of the Allure report."""
    return {"url": "http://127.0.0.1:5052/"}

@app.get("/stop-allure")
def stop_allure():
    """Stop Allure server by killing the process running on port 5052."""
    try:
        if platform.system() == "Windows":
            subprocess.run("taskkill /F /IM java.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run("pkill -f 'allure'", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"message": "✅ Allure server stopped."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/run-test")
def run_test(test_name: str = None):
    """Run a specific test case or the whole test script."""
    try:
        if test_name:
            # Run a single test using pytest -k
            command = f"pytest Automation-logic/suits/dev1/test_bugs.py -k {test_name} --alluredir=Automation-logic/allure-results"
        else:
            # Run the whole test script
            command = "pytest Automation-logic/suits/dev1/test_bugs.py --alluredir=Automation-logic/allure-results"

        subprocess.run(command, shell=True, check=True)
        return {"message": f"✅ Test '{test_name if test_name else 'ALL'}' executed!"}
    except subprocess.CalledProcessError as e:
        return {"error": f"❌ Test execution failed: {str(e)}"}

# Order Types & Payment Methods
ORDER_TYPES = {
    "phoneorder": {"name": "Phone Order", "methods": ["cash", "card"]},
    "takeoutorder": {"name": "Takeout Order", "methods": ["cash", "card"]},
    "dineinorder": {"name": "Dine-in Order", "methods": ["cash", "card"]},
    "openorder": {"name": "Open Order", "methods": ["cash", "card"]},
    "stayorder": {"name": "Stay Order", "methods": ["cash", "card"]}
}

def load_test_cases():
    yaml_file_path = "FastAPI_backend/test_cases.yaml"  # Update with actual path
    if not os.path.exists(yaml_file_path):
        raise FileNotFoundError("YAML configuration file not found!")

    with open(yaml_file_path, "r",encoding="UTF-8") as file:
        return yaml.safe_load(file)
    
test_cases = load_test_cases()

@app.get("/individual_test_case/{test_script}")
def individual_test_cases(test_script: str):
    if test_script not in test_cases:
        raise HTTPException(status_code=404, detail="Invalid order type!")
    test_case = test_cases[test_script].get("cases")
    if not test_case:
        raise HTTPException(status_code=400, detail="Test path missing in YAML!")
    return test_case

@app.get("/order-selection/{order_type}")
def get_order_selection(order_type: str):
    """Returns available payment methods for the selected order type."""
    if order_type not in ORDER_TYPES:
        raise HTTPException(status_code=404, detail="Invalid order type")

    order_data = ORDER_TYPES[order_type]
    return {"order_name": order_data["name"], "payment_methods": order_data["methods"]}

@app.get("/run-test/{test}")
def run_full_test(test: str):
    """Run the full test suite for the selected order type."""
    if test not in test_cases:
        raise HTTPException(status_code=404, detail="Invalid order type!")

    test_path = test_cases[test].get("full_test_path")
    if not test_path:
        raise HTTPException(status_code=400, detail="Test path missing in YAML!")

    return execute_test(["pytest", test_path, "-s"])

@app.get("/run-test/{full_suit_runner}/{case_function}")
def run_functional_test(full_suit_runner: str, case_function: str):
    if full_suit_runner not in test_cases:
        raise HTTPException(status_code=404, detail="Invalid order type!")

    test_path = test_cases[full_suit_runner].get("full_test_path")

    if not test_path:
        raise HTTPException(status_code=400, detail="Test path missing in YAML!")
    return execute_test(["pytest", test_path,"-k",case_function,"-s"])

@app.get("/run-test/{suit:path}")  # Allows slashes in the path
def run_suit(suit: str):
    decoded_suit = unquote(suit)  # Decode URL encoding (if any)
    print(f"Executing test suit: {decoded_suit}")  # Debugging
    return execute_test(["pytest", decoded_suit, "-s"])


