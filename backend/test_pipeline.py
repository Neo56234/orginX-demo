import httpx
import time
import json

def run_test():
    API_URL = "http://localhost:8000/api/analyze"
    # Using a short YouTube test video
    VIDEO_URL = "https://www.youtube.com/watch?v=jNQXAC9IVRw" # "Me at the zoo" - 19 seconds
    CONTEXT = "This video shows an elephant in the Bangladesh national zoo in 2024."

    print(f"Submitting investigation for: {VIDEO_URL}")
    print(f"Claimed context: {CONTEXT}")
    
    try:
        resp = httpx.post(API_URL, json={"video_url": VIDEO_URL, "claimed_context": CONTEXT})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Failed to submit request:", e)
        return

    inv_id = data["investigation_id"]
    print(f"\nInvestigation queued! ID: {inv_id}")
    print("Polling for results (this may take 1-2 minutes)...\n")

    while True:
        try:
            status_resp = httpx.get(f"http://localhost:8000/api/investigation/{inv_id}")
            status_data = status_resp.json()
            status = status_data.get("status")
            
            print(f"Current status: {status}")
            
            if status == "complete":
                print("\n✅ Investigation Complete!")
                print("Verdict:", status_data.get("verdict"))
                print("Confidence:", status_data.get("confidence"))
                print("Summary (BN):", status_data.get("summary_bn"))
                print("Actual Origin:", status_data.get("actual_origin_country"))
                break
            elif status == "failed":
                print("\n❌ Investigation Failed!")
                break
                
            time.sleep(5)
        except Exception as e:
            print("Error polling status:", e)
            time.sleep(5)

if __name__ == "__main__":
    run_test()
