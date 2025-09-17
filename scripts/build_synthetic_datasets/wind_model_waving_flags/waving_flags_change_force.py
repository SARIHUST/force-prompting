import bpy
import math
import random
import os
import json
import glob
from mathutils import Vector


# Global variables to store the random parameters
GENERATED_WIND_SPEED_1 = None
GENERATED_WIND_SPEED_2 = None
GENERATED_WIND_ANGLE_blender_interpretable_1 = None
GENERATED_WIND_ANGLE_blender_interpretable_2 = None
GENERATED_WIND_ANGLE_human_interpretable_1 = None
GENERATED_WIND_ANGLE_human_interpretable_2 = None
GENERATED_FLAG_COLORS = None
GENERATED_HDRI = None
OUTPUT_PATH = None

# New global variable to save the flag material so we don't have to search for it again.
FLAG_MATERIAL = None

def randomize_flag_colors(flag_material=None):
    """
    Randomize the flag colors.

    If flag_material is provided (not None), then update that material's color.
    Otherwise, search for a flag material (by name or via cloth modifiers) and save it in FLAG_MATERIAL.
    """
    global GENERATED_FLAG_COLORS, FLAG_MATERIAL

    colors = [
        # Reds
        (1.0, 0.0, 0.0), (0.8, 0.0, 0.0), (1.0, 0.2, 0.2), (0.6, 0.0, 0.0),
        (1.0, 0.4, 0.4), (0.7, 0.2, 0.2), (0.9, 0.2, 0.1), (0.8, 0.2, 0.2),
        (0.6, 0.2, 0.2), (0.5, 0.1, 0.1),
        # Oranges
        (1.0, 0.5, 0.0), (1.0, 0.6, 0.0), (0.9, 0.6, 0.2), (0.8, 0.4, 0.0),
        (1.0, 0.7, 0.3), (0.9, 0.5, 0.2), (0.7, 0.3, 0.0), (0.8, 0.5, 0.3),
        (0.9, 0.7, 0.5), (0.6, 0.3, 0.1),
        # Yellows
        (1.0, 1.0, 0.0), (1.0, 0.9, 0.0), (0.8, 0.8, 0.0), (1.0, 1.0, 0.6),
        (0.9, 0.8, 0.2), (1.0, 0.8, 0.2), (0.7, 0.7, 0.0), (1.0, 0.9, 0.6),
        (0.9, 0.8, 0.5), (0.8, 0.7, 0.3),
        # Greens
        (0.0, 1.0, 0.0), (0.0, 0.8, 0.0), (0.4, 1.0, 0.4), (0.0, 0.6, 0.0),
        (0.0, 0.4, 0.0), (0.4, 0.8, 0.4), (0.6, 0.8, 0.6), (0.4, 0.6, 0.4),
        (0.2, 0.8, 0.2), (0.5, 0.8, 0.0),
        # Cyans
        (0.0, 1.0, 1.0), (0.0, 0.8, 0.8), (0.6, 1.0, 1.0), (0.0, 0.6, 0.6),
        (0.2, 0.6, 0.6), (0.4, 0.8, 0.8), (0.0, 0.8, 1.0), (0.2, 0.7, 0.8),
        (0.4, 0.7, 0.7), (0.6, 0.9, 0.9),
        # Blues
        (0.0, 0.0, 1.0), (0.0, 0.0, 0.8), (0.4, 0.4, 1.0), (0.0, 0.0, 0.6),
        (0.0, 0.0, 0.4), (0.2, 0.2, 0.8), (0.2, 0.2, 0.6), (0.0, 0.2, 0.8),
        (0.4, 0.4, 0.8), (0.6, 0.6, 0.9),
        # Purples
        (0.5, 0.0, 0.5), (0.4, 0.0, 0.4), (0.8, 0.4, 0.8), (0.6, 0.0, 0.6),
        (0.3, 0.0, 0.5), (0.5, 0.0, 0.8), (0.4, 0.2, 0.6), (0.6, 0.4, 0.8),
        (0.8, 0.2, 0.8), (0.9, 0.4, 0.9),
        # Pinks
        (1.0, 0.4, 0.8), (1.0, 0.0, 0.5), (1.0, 0.7, 0.9), (0.9, 0.6, 0.8),
        (0.8, 0.5, 0.6), (1.0, 0.8, 0.9), (0.7, 0.0, 0.4), (0.9, 0.0, 0.3),
        (0.7, 0.0, 0.2), (0.6, 0.2, 0.4),
        # Browns
        (0.6, 0.4, 0.2), (0.5, 0.3, 0.1), (0.7, 0.5, 0.3), (0.4, 0.2, 0.0),
        (0.3, 0.2, 0.1), (0.8, 0.6, 0.4), (0.6, 0.5, 0.4), (0.5, 0.4, 0.3),
        (0.4, 0.3, 0.2), (0.7, 0.6, 0.5),
        # Greys
        (0.9, 0.9, 0.9), (0.8, 0.8, 0.8), (0.6, 0.6, 0.6), (0.4, 0.4, 0.4),
        (0.2, 0.2, 0.2), (0.1, 0.1, 0.1), (0.7, 0.7, 0.7), (0.5, 0.5, 0.5),
        (0.3, 0.3, 0.3), (0.95, 0.95, 0.98)
    ]

    color1_idx = random.randint(0, len(colors) - 1)
    color2_idx = random.randint(0, len(colors) - 1)
    while color2_idx == color1_idx:
        color2_idx = random.randint(0, len(colors) - 1)
    
    color1 = colors[color1_idx]
    color2 = colors[color2_idx]
    
    GENERATED_FLAG_COLORS = {"color1": color1, "color2": color2}
    
    if flag_material is not None:
        update_material_colors(flag_material, color1, color2)
        return True
    else:
        flag_found = False
        for material in bpy.data.materials:
            if "flag" in material.name.lower(): # see if there is a direct flag material
                update_material_colors(material, color1, color2)
                FLAG_MATERIAL = material
                flag_found = True
                break
        if not flag_found:
            for obj in bpy.data.objects:
                if any(mod.type == 'CLOTH' for mod in obj.modifiers):   # see if there is a cloth modifier
                    for mat_slot in obj.material_slots:
                        if mat_slot.material:
                            update_material_colors(mat_slot.material, color1, color2)
                            FLAG_MATERIAL = mat_slot.material
                            flag_found = True
                            break
                    if flag_found:
                        break
        if not flag_found:
            print("Warning: Could not find flag materials to colorize.")
            if len(bpy.data.materials) >= 2:
                update_material_colors(bpy.data.materials[0], color1, (1, 1, 1))
                update_material_colors(bpy.data.materials[1], color2, (1, 1, 1))
                FLAG_MATERIAL = bpy.data.materials[0]
                flag_found = True
        return flag_found

