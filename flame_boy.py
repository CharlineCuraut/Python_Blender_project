import bpy

def clean(tab) :
    """ Args : 
        tab ([string]) : name of objects we don't want to delete
        Return (void) : delete everything on the scene except objects in tab
    """
    # Select all except objects in tab
    bpy.ops.object.select_all(action='SELECT')
    for obj in tab :
        bpy.data.objects[obj].select_set(False)
    
    # Delete all selected objects
    bpy.ops.object.delete()

    # deselect everything
    bpy.ops.object.select_all(action='DESELECT')


clean(['Camera','Light'])
bpy.data.objects['Camera'].location = (0, 13.5, 4.5)


################################### HEAD ###################################

def head(radius=1, z_translation=1, proportional_size=1.8, name='Head') :
    """ Args :
        Subdivisions (int) : number of subdivisions for the creation of the ico_sphere
        Radius (float) : radius of the head
        z_translation (float) : stretching of the drop
        proportional_size (float) : proportion to edit SHARP
        name (string) : name of the mesh
        Return (bpy.data.object) : a drop shape (that will be a head here)
    """
    
    # creation of the sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        #subdivisions = subdivisions,
        radius = radius
    )

    ### selecting the right half of the sphere to apply the mirror modifier
    sphere = bpy.context.object.data
    # desactivate faces
    sphere.polygons.foreach_set("select", (False,) * len(sphere.polygons))
    # desactivate edges
    sphere.edges.foreach_set("select", (False,) * len(sphere.edges))
    # select the right vertices
    sphere.vertices.foreach_set(
            "select",
            [False]*6 + ([True]*75 + [False] + [True]*150) + [False]*250
    )
    # print(len(sphere.vertices)) --> 482
    # suppression of the right half of the sphere
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')

    ## add modifier mirror to head
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_add(type='MIRROR')

    sphere.vertices.foreach_set(
            "select",
            [False]*6 + [True]*1 + [False]*250
    )
    # print(len(sphere.vertices)) --> 257
    bpy.ops.object.mode_set(mode='EDIT')
    ### sphere shape to drop shape
    bpy.ops.transform.translate(value=(0,0,z_translation), 
                            constraint_axis=(False, False, True),
                            orient_type='GLOBAL',
                            orient_matrix_type='GLOBAL',
                            mirror=True, 
                            use_proportional_edit=True,
                            use_proportional_connected=False,
                            proportional_edit_falloff='SHARP',
                            proportional_size=proportional_size)

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

    sphere = bpy.data.objects['Sphere']
    sphere.name = name

    # return object reference
    return bpy.context.object

### linking "Fire" material to the head
head = head() 


################################### BODY ###################################

def extrusion_members(length=0.75) :
    """ Args :
        length (float) : length of the character's arms and legs
        return (void) : create a member
    """
    # mode edit activated
    bpy.ops.object.mode_set(mode='EDIT')
    # extrusion
    bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={
                                "value":(-3.55271e-15, 0, length), 
                                "orient_axis_ortho":'X', 
                                "orient_type":'NORMAL',  
                                "orient_matrix_type":'NORMAL', 
                                "constraint_axis":(True, True, True), 
                                "proportional_edit_falloff":'LINEAR'})
    # scale the hand/feet to make a single point
    bpy.ops.transform.resize(value=(0.0446274, 0.0446274, 0.0446274))
    # merge all the hands/foot points
    bpy.ops.mesh.remove_doubles(threshold=0.1)
    

