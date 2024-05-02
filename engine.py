import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import logging
import asyncio
from sqlalchemy import select
from models import Base, User
from orm_quary import orm_add_user, urm_quared_get_user_all
import json


logging.basicConfig(
    level=logging.INFO,
)

engine = create_async_engine(f"postgresql+asyncpg://{'postgres'}:{'123'}@{'localhost'}:{'5432'}/{'theatre'}", echo=True)


session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



# async def drop_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # async with session_maker() as session:
    #     data['session'] = session

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

async def main():
    await create_db()
    json_data = list()
    json_data = read_json_file('collected_data_with_dob1.json')

    async with session_maker() as session:

        await orm_add_user(session, json_data)
        # rows = await urm_quared_get_user_all(session)
        # for i in rows:
        #     print(i)



json_data = read_json_file('collected_data_with_dob1.json')

for values in json_data.values():
    print(values)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    loop.create_task(main())

    try:
        loop.run_forever()
    finally:
        loop.close()


# async with session_maker() as session:
# 	query = select(Category)
# 	result = await session.execute(query)
# 	for i in result:
# 		print(i.id)
#theatre