def update_material_colors(material, primary_color, secondary_color=None):
    """Update the colors of a material."""
    if not material.use_nodes:
        material.diffuse_color = primary_color + (1.0,)
        return
    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            node.inputs['Base Color'].default_value = primary_color + (1.0,)
        elif node.type == 'RGB' and secondary_color:
            node.outputs[0].default_value = secondary_color + (1.0,)
        elif node.type == 'MIX' and secondary_color:
            if 'Color1' in node.inputs:
                node.inputs['Color1'].default_value = primary_color + (1.0,)
            if 'Color2' in node.inputs:
                node.inputs['Color2'].default_value = secondary_color + (1.0,)

def setup_flag_position():
    """
    Legacy function to adjust camera position.
    """
    cam = None
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            cam = obj
            break
    if cam is None:
        print("No camera found in the scene.")
        return
    y_base = cam.location.y + 0.00001
    y_0 = random.uniform(-3.0, 3.0)
    new_y = y_base + y_0
    cam.location.y = new_y
    scale = new_y / y_base
    x_range_min = -1.9 * scale
    x_range_max =  1.9 * scale
    z_range_min = -0.2 * scale
    z_range_max =  1.0 * scale
    x_shift = random.uniform(x_range_min, x_range_max)
    z_shift = random.uniform(z_range_min, z_range_max)
    cam.location.x += x_shift
    cam.location.z += z_shift
    print("Camera adjustments applied:")
    print(f"  y_0: {y_0:.2f}, new y: {new_y:.2f}, scale factor: {scale:.2f}")
    print(f"  x_shift: {x_shift:.2f} (range: {x_range_min:.2f} to {x_range_max:.2f})")
    print(f"  z_shift: {z_shift:.2f} (range: {z_range_min:.2f} to {z_range_max:.2f})")
    print("New camera location:", cam.location)