def body(radius=0.80, location=(0.0, 0.0, -1.55), z_translation_bottom=0.175, proportional_size_body=0.9, length=0.9, name='Body') :
    """ Args :
        Subdivisions (int) : number of subdivisions for the creation of the ico_sphere
        Radius (float) : radius of the head
        Location (float) : location of the sphere
        z_translation (float) : stretching of the drop
        proportional_size (float) : proportion to edit SHARP
        name (string) : name of the mesh
        Return (bpy.data.object) : a drop shape (that will be a head here)
    """
    
    # creation of the sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius = radius,
        location = location
    )
    
    ### selecting the right half of the sphere to apply the mirror modifier
    sphere = bpy.context.object.data
    # desactivate faces
    sphere.polygons.foreach_set("select", (False,) * len(sphere.polygons))
    # desactivate edges
    sphere.edges.foreach_set("select", (False,) * len(sphere.edges))
    # select the right vertices
    sphere.vertices.foreach_set(
            "select",
            [False]*10 + [True]*225 + [False]*246
    )
    # print(len(sphere.vertices)) #--> 482
    # suppression of the right half of the sphere
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')

    ## add modifier mirror to body
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_add(type='MIRROR')
    
    

    ### selecting only the one lower vertex on the sphere
    sphere = bpy.context.object.data
    # desactivate faces
    sphere.polygons.foreach_set("select", (False,) * len(sphere.polygons))
    # desactivate edges
    sphere.edges.foreach_set("select", (False,) * len(sphere.edges))
    # select only lower vert 
    sphere.vertices.foreach_set(
        "select",
        [False]*40 + [True] + [False]*216
    )
    # print(len(sphere.vertices)) #--> 257

    ### flattening the bottom of the body
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.translate(value=(0,0,z_translation_bottom), 
                            constraint_axis=(False, False, True),
                            orient_type='GLOBAL',
                            orient_matrix_type='GLOBAL',
                            mirror=True, 
                            use_proportional_edit=True,
                            use_proportional_connected=False,
                            proportional_edit_falloff='SMOOTH',
                            proportional_size=proportional_size_body)
                            
    
    ### select vertices for left leg  
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Sphere'].select_set(True)
                        
    sphere = bpy.context.object.data
    sphere.polygons.foreach_set("select", (False,) * len(sphere.polygons))
    sphere.edges.foreach_set("select", (False,) * len(sphere.edges))
    sphere.vertices.foreach_set(
        "select",
        [False]*102 + 5*([False]*11 + [True]*4) + [False]*80
    )
    # print(len(sphere.vertices)) #--> 257
    #extrusion + resize + merge_by_distance
    extrusion_members(length)
    
    
    ### select vertices for left arm 
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Sphere'].select_set(True)
    sphere = bpy.context.object.data
    sphere.polygons.foreach_set("select", (False,) * len(sphere.polygons))
    sphere.edges.foreach_set("select", (False,) * len(sphere.edges)) 
    sphere.vertices.foreach_set(
        "select",
        [False]*120 + [True]*4 + [False]*9 + [True]*4 + [False]*9 + [True]*4 + [False]*102
    )
    # print(len(sphere.vertices)) #--> 252
    # extrusion + resize + merge_by_distance
    extrusion_members(length)
    # correction of the orientation of the arms for the T pose
    bpy.ops.transform.translate(value=(0, 0, -0.2))
        
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

    sphere = bpy.data.objects['Sphere']
    sphere.name = name
    
    # return object reference
    return bpy.context.object

## applying fire_inverse material on the body
body = body()
bpy.data.objects['Head'].select_set(True)
bpy.ops.object.join()


################################### FIRE ASPECT ###################################


body.data.materials.append(bpy.data.materials['Fire_full_body'])
    
### create the texture
tex = bpy.data.textures.new("Marble", 'MARBLE')
bpy.data.textures["Marble"].type = 'MARBLE'
bpy.data.textures["Marble"].noise_scale = 0.4


### add modifier + animation
# new axis for the animation
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(3, 0, 0), scale=(1, 1, 1))
# new modifier to look like fire
modifier = body.modifiers.new(name="Displace", type='DISPLACE')
modifier.texture = bpy.data.textures['Marble']
modifier.strength = 0.14
# link between modifier and new axis
modifier.texture_coords = 'OBJECT'
modifier.texture_coords_object = bpy.data.objects["Empty"]

# applying modifier to the main object
bpy.ops.object.modifier_apply(modifier='Displace')


### selecting only empty
empty = bpy.data.objects['Empty']
bpy.ops.object.select_all(action='DESELECT')
empty.select_set(True)


