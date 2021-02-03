import os


class Env:
    @staticmethod
    def get_env_or_default(key: str, default="") -> str:
        return os.getenv(key) if os.getenv(key) is not None else default

    @staticmethod
    def database_url() -> str:
        return Env.get_env_or_default("DATABASE_URL", "sqlite:///fan_match.db")

    @staticmethod
    def ken_pom_email() -> str:
        return Env.get_env_or_default("KEN_POM_EMAIL", "")

    @staticmethod
    def ken_pom_password() -> str:
        return Env.get_env_or_default("KEN_POM_PASSWORD", "")

    @staticmethod
    def selenium_flags() -> str:
        return Env.get_env_or_default("SELENIUM_FLAGS", "")