def randomize_hdri_background():
    """Find and apply a random HDRI from the HDRIs folder."""
    global GENERATED_HDRI
    hdri_dir = ".cache/HDRIs"
    if not os.path.exists(hdri_dir):
        print("ERROR: you need to download the HRDIs.")
    hdri_extensions = ['.exr', '.hdr']
    hdri_files = []
    for ext in hdri_extensions:
        pattern = os.path.join(hdri_dir, f"*{ext}")
        hdri_files.extend(glob.glob(pattern))
    if not hdri_files:
        print(f"Warning: No HDRI files found in {hdri_dir}")
        return False
    hdri_path = random.choice(hdri_files)
    hdri_filename = os.path.basename(hdri_path)
    GENERATED_HDRI = hdri_filename
    print(f"Selected HDRI: {hdri_filename}")
    setup_hdri_world(hdri_path)
    return True

def setup_hdri_world(hdri_path):
    """Set up the world to use the selected HDRI."""
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()
    node_background = nodes.new(type='ShaderNodeBackground')
    node_environment = nodes.new(type='ShaderNodeTexEnvironment')
    node_output = nodes.new(type='ShaderNodeOutputWorld')
    node_environment.location = (-300, 0)
    node_background.location = (0, 0)
    node_output.location = (300, 0)
    try:
        node_environment.image = bpy.data.images.load(hdri_path, check_existing=True)
        node_environment.image.colorspace_settings.name = 'Non-Color'
    except Exception as e:
        print(f"Error loading HDRI: {e}")
        return False
    links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
    links.new(node_background.outputs["Background"], node_output.inputs["Surface"])
    return True