### animation
scene = bpy.context.scene
frameStart = 0
frameEnd = 100
scene.frame_start = frameStart
scene.frame_end = frameEnd

# set the keyframe at frame 1
empty.keyframe_insert(data_path='location', index=2, frame=frameStart)
# set the keyframe at frame 100
empty.location.z += 12
empty.keyframe_insert(data_path='location', index=2, frame=frameEnd)

# ensure the action is still available
if empty.animation_data.action:
    # and store it in a convenience variable
    my_action = bpy.data.actions.get(empty.animation_data.action.name)
    my_fcu = my_action.fcurves.find("location", index=2)
    # for all points
    for pt in my_fcu.keyframe_points:
        pt.interpolation = 'LINEAR'


################################### EYES ###################################

def eye(location, name) :
    """ Args :
        location (Vector) : location of the eye
        name (string) : name of the eye
        return a sphere that will be an eye
    """
    #dimensions = (0.2010, 0.4875, 0.1157)
    #rotation_euler = (1.5708, 0.0, 0.0)
    # creation of eye
    eye = bpy.ops.mesh.primitive_uv_sphere_add(
        location = location,
        scale = (-0.1005, -0.2438, 0.0579)
    )
    
    bpy.ops.transform.rotate(value=1.5708, orient_axis='X')
    
    bpy.ops.object.shade_smooth()
    sphere = bpy.data.objects['Sphere']
    sphere.name = name
    
    return bpy.context.object

eye_left = eye((-0.35, 1.0, 0.0), "Left_eye")
eye_right = eye((0.35, 1.0, 0.0), "Right_eye")
    

# creation of eye material
mat_black = bpy.data.materials.new("Black")
mat_black.use_nodes = False
mat_black.diffuse_color = (0,0,0,1)
    
eye_left.data.materials.append(mat_black)
eye_right.data.materials.append(mat_black)


## placing the legs at z = 0 (approximately)
bpy.data.objects['Body'].select_set(True)
bpy.data.objects['Left_eye'].select_set(True)
bpy.data.objects['Right_eye'].select_set(True)
bpy.ops.transform.translate(value=(0,0,3))



################################### ARMATURE ###################################
## armature added and put in front mode (so that we can see it through the body)
bpy.ops.object.armature_add(enter_editmode=False, 
                            align='WORLD', 
                            location=(0, 0, 0), 
                            scale=(1, 1, 1)
                            )
bpy.context.object.show_in_front = True

# correctiong the size of the column
bpy.ops.object.mode_set(mode='EDIT')
obArmature = bpy.context.active_object #get the armature object
ebs = obArmature.data.edit_bones
ebs["Bone"].head = (0, 0, 0.87)
ebs["Bone"].tail = (0, 0, 1.97)

## defining a function to add bones to armature (with a parent/child relation)
def add_bone(name_parent, name_child, head_pos, tail_pos, tail=True) :
    """ Args :
        name_parent (string) : name of the parent bone
        name_child (string) : name of the child bone
        head_pos (Vector) : position of the child bone head
        tail_pos (Vector) : position of the child bone tail
        tail (boolean) : True if the child is connected to his parent by the parent's tail (else False)
        return (void) : create a bone and add it in the armature of the character
    """
    obArmature = bpy.context.active_object #get the armature object
    ebs = obArmature.data.edit_bones
    eb_new = ebs.new(name_child)
    # defining a parent/child relation between the two bones 
    parent = ebs[name_parent]
    child = eb_new
    if tail :
        # This line moves the parent's tail to the correct location
        parent.tail = head_pos
    else :
        parent.head = head_pos
    # This line moves the child's head to the correct location
    child.head = head_pos
    child.tail = tail_pos
    # The next lines make the connect
    child.parent = parent
    if tail :
        child.use_connect = True
    else : 
        child.use_connect = False
    
