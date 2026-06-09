import requests

class ThreatIntelligenceEngine:
    @staticmethod
    def check_virustotal(file_hash, api_key):
        """
        Cross-references the cryptographic hash against the global VirusTotal database.
        Returns the number of security vendors that flagged this file as malicious.
        """
        # Failsafe if the API key isn't configured yet
        if not api_key or api_key == 'YOUR_FREE_VIRUSTOTAL_API_KEY_HERE':
            return {"status": "skipped", "message": "API key not configured."}

        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {"x-apikey": api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                stats = data['data']['attributes']['last_analysis_stats']
                return {
                    "status": "success", 
                    "malicious_votes": stats['malicious'], 
                    "clean_votes": stats['undetected']
                }
            elif response.status_code == 404:
                return {"status": "not_found", "message": "Hash has never been seen globally."}
            else:
                return {"status": "error", "message": f"API Rejected: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}