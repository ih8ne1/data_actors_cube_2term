from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete


async def urm_quared_get_user_all(session):
    query = select(User)
    result = await session.execute(query)
    result = result.scalars().all()
    return result

import json

# Функция для добавления пользователей в базу данных
from datetime import datetime



async def orm_add_user(session, data):
    for key, values in data.items():
        try:
            date_of_birth = datetime.strptime(values['date_of_birth'], '%d.%m.%Y')
        except ValueError:
            print(f"Неверный формат даты рождения для пользователя с ID {key}: {values['date_of_birth']}")
            continue
        user = User(
            # id=key,
            name=values['name'],
            birthday=date_of_birth,
            project=values['theatre_works'][0] if values['theatre_works'] else 'dummy',
            # project='Ваш проект',  # Замените на ваше значение
            role='Г'  # Замените на ваше значение
        )
        session.add(user)
    await session.commit()

