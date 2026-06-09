import os
import hashlib
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

# Database Models
from models import db, Evidence, ChainOfCustody
from config import Config

# AI & Forensic Engines
from forensics.image_engine import AdvancedImageForensics
from forensics.video_engine import AdvancedVideoForensics
from forensics.audio_engine import AdvancedAudioForensics
from forensics.threat_engine import ThreatIntelligenceEngine

# Initialize Blueprint
analysis_blueprint = Blueprint('analysis', __name__)

# Supported File Matrices
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
AUDIO_EXTENSIONS = {'.wav', '.mp3', '.flac', '.ogg'}

def generate_file_hashes(file_path):
    """
    Safely calculates MD5, SHA1, and SHA256 hashes for an uploaded file
    using binary chunking to prevent RAM overload on massive files.
    """
    md5_hash = hashlib.md5()
    sha1_hash = hashlib.sha1()
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
            sha1_hash.update(byte_block)
            sha256_hash.update(byte_block)
    return {
        "md5": md5_hash.hexdigest(), 
        "sha1": sha1_hash.hexdigest(), 
        "sha256": sha256_hash.hexdigest()
    }

@analysis_blueprint.route('/upload', methods=['POST'])
def process_forensic_payload():
    # 1. Validate Initial Request Parameters
    if 'file' not in request.files or 'case_id' not in request.form:
        return jsonify({"status": "error", "message": "Missing diagnostic arguments"}), 400

    # Grab the array of files for batch processing
    uploaded_files = request.files.getlist('file')
    case_id = request.form['case_id']
    operator = request.form.get('operator', 'SOC_Analyst_Node')

    if not uploaded_files or uploaded_files[0].filename == '':
        return jsonify({"status": "error", "message": "Void file string submitted"}), 400

    # Ensure evidence storage directory exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    batch_results = []

    # 2. Execute Batch Processing Queue
    for target_file in uploaded_files:
        safe_name = secure_filename(target_file.filename)
        execution_path = os.path.join(Config.UPLOAD_FOLDER, safe_name)
        
        # Save physical file to secure container
        target_file.save(execution_path)

        # 3. Generate Cryptographic Fingerprints
        try:
            hashes = generate_file_hashes(execution_path)
        except Exception as e:
            batch_results.append({"filename": safe_name, "status": "error", "message": f"Hash failure: {str(e)}"})
            continue
            
        # 4. Execute Global Threat Intelligence Lookup
        threat_report = ThreatIntelligenceEngine.check_virustotal(hashes["sha256"], Config.VT_API_KEY)
        
        _, ext = os.path.splitext(safe_name.lower())
        file_type = "Unknown"
        authenticity_score = 1.0
        ai_prob = 0.0
        telemetry_metadata = {}

        # ==========================================
        # 5. MULTI-MODAL AI ROUTING MATRIX
        # ==========================================

        if ext in IMAGE_EXTENSIONS:
            file_type = "Image"
            ela_metrics = AdvancedImageForensics.calculate_error_level_analysis(execution_path, Config.UPLOAD_FOLDER)
            empirical_entropy = AdvancedImageForensics.calculate_entropy(execution_path)
            neural_predictions = AdvancedImageForensics.run_deep_neural_pipeline(execution_path)
            
            ai_prob = neural_predictions.get("vit_artifact_prob", 0.0)
            authenticity_score = 1.0 - ai_prob
            telemetry_metadata = {
                "entropy": empirical_entropy, 
                "ela": ela_metrics, 
                "deep_learning_telemetry": neural_predictions,
                "threat_intel": threat_report # Append Threat Intel
            }

        elif ext in VIDEO_EXTENSIONS:
            file_type = "Video"
            video_results = AdvancedVideoForensics.analyze_video_stream(execution_path, Config.UPLOAD_FOLDER, sample_rate=30)
            
            if video_results["status"] == "Success":
                ai_prob = video_results["aggregate_ai_probability"]
                authenticity_score = video_results["aggregate_authenticity_score"]
                telemetry_metadata = {
                    "container_metadata": video_results["metadata"],
                    "max_peak_anomaly": video_results["max_peak_anomaly"],
                    "flagged_keyframes": video_results["flagged_keyframes"],
                    "timeline_telemetry": video_results["timeline_telemetry"],
                    "threat_intel": threat_report # Append Threat Intel
                }
            else:
                batch_results.append({"filename": safe_name, "status": "error", "message": video_results["message"]})
                continue

        elif ext in AUDIO_EXTENSIONS:
            file_type = "Audio"
            audio_visuals = AdvancedAudioForensics.generate_mel_spectrogram(execution_path, Config.UPLOAD_FOLDER)
            neural_audio = AdvancedAudioForensics.run_voice_cloning_detection(execution_path)
            
            ai_prob = neural_audio.get("synthetic_voice_probability", 0.0)
            authenticity_score = 1.0 - ai_prob
            telemetry_metadata = {
                "duration_seconds": audio_visuals.get("duration_seconds", 0),
                "sample_rate": audio_visuals.get("sample_rate", 0),
                "spectrogram_filename": audio_visuals.get("spectrogram_filename", ""),
                "acoustic_signature": neural_audio.get("top_acoustic_signature", "Unknown"),
                "threat_intel": threat_report # Append Threat Intel
            }

        # ==========================================
        # 6. DATABASE COMMIT & CHAIN OF CUSTODY
        # ==========================================
        
        try:
            # Save core evidence metrics
            new_evidence = Evidence(
                case_id=int(case_id),
                filename=safe_name,
                file_path=execution_path,
                file_type=file_type,
                md5_hash=hashes["md5"],
                sha256_hash=hashes["sha256"],
                authenticity_score=float(authenticity_score),
                ai_probability=float(ai_prob),
                forensic_metadata=telemetry_metadata
            )
            db.session.add(new_evidence)
            db.session.commit()

            # Save immutable chain of custody log
            chain_log = ChainOfCustody(
                evidence_id=new_evidence.id,
                action=f"{file_type} Forensic Ingestion & Matrix Analysis Execution",
                operator_username=operator,
                notes="Batch processing completed via Multi-Modal Pipeline."
            )
            db.session.add(chain_log)
            db.session.commit()

            # Append successful result to our JSON batch array
            batch_results.append({
                "filename": safe_name,
                "status": "success",
                "file_type": file_type,
                "evidence_id": new_evidence.id,
                "authenticity_score": authenticity_score,
                "ai_probability": ai_prob
            })
            
        except Exception as e:
            db.session.rollback()
            batch_results.append({"filename": safe_name, "status": "error", "message": f"Database error: {str(e)}"})

    # 7. Transmit complete payload back to UI
    return jsonify({
        "status": "batch_complete", 
        "total_processed": len(uploaded_files), 
        "results": batch_results
    }), 201