## adding all the bones
add_bone("Bone", "Head", (0, 0, 1.97), (0, 0, 3), True)
add_bone("Bone", "Shoulder.L", (0, 0, 1.97), (-0.5, 0, 1.97), True)
add_bone("Bone", "Shoulder.R", (0, 0, 1.97), (0.5, 0, 1.97), True)
add_bone("Shoulder.L", "Arm.L", (-0.5, 0, 1.97), (-1.2, 0, 1.97), True)
add_bone("Shoulder.R", "Arm.R", (0.5, 0, 1.97), (1.2, 0, 1.97), True)    
add_bone("Bone", "Hip.L", (0, 0, 0.87), (-0.47, 0, 0.87), False)
add_bone("Bone", "Hip.R", (0, 0, 0.87), (0.47, 0, 0.87), False)
add_bone("Hip.L", "Leg.L", (-0.47, 0, 0.87), (-0.5, 0, 0.27), True)
add_bone("Hip.R", "Leg.R", (0.47, 0, 0.87), (0.5, 0, 0.27), True)
add_bone("Head", "Eye.L", (0, 0, 3), (-0.35, 0.8, 3), True)
add_bone("Head", "Eye.R", (0, 0, 3), (0.35, 0.8, 3), True)


bpy.ops.object.mode_set(mode='OBJECT')


## set parent with automatic weight (linking the armature to the body)
# NOTE : the active object is the last object that have been modify so there it is the 
# armature (that will be the parent of all selected object aka the body and both eyes)
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Armature'].select_set(True)
bpy.data.objects['Body'].select_set(True)
bpy.data.objects['Left_eye'].select_set(True)
bpy.data.objects['Right_eye'].select_set(True)
bpy.ops.object.parent_set(type='ARMATURE_AUTO', keep_transform=True)


# changing the armature's name (that one is for the flamme guy, if there is enough time, 
# there will be another one for the water girl)
armature_guy = bpy.data.objects['Armature']
armature_guy.name = 'Armature_guy'


## changing the weight of the vertices in the Leg.L and Arm.L vertex group of the body 
# (for the animation : a movement there won't change the body shape)
# and because the body has a miror modifier, the weight of the vertices of Leg.R and 
# Arm.R will be also change
bpy.context.view_layer.objects.active = bpy.data.objects['Armature_guy'].children[0]

guy = bpy.context.active_object
# we simply remove the vertices of the vertex group Leg.L that are above a certain heigh 
# and those that are on the back or on the stomach
for v in guy.data.vertices :
    if v.co[2] >= -0.5 or v.co[1]>=0.3 or v.co[1]<=-0.3 :
        #print("vertex found")
        for group in guy.vertex_groups :
            if group.index in [v.groups[i].group for i in range(len(v.groups))] :
                if group.name == "Leg.L":
                    #print("group found")
                    #print(group.name)
                    #print(v.index)
                    group.remove([v.index])
body.data.update

# now for the arms, we use the same method for the Arm.L vertex group
for v in guy.data.vertices :
    if v.co[2] <= 0.2 or v.co[2]>=0.6 or v.co[1]>=0.25 or v.co[1]<=-0.25 :
        for group in guy.vertex_groups :
            if group.index in [v.groups[i].group for i in range(len(v.groups))] :
                if group.name == "Arm.L":
                    group.remove([v.index])
body.data.update


# the lign under is to print all the vertices belonging to a certain vertex group 
#print([vert for vert in body.data.vertices if body.vertex_groups['Leg.L'].index in [i.group for i in vert.groups]])

## hiding the bones in all mode except edit mode
for bone in armature_guy.data.bones :
    bone.hide = True


################################### ANIMATION ###################################

### selecting only empty
bpy.ops.object.select_all(action='DESELECT')
armature_guy.select_set(True)


### animation
"""
scene = bpy.context.scene
frameStart = 1
frameEnd = 100
scene.frame_start = frameStart
scene.frame_end = frameEnd
"""


