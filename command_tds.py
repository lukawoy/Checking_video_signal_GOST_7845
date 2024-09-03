# Вспомогательные функции


def set_channel_param(scope, ch=1, coupling="DC", bw="OFF", prob=1, invert="OFF"):
    scope.write(f"CH{ch}:BANdwidth {bw}")
    scope.write(f"CH{ch}:COUPling {coupling}")
    scope.write(f"CH{ch}:PRObe {prob}")
    scope.write(f"CH{ch}:INVert {invert}")


def set_acquire_param(scope, mode="SAMPLE", average=64):
    scope.write(f"ACQuire:MODe {mode}")
    scope.write(f"ACQuire:NUMAVg {average}")


def set_display_param(scope, persistence=0, format_disp="YT", style="VECTORS"):
    scope.write(f"DISplay:FORMat {format_disp}")
    scope.write(f"DISplay:PERSistence {persistence}")
    scope.write(f"DISplay:STYle {style}")


def set_video_trigger_param(
    scope, polarity="NORMAL", source="EXT5", standart="PAL", sync="LINENUM"
):
    scope.write("TRIGger:MAIn:TYPe VID")
    scope.write(f"TRIGger:MAIn:VIDeo:POLarity {polarity}")
    scope.write(f"TRIGger:MAIn:VIDeo:SOUrce {source}")
    scope.write(f"TRIGger:MAIn:VIDeo:STANdard {standart}")
    scope.write(f"TRIGger:MAIn:VIDeo:SYNC {sync}")


def set_line(scope, num):
    set_video_trigger_param(scope)
    scope.write(f"TRIGger:MAIn:VIDeo:LINE {num}")


def get_p2p(scope):
    scope.write("MEASUrement:IMMed:TYPe PK2PK")
    p2p = scope.query("MEASUrement:IMMed:VALue?")
    return float(p2p)


def get_period(scope):
    scope.write("MEASUrement:IMMed:TYPe PERIOD")
    per = scope.query("MEASUrement:IMMed:VALue?")
    return float(per)


def get_negativ_width(scope):
    scope.write("MEASUrement:IMMed:TYPe NWIDTH")
    nwidth = scope.query("MEASUrement:IMMed:VALue?")
    return float(nwidth)


def get_posistive_width(scope):
    scope.write("MEASUrement:IMMed:TYPe PWIDTH")
    pwidth = scope.query("MEASUrement:IMMed:VALue?")
    return float(pwidth)


def get_rising_front(scope):
    scope.write("MEASUrement:IMMed:TYPe RISE")
    rise = scope.query("MEASUrement:IMMed:VALue?")
    return float(rise)


def get_falling_front(scope):
    scope.write("MEASUrement:IMMed:TYPe FALL")
    fall = scope.query("MEASUrement:IMMed:VALue?")
    return float(fall)


def set_horizontal_scale(scope, time_div=10e-6):
    scope.write(f"HORizontal:MAIn:SCAle {time_div}")


def set_horizontal_position(scope, position=0e1):
    scope.write(f"HORizontal:POSition {position}")


def set_vertical_scale(scope, ch=1, volt_div=2e-1):
    scope.write(f"CH{ch}:SCAle {volt_div}")


def set_vertical_position(scope, ch=1, position=-3):
    scope.write(f"CH{ch}:POSition {position}")


def set_vertical_cursors(scope, curs1, curs2):
    scope.write(f"CURSor:VBArs:POSITION1 {curs1}")
    scope.write(f"CURSor:VBArs:POSITION2 {curs2}")


def get_delta_t(scope):
    result = scope.query("CURSor:VBArs:DELTa?")
    return float(result)


# Проверки


def full_signal_scope(scope):
    set_acquire_param(scope)
    set_display_param(scope)
    set_channel_param(scope)
    set_video_trigger_param(scope)
    set_line(scope, 24)

    set_vertical_scale(scope)
    set_vertical_position(scope)
    set_horizontal_scale(scope, 2.5e-6)
    set_horizontal_position(scope, 14.2e-6)
    result = get_p2p(scope)
    return result * 1e3


def brightness_signal_scope(scope):
    set_horizontal_scale(scope, 1e-6)
    set_horizontal_position(scope, 14.92e-6)
    result = get_p2p(scope)
    return result * 1e3


def ratio_sinkv_impulse(scope, br_sig):
    set_horizontal_scale(scope, 100e-9)
    set_horizontal_position(scope, 41.6e-6)
    sinkv = get_p2p(scope) * 1e3
    result = (sinkv / br_sig) * 100
    return result


