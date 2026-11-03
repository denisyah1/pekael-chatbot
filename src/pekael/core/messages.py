"""User-facing status texts (FR-08, NFR-04).

They never contain provider error details, stack traces or keys. The out-of-scope fallback
text lives with the prompt policy (``prompts.FALLBACK_MESSAGE``).
"""

EMPTY_QUESTION = "Silakan tulis pertanyaan tentang PKL terlebih dahulu."
QUESTION_TOO_LONG = "Pertanyaan terlalu panjang. Batas maksimal {limit} karakter, silakan persingkat pertanyaan."
INDEX_NOT_READY = "Knowledge base Pekael belum disiapkan. Silakan hubungi admin."
RETRIEVAL_FAILED = "Pencarian pada knowledge base sedang bermasalah. Silakan coba lagi nanti."
QUOTA_EXHAUSTED = "Kuota layanan AI Pekael sedang habis. Silakan coba lagi beberapa saat lagi."
SERVICE_UNAVAILABLE = "Layanan AI Pekael sedang sibuk atau tidak dapat dihubungi. Silakan coba lagi nanti."
SERVICE_MISCONFIGURED = "Layanan AI Pekael belum dikonfigurasi dengan benar. Silakan hubungi admin."
GENERATION_FAILED = "Pekael gagal menyusun jawaban. Silakan coba lagi."
UNEXPECTED_ERROR = "Terjadi kesalahan pada Pekael. Silakan coba lagi nanti."