def insert_kf_armature(frame_fn) :
    """ Args :
        frame_fn (int) : the point at which we insert the keyframe
        return (void) : insert a key frame for every bone of the armature
    """
    for bone in armature_guy.data.bones :
        dp = 'pose.bones["' + bone.name
        dp_l = dp + '"].location'
        dp_r = dp + '"].rotation_quaternion'
        dp_s = dp + '"].scale'
        armature_guy.keyframe_insert(data_path=dp_l, frame=frame_fn)
        armature_guy.keyframe_insert(data_path=dp_r, frame=frame_fn)
        armature_guy.keyframe_insert(data_path=dp_s, frame=frame_fn)
 
     
# set the keyframe at frame 1 (all the bones are at an initial position)
insert_kf_armature(frameStart) 

# set the keyframe at frame 10
armature_guy.pose.bones["Bone"].rotation_quaternion = (0.998, -0.00089, 0.005, -0.064)
armature_guy.pose.bones["Hip.L"].rotation_quaternion = (0.997, -0.080, -0.001, -0.006)
armature_guy.pose.bones["Leg.R"].rotation_quaternion = (0.996, 0.005, 0.007, -0.088)
insert_kf_armature(10)

# set the keyframe at frame 20
armature_guy.pose.bones["Head"].rotation_quaternion = (0.996, 0.003, -0.004, -0.085)
armature_guy.pose.bones["Arm.R"].rotation_quaternion = (0.974, -0.227, 0.014, -0.004)
armature_guy.pose.bones["Arm.L"].rotation_quaternion = (0.911, 0.413, -0.019, -0.006)
insert_kf_armature(20)

# wave movement on frame 30 to 70
for i in range(30,71,20) :
    armature_guy.pose.bones["Arm.L"].rotation_quaternion = (1, 0, 0, 0)
    insert_kf_armature(i)
    armature_guy.pose.bones["Arm.L"].rotation_quaternion = (0.911, 0.413, -0.019, -0.006)
    insert_kf_armature(i+10)

# set the keyframe at frame 90
armature_guy.pose.bones["Head"].rotation_quaternion = (1, 0, 0, 0)
armature_guy.pose.bones["Arm.R"].rotation_quaternion = (1, 0, 0, 0)
armature_guy.pose.bones["Arm.L"].rotation_quaternion = (1, 0, 0, 0)
insert_kf_armature(90)

# set the keyframe at frame 100
armature_guy.pose.bones["Bone"].rotation_quaternion = (1, 0, 0, 0)
armature_guy.pose.bones["Hip.L"].rotation_quaternion = (1, 0, 0, 0)
armature_guy.pose.bones["Leg.R"].rotation_quaternion = (1, 0, 0, 0)
insert_kf_armature(frameEnd)


bpy.ops.screen.animation_play()


#################################### water ball #####################################

bpy.ops.mesh.primitive_uv_sphere_add(
        radius = 1,
        location = (-4,0,3)
    )
bpy.ops.object.shade_smooth()
bpy.data.objects['Sphere'].data.materials.append(bpy.data.materials['water'])



############################ Shader attempt ###########################

### head shading

#bpy.context.scene.eevee.use_bloom = True
# create a new material resource
#mat = bpy.data.materials.new("Fire up")
# enable the node-graph edition mode
#mat.use_nodes = True
# clear all starter nodes
#nodes = mat.node_tree.nodes
#nodes.clear()

# add Texture Coordinate
#node_tex_coor = nodes.new(type="ShaderNodeTexCoord")

# add Mapping
#node_mapping = nodes.new(type="ShaderNodeMapping")
# (input[1] is location), here we change the x field
#node_mapping.inputs[1].default_value[0] = 0.9
# (input[2] is rotation), here we change the y field
#node_mapping.inputs[2].default_value[1] = -90
# (input[3] is scale), here we change the z field
#node_mapping.inputs[3].default_value[2] = 0.35

# add Gradient Texture
#node_grad_tex = nodes.new(type="ShaderNodeTexGradient")

# add ColorRamp 
## Problem ??

#fire_strength = 5.0
# add the Emission node
#node_emission = nodes.new(type="ShaderNodeEmission")
# (input[1] is the strength)
#node_emission.inputs[1].default_value = fire_strength

