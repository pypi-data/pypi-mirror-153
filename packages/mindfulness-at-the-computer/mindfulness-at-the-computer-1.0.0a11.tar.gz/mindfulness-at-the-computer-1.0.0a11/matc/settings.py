import datetime
import json
import logging
import os
import shutil
import matc.globa

JSON_OBJ_TYPE = "__obj_type__"

# Setting Keys (SK)
SK_SHOW_BREATHING_TEXT = "show_breathing_text"
SK_BREATHING_AUDIO_VOLUME = "breathing_audio_volume"
SK_BREATHING_BREAK_TIMER_SECS = "breathing_break_timer_secs"
SK_BREATHING_PHRASES = "breathing_phrases"
SK_BREATHING_VISUALIZATION = "breathing_visualization"
SK_MOVE_MOUSE_CURSOR = "move_mouse_cursor"
# SK_DEBUG_USE_SECONDS_FOR_BR_TIMER = "debug_use_seconds_for_br_timer"

"""
SK_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN = "nr_of_times_until_feedback_shown"
SK_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN: matc.globa.INITIAL_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN,
FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP = -1
INITIAL_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN = 10

    def update_gui(self):
        self.gui_update_bool = True
        # settings = matc.settings.settings.is.SettingsM.get()
        self.show_again_qcb.setChecked(
            settings.nr_times_started_since_last_feedback_notif != matc.globa.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP
        )
        self.gui_update_bool = False

    def on_show_again_toggled(self, i_checked: bool):
        if self.gui_update_bool:
            return
        settings = matc.model.SettingsM.get()
        if i_checked:
            if settings.nr_times_started_since_last_feedback_notif == matc.globa.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP:
                settings.nr_times_started_since_last_feedback_notif = 0
            else:
                pass
        else:
            settings.nr_times_started_since_last_feedback_notif = matc.globa.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP


    self.show_again_qcb = QtWidgets.QCheckBox(self.tr("Show this dialog at startup again in the future"))
    self.show_again_qcb.toggled.connect(self.on_show_again_toggled)
    vbox_l2.addWidget(self.show_again_qcb)


"""

BREATHING_BREAK_TIMER_DEFAULT_SECS = 540

settings: dict = {
    SK_SHOW_BREATHING_TEXT: True,
    SK_BREATHING_AUDIO_VOLUME: 50,
    SK_BREATHING_BREAK_TIMER_SECS: BREATHING_BREAK_TIMER_DEFAULT_SECS,
    SK_BREATHING_PHRASES: [],
    SK_BREATHING_VISUALIZATION: matc.globa.BreathingVisalization.bar.value,
    SK_MOVE_MOUSE_CURSOR: False,
}
# -the values given here are the minimum values needed for the application to work
# settings_dict[SETTING_ONE_KEY]


# @dataclasses.dataclass
# In the future we may want to rewrite the three classes below to be dataclasses instead
# https://docs.python.org/3/library/dataclasses.html
# They are supported from Python 3.7

class SettingsListObject:
    def __init__(self, i_id: int):
        self.id: int = i_id


class BreathingPhrase(SettingsListObject):
    def __init__(self, i_id: int, i_in_breath: str, i_out_breath: str):
        super().__init__(i_id)
        self.in_breath: str = i_in_breath
        self.out_breath: str = i_out_breath


class RestAction(SettingsListObject):
    def __init__(self, i_id: int, i_title: str, i_image_path: str):
        super().__init__(i_id)
        self.title: str = i_title
        self.image_path: str = i_image_path


def _get_list_object(settings_key: str, i_list_id: int):
    # -> SettingsListObject
    # SettingsListObject
    list_objects: list = settings[settings_key]
    for o in list_objects:
        if o.id == i_list_id:
            return o
    raise Exception(f"No list object found in the list {settings_key} for the id {i_list_id}")


def get_topmost_breathing_phrase() -> BreathingPhrase:
    list_objects: list = settings[SK_BREATHING_PHRASES]
    if len(list_objects) < 1:
        raise Exception("List is empty, so cannot return item")
    return list_objects[0]


def get_breathing_phrase(i_id: int) -> BreathingPhrase:
    return _get_list_object(SK_BREATHING_PHRASES, i_id)


def get_breathing_volume() -> int:
    return settings[SK_BREATHING_AUDIO_VOLUME]


def _add_list_object(i_settings_key: str, i_class, *args) -> int:
    """
    Order of JSON arrays is preserved (and of course Python lists too)
    https://stackoverflow.com/a/7214312/2525237
    """
    list_objects: list = settings[i_settings_key]
    highest_id: int = 0
    if list_objects:
        highest_id: int = max(lo.id for lo in list_objects)
    new_id: int = highest_id + 1
    new_br_phrase = i_class(new_id, *args)
    list_objects.append(new_br_phrase)
    # settings[i_settings_key] = list_objects
    return new_id


def add_breathing_phrase(i_in_breath: str, i_out_breath: str) -> int:
    new_id = _add_list_object(SK_BREATHING_PHRASES, BreathingPhrase, i_in_breath, i_out_breath)
    return new_id


def _remove_list_object(i_settings_key: str, i_id: int) -> None:
    list_objects: list = settings[i_settings_key]
    for o in list_objects:
        if o.id == i_id:
            list_objects.remove(o)
            return


def remove_breathing_phrase(i_id: int):
    _remove_list_object(SK_BREATHING_PHRASES, i_id)


def _set_list_object_attributes(i_settings_key: str, i_id: int, **kwargs):
    list_objects: list = settings[i_settings_key]
    for o in list_objects:
        if o.id == i_id:
            for k, v in kwargs.items():
                if getattr(o, k):
                    setattr(o, k, v)
                else:
                    logging.warning(f"Could not find attribute {k} in object {o}. Continuing")
            return