def setup_wind():
    # set up a changable wind force field: 1st 1/3 of the animation is no wind, 2nd 1/3 is a certain wind, 3rd 1/3 is a different wind
    global GENERATED_WIND_SPEED_1, GENERATED_WIND_SPEED_2, GENERATED_WIND_ANGLE_blender_interpretable_1, GENERATED_WIND_ANGLE_blender_interpretable_2, GENERATED_WIND_ANGLE_human_interpretable_1, GENERATED_WIND_ANGLE_human_interpretable_2
    
    scene = bpy.context.scene
    if scene.animation_data:
        scene.animation_data_clear()
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    total_frames = end_frame - start_frame + 1

    # divide the animation into 3 parts
    seg_len = total_frames // 3
    phase0_start = start_frame
    phase0_end = start_frame + seg_len - 1
    phase1_start = phase0_end + 1
    phase1_end = phase1_start + seg_len - 1
    phase2_start = phase1_end + 1
    phase2_end = end_frame

    # set up the random parameters for each phase
    #NOTE: Later we can add constraints to the wind parameters so that the winds are quite different from each other
    speed1 = random.uniform(0, 15000)
    angle1_blender = random.uniform(0.0, 360.0)
    angle1_human = (90 - angle1_blender) % 360

    speed2 = random.uniform(0, 15000)
    angle2_blender = random.uniform(0.0, 360.0)
    # angle2_blender = (angle1_blender + 180) % 360   # sanity check, reverse the direction of the wind
    angle2_human = (90 - angle2_blender) % 360

    # pass the parameters to the global variables
    GENERATED_WIND_SPEED_1 = speed1
    GENERATED_WIND_ANGLE_blender_interpretable_1 = angle1_blender
    GENERATED_WIND_ANGLE_human_interpretable_1 = angle1_human
    GENERATED_WIND_SPEED_2 = speed2
    GENERATED_WIND_ANGLE_blender_interpretable_2 = angle2_blender
    GENERATED_WIND_ANGLE_human_interpretable_2 = angle2_human

    if scene.animation_data:
        scene.animation_data_clear()
    wind_obj = None
    for obj in bpy.data.objects:
        if hasattr(obj, 'field') and obj.field and hasattr(obj.field, 'type') and obj.field.type == 'WIND':
            wind_obj = obj
            break
    
    if not wind_obj:
        print("Error: No wind force field found in the scene.")
        return
    current_x = wind_obj.rotation_euler.x
    current_z = wind_obj.rotation_euler.z
    wind = wind_obj.field

    # remove all existing keyframes, without this, there will be some unexpected results
    if wind_obj.animation_data and wind_obj.animation_data.action:
        action = wind_obj.animation_data.action
        for fc in list(action.fcurves):
            if fc.data_path.endswith("strength"):
                action.fcurves.remove(fc)

    # phase 0: no wind
    wind.strength = 0
    wind.keyframe_insert(data_path="strength", frame=phase0_start)
    wind.keyframe_insert(data_path="strength", frame=phase0_end)

    # phase 1: wind 1
    wind.strength = speed1
    wind.keyframe_insert(data_path="strength", frame=phase1_start)
    wind.keyframe_insert(data_path="strength", frame=phase1_end)
    wind_obj.rotation_euler = (current_x, math.radians(angle1_blender), current_z)
    wind_obj.keyframe_insert(data_path="rotation_euler", frame=phase1_start)
    wind_obj.rotation_euler = (current_x, math.radians(angle1_blender), current_z)
    wind_obj.keyframe_insert(data_path="rotation_euler", frame=phase1_end)

    # phase 2: wind 2
    wind.strength = speed2
    wind.keyframe_insert(data_path="strength", frame=phase2_start)
    wind.keyframe_insert(data_path="strength", frame=phase2_end)
    wind_obj.rotation_euler = (current_x, math.radians(angle2_blender), current_z)
    wind_obj.keyframe_insert(data_path="rotation_euler", frame=phase2_start)
    wind_obj.rotation_euler = (current_x, math.radians(angle2_blender), current_z)
    wind_obj.keyframe_insert(data_path="rotation_euler", frame=phase2_end)

    if wind_obj.animation_data and wind_obj.animation_data.action:
        for fcurve in wind_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BEZIER'

    # #NOTE: check the keyframes and the values for each frame
    # print("Speed1: ", speed1, "Speed2: ", speed2)
    # print("Angle1: ", angle1_blender, "Angle2: ", angle2_blender)

    # for fcurve in wind_obj.animation_data.action.fcurves:
    #     if fcurve.data_path.endswith("strength"):
    #         print("keyframe number:", len(fcurve.keyframe_points))
    #         for kf in fcurve.keyframe_points:
    #             print("frame", kf.co.x, "value", kf.co.y)

    # frame_start = phase0_start
    # frame_end   = phase2_end

    # # find the fcurve of strength
    # fc_strength = None
    # fc_angle_y  = None

    # if wind_obj.animation_data and wind_obj.animation_data.action:
    #     for fc in wind_obj.animation_data.action.fcurves:
    #         if fc.data_path == "field.strength":
    #             fc_strength = fc
    #         if fc.data_path == "rotation_euler" and fc.array_index == 1:
    #             fc_angle_y = fc

    # # sample the strength and angle
    # rows = [("frame", "strength", "angle_deg")]
    # for f in range(frame_start, frame_end + 1):
    #     # evaluate strength
    #     val_s = fc_strength.evaluate(f) if fc_strength else wind.strength
    #     # evaluate rotation Y and convert to degrees
    #     val_a = math.degrees(fc_angle_y.evaluate(f)) if fc_angle_y else math.degrees(wind_obj.rotation_euler[1])
    #     rows.append((f, val_s, val_a))

    # # write to CSV
    # out_path = "/projects/vig/hhwang/wind_strength_angle.csv"
    # with open(out_path, "w", newline="") as fp:
    #     import csv
    #     writer = csv.writer(fp)
    #     writer.writerows(rows)
    # print(f"Saved: {out_path}")
    # exit()

    update_output_path()
    print(f"[3-phase wind] Frames {phase0_start}-{phase0_end}: Calm, "
          f"{phase1_start}-{phase1_end}: Wind1 (speed={speed1:.1f}, angle={angle1_human:.1f}°), "
          f"{phase2_start}-{phase2_end}: Wind2 (speed={speed2:.1f}, angle={angle2_human:.1f}°)")
    print(f"Output directory set to: {OUTPUT_PATH}")

