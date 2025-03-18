from fastapi import FastAPI
import subprocess
import platform

app = FastAPI()

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