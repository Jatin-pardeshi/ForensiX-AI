import os
import cv2
import numpy as np
from forensics.image_engine import AdvancedImageForensics

class AdvancedVideoForensics:
    @staticmethod
    def analyze_video_stream(video_path, output_dir, sample_rate=15):
        """
        Deconstructs a video file frame-by-frame, applies spatial deep-learning models 
        at targeted intervals, and computes a continuous temporal authenticity score.
        """
        if not os.path.exists(video_path):
            return {"status": "Error", "message": "Source video file not found."}

        # 1. Open the video container via OpenCV
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {"status": "Error", "message": "Failed to open video container stream."}

        # 2. Extract structural video metadata
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration_seconds = total_frames / fps if fps > 0 else 0

        frame_timeline = []
        sampled_scores = []
        suspicious_frames_saved = []
        
        frame_idx = 0
        analyzed_count = 0

        # 3. Step through the frame sequencing array
        while True:
            # ---> THE FIX: Changed cap.get() to cap.read() <---
            ret, frame = cap.read() 
            if not ret:
                break # Reached terminal frame pointer

            # Sample frames based on chosen rate to preserve CPU resource limits
            if frame_idx % sample_rate == 0:
                analyzed_count += 1
                timestamp = float(frame_idx) / fps if fps > 0 else 0.0

                # Save the isolated frame temporarily to disk to run through the image pipeline
                temp_frame_path = os.path.join(output_dir, f"tmp_frame_{frame_idx}.jpg")
                cv2.imwrite(temp_frame_path, frame)

                # Execute spatial model inference on the static frame
                neural_metrics = AdvancedImageForensics.run_deep_neural_pipeline(temp_frame_path)
                ai_prob = neural_metrics["vit_artifact_prob"]
                sampled_scores.append(ai_prob)

                # Log specific timeline telemetry
                frame_data = {
                    "frame_index": frame_idx,
                    "timestamp_sec": round(timestamp, 2),
                    "ai_probability": ai_prob
                }
                frame_timeline.append(frame_data)

                # If a frame exhibits critically high manipulation signatures, archive it as evidence
                if ai_prob > 0.70 and len(suspicious_frames_saved) < 5:
                    archived_filename = f"flagged_frame_case_{frame_idx}.jpg"
                    archived_path = os.path.join(output_dir, archived_filename)
                    cv2.imwrite(archived_path, frame)
                    suspicious_frames_saved.append(archived_filename)

                # Clean up the volatile temporary scratch file
                if os.path.exists(temp_frame_path):
                    os.remove(temp_frame_path)

            frame_idx += 1

        cap.release()

        # 4. Formulate overall compound statistical aggregations
        if len(sampled_scores) > 0:
            aggregate_ai_probability = float(np.mean(sampled_scores))
            max_peak_anomaly = float(np.max(sampled_scores))
        else:
            aggregate_ai_probability = 0.0
            max_peak_anomaly = 0.0

        aggregate_authenticity_score = 1.0 - aggregate_ai_probability

        return {
            "status": "Success",
            "metadata": {
                "total_frames": total_frames,
                "fps": round(fps, 2),
                "duration_seconds": round(duration_seconds, 2)
            },
            "aggregate_ai_probability": aggregate_ai_probability,
            "aggregate_authenticity_score": aggregate_authenticity_score,
            "max_peak_anomaly": max_peak_anomaly,
            "flagged_keyframes": suspicious_frames_saved,
            "timeline_telemetry": frame_timeline
        }