import matplotlib.pyplot as plt
from IPython.display import Audio, Video, display
from matplotlib.pyplot import imread


def print_image(df, print_option):
    w = 40
    h = 40
    fig = plt.figure(figsize=(w, h))

    column_name = df.columns[0]

    num_cols = 5
    num_rows = 5
    df = df[: num_cols * num_rows]
    base_dir = print_option.get("base_dir", "")
    for idx, image_path in enumerate(df[column_name]):
        image_full_path = f"{base_dir}/{image_path}"
        image = imread(image_full_path)
        fig.add_subplot(num_rows, num_cols, idx + 1)
        plt.axis("off")
        plt.title(image_full_path, fontdict={"fontsize": 50 / num_cols})
        plt.imshow(image)
    plt.show()
    return


def print_audio(df, print_option):
    column_name = df.columns[0]
    audio_file_list = list(df[column_name])

    ### display 5 videos max
    limit = 5
    base_dir = print_option.get("base_dir", "")
    for audio_path in audio_file_list[:limit]:
        audio_full_path = f"{base_dir}/{audio_path}"
        print(audio_full_path)
        display(Audio(audio_full_path))
    return


def print_video(df, print_option):
    column_name = df.columns[0]
    video_file_list = list(df[column_name])

    ### display 5 videos max
    limit = 5
    base_dir = print_option.get("base_dir", "")
    for video_path in video_file_list[:limit]:
        video_full_path = f"{base_dir}/{video_path}"
        print(video_full_path)
        display(Video(video_full_path, embed=True))
    return