def create_flag_template_group():
    """
    Create a template group from Plane, Plane.001, and Sphere.
    Returns the Empty object for duplication.
    """
    objs = bpy.data.objects
    try:
        flag_cloth = objs["Plane"]
        flag_pole = objs["Plane.001"]
        flag_sphere = objs["Sphere"]
    except KeyError as e:
        print(f"Missing expected object: {e}")
        return None

    # Create an empty to group them
    template = bpy.data.objects.new("FlagTemplate", None)
    template.empty_display_size = 1
    template.empty_display_type = 'PLAIN_AXES'
    bpy.context.collection.objects.link(template)

    # Parent the components to the template
    for obj in [flag_cloth, flag_pole, flag_sphere]:
        obj.parent = template

    return template


def place_extra_flags():
    global FLAG_MATERIAL

    cam = bpy.data.objects.get("Camera")
    if not cam:
        print("Camera not found.")
        return

    template = create_flag_template_group()
    if not template:
        print("Could not create flag template.")
        return

    cam_pos = cam.location
    x0, y0, z0 = cam_pos.x, cam_pos.y, cam_pos.z

    # Get z level of the original flag
    try:
        y_flag = bpy.data.objects["Plane.001"].location.y
        z_flag = bpy.data.objects["Plane.001"].location.z
    except KeyError:
        print("Original flagpole (Plane.001) not found.")
        return

    # Define bounding box parameters
    scale = 2.0  # adjust to control how wide the X spread is
    alpha = scale * abs(y0)
    beta = 50.0   # max forward distance from flag 1
    min_x_spacing = 0.5

    x_bounds = (x0 - alpha, x0 + alpha)
    y_bounds = (y_flag, y_flag + beta)

    n_extra = random.randint(0, 63)
    print(f"Placing {n_extra} extra flags")

    placed_x = []

    for i in range(n_extra):
        attempts = 0
        while attempts < 100:
            x = random.uniform(*x_bounds)
            y = random.uniform(*y_bounds)
            z_bounds = (z_flag - (y-y_flag)*alpha/50, z_flag + (y-y_flag)*alpha/32)
            z = random.uniform(*z_bounds)

            # Visual separation via X coordinate only
            if any(abs(x - px) < min_x_spacing for px in placed_x):
                attempts += 1
                continue

            placed_x.append(x)
            break

        if attempts >= 100:
            print(f"Could not place flag {i+1}")
            continue

        # Final position
        pos = Vector((x, y, z))

        # Duplicate group
        new_group = template.copy()
        new_group.name = f"FlagInstance_{i}"
        bpy.context.collection.objects.link(new_group)
        new_group.location = pos

        # Duplicate children
        new_children = []
        for child in template.children:
            new_child = child.copy()
            if child.data:
                new_child.data = child.data.copy()
            new_child.name = f"{child.name}_{i}"
            new_child.parent = new_group
            bpy.context.collection.objects.link(new_child)
            new_children.append(new_child)

        # Assign flag material
        for child in new_children:
            if child.type == 'MESH' and "Plane" in child.name:
                new_mat = FLAG_MATERIAL.copy()
                child.active_material = new_mat
                randomize_flag_colors(flag_material=new_mat)
                break

        print(f"Placed flag {i+1} at {pos}")




