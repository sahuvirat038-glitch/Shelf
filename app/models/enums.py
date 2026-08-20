import enum

class OAuthProvider(str, enum.Enum):
    GOOGLE = "google"
    GITHUB = "github"

class ReadingStatus(str, enum.Enum):
    WANT_TO_READ = "want_to_read"
    CURRENTLY_READING = "currently_reading"
    FINISHED = "finished"

class ClubRole(str, enum.Enum):
    OWNER = "owner"
    MEMBER = "member"