def pulse_emissions(scope):
    set_line(scope, 312)
    set_horizontal_scale(scope, 50e-9)
    set_horizontal_position(scope, 8.16e-6)

    set_vertical_scale(scope, volt_div=10e-3)
    set_vertical_position(scope, position=-31)
    eq_imp_n = get_p2p(scope)
    set_horizontal_scale(scope, 2.5e-6)
    set_vertical_scale(scope, volt_div=200e-3)
    set_vertical_position(scope, position=-3)
    eq_imp = get_p2p(scope)
    ratio_eq = (eq_imp_n / eq_imp) * 100

    set_line(scope, 320)
    set_horizontal_scale(scope, 100e-9)
    set_horizontal_position(scope, 600e-9)
    set_vertical_scale(scope, volt_div=10e-3)
    sync_imp_n = get_p2p(scope)
    set_vertical_scale(scope, volt_div=200e-3)
    set_horizontal_scale(scope, 500e-9)
    sync_imp = get_p2p(scope)
    ratio_sync = (sync_imp_n / sync_imp) * 100

    set_line(scope, 310)
    set_horizontal_scale(scope, 500e-9)
    set_horizontal_position(scope, 7.4e-6)
    set_vertical_scale(scope, volt_div=10e-3)
    set_vertical_position(scope, position=-30)
    que_imp_n = get_p2p(scope)
    set_vertical_scale(scope, volt_div=200e-3)
    set_vertical_position(scope, position=-3)
    set_horizontal_position(scope, 6.4e-6)
    que_imp = get_p2p(scope)
    ratio_que = (que_imp_n / que_imp) * 100

    return ratio_eq, ratio_sync, ratio_que


def string_length(scope):
    set_line(scope, 338)
    set_horizontal_scale(scope, 10e-6)
    set_horizontal_position(scope, 33.2e-6)
    result = get_period(scope)
    return result * 1e6


def rejecting_lines(scope):
    set_line(scope, 338)
    set_horizontal_scale(scope, 25e-9)
    set_horizontal_position(scope, 10.25e-6)
    set_vertical_scale(scope, volt_div=100e-3)
    set_vertical_position(scope, position=-6.28)
    set_display_param(scope, persistence=99)
    set_vertical_cursors(scope, 10.25e-6, 10.3e-6)


def length_quenching_pulse(scope):
    set_display_param(scope, persistence=0)
    set_vertical_position(scope)
    set_vertical_scale(scope)
    set_line(scope, 338)
    set_horizontal_scale(scope, 2.5e-6)
    set_horizontal_position(scope, 4.1e-6)
    result = get_negativ_width(scope)
    return result


def interval_bet_front(scope):
    set_line(scope, 338)
    set_horizontal_scale(scope, 250e-9)
    set_horizontal_position(scope, -1e-6)
    set_vertical_cursors(scope, -1.81e-6, -240e-9)


def length_syncpulse(scope):
    set_line(scope, 338)
    set_horizontal_position(scope, 2.1e-6)
    set_horizontal_scale(scope, 500e-9)
    result = get_negativ_width(scope)
    return result


def interval_bet_front_2(scope):
    set_line(scope, 311)
    set_horizontal_scale(scope, 250e-9)
    set_horizontal_position(scope, -1e-6)
    set_vertical_cursors(scope, -1.81e-6, -240e-9)


def length_eqpulse(scope):
    set_line(scope, 311)
    set_horizontal_scale(scope, 500e-9)
    set_horizontal_position(scope, 980e-9)
    result = get_negativ_width(scope)
    return result


def length_bet_sync_pole(scope):
    set_line(scope, 313)
    set_horizontal_scale(scope, 5e-6)
    set_horizontal_position(scope, 37.2e-6)
    result = get_negativ_width(scope)
    return result


def length_bet_sync(scope):
    set_line(scope, 313)
    set_horizontal_scale(scope, 1e-6)
    set_horizontal_position(scope, 61.28e-6)
    result = get_posistive_width(scope)
    return result


def length_seq_eqpulses_1(scope):
    set_line(scope, 311)
    set_horizontal_scale(scope, 25e-6)
    set_horizontal_position(scope, 84e-6)
    set_vertical_cursors(scope, -1e-6, 159e-6)


def length_seq_polepulses(scope):
    set_line(scope, 313)
    set_horizontal_scale(scope, 25e-6)
    set_horizontal_position(scope, 90e-6)
    set_vertical_cursors(scope, 32e-6, 192e-6)


def length_seq_eqpulses_2(scope):
    set_line(scope, 6)
    set_horizontal_scale(scope, 25e-6)
    set_horizontal_position(scope, -100e-6)
    set_vertical_cursors(scope, -160e-6, 0e-6)


def length_bet_0n_eqpulse(scope):
    set_line(scope, 25)
    set_horizontal_scale(scope, 2.5e-6)
    set_horizontal_position(scope, 3e-6)
    set_vertical_cursors(scope, -100e-9, 10.4e-6)


def length_front_eqpulse(scope):
    set_line(scope, 25)
    set_horizontal_scale(scope, 50e-9)
    set_horizontal_position(scope, 62.18e-6)
    fall = get_falling_front(scope)
    set_horizontal_position(scope, 10.21e-6)
    rise = get_rising_front(scope)
    return fall, rise


def length_front_syncpulse(scope):
    set_line(scope, 25)
    set_horizontal_scale(scope, 50e-9)
    set_horizontal_position(scope, -200e-6)
    fall = get_falling_front(scope)
    set_horizontal_position(scope, 4.4e-6)
    rise = get_rising_front(scope)
    return fall, rise


def length_pole(scope):
    set_line(scope, 35)
    set_horizontal_scale(scope, 2.5e-3)
    set_horizontal_position(scope, 7.6e-3)
    set_vertical_cursors(scope, -2.4e-3, 17.6e-3)


def length_eqpulse_pole(scope):
    set_line(scope, 312)
    set_horizontal_scale(scope, 250e-6)
    set_horizontal_position(scope, 770e-6)
    set_vertical_cursors(scope, -70e-6, 1.54e-3)
