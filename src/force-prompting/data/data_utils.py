import torch

def collate_fn_ForcePromptingDataset_PointForce(examples): 

    videos = [example["video"] for example in examples]
    prompts = [example["caption"] for example in examples]
    controlnet_videos = [example["controlnet_video"] for example in examples]
    file_ids = [example["file_id"] for example in examples]

    forces = [example["force"] for example in examples]
    angles = [example["angle"] for example in examples]
    x_poss = [example["x_pos"] for example in examples]
    y_poss = [example["y_pos"] for example in examples]

    videos = torch.stack(videos)
    videos = videos.to(memory_format=torch.contiguous_format).float()

    # nate added this
    first_frames = videos[:, 0]
    first_frames = first_frames.to(memory_format=torch.contiguous_format).float()

    controlnet_videos = torch.stack(controlnet_videos)
    controlnet_videos = controlnet_videos.to(memory_format=torch.contiguous_format).float()

    return {
        "file_ids" : file_ids,
        "first_frames" : first_frames,
        "videos": videos,
        "prompts": prompts,
        "controlnet_videos": controlnet_videos,
        "force": forces,
        "angle": angles,
        "x_pos" : x_poss,
        "y_pos" : y_poss,
    }

def collate_fn_ForcePromptingDataset_WindForce(examples): 

    videos = [example["video"] for example in examples]
    prompts = [example["caption"] for example in examples]
    controlnet_videos = [example["controlnet_video"] for example in examples]
    file_ids = [example["file_id"] for example in examples]

    forces = [example["force"] for example in examples]
    angles = [example["angle"] for example in examples]

    videos = torch.stack(videos)
    videos = videos.to(memory_format=torch.contiguous_format).float()

    # nate added this
    first_frames = videos[:, 0]
    first_frames = first_frames.to(memory_format=torch.contiguous_format).float()

    controlnet_videos = torch.stack(controlnet_videos)
    controlnet_videos = controlnet_videos.to(memory_format=torch.contiguous_format).float()

    return {
        "file_ids" : file_ids,
        "first_frames" : first_frames,
        "videos": videos,
        "prompts": prompts,
        "controlnet_videos": controlnet_videos,
        "force": forces,
        "angle": angles,
    }

# This is used for the training stage of the wind force change dataset
def collate_fn_ForcePromptingDataset_WindForce_Change(examples): 

    videos = [example["video"] for example in examples]
    prompts = [example["caption"] for example in examples]
    controlnet_videos = [example["controlnet_video"] for example in examples]
    file_ids = [example["file_id"] for example in examples]

    force_1s = [example["force_1"] for example in examples]
    force_2s = [example["force_2"] for example in examples]
    angle_1s = [example["angle_1"] for example in examples]
    angle_2s = [example["angle_2"] for example in examples]

    videos = torch.stack(videos)
    videos = videos.to(memory_format=torch.contiguous_format).float()

    # nate added this
    first_frames = videos[:, 0]
    first_frames = first_frames.to(memory_format=torch.contiguous_format).float()

    controlnet_videos = torch.stack(controlnet_videos)
    controlnet_videos = controlnet_videos.to(memory_format=torch.contiguous_format).float()

    return {
        "file_ids" : file_ids,
        "first_frames" : first_frames,
        "videos": videos,
        "prompts": prompts,
        "controlnet_videos": controlnet_videos,
        "force_1": force_1s,
        "force_2": force_2s,
        "angle_1": angle_1s,
        "angle_2": angle_2s,
    }

TRANSFORM_MODES = [
    (0,   0.5),
    (90,  1.0),
    (90,  0.5),
    (180, 1.0),
    (180, 0.5),
    (270, 1.0),
    (270, 0.5),
]