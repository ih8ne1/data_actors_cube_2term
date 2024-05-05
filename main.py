import asyncio
import json
import tkinter as tk

from engine import SESSION_MAKER, create_db
from orm_quary import (
    orm_add_user, 
    urm_quared_get_user_all,
    orm_query_get_user,
    )
from visual import visual_get_users, visual_get_data, visual_get_project


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# async def main(output_widget):
#     await create_db()
#     json_data = list()
#     json_data = read_json_file('collected_data_with_dob_test.json')

#     async with SESSION_MAKER() as session:

#         # await orm_add_user(session, json_data)
#         # rows = await urm_quared_get_user_all(session)
#         # for i in rows:
#         #     output_widget.insert(tk.END, i.name + '\n')
#         # session.close()
#         rows = await orm_query_get_user(session=session, name='СЕРГЕЙ АКИМОВ')
#         for i in rows:
#             print(i.name)


async def get_data_and_display(output_widget, entry):
    username = entry.get()
    if not username:
        return
    await visual_get_users(output_widget, username)

async def get_data_and_display1(output_widget, entry):
    username = entry.get()
    if not username:
        return
    await visual_get_project(output_widget, username)

async def get_data_and_display2(output_widget, entry):
    username = entry.get()
    if not username:
        return
    await visual_get_data(output_widget, username)

async def main():
    app = tk.Tk()
    app.title("ORM Data Viewer")

    output_text = tk.Text(app)
    output_text.pack()

    entry_frame = tk.Frame(app)
    entry_frame.pack()

    entry0 = tk.Entry(entry_frame)
    entry0.grid(row=0, column=0)

    button0 = tk.Button(entry_frame, text="Достать данные все", command=lambda: asyncio.create_task(get_data_and_display(output_text, entry0)))
    button0.grid(row=0, column=1)

    entry1 = tk.Entry(entry_frame)
    entry1.grid(row=0, column=2)

    button1 = tk.Button(entry_frame, text="Достать данные проекты", command=lambda: asyncio.create_task(get_data_and_display1(output_text, entry1)))
    button1.grid(row=0, column=3)

    entry0 = tk.Entry(entry_frame)
    entry0.grid(row=0, column=4)

    button1 = tk.Button(entry_frame, text="Достать данные даты", command=lambda: asyncio.create_task(get_data_and_display2(output_text, entry1)))
    button1.grid(row=0, column=5)

    async def update_tkinter():
        while True:
            try:
                app.update()
                await asyncio.sleep(0.01)
            except tk.TclError:
                break

    await asyncio.gather(update_tkinter(), asyncio.sleep(0.01))
    app.mainloop()

if __name__ == '__main__':
    asyncio.run(main())