import cv2
import argparse
import time
from pose_detector import PoseDetector
from gym_trainer import GymTrainer

def main():
    parser = argparse.ArgumentParser(description='AI Gym Trainer')
    parser.add_argument('--source', type=str, default='0', help='Video source: 0 for webcam or path to video file')
    parser.add_argument('--exercise', type=str, default='squat', choices=['squat', 'pushup', 'custom'], help='Exercise type: squat, pushup, or custom')
    parser.add_argument('--save', type=str, default=None, help='Path to save the output video (e.g., output.mp4)')
    parser.add_argument('--display', action='store_true', default=True, help='Display the output window (default: True)')
    parser.add_argument('--no-display', action='store_false', dest='display', help='Do not display the output window')
    parser.add_argument('--device', type=str, default=None, help='Device to run inference on (e.g., cpu, 0, 1)')
    args = parser.parse_args()

    # Initialize Detector and Trainer
    detector = PoseDetector(device=args.device)
    trainer = GymTrainer(exercise_type=args.exercise)

    # Video Capture
    source = args.source
    if source.isdigit():
        source = int(source)
    elif source.lower() == 'None':
         source = 0
    else:
        # It's a file path, execute simple checks
        import os
        if not os.path.exists(source):
            print(f"Error: File {source} not found.")
            return
        source = os.path.abspath(source)
    
    print(f"Attempting to open source: {source}")
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {source}.")
        return

    # FPS variables
    pTime = 0

    print(f"Starting {args.exercise} trainer...")
    print("Press 'q' to exit.")

    # Video Writer
    save_path = args.save
    writer = None

    while True:
        success, img = cap.read()
        if not success:
            print("Video ended or failed to read.")
            break

        # Resize for better performance/view (optional, but good for large videos)
        # img = cv2.resize(img, (1280, 720))

        # 1. Find Pose
        img = detector.find_pose(img, draw=False) # We draw manually or in find_angle

        # 2. Get Landmark Positions
        lm_list = detector.get_position(img, draw=False)

        # 3. Process if landmarks found
        if len(lm_list) != 0:
            # Calculate Angle based on exercise
            # GymTrainer knows which points to use (p1, p2, p3)
            angle = detector.find_angle(img, trainer.p1, trainer.p2, trainer.p3, lm_list)
            
            # Count Reps and Feedack
            img, count = trainer.processing(img, angle)

        # Calculate and Draw FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        # Display
        # Check if running in a headless environment or if display is requested
        if args.display:
            cv2.imshow("AI Gym Trainer", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Save Video
        if save_path:
            if writer is None:
                # Initialize writer on first frame
                height, width, _ = img.shape
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                writer = cv2.VideoWriter(save_path, fourcc, 30, (width, height))
            writer.write(img)

    cap.release()
    if writer:
        writer.release()
    if args.display:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
