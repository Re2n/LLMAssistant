import hashlib

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.Environment import get_environment_variables

env = get_environment_variables()

DATABASE_URL = "sqlite+aiosqlite:///./llm_assistant.db"


class Db:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False, expire_on_commit=False
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session


db = Db(DATABASE_URL)
bot_token = env.BOT_TOKEN
ollama_url = env.OLLAMA_URL
model_name = env.MODEL_NAME
credentials = [env.ADMIN_USER, env.ADMIN_PASSWORD]
token = hashlib.sha256((str(env.ADMIN_USER)+str(env.ADMIN_PASSWORD)).encode('utf-8')).hexdigest()
