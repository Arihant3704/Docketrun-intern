import sys
import os
from run_yolo import process_video

# Constants
VIDEO_PATH = "Construction_Safety_Hazard_CCTV_Video.mp4"
MODEL_PATH = "best.pt"
CONF_THRESHOLD = 0.20

def main():
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: Video file '{VIDEO_PATH}' not found.")
        return
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file '{MODEL_PATH}' not found.")
        return

    print(f"Starting inference on {VIDEO_PATH} with model {MODEL_PATH}")

    # 1. Run with BoT-SORT (Default Tracker) - Likely the 'Stable' option
    print("\n--- Run 1: BoT-SORT (Stable/Default Tracker) ---")
    output_1 = "output_1_botsort.mp4"
    try:
        process_video(MODEL_PATH, VIDEO_PATH, output_1, tracker="botsort.yaml", conf=CONF_THRESHOLD)
        print(f"saved to {output_1}")
    except Exception as e:
        print(f"Failed to run BoT-SORT: {e}")

    # # 2. Run with ByteTrack
    # print("\n--- Run 2: ByteTrack ---")
    # output_2 = "output_2_bytetrack.mp4"
    # try:
    #     process_video(MODEL_PATH, VIDEO_PATH, output_2, tracker="bytetrack.yaml", conf=CONF_THRESHOLD)
    #     print(f"saved to {output_2}")
    # except Exception as e:
    #     print(f"Failed to run ByteTrack: {e}")

    # # 3. Run with No Tracker (Detection Only) - Baseline/Comparison
    # print("\n--- Run 3: No Tracker (Detection Only) ---")
    # output_3 = "output_3_no_tracker.mp4"
    # try:
    #     process_video(MODEL_PATH, VIDEO_PATH, output_3, tracker=None, conf=CONF_THRESHOLD)
    #     print(f"saved to {output_3}")
    # except Exception as e:
    #     print(f"Failed to run No Tracker: {e}")

    print("\nAll tasks completed.")
    print(f"Generated videos:\n1. {output_1}\n2. {output_2}\n3. {output_3}")

if __name__ == "__main__":
    main()
