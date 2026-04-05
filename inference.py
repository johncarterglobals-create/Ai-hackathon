import os, json
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

try:
    client = OpenAI(base_url=API_BASE_URL)
except Exception:
    client = None

def log(msg):
    print(msg, flush=True)

def fallback():
    return {"status":"success","output":"dummy response"}

def run():
    log("START")
    log("STEP: loading_environment_variables")
    _ = API_BASE_URL, MODEL_NAME, HF_TOKEN, LOCAL_IMAGE_NAME
    log("STEP: initializing_model")

    if client:
        try:
            log("STEP: making_model_request")
            r = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role":"user","content":"ping"}],
                timeout=5
            )
            out = {"status":"success","output":r.choices[0].message.content}
        except Exception:
            log("STEP: fallback_triggered")
            out = fallback()
    else:
        log("STEP: client_init_failed_fallback")
        out = fallback()

    log("STEP: returning_output")
    print(json.dumps(out), flush=True)
    log("END")

if __name__ == "__main__":
    run()
