import config

def get_camel_case_name(category):
    return category.title().replace(' ', '')

def get_checkpoints_flag():
    load_checkpoints_file = open(config.LOAD_CHECKPOINTS_FILE, "r")
    value = load_checkpoints_file.read().splitlines()[0]
    load_checkpoints_file.close()

    return int(value)

def set_checkpoints_flag(new_value):
    load_checkpoints_file = open(config.LOAD_CHECKPOINTS_FILE, "w")
    load_checkpoints_file.write(new_value)
    load_checkpoints_file.close()

def get_processed_video_count():
    processed_video_file = open(config.PROCESSED_VIDEO_COUNT_FILE, "r")
    value = processed_video_file.read().splitlines()[0]
    processed_video_file.close()
    return int(value)

def set_processed_video_count(new_value):
    processed_video_file = open(config.PROCESSED_VIDEO_COUNT_FILE, "w")
    processed_video_file.write(str(new_value))
    processed_video_file.close()