def set_breathing_phrase_attributes(i_id: int, **kwargs):
    # Example: set_breathing_phrase_attributes(1, in_breath="Breathing in, i know i ___")
    # Changing to these arguments? in_breath=i_in_breath, out_breath=i_out_breath
    _set_list_object_attributes(SK_BREATHING_PHRASES, i_id, **kwargs)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):  # -overridden
        if issubclass(type(obj), SettingsListObject):
            object_dictionary: dict = obj.__dict__
            type_value = type(obj).__name__
            # if isinstance(obj, BreathingPhrase):
            # type_value = BreathingPhrase.__name__
            # else: raise Exception(f"Cannot endode object: Case is not covered")
            object_dictionary[JSON_OBJ_TYPE] = type_value
            return obj.__dict__
        else:
            return super().default(obj)


def my_decode(dct: dict):
    """
    :param dct:
    From the documentation:
    "object_hook is an optional function that will be called with the result of any object literal
    decoded (a dict). The return value of object_hook will be used instead of the dict."
    :return:
    """
    if JSON_OBJ_TYPE in dct and dct[JSON_OBJ_TYPE] == RestAction.__name__:
        rest_action_obj = RestAction(
            i_id=dct["id"],
            i_title=dct["title"],
            i_image_path=dct["image_path"]
        )
        return rest_action_obj
    if JSON_OBJ_TYPE in dct and dct[JSON_OBJ_TYPE] == BreathingPhrase.__name__:
        breathing_phrase_obj = BreathingPhrase(
            i_id=dct["id"],
            i_in_breath=dct["in_breath"],
            i_out_breath=dct["out_breath"]
        )
        return breathing_phrase_obj
    return dct


def settings_file_exists() -> bool:
    return os.path.isfile(matc.globa.settings_file_path)


def backup_settings_file() -> None:
    if matc.globa.testing_bool:
        return
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name_sg = matc.globa.get_settings_file_path(date_sg)
    shutil.copyfile(matc.globa.settings_file_path, new_file_name_sg)

    # Removing older backups

    # Checking if it's well-formatted (JSON ok?)


def save_settings_to_json_file():
    logging.debug("Saving to json file")
    logging.debug(f"{matc.settings.settings=}")
    with open(matc.globa.settings_file_path, "w") as write_file:
        json.dump(matc.settings.settings, write_file, indent=2, cls=MyEncoder)


def update_settings_dict_with_json_data(i_min_dict_ref: dict, i_file_path: str):
    logging.debug("update_dict_with_json_data")
    if os.path.isfile(i_file_path):
        with open(i_file_path, "r") as read_file:
            # try:
            #     pass
            # except json.decoder.JSONDecodeError:
            #     pass

            from_file_dict: dict = json.load(read_file, object_hook=my_decode)

            diff_key_list: list = []
            for min_key in i_min_dict_ref.keys():
                if min_key not in from_file_dict.keys():
                    diff_key_list.append(min_key)
            if diff_key_list:
                # diff_keys_str = ", ".join(diff_key_list)
                logging.warning(f"One or more keys needed for the application to work were not "
                f"available in {os.path.basename(i_file_path)} so have been added now "
                f"(with a default value). These are the keys: {diff_key_list}")

            diff_key_list: list = []
            for file_key in from_file_dict.keys():
                if file_key not in i_min_dict_ref.keys():
                    diff_key_list.append(file_key)
            if diff_key_list:
                # diff_keys_str = ", ".join(diff_key_list)
                logging.warning(f"One or more keys in {os.path.basename(i_file_path)} are not "
                f"used by the application (though may have been used before). "
                f"These are the keys: {diff_key_list}")

            for min_key in i_min_dict_ref.keys():
                if min_key not in from_file_dict.keys():
                    diff_key_list.append(min_key)
            for file_key in from_file_dict.keys():
                if file_key not in i_min_dict_ref.keys():
                    diff_key_list.append(file_key)

            # logging.debug(f"Before merge {i_min_dict_ref=}")
            # logging.debug(f"Before merge {from_file_dict=}")
            i_min_dict_ref.update(from_file_dict)
            # -if there are different values for the same key, the value
            #  in from_file_dict takes precendence
            # logging.debug(f"After merge {i_min_dict_ref=}")


# Initial setup
if not settings_file_exists():
    # min_settings_dict[SK_REST_ACTIONS].update(init_rest_actions)
    add_breathing_phrase(
        "Breathing in I know I am breathing in",
        "Breathing out I know I am breathing out"
    )
    add_breathing_phrase(
        "Breathing in I follow the whole length of my in-breath",
        "Breathing out I follow the whole length of my out-breath"
    )
    add_breathing_phrase(
        "Breathing in I am aware of my body",
        "Breathing out I am aware of my body"
    )
    add_breathing_phrase(
        "Breathing in I am aware of my posture",
        "Breathing out I adjust my posture"
    )
    add_breathing_phrase(
        "May everyone live with compassion",
        "May everyone live in peace"
    )
    """
    "Breathing in, I know I am breathing in","Breathing out, I know I am breathing out",
    "Aware of my body, I breathe in","Aware of my body, I breathe out",
    "Breathing in, I care for my body","Breathing out, I relax my body",
    "Happy, At Peace","May I be happy",
    "Breathing in I share the well-being of others","Breathing out I contribute to the well-being of others",
    "Breathing in compassion to myself","Breathing out compassion to others",
    "Self-love and acceptance","I love and accept myself just as I am",
    """


# update_dict_with_json_data(settings, matc.globa.get_settings_file_path())
# logging.debug(f"{settings=}")