def setup_random_scene():
    """Main function to set up all random parameters for the scene."""
    hdri_set = randomize_hdri_background()
    if hdri_set:
        print(f"HDRI background set to: {GENERATED_HDRI}")
    else:
        print("Warning: Could not set HDRI background")
    
    # Randomize the flag colors for the first flag.
    # Since no material is passed, the function searches for the flag material and saves it in FLAG_MATERIAL.
    colors_set = randomize_flag_colors()
    if colors_set:
        print("Flag colors randomized successfully!")
        color1 = GENERATED_FLAG_COLORS["color1"]
        color2 = GENERATED_FLAG_COLORS["color2"]
        print(f"Primary color: RGB({color1[0]:.2f}, {color1[1]:.2f}, {color1[2]:.2f})")
        print(f"Secondary color: RGB({color2[0]:.2f}, {color2[1]:.2f}, {color2[2]:.2f})")
    else:
        print("Warning: Flag colors could not be randomized")
    
    setup_wind()
    setup_flag_position()
    
    # Now place extra flags using the saved FLAG_MATERIAL.
    place_extra_flags()

def update_output_path():
    global GENERATED_WIND_SPEED_1, GENERATED_WIND_SPEED_2, GENERATED_WIND_ANGLE_blender_interpretable_1, GENERATED_WIND_ANGLE_blender_interpretable_2, GENERATED_WIND_ANGLE_human_interpretable_1, GENERATED_WIND_ANGLE_human_interpretable_2, GENERATED_FLAG_COLORS, GENERATED_HDRI, OUTPUT_PATH
    speed_str1 = f"{GENERATED_WIND_SPEED_1:.1f}"
    angle_str1 = f"{GENERATED_WIND_ANGLE_human_interpretable_1:.1f}"
    speed_str2 = f"{GENERATED_WIND_SPEED_2:.1f}"
    angle_str2 = f"{GENERATED_WIND_ANGLE_human_interpretable_2:.1f}"
    color_part = ""
    if GENERATED_FLAG_COLORS:
        color1 = GENERATED_FLAG_COLORS["color1"]
        color2 = GENERATED_FLAG_COLORS["color2"]
        color_id = f"c_{int(color1[0]*255):02x}{int(color1[1]*255):02x}{int(color1[2]*255):02x}_{int(color2[0]*255):02x}{int(color2[1]*255):02x}{int(color2[2]*255):02x}"
        color_part = f"_{color_id}"
    hdri_part = ""
    if GENERATED_HDRI:
        hdri_name = os.path.splitext(GENERATED_HDRI)[0]
        if len(hdri_name) > 20:
            hdri_name = hdri_name[:20]
        hdri_part = f"_hdri_{hdri_name}"
    base_output_dir = bpy.context.scene.render.filepath
    base_output_dir = os.path.dirname(base_output_dir)
    if not base_output_dir.endswith('/'):
        base_output_dir += '/'
    param_dir = f"flag_speed_{speed_str1}_{speed_str2}_angle_{angle_str1}_{angle_str2}"
    OUTPUT_PATH = os.path.join(base_output_dir, param_dir)
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    bpy.context.scene.render.filepath = os.path.join(OUTPUT_PATH, "frame####")
    params = {
        "wind_speed_1": GENERATED_WIND_SPEED_1,
        "wind_angle_1": GENERATED_WIND_ANGLE_human_interpretable_1,
        "wind_speed_2": GENERATED_WIND_SPEED_2,
        "wind_angle_2": GENERATED_WIND_ANGLE_human_interpretable_2,
        "flag_colors": GENERATED_FLAG_COLORS,
        "hdri_background": GENERATED_HDRI
    }
    with open(os.path.join(OUTPUT_PATH, "params.json"), 'w') as f:
        json.dump(params, f, indent=4)

