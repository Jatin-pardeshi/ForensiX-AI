import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

class PDFReportGenerator:
    @staticmethod
    def generate_report(evidence_record, upload_folder):
        """
        Dynamically constructs a court-admissible PDF document containing
        cryptographic hashes, AI telemetry matrices, and visual artifacts.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading1'],
            alignment=1, 
            textColor=colors.HexColor('#1f2937'),
            fontSize=16,
            spaceAfter=20
        )
        normal_style = styles['Normal']
        
        elements = []
        
        # --- 1. REPORT HEADER ---
        elements.append(Paragraph("FORENSIX AI // OFFICIAL FORENSIC REPORT", title_style))
        
        # --- 2. MASTER CASE DATA TABLE ---
        case_data = [
            ["Case Reference:", f"CASE-{evidence_record.case_id}"],
            ["Evidence ID:", f"#{evidence_record.id}"],
            ["Target File:", evidence_record.filename],
            ["Media Type:", evidence_record.file_type],
            ["Analysis Date:", evidence_record.analyzed_at.strftime('%Y-%m-%d %H:%M:%S UTC')]
        ]
        
        t_case = Table(case_data, colWidths=[150, 350])
        t_case.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#d1d5db'))
        ]))
        elements.append(t_case)
        elements.append(Spacer(1, 20))
        
        # --- 3. CRYPTOGRAPHIC CHAIN OF CUSTODY ---
        elements.append(Paragraph("1. Cryptographic Chain of Custody", styles['Heading2']))
        hash_data = [
            ["MD5:", evidence_record.md5_hash],
            ["SHA256:", evidence_record.sha256_hash]
        ]
        t_hashes = Table(hash_data, colWidths=[80, 420])
        t_hashes.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME', (1,0), (1,-1), 'Courier'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        elements.append(t_hashes)
        elements.append(Spacer(1, 20))
        
        # --- 4. NEURAL TELEMETRY ---
        elements.append(Paragraph("2. AI Telemetry & Authentication Matrix", styles['Heading2']))
        ai_data = [
            ["Authenticity Index (Verified Human):", f"{round(evidence_record.authenticity_score * 100, 2)}%"],
            ["AI Synthesis Risk (Deepfake Probability):", f"{round(evidence_record.ai_probability * 100, 2)}%"]
        ]
        t_ai = Table(ai_data, colWidths=[250, 250])
        t_ai.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (1,0), (1,0), colors.HexColor('#10b981')), 
            ('TEXTCOLOR', (1,1), (1,1), colors.HexColor('#ef4444')), 
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        elements.append(t_ai)
        elements.append(Spacer(1, 20))
        
        # --- 5. VISUAL ARTIFACTS ---
        elements.append(Paragraph("3. Extracted Forensic Artifacts", styles['Heading2']))
        
        if evidence_record.file_type == 'Image':
            # FIX: Pull the exact generated filename from the database JSON metadata
            ela_filename = evidence_record.forensic_metadata.get('ela', {}).get('heatmap_filename')
            
            # Fallback for old records where metadata might be slightly different
            if not ela_filename:
                ela_filename = f"ela_heatmap_{evidence_record.filename}.png"
                
            ela_path = os.path.join(upload_folder, ela_filename)
            
            if os.path.exists(ela_path):
                elements.append(Paragraph("Error Level Analysis (ELA) Compression Heatmap:", normal_style))
                elements.append(Spacer(1, 10))
                img_ela = Image(ela_path)
                img_ela._restrictSize(450, 300)
                elements.append(img_ela)
                
        elif evidence_record.file_type == 'Audio':
            spec_name = evidence_record.forensic_metadata.get('spectrogram_filename')
            if spec_name:
                spec_path = os.path.join(upload_folder, spec_name)
                if os.path.exists(spec_path):
                    elements.append(Paragraph("Acoustic Mel-Spectrogram Matrix:", normal_style))
                    elements.append(Spacer(1, 10))
                    img_spec = Image(spec_path)
                    img_spec._restrictSize(450, 250)
                    elements.append(img_spec)

        elif evidence_record.file_type == 'Video':
             elements.append(Paragraph("Video analysis generated multi-frame spatial telemetry. Review active system ledger for complete keyframe breakdown.", normal_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer