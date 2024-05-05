from engine import SESSION_MAKER
from orm_quary import orm_query_get_user, orm_query_get_project, orm_query_get_data

import asyncio
import tkinter as tk


async def visual_get_users(output_widget, username):
    async with SESSION_MAKER() as session:
        rows = await orm_query_get_user(session=session, name=username)
        output_widget.delete('1.0', tk.END)  # Очищаем предыдущий вывод
        for i in rows:
            output_widget.insert(tk.END, f'{i.name}, {i.project}, {i.birthday}\n')

async def visual_get_project(output_widget, username):
    async with SESSION_MAKER() as session:
        rows = await orm_query_get_project(session=session, name=username)
        output_widget.delete('1.0', tk.END)  # Очищаем предыдущий вывод
        for i in rows:
            output_widget.insert(tk.END, f'{i.name}, {i.project}, {i.birthday}\n')

async def visual_get_data(output_widget, username):
    async with SESSION_MAKER() as session:
        rows = await orm_query_get_data(session=session, name=username)
        output_widget.delete('1.0', tk.END)  # Очищаем предыдущий вывод
        for i in rows:
            output_widget.insert(tk.END, f'{i.name}, {i.project}, {i.birthday}\n')