def render_pre_handler(scene):
    if scene.frame_current != scene.frame_start:
        return
    setup_random_scene()

class OBJECT_OT_setup_random_scene(bpy.types.Operator):
    bl_idname = "object.setup_random_scene"
    bl_label = "Setup Random Wind, Colors and HDRI"
    
    def execute(self, context):
        setup_random_scene()
        return {'FINISHED'}

def render_complete_handler(scene):
    global OUTPUT_PATH, GENERATED_WIND_SPEED_1, GENERATED_WIND_ANGLE_human_interpretable_1, GENERATED_WIND_SPEED_2, GENERATED_WIND_ANGLE_human_interpretable_2, GENERATED_FLAG_COLORS, GENERATED_HDRI
    if not OUTPUT_PATH or not GENERATED_WIND_SPEED_1 or not GENERATED_WIND_ANGLE_human_interpretable_1 or not GENERATED_WIND_SPEED_2 or not GENERATED_WIND_ANGLE_human_interpretable_2:
        print("Missing parameters for post-render processing")
        return
    print(f"Rendering complete! Files saved to: {OUTPUT_PATH}")
    print(f"Parameters used: Wind Speed1 = {GENERATED_WIND_SPEED_1}, Wind Angle1 = {GENERATED_WIND_ANGLE_human_interpretable_1}, Wind Speed2 = {GENERATED_WIND_SPEED_2}, Wind Angle2 = {GENERATED_WIND_ANGLE_human_interpretable_2}")
    if GENERATED_FLAG_COLORS:
        color1 = GENERATED_FLAG_COLORS["color1"]
        color2 = GENERATED_FLAG_COLORS["color2"]
        print(f"Flag colors: Primary RGB({color1[0]:.2f}, {color1[1]:.2f}, {color1[2]:.2f}), Secondary RGB({color2[0]:.2f}, {color2[1]:.2f}, {color2[2]:.2f})")
    if GENERATED_HDRI:
        print(f"HDRI background: {GENERATED_HDRI}")
    print(f"For MP4 creation, use: flag_sample_{GENERATED_WIND_SPEED_1:.1f}_{GENERATED_WIND_SPEED_2:.1f}_{GENERATED_WIND_ANGLE_human_interpretable_1:.1f}_{GENERATED_WIND_ANGLE_human_interpretable_2:.1f}.mp4")

classes = (OBJECT_OT_setup_random_scene,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    for handler in bpy.app.handlers.render_pre:
        if handler.__name__ == 'render_pre_handler':
            bpy.app.handlers.render_pre.remove(handler)
    for handler in bpy.app.handlers.render_complete:
        if handler.__name__ == 'render_complete_handler':
            bpy.app.handlers.render_complete.remove(handler)
    bpy.app.handlers.render_pre.append(render_pre_handler)
    bpy.app.handlers.render_complete.append(render_complete_handler)
    print("Random scene generation handlers registered successfully!")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    for handler in bpy.app.handlers.render_pre:
        if handler.__name__ == 'render_pre_handler':
            bpy.app.handlers.render_pre.remove(handler)
    for handler in bpy.app.handlers.render_complete:
        if handler.__name__ == 'render_complete_handler':
            bpy.app.handlers.render_complete.remove(handler)

if __name__ == "__main__":
    register()
    print("Random scene generator script loaded!")
    print("- For command line: Scene will be randomized automatically when rendering starts")
    print("- For GUI: Run the 'Setup Random Wind, Colors and HDRI' operator from the search menu (F3)")
