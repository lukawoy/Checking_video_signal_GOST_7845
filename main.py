from tkinter import TOP, Button, Label, N, StringVar, Tk, W, ttk
from tkinter import messagebox as mb

import pyvisa

import command_tds as tds

rm = pyvisa.ResourceManager()

scope = 0


def connect():
    global scope
    try:
        scope = rm.open_resource(usb_devices.get())
        scope.timeout = 2000

        res = scope.query("*IDN?")
    except pyvisa.errors.VisaIOError:
        res = 0
    if res:
        label_connect.config(
            text=f"Установлена связь с устройством\n{res[0:27]}", foreground="green"
        )
        check_button.config(state="normal")
        scope.timeout = 2000
    else:
        label_connect.config(text=f"Связь не установлена", foreground="red")


def check_video_signal():
    mb.showinfo(
        "Внимание!", "Необходимо подключить внешнюю снхронизацию (тот же сигнал)"
    )
    mb.showinfo("Внимание!", "Необходимо подключить сигнал I по ГОСТ 18471")
    val_1 = tds.full_signal_scope(scope)
    val_2 = tds.brightness_signal_scope(scope)
    val_3 = tds.ratio_sinkv_impulse(scope, val_2)
    mb.showinfo("Внимание!", "Необходимо подключить сигнал белого поля")
    val_4, val_5, val_6 = tds.pulse_emissions(scope)
    val_7 = tds.string_length(scope)
    tds.rejecting_lines(scope)
    mb.showinfo(
        "Внимание!", "Установите курсоры для измерения отклонения длительностей строк"
    )
    val_8 = tds.get_delta_t(scope)
    val_9 = tds.length_quenching_pulse(scope)
    tds.interval_bet_front(scope)
    mb.showinfo(
        "Внимание!",
        "Установите курсоры для измерения интервала между фронтами гасящего и синхронизирующего импульсов строк",
    )
    val_10 = tds.get_delta_t(scope)
    val_11 = tds.length_syncpulse(scope)
    tds.interval_bet_front_2(scope)
    mb.showinfo(
        "Внимание!",
        "Установите курсоры для измерения интервала между фронтами гасящего имп. полей и 1-го уравнивающего имп.",
    )
    val_12 = tds.get_delta_t(scope)
    val_13 = tds.length_eqpulse(scope)
    val_14 = tds.length_bet_sync_pole(scope)
    val_144 = tds.length_bet_sync(scope)
    tds.length_seq_eqpulses_1(scope)
    mb.showinfo(
        "Внимание!",
        "Установите курсоры для измерения длительности 1-ой последовательности уравнивающих импульсов",
    )
    val_15 = tds.get_delta_t(scope)
    tds.length_seq_polepulses(scope)
    mb.showinfo(
        "Внимание!",
        "Установите курсоры для измерения длительности последовательности  синх. имп. полей",
    )
    val_16 = tds.get_delta_t(scope)
    tds.length_seq_eqpulses_2(scope)
    mb.showinfo(
        "Внимание!",
        "Установите курсоры для измерения длительности 2-ой последовательности уравнивающих импульсов",
    )
    val_17 = tds.get_delta_t(scope)
    tds.length_bet_0n_eqpulse(scope)
    mb.showinfo(
        "Внимание!",
        "Установите курсоры для измерения номинального интервала между началом строки 0н и срезом гасящего имп. строк",
    )
    val_18 = tds.get_delta_t(scope)
    val_19, val_20 = tds.length_front_eqpulse(scope)
    val_21, val_22 = tds.length_front_syncpulse(scope)
    tds.length_pole(scope)
    mb.showinfo(
        "Внимание!", "Установите курсоры для измерения длительности поля ТВ-сигнала"
    )
    val_23 = tds.get_delta_t(scope)
    tds.length_eqpulse_pole(scope)
    mb.showinfo(
        "Внимание!", "Установите курсоры для измерения длительности гасящего имп. полей"
    )
    val_24 = tds.get_delta_t(scope)

    if abs(val_1 - 1000) <= 30:
        check_label_1.config(
            text=f"Размах полного ТВ-сигнала {format(val_1, '.2f')} мВ - Соответсвует",
            foreground="green",
        )
    else:
        check_label_1.config(
            text=f"Размах полного ТВ-сигнала {format(val_1, '.2f')} мВ - Несоответсвует",
            foreground="red",
        )
    if abs(val_2 - 700) <= 20:
        check_label_2.config(
            text=f"Размах сигнала яркости {format(val_2, '.2f')} мВ - Соответсвует",
            foreground="green",
        )
    else:
        check_label_2.config(
            text=f"Размах сигнала яркости {format(val_2, '.2f')} мВ - Несоответсвует",
            foreground="red",
        )
    if abs(val_3 - 99) <= 7:
        check_label_3.config(
            text=f"Отношение син.кв. имп./имп. белого {format(val_3, '.2f')} % - Соответсвует",
            foreground="green",
        )
    else:
        check_label_3.config(
            text=f"Отношение син.кв. имп./имп. белого {format(val_3, '.2f')} % - Несоответсвует",
            foreground="red",
        )
    if val_4 <= 5:
        check_label_4.config(
            text=f"Выбросы синх. имп/имп. белого {format(val_4, '.2f')} % - Соответсвует",
            foreground="green",
        )
    else:
        check_label_4.config(
            text=f"Выбросы синх. имп/имп. белого {format(val_4, '.2f')} % - Несоответсвует",
            foreground="red",
        )
    if val_5 <= 5:
        check_label_5.config(
            text=f"Выбросы гасящих имп/имп. белого {format(val_5, '.2f')} % - Соответсвует",
            foreground="green",
        )
    else:
        check_label_5.config(
            text=f"Выбросы гасящих имп/имп. белого {format(val_5, '.2f')} % - Несоответсвует",
            foreground="red",
        )
    if val_6 <= 5:
        check_label_6.config(
            text=f"Выбросы урав. имп/имп. белого {format(val_6, '.2f')} % - Соответсвует",
            foreground="green",
        )
    else:
        check_label_6.config(
            text=f"Выбросы урав. имп/имп. белого {format(val_6, '.2f')} % - Несоответсвует",
            foreground="red",
        )
    if abs(val_7 - 64) <= 0.012:
        check_label_7.config(
            text=f"Длительность строки {format(val_7, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_7.config(
            text=f"Длительность строки {format(val_7, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if (val_8 * 1e9) <= 32:
        check_label_8.config(
            text=f"Отклонения длительности строк {format(val_8 * 1e9, '.2f')} нс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_8.config(
            text=f"Отклонения длительности строк {format(val_8 * 1e9, '.2f')} нс - Несоответсвует",
            foreground="red",
        )
    if abs(val_9 * 1e6 - 12) <= 0.3:
        check_label_9.config(
            text=f"Длительность гасящего импульса строк {format(val_9 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_9.config(
            text=f"Длительность гасящего импульса строк {format(val_9 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_10 * 1e6 - 1.5) <= 0.3:
        check_label_10.config(
            text=f"Интервал между фронтами гасящего и синх. имп. {format(val_10 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_10.config(
            text=f"Интервал между фронтами гасящего и синх. имп. {format(val_10 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_11 * 1e6 - 4.7) <= 0.2:
        check_label_11.config(
            text=f"Длительность синх. имп. {format(val_11 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_11.config(
            text=f"Длительность синх. имп. {format(val_11 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_12 * 1e6 - 3) <= 2:
        check_label_12.config(
            text=f"Интервал между фронтами гасящего имп. полей и 1-го урав. имп. {format(val_12 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_12.config(
            text=f"Интервал между фронтами гасящего имп. полей и 1-го урав. имп. {format(val_12 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_13 * 1e6 - 2.35) <= 0.1:
        check_label_13.config(
            text=f"Длительность урав. имп. {format(val_13 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_13.config(
            text=f"Длительность урав. имп. {format(val_13 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_14 * 1e6 - 27.3) <= 0.2:
        check_label_14.config(
            text=f"Длительность синх. имп. полей {format(val_14 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_14.config(
            text=f"Длительность синх. имп. полей {format(val_14 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_144 * 1e6 - 4.7) <= 0.2:
        check_label_15.config(
            text=f"Длительность интервала между соседними синх. имп. полей {format(val_144 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_15.config(
            text=f"Длительность интервала между соседними синх. имп. полей {format(val_144 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_15 * 1e6 - 160) <= 1:
        check_label_16.config(
            text=f"Длительность 1-ой посл. урав. имп. {format(val_15 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_16.config(
            text=f"Длительность 1-ой посл. урав. имп. {format(val_15 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_16 * 1e6 - 160) <= 1:
        check_label_17.config(
            text=f"Длительность посл. синх. имп. {format(val_16 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_17.config(
            text=f"Длительность посл. синх. имп. {format(val_16 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_17 * 1e6 - 160) <= 1:
        check_label_18.config(
            text=f"Длительность 2-ой посл. урав. имп. {format(val_17 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_18.config(
            text=f"Длительность 2-ой посл. урав. имп. {format(val_17 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_18 * 1e6 - 10.5) <= 0.1:
        check_label_19.config(
            text=f"Интервал между началом строки 0н и срезом гасящего имп. {format(val_18 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_19.config(
            text=f"Интервал между началом строки 0н и срезом гасящего имп. {format(val_18 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )
    if abs(val_19 * 1e6 - 0.3) <= 0.1 or abs(val_20 * 1e6 - 0.3) <= 0.1:
        check_label_20.config(
            text=f"Длительность фронта {format(val_19 * 1e6, '.2f')} мкс, среза {format(val_20 * 1e6, '.2f')} мкс гасящего  имп. - Соответсвует",
            foreground="green",
        )
    else:
        check_label_20.config(
            text=f"Длительность фронта {format(val_19 * 1e6, '.2f')} мкс, среза {format(val_20 * 1e6, '.2f')} мкс гасящего  имп. - Несоответсвует",
            foreground="red",
        )
    if abs(val_21 * 1e6 - 0.2) <= 0.1 or abs(val_22 * 1e6 - 0.2) <= 0.1:
        check_label_21.config(
            text=f"Длительность фронта стр. синх. имп. {format(val_21 * 1e6, '.2f')} мкс, среза {format(val_22 * 1e6, '.2f')} мкс синх. имп. полей  имп. - Соответсвует",
            foreground="green",
        )
    else:
        check_label_21.config(
            text=f"Длительность фронта стр. синх. имп. {format(val_21 * 1e6, '.2f')} мкс, среза {format(val_22 * 1e6, '.2f')} мкс синх. имп. полей  имп. - Несоответсвует",
            foreground="red",
        )
    if abs(val_23 * 1e3 - 20) <= 0.004:
        check_label_22.config(
            text=f"Длительность поля {format(val_23 * 1e3, '.2f')} мс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_22.config(
            text=f"Длительность поля {format(val_23 * 1e3, '.2f')} мс - Несоответсвует",
            foreground="red",
        )
    if abs(val_24 * 1e6 - 1610) <= 1:
        check_label_23.config(
            text=f"Длительность гасящего имп. полей {format(val_24 * 1e6, '.2f')} мкс - Соответсвует",
            foreground="green",
        )
    else:
        check_label_23.config(
            text=f"Длительность гасящего имп. полей {format(val_24 * 1e6, '.2f')} мкс - Несоответсвует",
            foreground="red",
        )


root = Tk()
root.title("Проверка видеосигнала")
root.geometry("550x650")

label_devices = Label(text="Доступные USB-устройства")
list_res = rm.list_resources()
if list_res:
    first_var = StringVar(value=rm.list_resources()[0])
    usb_devices = ttk.Combobox(textvariable=first_var, values=rm.list_resources())
else:
    usb_devices = ttk.Combobox()
label_connect = Label()
connect_device = Button(text="Подключиться", command=connect)
check_button = Button(
    text="Проверка видеосигнала", command=check_video_signal, state="disabled"
)

check_label_1 = Label()
check_label_2 = Label()
check_label_3 = Label()
check_label_4 = Label()
check_label_5 = Label()
check_label_6 = Label()
check_label_7 = Label()
check_label_8 = Label()
check_label_9 = Label()
check_label_10 = Label()
check_label_11 = Label()
check_label_12 = Label()
check_label_13 = Label()
check_label_14 = Label()
check_label_15 = Label()
check_label_16 = Label()
check_label_17 = Label()
check_label_18 = Label()
check_label_19 = Label()
check_label_20 = Label()
check_label_21 = Label()
check_label_22 = Label()
check_label_23 = Label()

label_connect.pack(anchor=N, side=TOP)
label_devices.pack(anchor=N, side=TOP)
usb_devices.pack(anchor=N, side=TOP)
connect_device.pack(anchor=N, side=TOP)
check_button.pack(anchor=N, side=TOP)
check_label_1.pack(anchor=W, side=TOP)
check_label_2.pack(anchor=W, side=TOP)
check_label_3.pack(anchor=W, side=TOP)
check_label_4.pack(anchor=W, side=TOP)
check_label_5.pack(anchor=W, side=TOP)
check_label_6.pack(anchor=W, side=TOP)
check_label_7.pack(anchor=W, side=TOP)
check_label_8.pack(anchor=W, side=TOP)
check_label_9.pack(anchor=W, side=TOP)
check_label_10.pack(anchor=W, side=TOP)
check_label_11.pack(anchor=W, side=TOP)
check_label_12.pack(anchor=W, side=TOP)
check_label_13.pack(anchor=W, side=TOP)
check_label_14.pack(anchor=W, side=TOP)
check_label_15.pack(anchor=W, side=TOP)
check_label_16.pack(anchor=W, side=TOP)
check_label_17.pack(anchor=W, side=TOP)
check_label_18.pack(anchor=W, side=TOP)
check_label_19.pack(anchor=W, side=TOP)
check_label_20.pack(anchor=W, side=TOP)
check_label_21.pack(anchor=W, side=TOP)
check_label_22.pack(anchor=W, side=TOP)
check_label_23.pack(anchor=W, side=TOP)

root.mainloop()
