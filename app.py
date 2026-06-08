import os
from flask import Flask, render_template, send_from_directory
from models import db, Evidence  # <-- Added Evidence here
from config import Config
from models import db
from api.analysis import analysis_blueprint
from flask import Flask, render_template, send_from_directory, send_file, abort
from forensics.report_engine import PDFReportGenerator

def create_app():
    # Initialize the core application
    app = Flask(__name__)
    
    # Load settings from config.py
    app.config.from_object(Config)

    # Initialize the Database
    db.init_app(app)

    # Register the Forensics API Sub-routes
    # All routes in api/analysis.py will now start with /api/v1/forensics
    app.register_blueprint(analysis_blueprint, url_prefix='/api/v1/forensics')

    # ==========================================
    # USER INTERFACE ROUTING
    # ==========================================

    @app.route('/')
    def dashboard():
        """
        Renders the main Security Operations Center (SOC) dashboard.
        """
        return render_template('dashboard.html')
    
    @app.route('/ledger')
    def evidence_ledger():
        """
        Renders the Evidence Management Ledger, pulling all analyzed 
        historical records from the secure database.
        """
        # Fetch all evidence, sorting by newest first
        all_evidence = Evidence.query.order_by(Evidence.analyzed_at.desc()).all()
        return render_template('evidence.html', evidence_items=all_evidence)
    
    @app.route('/export/pdf/<int:evidence_id>')
    def export_pdf_report(evidence_id):
        """
        Generates and serves a dynamically constructed PDF report for a specific case.
        """
        # Fetch the case from the database
        evidence = Evidence.query.get(evidence_id)
        if not evidence:
            abort(404, description="Evidence record not found in system.")
            
        # Generate the PDF stream
        pdf_stream = PDFReportGenerator.generate_report(evidence, Config.UPLOAD_FOLDER)
        
        # Name the file dynamically based on the case
        safe_filename = f"Forensic_Report_CASE_{evidence.case_id}_ID_{evidence.id}.pdf"
        
        # Serve the file directly to the user's browser as a download
        return send_file(
            pdf_stream,
            as_attachment=True,
            download_name=safe_filename,
            mimetype='application/pdf'
        )

    @app.route('/evidence/<filename>')
    def serve_evidence(filename):
        """
        Securely serves generated forensic files (like ELA heatmaps) 
        and original evidence back to the frontend UI.
        """
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    # ==========================================
    # SYSTEM INITIALIZATION
    # ==========================================

    with app.app_context():
        # Automatically generate SQL tables if they don't exist
        db.create_all()

    return app

if __name__ == '__main__':
    # Launch the application
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)