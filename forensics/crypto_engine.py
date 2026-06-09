import hashlib

class CryptoForensicsEngine:
    @staticmethod
    def generate_hashes_and_metadata(file_path):
        """
        Generates court-verifiable tracking verification signatures over incoming binary evidence strings.
        """
        md5_factory = hashlib.md5()
        sha1_factory = hashlib.sha1()
        sha256_factory = hashlib.sha256()

        with open(file_path, "rb") as target_file:
            while chunk := target_file.read(8192):
                md5_factory.update(chunk)
                sha1_factory.update(chunk)
                sha256_factory.update(chunk)

        return {
            "md5": md5_factory.hexdigest(),
            "sha1": sha1_factory.hexdigest(),
            "sha256": sha256_factory.hexdigest()
        }