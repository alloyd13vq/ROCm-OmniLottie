import torch
import re
import json
from typing import Union, List, Dict, Tuple, Optional, Any
import difflib
from .test2_0518 import *
import numpy as np
#from test_0819 import *



class LottieTensor:
    # Command type constants (添加新的命令常量)
    tokenizer = None
    CMD_ANIMATION = 0 
    CMD_LAYER = 1 
    CMD_TRANSFORM = 2 
    CMD_POSITION = 3
    CMD_KEYFRAME = 4
    CMD_POSITION_END = 5
    CMD_SCALE = 6
    CMD_SCALE_END = 7
    CMD_ROTATION = 8
    CMD_OPACITY = 9
    CMD_OPACITY_END = 10
    CMD_ANCHOR = 11 
    CMD_GROUP = 12 
    CMD_GROUP_END = 13 
    CMD_TRANSFORM_SHAPE = 14 
    CMD_PATH = 15 
    CMD_PATH_END = 16 
    CMD_POINT = 17 
    CMD_FILL = 18 
    CMD_GRADIENT_FILL = 19 
    CMD_GRADIENT_FILL_END = 20 
    CMD_START_POINT = 21 
    CMD_END_POINT = 22 
    CMD_GRADIENT_TYPE = 23 
    CMD_HIGHLIGHT_LENGTH = 24
    CMD_HIGHLIGHT_ANGLE = 25 
    CMD_TRANSFORM_END = 26
    CMD_LAYER_END = 27
    CMD_PAD = 28
    CMD_EOS = 29
    CMD_SOS = 30 
    CMD_RECT = 31
    CMD_RECT_END = 32
    CMD_SIZE = 33
    CMD_ROUNDED = 34
    CMD_ELLIPSE = 35
    CMD_ELLIPSE_END = 36
    CMD_STROKE = 37
    CMD_SKEW = 38
    CMD_SKEW_AXIS = 39
    CMD_ASSET = 40
    CMD_ASSET_END = 41
    CMD_PARENT = 42
    CMD_NULL_LAYER = 43
    CMD_NULL_LAYER_END = 44
    CMD_PRECOMP_LAYER = 45
    CMD_PRECOMP_LAYER_END = 46
    CMD_REFERENCE_ID = 47
    CMD_DIMENSIONS = 48
    CMD_ROTATION_END = 49
    CMD_STAR = 50
    CMD_STAR_END = 51
    CMD_INNER_RADIUS = 52
    CMD_OUTER_RADIUS = 53
    CMD_INNER_ROUNDNESS = 54
    CMD_OUTER_ROUNDNESS = 55
    CMD_POINTS = 56
    CMD_STAR_ROTATION = 57
    CMD_TRIM = 58
    CMD_TRIM_END = 59
    CMD_START = 60
    CMD_END = 61
    CMD_OFFSET = 62
    CMD_MULTIPLE = 63
    CMD_REPEATER = 64
    CMD_REPEATER_END = 65
    CMD_COPIES = 66
    CMD_REPEATER_OFFSET = 67
    CMD_COMPOSITE = 68
    CMD_REPEATER_TRANSFORM = 69
    CMD_REPEATER_TRANSFORM_END = 70
    CMD_GRADIENT_STROKE = 71
    CMD_GRADIENT_STROKE_END = 72
    CMD_WIDTH = 73
    CMD_LINE_CAP = 74
    CMD_LINE_JOIN = 75
    CMD_MITER_LIMIT = 76
    CMD_MERGE = 77
    CMD_MERGE_END = 78
    CMD_MERGE_MODE = 79
    CMD_ROUNDED_CORNERS = 80
    CMD_ROUNDED_CORNERS_END = 81
    CMD_RADIUS = 82
    CMD_TWIST = 83
    CMD_TWIST_END = 84
    CMD_ANGLE = 85
    CMD_CENTER = 86
    CMD_BEZIER = 87
    CMD_BEZIER_END = 88
    CMD_TEXT_LAYER = 89
    CMD_TEXT_LAYER_END = 90
    CMD_TEXT_DATA = 91
    CMD_TEXT_DATA_END = 92
    CMD_DOCUMENT = 93
    CMD_SOLID_LAYER = 94
    CMD_SOLID_LAYER_END = 95
    CMD_POSITION_X = 96
    CMD_POSITION_Y = 97
    CMD_POSITION_Z = 98
    CMD_POSITION_X_END = 99
    CMD_POSITION_Y_END = 100
    CMD_POSITION_Z_END = 101
    CMD_SCALE_X = 102
    CMD_SCALE_Y = 103
    CMD_SCALE_Z = 104
    CMD_SCALE_X_END = 105
    CMD_SCALE_Y_END = 106
    CMD_SCALE_Z_END = 107
    CMD_ROTATION_X = 108
    CMD_ROTATION_Y = 109
    CMD_ROTATION_Z = 110
    CMD_ROTATION_X_END = 111
    CMD_ROTATION_Y_END = 112
    CMD_ROTATION_Z_END = 113
    CMD_EFFECTS = 114
    CMD_EFFECTS_END = 115
    CMD_EFFECT = 116
    CMD_EFFECT_END = 117
    CMD_HAS_MASK = 118
    CMD_MASKS_PROPERTIES = 119
    CMD_CT = 120
    CMD_EF = 121
    CMD_TT = 122
    CMD_TP = 123
    CMD_TD = 124
    CMD_HD = 125
    CMD_CL = 126
    CMD_LN = 127
    CMD_AO = 128
    CMD_ANCHOR_END = 129
    CMD_OPACITY_FILL = 130
    CMD_FILL_RULE = 131
    CMD_COLOR_DIM = 132
    CMD_DDD = 133
    CMD_MARKERS = 134
    CMD_PROPS = 135
    CMD_ORIGINAL_COLORS = 136
    CMD_COLOR_POINTS = 137
    CMD_COLORS = 138
    CMD_ML2 = 139
    CMD_ML2_IX = 140
    CMD_OFFSET_IX = 141
    CMD_TR_P_IX = 142
    CMD_TR_A_IX = 143
    CMD_TR_SCALE = 144
    CMD_TR_S_IX = 145
    CMD_TR_R_IX = 146
    CMD_TR_SO_IX = 147
    CMD_TR_EO_IX = 148
    CMD_KEYFRAME_END = 149
    CMD_POSITION_EXPR = 150
    CMD_SCALE_EXPR = 151
    CMD_ROTATION_EXPR = 152
    CMD_WIDTH_KEYFRAME = 153  # 新增
    CMD_WIDTH_ANIMATED_END = 154  # 新增
    CMD_FONTS = 155
    CMD_FONTS_END = 156
    CMD_FONT = 157
    CMD_CHARS = 158
    CMD_CHARS_END = 159
    CMD_CHAR = 160
    CMD_CHAR_END = 161
    CMD_CHAR_SHAPES = 162
    CMD_CHAR_SHAPES_END = 163
    CMD_TEXT_KEYFRAMES = 164
    CMD_TEXT_KEYFRAMES_END = 165
    CMD_TEXT_KEYFRAME = 166
    CMD_TEXT_DOC = 167
    CMD_TEXT_DOC_END = 168
    CMD_FONT_SIZE = 169
    CMD_FONT_FAMILY = 170
    CMD_TEXT = 171
    CMD_CA = 172
    CMD_JUSTIFY = 173
    CMD_TRACKING = 174
    CMD_LINE_HEIGHT = 175
    CMD_LETTER_SPACING = 176
    CMD_FILL_COLOR = 177
    CMD_MORE_OPTIONS = 178
    CMD_MORE_OPTIONS_END = 179
    CMD_G = 180
    CMD_ALIGNMENT = 181
    CMD_ALIGNMENT_K = 182
    CMD_ALIGNMENT_IX = 183
    CMD_DROPDOWN = 184
    CMD_IGNORED = 185 
    CMD_SLIDER = 186
    CMD_COLOR = 187
    CMD_OPACITY_ANIMATED = 188
    CMD_OPACITY_KEYFRAME = 189
    CMD_MASKS_PROPERTIES_END = 190
    CMD_MASK = 191
    CMD_MASK_END = 192
    CMD_MASK_PT = 193
    CMD_MASK_PT_END = 194
    CMD_MASK_PT_K = 195
    CMD_MASK_PT_K_END = 196
    CMD_MASK_PT_K_I = 197
    CMD_MASK_PT_K_O = 198
    CMD_MASK_PT_K_V = 199
    CMD_MASK_O = 200
    CMD_MASK_X = 201
    CMD_TM = 202
    CMD_TM_END = 203
    CMD_MASK_PT_K_ARRAY = 204
    CMD_MASK_PT_K_ARRAY_END = 205
    CMD_MASK_PT_KEYFRAME = 206
    CMD_MASK_PT_KEYFRAME_END = 207
    CMD_MASK_PT_KF_I = 208
    CMD_MASK_PT_KF_O = 209
    CMD_MASK_PT_KF_S = 210
    CMD_MASK_PT_KF_S_END = 211
    CMD_MASK_PT_KF_SHAPE = 212
    CMD_MASK_PT_KF_SHAPE_END = 213
    CMD_MASK_PT_KF_SHAPE_I = 214
    CMD_MASK_PT_KF_SHAPE_O = 215
    CMD_MASK_PT_KF_SHAPE_V = 216
    CMD_VALUE = 217
    CMD_VALUE_END = 218
    CMD_TR_POSITION = 219
    CMD_TR_ANCHOR = 220
    CMD_TR_ROTATION = 221
    CMD_TR_START_OPACITY = 222
    CMD_TR_END_OPACITY = 223
    CMD_ZIG_ZAG = 224
    CMD_ZIG_ZAG_END = 225
    CMD_FREQUENCY = 226
    CMD_AMPLITUDE = 227
    CMD_POINT_TYPE = 228
    CMD_ANIMATORS = 229
    CMD_ANIMATORS_END = 230
    CMD_ANIMATOR = 231
    CMD_ANIMATOR_END = 232
    CMD_RANGE_SELECTOR = 233
    CMD_RANGE_SELECTOR_END = 234
    CMD_RANGE_START = 235
    CMD_RANGE_START_END = 236
    CMD_RANGE_START_KEYFRAME = 237
    CMD_AMOUNT = 238
    CMD_MAX_EASE = 239
    CMD_MIN_EASE = 240
    CMD_ANIMATOR_PROPERTIES = 241
    CMD_ANIMATOR_PROPERTIES_END = 242
    CMD_OPACITY_ANIMATED_END = 243
    CMD_MASK_PT_K_C = 244
    CMD_RANGE_END = 245
    CMD_RANGE_END_END = 246
    CMD_RANGE_END_KEYFRAME = 247
    CMD_END_END = 248
    CMD_START_END = 249
    CMD_OFFSET_END = 250
    CMD_POINTS_STAR = 251
    CMD_RANGE_OFFSET = 252
    CMD_RANGE_OFFSET_END = 253
    CMD_RANGE_OFFSET_KEYFRAME = 254
    CMD_S_M = 255
    CMD_OPACITY_ANIMATORS = 256
    CMD_SCALE_ANIMATORS = 257
    CMD_SCALE_ANIMATORS_END = 258
    CMD_ROTATION_ANIMATORS = 259
    CMD_ROTATION_ANIMATORS_END = 260
    CMD_POSITION_ANIMATORS = 261
    CMD_POSITION_ANIMATORS_END = 262
    CMD_TRACKING_ANIMATORS = 263
    CMD_OPACITY_ANIMATORS_END = 264
    CMD_COLOR_KEYFRAME = 265  # Add this constant
    CMD_COLOR_ANIMATED_END = 266 
    CMD_DASHES = 267
    CMD_DASHES_END = 268
    CMD_DASH = 269
    CMD_DASH_OFFSET = 270
    CMD_LAYER_EFFECT = 271 
    CMD_NO_VALUE = 272
    CMD_WIDTH_ANIMATED = 273   # Add this if it doesn't exist
    CMD_SIZE_END = 274
    CMD_RECT_SIZE = 275  # Add this new constant
    CMD_ELLIPSE_SIZE = 276 
    CMD_RECT_ROUNDED = 277  # Add this new constant for animated rect_rounded
    CMD_RECT_ROUNDED_END = 278
    CMD_DASH_ANIMATED = 279  # New constant
    CMD_DASH_KEYFRAME = 280   # New constant  
    CMD_DASH_ANIMATED_END = 281  # New constant
    
    # Command names mapped to their numeric constants
    COMMANDS = [
        "animation",          # 0
        "layer",             # 1
        "transform",         # 2
        "position",          # 3
        "keyframe",          # 4
        "/position",         # 5
        "scale",             # 6
        "/scale",            # 7
        "rotation",          # 8
        "opacity",           # 9
        "/opacity",          # 10
        "anchor",            # 11
        "group",             # 12
        "/group",            # 13
        '"TransformShape"',  # 14
        "path",              # 15
        "/path",             # 16
        "point",             # 17
        "fill",              # 18
        "gradient_fill",     # 19
        "/gradient_fill",    # 20
        "start_point",       # 21
        "end_point",         # 22
        "gradient_type",     # 23
        "highlight_length",  # 24
        "highlight_angle",   # 25
        "/transform",        # 26
        "/layer",            # 27
        "PAD",               # 28
        "EOS",               # 29
        "SOS",               # 30
        "rect",              # 31
        "/rect",             # 32
        "size",              # 33
        "rounded",           # 34
        "ellipse",           # 35
        "/ellipse",          # 36
        "stroke",            # 37
        "skew",              # 38
        "skew_axis",         # 39
        "asset",             # 40
        "/asset",            # 41
        "parent",            # 42
        "null_layer",        # 43
        "/null_layer",       # 44
        "precomp_layer",     # 45
        "/precomp_layer",    # 46
        "reference_id",      # 47
        "dimensions",        # 48
        "/rotation",         # 49
        "star",              # 50
        "/star",             # 51
        "inner_radius",      # 52
        "outer_radius",      # 53
        "inner_roundness",   # 54
        "outer_roundness",   # 55
        "points",            # 56
        "star_rotation",     # 57
        "trim",              # 58
        "/trim",             # 59
        "start",             # 60
        "end",               # 61
        "offset",            # 62
        "multiple",          # 63
        "repeater",          # 64
        "/repeater",         # 65
        "copies",            # 66
        "repeater_offset",   # 67
        "composite",         # 68
        "repeater_transform", # 69
        "/repeater_transform", # 70
        "gradient_stroke",   # 71
        "/gradient_stroke",  # 72
        "width",             # 73
        "line_cap",          # 74
        "line_join",         # 75
        "miter_limit",       # 76
        "merge",             # 77
        "/merge",            # 78
        "merge_mode",        # 79
        "rounded_corners",   # 80
        "/rounded_corners",  # 81
        "radius",            # 82
        "twist",             # 83
        "/twist",            # 84
        "angle",             # 85
        "center",            # 86
        "bezier",            # 87
        "/bezier",           # 88
        "text_layer",        # 89
        "/text_layer",       # 90
        "text_data",         # 91
        "/text_data",        # 92
        "document",          # 93
        "solid_layer",       # 94
        "/solid_layer",      # 95
        "position_x",        # 96
        "position_y",        # 97
        "position_z",        # 98
        "/position_x",       # 99
        "/position_y",       # 100
        "/position_z",       # 101
        "scale_x",           # 102
        "scale_y",           # 103
        "scale_z",           # 104
        "/scale_x",          # 105
        "/scale_y",          # 106
        "/scale_z",          # 107
        "rotation_x",        # 108
        "rotation_y",        # 109
        "rotation_z",        # 110
        "/rotation_x",       # 111
        "/rotation_y",       # 112
        "/rotation_z",       # 113
        "effects",           # 114
        "/effects",          # 115
        "effect",            # 116
        "/effect",           # 117
        "hasMask",           # 118
        "masksProperties",   # 119
        "ct",                # 120
        "ef",                # 121
        "tt",                # 122
        "tp",                # 123
        "td",                # 124
        "hd",                # 125
        "cl",                # 126
        "ln",                # 127
        "ao",                # 128
        "/anchor",           # 129
        "opacity_fill",      # 130
        "fill_rule",         # 131
        "color_dim",         # 132
        "ddd",               # 133
        "markers",           # 134
        "props",             # 135
        "original_colors",   # 136
        "color_points",      # 137
        "colors",            # 138
        "ml2",               # 139
        "ml2_ix",            # 140
        "offset_ix",         # 141
        "tr_p_ix",           # 142
        "tr_a_ix",           # 143
        "tr_scale",          # 144
        "tr_s_ix",           # 145
        "tr_r_ix",           # 146
        "tr_so_ix",          # 147
        "tr_eo_ix",          # 148
        "/keyframe",         # 149
        "position_expr",     # 150
        "scale_expr",        # 151
        "rotation_expr",     # 152
        "width_keyframe",    # 153  # 新增
        "/width_animated",   # 154  # 新增
        "fonts",              # 155
        "/fonts",            # 156
        "font",              # 157
        "chars",             # 158
        "/chars",            # 159
        "char",              # 160
        "/char",             #161
        "char_shapes",       # 162
        "/char_shapes",      # 163
        "text_keyframes",    # 164
        "/text_keyframes",   # 165
        "text_keyframe",     # 166
        "text_doc",          # 167
        "/text_doc",         # 168
        "font_size",         # 169
        "font_family",       # 170
        "text",              # 171
        "ca",                # 172
        "justify",           # 173
        "tracking_animators", # 174
        "line_height",       # 175
        "letter_spacing",    # 176
        "fill_color",        # 177
        "more_options",      # 178
        "/more_options",     # 179
        "g",                 # 180
        "alignment",         # 181
        "alignment_k",       # 182
        "alignment_ix",      # 183
        "dropdown",          # 184
        "ignored",           # 185
        "slider",            # 186
        "color",             # 187
        "opacity_animated",  # 188
        "opacity_keyframe",  # 189
        "/masksProperties",  # 190
        "mask",              # 191
        "/mask",             # 192
        "mask_pt",           # 193
        "/mask_pt",          # 194
        "mask_pt_k",         # 195
        "/mask_pt_k",        # 196
        "mask_pt_k_i",       # 197
        "mask_pt_k_o",       # 198
        "mask_pt_k_v",       # 199
        "mask_o",            # 200
        "mask_x",            # 201
        "tm",                # 202
        "/tm",               # 203
        "mask_pt_k_array",       # 204
        "/mask_pt_k_array",      # 205
        "mask_pt_keyframe",      # 206
        "/mask_pt_keyframe",     # 207
        "mask_pt_kf_i",          # 208
        "mask_pt_kf_o",          # 209
        "mask_pt_kf_s",          # 210
        "/mask_pt_kf_s",         # 211
        "mask_pt_kf_shape",      # 212
        "/mask_pt_kf_shape",     # 213
        "mask_pt_kf_shape_i",    # 214
        "mask_pt_kf_shape_o",    # 215
        "mask_pt_kf_shape_v",    # 216
        "value",              # 217
        "/value",             # 218
        "tr_position",       # 219
        "tr_anchor",         # 220
        "tr_rotation",       # 221
        "tr_start_opacity",  # 222
        "tr_end_opacity",    # 223
        "zig_zag",           # 224
        "/zig_zag",          # 225
        "frequency",         # 226
        "amplitude",         # 227
        "point_type",        # 228
        "animators",         # 229
        "/animators",        # 230
        "animator",          # 231
        "/animator",         # 232
        "range_selector",    # 233
        "/range_selector",   # 234
        "range_start",       # 235
        "/range_start",      # 236
        "range_start_keyframe", # 237
        "amount",            # 238
        "max_ease",          # 239
        "min_ease",          # 240
        "animator_properties", # 241
        "/animator_properties", # 242
        "/opacity_animated",  # 243
        "mask_pt_k_c", #244
        "range_end",              # 245
        "/range_end",             # 246
        "range_end_keyframe",     # 247
        "/end", #248
        "/start" , # 249
        "/offset" , # 250
        "points_star", #251
        "range_offset",        # 252
        "/range_offset",       # 253
        "range_offset_keyframe", # 254
        "s_m",                 # 255
        "opacity_animators",   # 256
        "scale_animators",     # 257
        "/scale_animators",    # 258
        "rotation_animators",  # 259
        "/rotation_animators", # 260
        "position_animators",  # 261
        "/position_animators", # 262
        "tracking_animators",  # 263
        "/opacity_animators", #264
        "color_keyframe",  # 265
        "/color_animated", #266
        "dashes",  # 267
        "/dashes",  # 268
        "dash",  # 269
        "dash_offset",  # 270
        "layer_effect", # 271
        "no_value", #272
        "width_animated" , #273
        "/size", #274
        "rect_size",  # 275  # Add this new command
        "ellipse_size",  # 276
        "rect_rounded",  # 277 
        "/rounded", #278
        "dash_animated",  # 279  # Add this
        "dash_keyframe",  # 280  # Add this
        "/dash_animated", # 281  # Add this
    ]
    
    # Command to index mapping
    COMMAND_TO_IDX = {cmd: idx for idx, cmd in enumerate(COMMANDS)}
    _OFFSET_CACHE = {}

    # Parameter indices for each command type (添加新的Index定义)
    class Index:
        # Animation parameters
        class Animation:
            FR = 0
            IP = 1
            OP = 2
            W = 3
            H = 4
            DDD = 5
            
        class Layer:
            INDEX = 0
            IN_POINT = 1
            OUT_POINT = 2
            START_TIME = 3
            DDD = 4
            HD = 5
            HAS_MASK = 6
            AO = 7
            TT = 8
            TP = 9
            TD = 10
            CT = 11
            CP = 12
            
        
        class Value:
            VALUE = 0
        
        class Transform:
            ANIMATED = 0
            X = 1
            Y = 2
            Z = 3
                
        class Keyframe:
            T = 0
            S1 = 1
            S2 = 2
            S3 = 3
            I_X = 4  # 第一个值，或单值情况
            I_Y = 5  # 第一个值，或单值情况
            O_X = 6  # 第一个值，或单值情况
            O_Y = 7  # 第一个值，或单值情况
            TO1 = 8
            TO2 = 9
            TO3 = 10
            TI1 = 11
            TI2 = 12
            TI3 = 13
            # Multi-dimensional easing (for scale, position, anchor)
            I_X2 = 14
            I_X3 = 15
            I_Y2 = 16
            I_Y3 = 17
            O_X2 = 18
            O_X3 = 19
            O_Y2 = 20
            O_Y3 = 21
            H_FLAG = 22
            E1 = 23
            E2 = 24
            E3 = 25
        
            
        class Tm:
            A = 0
            #IX = 1
        

        class WidthKeyframe:  # 新增
            T = 0
            S = 1
            I_X = 2
            I_Y = 3
            O_X = 4
            O_Y = 5
            
        class Path:
            IX = 0
            IND = 1
            KS_IX = 2
            CLOSED = 3
            HD = 4
            ANIMATED = 5 
            
        class Point:
            X = 0
            Y = 1
            IN_X = 2
            IN_Y = 3
            OUT_X = 4
            OUT_Y = 5
            
        class Fill:
            R = 0
            G = 1
            B = 2
            COLOR_DIM = 3
            HAS_C_A = 4
            HAS_C_IX = 5
            C_IX = 6
            BM = 7
            FILL_RULE = 8
            OPACITY = 9
            COLOR_ANIMATED = 10  # New
            OPACITY_ANIMATED = 11  # New
            HAS_O_A = 12  # New
            HAS_O_IX = 13  # New
            O_IX = 14  # New
        
        class TransformShape:
            POSITION_X = 0
            POSITION_Y = 1
            SCALE_X = 2
            SCALE_Y = 3
            ROTATION = 4
            OPACITY = 5
            ANCHOR_X = 6
            ANCHOR_Y = 7
            SKEW = 8
            SKEW_AXIS = 9
            HD = 10
            
        class Stroke:
            R = 0
            G = 1
            B = 2
            COLOR_DIM = 3
            HAS_C_A = 4
            HAS_C_IX = 5
            C_IX = 6
            BM = 7
            LC = 8
            LJ = 9
            ML = 10
            #WIDTH = 11
            #OPACITY = 12
            WIDTH_ANIMATED = 11  # 新增
            COLOR_ANIMATED = 12  # Add this
            A = 13  # Add alpha channel support

        class Bezier:
            CLOSED = 0
            
        class Group:
            IX = 0
            CIX = 1
            BM = 2
            HD = 3
            NP = 4
            
        class Star:
            D = 0
            SY = 1
        
        class StarValue:  # 新增用于 star 的子命令
            VALUE = 0
        
        class Trim:
            IX = 0
            START = 1
            END = 2
            OFFSET = 3
            MULTIPLE = 4
            
        class TrimValue:
            VALUE = 0
            ANIMATED = 1
            IX = 2
            
        class Repeater:
            IX = 0
            COPIES = 1
            REPEATER_OFFSET = 2
            COMPOSITE = 3
            TR_P_IX = 4
            TR_A_IX = 5
            TR_SCALE = 6
            TR_S_IX = 7
            TR_R_IX = 8
            TR_SO_IX = 9
            TR_EO_IX = 10
            

        class Asset:
            #ID = 0
            FR = 0
            ID_TOKEN_0 = 1
            ID_TOKEN_1 = 2
            ID_TOKEN_2 = 3
            ID_TOKEN_3 = 4
            ID_TOKEN_4 = 5
            ID_TOKEN_5 = 6
            ID_TOKEN_6 = 7
            ID_TOKEN_7 = 8
            ID_TOKEN_8 = 9
            ID_TOKEN_9 = 10
            ID_TOKEN_COUNT = 11  # Store count of tokens
            
        class Rect:
            HD = 0
            D = 1
            POSITION_X = 2
            POSITION_Y = 3
            SIZE_X = 4
            SIZE_Y = 5
            ROUNDED = 6
            IX = 7
        
        class Ellipse:
            POSITION_X = 0
            POSITION_Y = 1
            SIZE_X = 2
            SIZE_Y = 3
               
        class SingleValue:
            VALUE = 0
            IX = 1
            ANIMATED = 2
            
        class TwoValues:
            VALUE1 = 0
            VALUE2 = 1
            IX = 2
            
        class ThreeValues:
            VALUE1 = 0
            VALUE2 = 1
            VALUE3 = 2
            
        class NullLayer:
            INDEX = 0
            IN_POINT = 1
            OUT_POINT = 2
            START_TIME = 3
            CT = 4
            #DDD = 5
            HD = 5
            HAS_MASK = 6
            AO = 7
            TT = 8
            TP = 9
            TD = 10
            CP = 11
            
        class PrecompLayer:
            INDEX = 0
            IN_POINT = 1
            OUT_POINT = 2
            START_TIME = 3
            W = 4
            H = 5
            CT = 6  # 添加CT参数
            HAS_MASK = 7
            AO = 8
            TT = 9
            TP = 10
            TD = 11
            DDD  =12
            HD = 13
            CP = 14
            
        class SolidLayer:
            INDEX = 0
            IN_POINT = 1
            OUT_POINT = 2
            START_TIME = 3
            WIDTH = 4
            HEIGHT = 5
            HAS_MASK = 6
            COLOR_R = 7
            COLOR_G = 8
            COLOR_B = 9
            COLOR_A = 10
        
        class Parent:
            PARENT_INDEX= 0
        
        class ReferenceId:  # 新增
            ID_TOKEN_0 = 0
            ID_TOKEN_1 = 1
            ID_TOKEN_2 = 2
            ID_TOKEN_3 = 3
            ID_TOKEN_4 = 4
            ID_TOKEN_5 = 5
            ID_TOKEN_6 = 6
            ID_TOKEN_7 = 7
            ID_TOKEN_8 = 8
            ID_TOKEN_9 = 9
            ID_TOKEN_COUNT = 10  # Store count of tokens
        
        class Dimensions:  # 新增
            WIDTH = 0
            HEIGHT = 1

        class Font:
            ASCENT = 0
            FAMILY_TOKEN_0 = 1
            FAMILY_TOKEN_1 = 2
            FAMILY_TOKEN_2 = 3
            FAMILY_TOKEN_3 = 4
            FAMILY_TOKEN_4 = 5
            FAMILY_TOKEN_5 = 6
            FAMILY_TOKEN_6 = 7
            FAMILY_TOKEN_7 = 8
            FAMILY_TOKEN_8 = 9
            FAMILY_TOKEN_9 = 10
            FAMILY_TOKEN_COUNT = 11
            # Reserve slots for style tokens
            STYLE_TOKEN_0 = 12
            STYLE_TOKEN_1 = 13
            STYLE_TOKEN_2 = 14
            STYLE_TOKEN_3 = 15
            STYLE_TOKEN_4 = 16
            STYLE_TOKEN_5 = 17
            STYLE_TOKEN_6 = 18
            STYLE_TOKEN_7 = 19
            STYLE_TOKEN_8 = 20
            STYLE_TOKEN_9 = 21
            STYLE_TOKEN_COUNT = 22
            
        class Char:
            SIZE = 0
            W = 1
            CH_TOKEN_0 = 2
            CH_TOKEN_1 = 3
            CH_TOKEN_2 = 4
            CH_TOKEN_3 = 5
            CH_TOKEN_4 = 6
            CH_TOKEN_5 = 7
            CH_TOKEN_6 = 8
            CH_TOKEN_7 = 9
            CH_TOKEN_8 = 10
            CH_TOKEN_9 = 11
            CH_TOKEN_COUNT = 12
            # Reserve slots for style tokens
            STYLE_TOKEN_0 = 13
            STYLE_TOKEN_1 = 14
            STYLE_TOKEN_2 = 15
            STYLE_TOKEN_3 = 16
            STYLE_TOKEN_4 = 17
            STYLE_TOKEN_5 = 18
            STYLE_TOKEN_6 = 19
            STYLE_TOKEN_7 = 20
            STYLE_TOKEN_8 = 21
            STYLE_TOKEN_9 = 22
            STYLE_TOKEN_COUNT = 23
            # Reserve slots for family tokens
            FAMILY_TOKEN_0 = 24
            FAMILY_TOKEN_1 = 25
            FAMILY_TOKEN_2 = 26
            FAMILY_TOKEN_3 = 27
            FAMILY_TOKEN_4 = 28
            FAMILY_TOKEN_5 = 29
            FAMILY_TOKEN_6 = 30
            FAMILY_TOKEN_7 = 31
            FAMILY_TOKEN_8 = 32
            FAMILY_TOKEN_9 = 33
            FAMILY_TOKEN_COUNT = 34
            
        class TextLayer:
            INDEX = 0
            IN_POINT = 1
            OUT_POINT = 2
            START_TIME = 3
            HAS_MASK = 4  # 新增
            
        class TextKeyframe:
            T = 0
            STROKE_WIDTH = 1
            OFFSET = 2
            WRAP_POSITION_X = 3
            WRAP_POSITION_Y = 4
            WRAP_SIZE_X = 5
            WRAP_SIZE_Y = 6
            # Add numeric fields instead of string storage
            FONT_SIZE = 7
            CA = 8
            JUSTIFY = 9
            TRACKING = 10
            LINE_HEIGHT = 11
            LETTER_SPACING = 12
            FILL_COLOR_R = 13
            FILL_COLOR_G = 14
            FILL_COLOR_B = 15
            STROKE_COLOR_R = 16
            STROKE_COLOR_G = 17
            STROKE_COLOR_B = 18
            HAS_STROKE_COLOR = 19  # Flag to indicate if stroke_color exists
            FONT_FAMILY_TOKENS_START = 20  # Store up to 10 tokens for font_family
            TEXT_TOKENS_START = 30  # Store up to 15 tokens for text
            FONT_FAMILY_TOKEN_COUNT = 45  # Store the count of font_family tokens
            TEXT_TOKEN_COUNT = 46  # Store the count of text tokens
    
        class MoreOptions:
            G = 0
            ALIGNMENT_A = 1
            ALIGNMENT_K1 = 2
            ALIGNMENT_K2 = 3
            ALIGNMENT_IX = 4
        
        class OriginalColors:
            # Support up to 18 color values
            COLOR_0 = 0
            COLOR_1 = 1
            COLOR_2 = 2
            COLOR_3 = 3
            COLOR_4 = 4
            COLOR_5 = 5
            COLOR_6 = 6
            COLOR_7 = 7
            COLOR_8 = 8
            COLOR_9 = 9
            COLOR_10 = 10
            COLOR_11 = 11
            COLOR_12 = 12
            COLOR_13 = 13
            COLOR_14 = 14
            COLOR_15 = 15
            COLOR_16 = 16
            COLOR_17 = 17
            COLOR_18 = 18  # Added
            COLOR_19 = 19  # Added
            COLOR_20 = 20  # Added
            COLOR_21 = 21  # Added
            COLOR_22 = 22  # Added
            COLOR_23 = 23  # Added
            COLOR_24 = 24  # Added
            COLOR_25 = 25  # Added
            COLOR_26 = 26  # Added
            COLOR_27 = 27  # Added
            COLOR_28 = 28  # Added
            COLOR_29 = 29  # Added
            COLOR_30 = 30  # Added
            COLOR_31 = 31  # Added
            COLOR_32 = 32  # Added
            COLOR_33 = 33  # Added
            COLOR_34 = 34  # Added
            COLOR_35 = 35  # Added
            COLOR_36 = 36  # Added
            COLOR_37 = 37  # Added
            COLOR_38 = 38  # Added
            COLOR_39 = 39  # Added
            COLOR_40 = 40  # Added
            COLOR_41 = 41  # Added
            COLOR_42 = 42  # Added
            COLOR_43 = 43  # Added
            COLOR_44 = 44  # Added
            COLOR_45 = 45  # Added
            COLOR_46 = 46  # Added
            COUNT = 47  # Store the count of colors
            
        
    
        class FontSize:
            SIZE = 0
            
        class Text:
            TEXT_TOKEN_0 = 0
            TEXT_TOKEN_1 = 1
            TEXT_TOKEN_2 = 2
            TEXT_TOKEN_3 = 3
            TEXT_TOKEN_4 = 4
            TEXT_TOKEN_5 = 5
            TEXT_TOKEN_6 = 6
            TEXT_TOKEN_7 = 7
            TEXT_TOKEN_8 = 8
            TEXT_TOKEN_9 = 9
            TEXT_TOKEN_COUNT = 10
            
        class Ca:
            VALUE = 0
            
        class Justify:
            VALUE = 0
            
        class Tracking:
            VALUE = 0
            
        class LineHeight:
            VALUE = 0
            
        class LetterSpacing:
            VALUE = 0
            
        class FillColor:
            R = 0
            G = 1
            B = 2
            
        class G:
            VALUE = 0
            
        class Alignment:
            A = 0
            
        class AlignmentK:
            VALUE1 = 0
            VALUE2 = 1
            
        class AlignmentIx:
            VALUE = 0
        
        class GradientFill:
            OPACITY = 0
            FILL_RULE = 1
            START_POINT_X = 2
            START_POINT_Y = 3
            END_POINT_X = 4
            END_POINT_Y = 5
            GRADIENT_TYPE = 6
            HIGHLIGHT_LENGTH = 7
            HIGHLIGHT_ANGLE = 8
            COLOR_POINTS = 9
            # Original colors (up to 12 values for RGBA * 3 color stops)
            ORIGINAL_COLOR_0 = 10
            ORIGINAL_COLOR_1 = 11
            ORIGINAL_COLOR_2 = 12
            ORIGINAL_COLOR_3 = 13
            ORIGINAL_COLOR_4 = 14
            ORIGINAL_COLOR_5 = 15
            ORIGINAL_COLOR_6 = 16
            ORIGINAL_COLOR_7 = 17
            ORIGINAL_COLOR_8 = 18
            ORIGINAL_COLOR_9 = 19
            ORIGINAL_COLOR_10 = 20
            ORIGINAL_COLOR_11 = 21
            ORIGINAL_COLOR_12 = 22  # Added
            ORIGINAL_COLOR_13 = 23  # Added
            ORIGINAL_COLOR_14 = 24  # Added
            ORIGINAL_COLOR_15 = 25  # Added
            ORIGINAL_COLOR_16 = 26  # Added
            ORIGINAL_COLOR_17 = 27  # Added
            ORIGINAL_COLOR_18 = 28  # Added
            ORIGINAL_COLOR_19 = 29  # Added
            ORIGINAL_COLOR_20 = 30  # Added
            ORIGINAL_COLOR_21 = 31  # Added
            ORIGINAL_COLOR_22 = 32  # Added
            ORIGINAL_COLOR_23 = 33  # Added

        class GradientStroke:
            OPACITY = 0
            WIDTH = 1
            LINE_CAP = 2
            LINE_JOIN = 3
            MITER_LIMIT = 4
            ML2 = 5
            ML2_IX = 6
            START_POINT_X = 7
            START_POINT_Y = 8
            END_POINT_X = 9
            END_POINT_Y = 10
            GRADIENT_TYPE = 11
            HIGHLIGHT_LENGTH = 12
            HIGHLIGHT_ANGLE = 13
            COLOR_POINTS = 14
            # Original colors (up to 18 values for RGBA * 4.5 color stops)
            ORIGINAL_COLOR_0 = 15
            ORIGINAL_COLOR_1 = 16
            ORIGINAL_COLOR_2 = 17
            ORIGINAL_COLOR_3 = 18
            ORIGINAL_COLOR_4 = 19
            ORIGINAL_COLOR_5 = 20
            ORIGINAL_COLOR_6 = 21
            ORIGINAL_COLOR_7 = 22
            ORIGINAL_COLOR_8 = 23
            ORIGINAL_COLOR_9 = 24
            ORIGINAL_COLOR_10 = 25
            ORIGINAL_COLOR_11 = 26
            ORIGINAL_COLOR_12 = 27
            ORIGINAL_COLOR_13 = 28
            ORIGINAL_COLOR_14 = 29
            ORIGINAL_COLOR_15 = 30
            ORIGINAL_COLOR_16 = 31
            ORIGINAL_COLOR_17 = 32
            ORIGINAL_COLOR_18 = 33  # Added
            ORIGINAL_COLOR_19 = 34  # Added
            ORIGINAL_COLOR_20 = 35  # Added
            ORIGINAL_COLOR_21 = 36  # Added
            ORIGINAL_COLOR_22 = 37  # Added
            ORIGINAL_COLOR_23 = 38  # Added
            
        class StartPointCmd:
            X = 0
            Y = 1
            
        class EndPointCmd:
            X = 0
            Y = 1
            
        class OriginalColorsCmd:
            COLOR_1 = 0
            COLOR_2 = 1
            COLOR_3 = 2
            COLOR_4 = 3
            COLOR_5 = 4
            COLOR_6 = 5
            COLOR_7 = 6
            COLOR_8 = 7
            COLOR_9 = 8
            COLOR_10 = 9
            COLOR_11 = 10
            COLOR_12 = 11
        
        class ColorPoints:
            VALUE = 0
        
        class Effect:
            TYPE = 0
            INDEX = 1
            NP = 2
            ENABLED = 3
        
        class LayerEffect:  # Add new Index class
            INDEX = 0
            VALUE = 1
    
        class Dropdown:
            INDEX = 0
            VALUE = 1
            
        class NO_VALUE:
            INDEX = 0
            VALUE = 1 
               
        class Ignored:
            INDEX = 0
            VALUE = 1
            
        class Slider:
            INDEX = 0
            VALUE = 1    
        
        class Color:
            NAME_INDEX = 0  # Using NAME_INDEX to avoid confusion with INDEX
            INDEX = 1
            R = 2
            G = 3
            B = 4
        
        class Merge:
            # merge命令的name会存储在string_params中
            pass
        
        class MergeMode:
            MODE = 0

        class Mask:
            INDEX = 0
            INV = 1
            MODE = 2  # mode will be stored as string
            # nm will be stored in string_params
            
        class MaskPt:
            A = 0
            IX = 1
            
        class MaskPtK:
            C = 0  # closed
            
        class MaskPtKValues:  # For i, o, v
            V1 = 0
            V2 = 1
            V3 = 2
            V4 = 3
            V5 = 4
            V6 = 5
            V7 = 6
            V8 = 7
            V9 = 8
            V10 = 9
            V11 = 10
            V12 = 11
            V13 = 12
            V14 = 13
            V15 = 14
            V16 = 15
            V17 = 16
            V18 = 17
            V19 = 18
            V20 = 19
            COUNT = 20  
            
        class MaskO:  # For mask_o
            A = 0
            K = 1
            IX = 2
            
        class MaskX:  # For mask_x
            A = 0
            K = 1
            IX = 2 
    
    
        class MaskPtKeyframe:
            INDEX = 0
            T = 1
            
        class MaskPtKfI:
            X = 0
            Y = 1
            
        class MaskPtKfO:
            X = 0
            Y = 1
            
        class MaskPtKfShape:
            INDEX = 0
            C = 1  # closed
            

        class MaskPtKfShapeValues:  # For shape_i, shape_o, shape_v
            V1 = 0
            V2 = 1
            V3 = 2
            V4 = 3
            V5 = 4
            V6 = 5
            V7 = 6
            V8 = 7
            V9 = 8
            V10 = 9
            V11 = 10
            V12 = 11
            V13 = 12
            V14 = 13
            V15 = 14
            V16 = 15
            V17 = 16
            V18 = 17
            V19 = 18
            V20 = 19
            COUNT = 20  # Add this to store the count
  
        class TrPosition:
            X = 0
            Y = 1
            
        class TrAnchor:
            X = 0
            Y = 1
            
        class TrRotation:
            VALUE = 0
            
        class TrStartOpacity:
            VALUE = 0
            
        class TrEndOpacity:
            VALUE = 0
        class ZigZag:
            NAME_INDEX = 0  # Will store in string_params
            IX = 1
            
        class Frequency:
            VALUE = 0
            
        class Amplitude:
            VALUE = 0
            
        class PointType:
            VALUE = 0
        
        class Animator:
            # nm will be stored in string_params
            pass
            
        class RangeSelector:
            T = 0
            R = 1
            B = 2
            SH = 3
            RN = 4
            
        class RangeStart:
            A = 0
            
        class RangeStartKeyframe:
            T = 0
            S = 1
            I_X = 2
            I_Y = 3
            O_X = 4
            O_Y = 5
            
        class Amount:
            A = 0
            K = 1
            IX = 2
            
        class MaxEase:
            A = 0
            K = 1
            IX = 2
            
        class MinEase:
            A = 0
            K = 1
            IX = 2
        
        class Radius:
            VALUE = 0
        
        class RangeEnd:
            A = 0
            
        class RangeEndKeyframe:
            T = 0
            S = 1
            I_X = 2
            I_Y = 3
            O_X = 4
            O_Y = 5
        
        #class RangeOffset:
        #    A = 0
            
        class RangeOffsetKeyframe:
            T = 0
            S = 1
            I_X = 2
            I_Y = 3
            O_X = 4
            O_Y = 5
            
        class SM:
            A = 0
            K = 1
            IX = 2
            
        class OpacityAnimators:
            A = 0
            K = 1
            IX = 2
        class ScaleAnimators:
            A = 0
            K_X = 1
            K_Y = 2
            K_Z = 3
            IX = 4
            
        class RotationAnimators:
            A = 0
            K = 1
            IX = 2

        class PositionAnimators:
            A = 0
            K_X = 1
            K_Y = 2
            K_Z = 3
            IX = 4

        class TrackingAnimators:
            A = 0
            K = 1
            IX = 2
        class Dashes:
            # Container command, no parameters
            pass

        class Dash:
            TYPE = 0  # Store type as numeric (0 for "d", 1 for "g", 2 for "o")
            LENGTH = 1  # dash length
            V_IX = 2  # v_ix parameter
        
        class DashAnimated:
            TYPE = 0  # Store type as numeric
            V_IX = 1  # v_ix parameter
        
        class DashKeyframe:
            T = 0
            S = 1
            I_X = 2
            I_Y = 3
            O_X = 4
            O_Y = 5
        
        
        class DashOffset:
            O = 0  # offset value

    # Parameter dimension (fixed length for all commands)
    PARAM_DIM = 50
    PAD_VAL = -2001
    
    def __init__(self, commands, params, seq_len=None, PAD_VAL=-2001, flattened_data=None):
        """Initialize LottieTensor"""
        self.PAD_VAL = PAD_VAL
        
        self.commands = commands.reshape(-1, 1).long()
        self.params = params.float()
        self.seq_len = torch.tensor(len(commands)) if seq_len is None else seq_len
        
        self.sos_token = torch.tensor([LottieTensor.CMD_SOS]).unsqueeze(-1).long()
        self.eos_token = self.pad_token = torch.tensor([LottieTensor.CMD_EOS]).unsqueeze(-1).long()
        
        # Store original string values
        self.string_params = {}
    
    @staticmethod
    def _parse_easing_value(value_str: str) -> int:
        """Helper function to parse easing values and return as int"""
        if not value_str:
            return 0
            
        # Handle quoted format "0.833 0.833 0.833"
        if value_str.startswith('"') and value_str.endswith('"'):
            value_str = value_str[1:-1]
            
        # Handle space-separated (take first value)
        parts = value_str.split()
        if parts:
            try:
                return round(float(parts[0]))
            except ValueError:
                return 0
        
        # Try to parse as plain number
        try:
            return round(float(value_str))
        except ValueError:
            return 0


    @staticmethod
    def _parse_multi_easing_values(value_str: str) -> List[int]:
        """Parse multi-dimensional easing values like '0.3 0.3 0.3' and return as int list"""
        values = [0, 0, 0]
        
        if not value_str:
            return values
            
        # Handle quoted format "0.3 0.3 0.3"
        if value_str.startswith('"') and value_str.endswith('"'):
            value_str = value_str[1:-1]
            
        # Parse space-separated values
        parts = value_str.split()
        for i, part in enumerate(parts[:3]):
            try:
                values[i] = round(float(part))
            except ValueError:
                values[i] = 0
                
        # If only one value provided, use it for all dimensions
        if len(parts) == 1 and parts[0]:
            try:
                val = round(float(parts[0]))
                values = [val, val, val]
            except ValueError:
                pass
                
        return values


    @staticmethod
    def from_sequence(sequence: str) -> 'LottieTensor':
        """Convert a string sequence to LottieTensor"""
        raw_lines = [line.strip() for line in sequence.strip().split('\n') if line.strip()]
        
        # Process each line and extract all commands
        lines = []
        for raw_line in raw_lines:
            # Find all commands in the line (commands are enclosed in parentheses)
            import re
            commands_in_line = re.findall(r'\([^)]+\)', raw_line)
            lines.extend(commands_in_line)
        
        commands = []
        params_list = []
        string_params = {}
        current_context = None
        
        for idx, line in enumerate(lines):
            if not (line.startswith('(') and line.endswith(')')):
                continue
                
            # Extract command name and attributes
            content = line[1:-1].strip()
            
            # Handle end tags
            if content.startswith('/'):
                cmd = content
                if cmd in LottieTensor.COMMAND_TO_IDX:
                    commands.append(LottieTensor.COMMAND_TO_IDX[cmd])
                    params_list.append([LottieTensor.PAD_VAL] * LottieTensor.PARAM_DIM)
                    
                    # Reset context for certain end tags
                    if cmd in ["/position", "/scale", "/opacity", "/rotation", "/keyframe", "/anchor", "/path", "/width_animated", 
                            "/position_x", "/position_y", "/position_z", "/tm", "/range_start", "/range_end", "/animator_properties",
                            "/start", "/end", "/offset", "/color_animated", "/rounded"]:
                        current_context = None
                continue
            
            # Parse command and attributes
            parts = content.split(' ', 1)
            cmd = parts[0]
            
            # Handle quoted commands
            if cmd.startswith('"') and cmd.endswith('"'):
                cmd = cmd
            
            attrs_str = parts[1] if len(parts) > 1 else ""
            
            # Update context - modified to track path animation, width animation, and individual position components
            if cmd in ["position", "scale", "opacity", "rotation", "anchor"]:
                current_context = cmd
            elif cmd in ["position_x", "position_y", "position_z"]:
                # Check if animated
                if "animated" in attrs_str and "true" in attrs_str.lower():
                    current_context = cmd
            elif cmd == "path" and "animated" in attrs_str:
                current_context = "path"
            elif cmd == "width_keyframe":
                current_context = "width"
            elif cmd == "start" and "animated" in attrs_str and "true" in attrs_str.lower():
                current_context = "trim_start"
            elif cmd == "end" and "animated" in attrs_str and "true" in attrs_str.lower():
                current_context = "trim_end"
            elif cmd == "offset" and "animated" in attrs_str and "true" in attrs_str.lower():
                current_context = "trim_offset"
            elif cmd == "mask_x":
                # Check if animated (a=1)
                mask_x_attrs = LottieTensor._parse_attributes(attrs_str)
                if float(mask_x_attrs.get("a", 0)) > 0.5:
                    current_context = "mask_x"

            elif cmd == "scale_animators":
                # Check if animated
                scale_animators_attrs = LottieTensor._parse_attributes(attrs_str)
                if float(scale_animators_attrs.get("a", 0)) > 0.5:
                    current_context = "scale_animators"
            elif cmd == "rotation_animators":
                # Check if animated
                rotation_animators_attrs = LottieTensor._parse_attributes(attrs_str)
                if float(rotation_animators_attrs.get("a", 0)) > 0.5:
                    current_context = "rotation_animators"

            elif cmd == "opacity_animators":
                # Check if animated
                opacity_animators_attrs = LottieTensor._parse_attributes(attrs_str)
                if float(opacity_animators_attrs.get("a", 0)) > 0.5:
                    current_context = "opacity_animators"

            elif cmd == "position_animators":
                # Check if animated
                position_animators_attrs = LottieTensor._parse_attributes(attrs_str)
                if float(position_animators_attrs.get("a", 0)) > 0.5:
                    current_context = "position_animators"

            elif cmd == "tracking_animators":
                # Check if animated
                tracking_animators_attrs = LottieTensor._parse_attributes(attrs_str)
                if float(tracking_animators_attrs.get("a", 0)) > 0.5:
                    current_context = "tracking_animators"
            
            elif cmd == "rect_rounded" and "animated" in attrs_str and "true" in attrs_str.lower():
                current_context = "rect_rounded"            
            if cmd not in LottieTensor.COMMAND_TO_IDX:
                continue
                
            cmd_idx = LottieTensor.COMMAND_TO_IDX[cmd]
            cmd_key = f"{len(commands)}"  # Use command index as key
            commands.append(cmd_idx)
            
            # Initialize parameters
            params = [LottieTensor.PAD_VAL] * LottieTensor.PARAM_DIM
            attrs = LottieTensor._parse_attributes(attrs_str)
            
            # Parse parameters based on command type
            if cmd_idx == LottieTensor.CMD_ANIMATION:
                # Store original string values
                #string_params[f"{cmd_key}_v"] = attrs.get("v", "5.12.1")
                #string_params[f"{cmd_key}_nm"] = attrs.get("nm", "Comp 1")
                #string_params[f"{cmd_key}_markers"] = attrs.get("markers", "[]")
                #string_params[f"{cmd_key}_props"] = attrs.get("props", "{}")
                
                params[LottieTensor.Index.Animation.FR] = round(float(attrs.get("fr", 60))) 
                params[LottieTensor.Index.Animation.IP] = round(float(attrs.get("ip", 0))) 
                params[LottieTensor.Index.Animation.OP] = round(float(attrs.get("op", 150))) 
                params[LottieTensor.Index.Animation.W] = round(float(attrs.get("w", 512))) 
                params[LottieTensor.Index.Animation.H] = round(float(attrs.get("h", 512))) 
                params[LottieTensor.Index.Animation.DDD] = int(attrs.get("ddd", 0)) 
                #eos token
                #print("params", params)
            
            elif cmd_idx == LottieTensor.CMD_LAYER:
                # Store layer name and string attributes
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Layer")
                
                # 必需的属性
                #params[LottieTensor.Index.Layer.INDEX] = float(attrs.get("index", 0))
                params[LottieTensor.Index.Layer.INDEX] = LottieTensor._index_clamp_value(round(float(attrs.get("index", "0")))) # index 0-100
                #params[LottieTensor.Index.Layer.IN_POINT] = float(attrs.get("in_point", 0))
                #params[LottieTensor.Index.Layer.OUT_POINT] = float(attrs.get("out_point", 60))
                params[LottieTensor.Index.Layer.IN_POINT] = LottieTensor._clamp_value(round(float(attrs.get("in_point", 0))))  #ip -2000-2000
                params[LottieTensor.Index.Layer.OUT_POINT] = LottieTensor._clamp_value(round(float(attrs.get("out_point", 60)))) #op -2000-2000
                params[LottieTensor.Index.Layer.START_TIME] = LottieTensor._clamp_value(round(float(attrs.get("start_time", 0)))) #st -2000-2000
                
                # 可选属性 - 只在存在时解析，不设置默认值
                if "ddd" in attrs:
                    params[LottieTensor.Index.Layer.DDD] = float(attrs.get("ddd"))  #0-1
                
                if "hd" in attrs:
                    params[LottieTensor.Index.Layer.HD] = 1.0 if attrs.get("hd").lower() == "true" else 0.0 # 0-1
                 
                if "cp" in attrs:
                    params[LottieTensor.Index.Layer.CP] = 1.0 if attrs.get("cp").lower() == "true" else 0.0  # 0-1
                
                if "hasMask" in attrs:
                    params[LottieTensor.Index.Layer.HAS_MASK] = 1.0 if attrs.get("hasMask").lower() == "true" else 0.0  # 0-1
                
                if "ao" in attrs:
                    params[LottieTensor.Index.Layer.AO] = int(attrs.get("ao")) # 0-1
                
                if "tt" in attrs:
                    params[LottieTensor.Index.Layer.TT] = int(attrs.get("tt")) # 0-4
                
                if "tp" in attrs:
                    params[LottieTensor.Index.Layer.TP] = int(attrs.get("tp")) #0-100以内
                
                if "td" in attrs:
                    params[LottieTensor.Index.Layer.TD] = int(attrs.get("td"))  #0-1
                
                if "ct" in attrs:
                    params[LottieTensor.Index.Layer.CT] = int(attrs.get("ct")) #0-1
                
            elif cmd_idx == LottieTensor.CMD_NULL_LAYER:
                # Store layer name and string attributes
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "null_layer")

                #params[LottieTensor.Index.NullLayer.INDEX] = int(attrs.get("index", 0))
                params[LottieTensor.Index.NullLayer.INDEX] = LottieTensor._index_clamp_value(round(float(attrs.get("index", 0))))
                #params[LottieTensor.Index.NullLayer.IN_POINT] = float(attrs.get("in_point", 0))
                #params[LottieTensor.Index.NullLayer.OUT_POINT] = float(attrs.get("out_point", 60))
                params[LottieTensor.Index.NullLayer.IN_POINT] = LottieTensor._clamp_value(round(float(attrs.get("in_point", 0))))
                params[LottieTensor.Index.NullLayer.OUT_POINT] = LottieTensor._clamp_value(round(float(attrs.get("out_point", 60))))
                params[LottieTensor.Index.NullLayer.START_TIME] = LottieTensor._clamp_value(round(float(attrs.get("start_time", 0))))

                if "hd" in attrs:
                    params[LottieTensor.Index.PrecompLayer.HD] = 1.0 if attrs.get("hd").lower() == "true" else 0.0
                
                if "cp" in attrs:
                    params[LottieTensor.Index.PrecompLayer.CP] = 1.0 if attrs.get("cp").lower() == "true" else 0.0
                
                if "hasMask" in attrs:
                    params[LottieTensor.Index.PrecompLayer.HAS_MASK] = 1.0 if attrs.get("hasMask").lower() == "true" else 0.0
                
                if "ao" in attrs:
                    params[LottieTensor.Index.PrecompLayer.AO] = int(attrs.get("ao"))
                
                if "tt" in attrs:
                    params[LottieTensor.Index.PrecompLayer.TT] = int(attrs.get("tt"))
                
                if "tp" in attrs:
                    params[LottieTensor.Index.PrecompLayer.TP] = int(attrs.get("tp"))
                
                if "td" in attrs:
                    params[LottieTensor.Index.PrecompLayer.TD] = int(attrs.get("td"))
                
            elif cmd_idx == LottieTensor.CMD_PRECOMP_LAYER:
                # Parse name more carefully to handle names with spaces
                name = attrs.get("name", "precomp_layer")
                # If name wasn't properly captured (e.g., due to spaces), try regex
                if name == "precomp_layer" or not name:
                    # Look for name="..." pattern in the original attrs_str
                    import re
                    name_match = re.search(r'name="([^"]*)"', attrs_str)
                    if name_match:
                        name = name_match.group(1)
                    else:
                        # Try without quotes
                        name_match = re.search(r'name=([^\s]+)', attrs_str)
                        if name_match:
                            name = name_match.group(1)
                        else:
                            name = "precomp_layer"
                
                #string_params[f"{cmd_key}_name"] = name
                
                # Parse numeric parameters
                #params[LottieTensor.Index.PrecompLayer.INDEX] = float(attrs.get("index", 0))
                params[LottieTensor.Index.PrecompLayer.INDEX] = LottieTensor._index_clamp_value(round(float(attrs.get("index", 0))))
                #params[LottieTensor.Index.PrecompLayer.IN_POINT] = float(attrs.get("in_point", 0))
                #params[LottieTensor.Index.PrecompLayer.OUT_POINT] = float(attrs.get("out_point", 120))
                params[LottieTensor.Index.PrecompLayer.IN_POINT] = LottieTensor._clamp_value(round(float(attrs.get("in_point", 0))))
                params[LottieTensor.Index.PrecompLayer.OUT_POINT] = LottieTensor._clamp_value(round(float(attrs.get("out_point", 120))))
                params[LottieTensor.Index.PrecompLayer.START_TIME] = LottieTensor._clamp_value(round(float(attrs.get("start_time", 0))))
                
                # 可选属性 - 只在存在时解析，不设置默认值
                if "h" in attrs:
                    params[LottieTensor.Index.PrecompLayer.H] = round(float(attrs.get("h")))  #0-2000

                if "w" in attrs:
                    params[LottieTensor.Index.PrecompLayer.W] = round(float(attrs.get("w"))) #0-2000
                
                
                if "ddd" in attrs:
                    params[LottieTensor.Index.PrecompLayer.DDD] = int(attrs.get("ddd")) #0-1
                
                if "hd" in attrs:
                    params[LottieTensor.Index.PrecompLayer.HD] = 1.0 if attrs.get("hd").lower() == "true" else 0.0 #0-1
                
                if "cp" in attrs:
                    params[LottieTensor.Index.PrecompLayer.CP] = 1.0 if attrs.get("cp").lower() == "true" else 0.0 #0-1
                
                if "hasMask" in attrs:
                    params[LottieTensor.Index.PrecompLayer.HAS_MASK] = 1.0 if attrs.get("hasMask").lower() == "true" else 0.0 #0-1
                
                if "ao" in attrs:
                    params[LottieTensor.Index.PrecompLayer.AO] = int(attrs.get("ao")) #0-1
                
                if "tt" in attrs:
                    params[LottieTensor.Index.PrecompLayer.TT] = int(attrs.get("tt"))
                
                if "tp" in attrs:
                    params[LottieTensor.Index.PrecompLayer.TP] = int(attrs.get("tp"))
                
                if "td" in attrs:
                    params[LottieTensor.Index.PrecompLayer.TD] = int(attrs.get("td"))
                
                if "ct" in attrs:
                    params[LottieTensor.Index.PrecompLayer.CT] = int(attrs.get("ct"))
            
            
            elif cmd_idx == LottieTensor.CMD_TEXT_LAYER:
                # 存储name
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Text Layer")
                
                #params[LottieTensor.Index.TextLayer.INDEX] = float(attrs.get("index", 0))
                params[LottieTensor.Index.TextLayer.INDEX] = LottieTensor._index_clamp_value(round(float(attrs.get("index", 0))))  
                #params[LottieTensor.Index.TextLayer.IN_POINT] = float(attrs.get("in_point", 0))
                #params[LottieTensor.Index.TextLayer.OUT_POINT] = float(attrs.get("out_point", 60))
                params[LottieTensor.Index.TextLayer.IN_POINT] = LottieTensor._clamp_value(round(float(attrs.get("in_point", 0))))
                params[LottieTensor.Index.TextLayer.OUT_POINT] = LottieTensor._clamp_value(round(float(attrs.get("out_point", 60))))
                params[LottieTensor.Index.TextLayer.START_TIME] = LottieTensor._clamp_value(round(float(attrs.get("start_time", 0))))
                params[LottieTensor.Index.TextLayer.HAS_MASK] = 1.0 if attrs.get("hasMask", "false").lower() == "true" else 0.0  # 新增

            elif cmd_idx == LottieTensor.CMD_SOLID_LAYER:
                # Store string attributes
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Solid Layer")
                #string_params[f"{cmd_key}_color"] = attrs.get("color", "#000000")
                hex_color = attrs.get("color", "#00000000")
                # Remove '#' if present
                hex_color = hex_color.lstrip('#')
                # Convert to RGB
                r = int(hex_color[0:2], 16) if len(hex_color) >= 2 else 0
                g = int(hex_color[2:4], 16) if len(hex_color) >= 4 else 0
                b = int(hex_color[4:6], 16) if len(hex_color) >= 6 else 0
                a = int(hex_color[6:8], 16) if len(hex_color) >= 8 else 0

                # Store RGB values as separate parameters
                params[LottieTensor.Index.SolidLayer.COLOR_R] = round(float(r))
                params[LottieTensor.Index.SolidLayer.COLOR_G] = round(float(g))
                params[LottieTensor.Index.SolidLayer.COLOR_B] = round(float(b))
                params[LottieTensor.Index.SolidLayer.COLOR_A] = round(float(a))  #这里的color都是0-255吧
                
                
                #params[LottieTensor.Index.SolidLayer.INDEX] = float(attrs.get("index", 0))
                params[LottieTensor.Index.SolidLayer.INDEX] = LottieTensor._index_clamp_value(round(float(attrs.get("index", 0))))
                #params[LottieTensor.Index.SolidLayer.IN_POINT] = float(attrs.get("in_point", 0))
                #params[LottieTensor.Index.SolidLayer.OUT_POINT] = float(attrs.get("out_point", 60))
                params[LottieTensor.Index.SolidLayer.IN_POINT] = LottieTensor._clamp_value(round(float(attrs.get("in_point", 0))))
                params[LottieTensor.Index.SolidLayer.OUT_POINT] = LottieTensor._clamp_value(round(float(attrs.get("out_point", 60))))
                params[LottieTensor.Index.SolidLayer.START_TIME] = LottieTensor._clamp_value(round(float(attrs.get("start_time", 0))))
                params[LottieTensor.Index.SolidLayer.WIDTH] = LottieTensor._clamp_value(round(float(attrs.get("width", 512))))
                params[LottieTensor.Index.SolidLayer.HEIGHT] = LottieTensor._clamp_value(round(float(attrs.get("height", 512))))
                params[LottieTensor.Index.SolidLayer.HAS_MASK] = 1.0 if attrs.get("hasMask", "false").lower() == "true" else 0.0
                
            elif cmd_idx in [LottieTensor.CMD_FONTS, LottieTensor.CMD_FONTS_END, LottieTensor.CMD_CHARS, LottieTensor.CMD_CHARS_END, LottieTensor.CMD_CHAR_SHAPES, LottieTensor.CMD_CHAR_SHAPES_END, LottieTensor.CMD_TEXT_KEYFRAMES, LottieTensor.CMD_MORE_OPTIONS, LottieTensor.CMD_OPACITY_ANIMATED_END, LottieTensor.CMD_END_END, LottieTensor.CMD_START_END, LottieTensor.CMD_OFFSET_END, LottieTensor.CMD_OPACITY_ANIMATORS_END]:
                pass


            elif cmd_idx == LottieTensor.CMD_TEXT_KEYFRAME:
                if LottieTensor.tokenizer is None:
                    LottieTensor.init_tokenizer()

                # Parse all attributes from text_keyframe
                params[LottieTensor.Index.TextKeyframe.T] = LottieTensor._clamp_value(round(float(attrs.get("t", 0))))
                
                # Parse stroke_width as a numeric parameter
                stroke_width_str = attrs.get("stroke_width", "0")
                try:
                    params[LottieTensor.Index.TextKeyframe.STROKE_WIDTH] = round(float(stroke_width_str))
                except ValueError:
                    params[LottieTensor.Index.TextKeyframe.STROKE_WIDTH] = 0
                
                # Parse offset as a boolean (1.0 for true, 0.0 for false)
                offset_str = attrs.get("offset", "false")
                params[LottieTensor.Index.TextKeyframe.OFFSET] = 1 if offset_str.lower() == "true" else 0.0
                
                # Parse wrap_position array (新增)
                wrap_position_str = attrs.get("wrap_position", "")
                if wrap_position_str:
                    if wrap_position_str.startswith("[") and wrap_position_str.endswith("]"):
                        wrap_position_str = wrap_position_str[1:-1]
                        pos_parts = wrap_position_str.split(",")
                        if len(pos_parts) >= 2:
                            try:
                                params[LottieTensor.Index.TextKeyframe.WRAP_POSITION_X] = round(float(pos_parts[0].strip()))
                                params[LottieTensor.Index.TextKeyframe.WRAP_POSITION_Y] = round(float(pos_parts[1].strip()))
                            except ValueError:
                                pass
                
                # Parse wrap_size array (新增)
                wrap_size_str = attrs.get("wrap_size", "")
                if wrap_size_str:
                    if wrap_size_str.startswith("[") and wrap_size_str.endswith("]"):
                        wrap_size_str = wrap_size_str[1:-1]
                        size_parts = wrap_size_str.split(",")
                        if len(size_parts) >= 2:
                            try:
                                params[LottieTensor.Index.TextKeyframe.WRAP_SIZE_X] = round(float(size_parts[0].strip()))
                                params[LottieTensor.Index.TextKeyframe.WRAP_SIZE_Y] = round(float(size_parts[1].strip()))
                            except ValueError:
                                pass
                
                # Store all text_keyframe attributes in string_params
                #string_params[f"{cmd_key}_font_size"] = attrs.get("font_size", "12")
                #string_params[f"{cmd_key}_font_family"] = attrs.get("font_family", "")
                #string_params[f"{cmd_key}_text"] = attrs.get("text", "")
                #string_params[f"{cmd_key}_ca"] = attrs.get("ca", "1")
                #string_params[f"{cmd_key}_justify"] = attrs.get("justify", "0")
                #string_params[f"{cmd_key}_tracking"] = attrs.get("tracking", "0")
                #string_params[f"{cmd_key}_line_height"] = attrs.get("line_height", "0")
                #string_params[f"{cmd_key}_letter_spacing"] = attrs.get("letter_spacing", "0")
                params[LottieTensor.Index.TextKeyframe.FONT_SIZE] = round(float(attrs.get("font_size", 12)))
                params[LottieTensor.Index.TextKeyframe.CA] = int(attrs.get("ca", 1))
                params[LottieTensor.Index.TextKeyframe.JUSTIFY] = int(attrs.get("justify", 0))
                params[LottieTensor.Index.TextKeyframe.TRACKING] = int(float(attrs.get("tracking", 0)))
                params[LottieTensor.Index.TextKeyframe.LINE_HEIGHT] = round(float(attrs.get("line_height", 0)))
                params[LottieTensor.Index.TextKeyframe.LETTER_SPACING] = int(float(attrs.get("letter_spacing", 0)))
                
                font_family = attrs.get("font_family", "")
                if font_family:
                    font_family_tokens = LottieTensor.tokenizer.encode(font_family, add_special_tokens=False)
                    # Store up to 10 tokens
                    for i, token in enumerate(font_family_tokens[:10]):
                        params[LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKENS_START + i] = int(token)
                    params[LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKEN_COUNT] = int(len(font_family_tokens[:10]))
                else:
                    params[LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKEN_COUNT] = 0
                
                # Tokenize text
                text = attrs.get("text", "")
                if text:
                    text_tokens = LottieTensor.tokenizer.encode(text, add_special_tokens=False)
                    # Store up to 15 tokens
                    for i, token in enumerate(text_tokens[:15]):
                        params[LottieTensor.Index.TextKeyframe.TEXT_TOKENS_START + i] = int(token)
                    params[LottieTensor.Index.TextKeyframe.TEXT_TOKEN_COUNT] = int(len(text_tokens[:15]))
                else:
                    params[LottieTensor.Index.TextKeyframe.TEXT_TOKEN_COUNT] = 0
                
                
                # Parse fill_color array
                fill_color_str = attrs.get("fill_color", "[0,0,0]")
                if fill_color_str.startswith("[") and fill_color_str.endswith("]"):
                    fill_color_str = fill_color_str[1:-1]
                    color_parts = fill_color_str.split(",")
                    #string_params[f"{cmd_key}_fill_color"] = ",".join([p.strip() for p in color_parts])
                    if len(color_parts) >= 3:
                        params[LottieTensor.Index.TextKeyframe.FILL_COLOR_R] = round(float(color_parts[0].strip()) * 255)
                        params[LottieTensor.Index.TextKeyframe.FILL_COLOR_G] = round(float(color_parts[1].strip()) * 255)
                        params[LottieTensor.Index.TextKeyframe.FILL_COLOR_B] = round(float(color_parts[2].strip()) * 255)
                
                # Parse stroke_color array (if present)
                stroke_color_str = attrs.get("stroke_color", "")
                if stroke_color_str:
                    if stroke_color_str.startswith("[") and stroke_color_str.endswith("]"):
                        stroke_color_str = stroke_color_str[1:-1]
                        color_parts = stroke_color_str.split(",")
                        if len(color_parts) >= 3:
                            params[LottieTensor.Index.TextKeyframe.STROKE_COLOR_R] = round(float(color_parts[0].strip()) * 255)
                            params[LottieTensor.Index.TextKeyframe.STROKE_COLOR_G] = round(float(color_parts[1].strip()) * 255)
                            params[LottieTensor.Index.TextKeyframe.STROKE_COLOR_B] = round(float(color_parts[2].strip()) * 255)
                else:
                    params[LottieTensor.Index.TextKeyframe.HAS_STROKE_COLOR] = 0
                
            
            elif cmd_idx == LottieTensor.CMD_MORE_OPTIONS:
                # Parse the entire more_options line
                parts_list = attrs_str.split()
                i = 0
                while i < len(parts_list):
                    if parts_list[i] == "g" and i + 1 < len(parts_list):
                        params[LottieTensor.Index.MoreOptions.G] = round(float(parts_list[i + 1]))  #1-4
                        i += 2
                    elif parts_list[i] == "alignment" and i + 1 < len(parts_list):
                        if parts_list[i + 1].startswith("a="):
                            params[LottieTensor.Index.MoreOptions.ALIGNMENT_A] = round(float(parts_list[i + 1].split("=")[1]))
                            i += 2
                        else:
                            i += 1
                    elif parts_list[i] == "alignment_k" and i + 2 < len(parts_list):
                        params[LottieTensor.Index.MoreOptions.ALIGNMENT_K1] = round(float(parts_list[i + 1]))
                        params[LottieTensor.Index.MoreOptions.ALIGNMENT_K2] = round(float(parts_list[i + 2]))
                        i += 3
                    elif parts_list[i] == "alignment_ix" and i + 1 < len(parts_list):
                        params[LottieTensor.Index.MoreOptions.ALIGNMENT_IX] = round(float(parts_list[i + 1]))
                        i += 2
                    else:
                        i += 1


            elif cmd_idx == LottieTensor.CMD_REFERENCE_ID:
                if LottieTensor.tokenizer is None:
                    LottieTensor.init_tokenizer()
                
                # Extract reference_id from attrs_str
                ref_id_match = re.search(r'"([^"]*)"', attrs_str)
                if ref_id_match:
                    reference_id = ref_id_match.group(1)
                else:
                    # Try without quotes
                    parts = attrs_str.strip().split()
                    if parts:
                        reference_id = parts[0]
                    else:
                        reference_id = "comp_0"
                
                # Tokenize reference_id
                id_tokens = LottieTensor.tokenizer.encode(reference_id, add_special_tokens=False)[:10]  # Limit to 10 tokens
                
                for i, token_id in enumerate(id_tokens):
                    if i < 10:
                        params[LottieTensor.Index.ReferenceId.ID_TOKEN_0 + i] = int(token_id)
                params[LottieTensor.Index.ReferenceId.ID_TOKEN_COUNT] = int(len(id_tokens))

           
           
            elif cmd_idx == LottieTensor.CMD_DIMENSIONS:
                # 处理dimensions命令
                params[LottieTensor.Index.Dimensions.WIDTH] = round(float(attrs.get("width", 512))) #0-2000
                params[LottieTensor.Index.Dimensions.HEIGHT] = round(float(attrs.get("height", 512))) #0-2000
            
            

            # 3. Modify the stroke parsing in from_sequence method:


            elif cmd_idx == LottieTensor.CMD_STROKE:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Stroke")
                
                # Check if color is animated
                color_animated = attrs.get("color_animated", "false").lower() == "true" 
                params[LottieTensor.Index.Stroke.COLOR_ANIMATED] = 1.0 if color_animated else 0.0  # 0-1
                
                if not color_animated:
                    # Parse static color and convert from 0-1 to 0-255 range
                    params[LottieTensor.Index.Stroke.R] = round(float(attrs.get("r", 0)) * 255)  # 0-1 → 0-255
                    params[LottieTensor.Index.Stroke.G] = round(float(attrs.get("g", 0)) * 255) # 0-1 → 0-255
                    params[LottieTensor.Index.Stroke.B] = round(float(attrs.get("b", 0)) * 255)  # 0-1 → 0-255
                    params[LottieTensor.Index.Stroke.A] = round(float(attrs.get("a", 1)) * 255)  # 0-1 → 0-255
                
                params[LottieTensor.Index.Stroke.COLOR_DIM] = int(attrs.get("color_dim", 4)) #3-4
                params[LottieTensor.Index.Stroke.HAS_C_A] = 1.0 if attrs.get("has_c_a", "").lower() == "true" else 0.0 #0-1
                params[LottieTensor.Index.Stroke.HAS_C_IX] = 1.0 if attrs.get("has_c_ix", "").lower() == "true" else 0.0 #0-1
                params[LottieTensor.Index.Stroke.C_IX] = int(attrs.get("c_ix", 3))  #2-4
                params[LottieTensor.Index.Stroke.BM] = int(attrs.get("bm", 0)) #0-1
                params[LottieTensor.Index.Stroke.LC] = int(attrs.get("lc", 1)) #1-3
                params[LottieTensor.Index.Stroke.LJ] = int(attrs.get("lj", 1)) #1-3
                params[LottieTensor.Index.Stroke.ML] = int(float((attrs.get("ml", "4")))) #0-50
                
                # Handle width or width_animated
                if "width_animated" in attrs and attrs.get("width_animated", "").lower() == "true":
                    params[LottieTensor.Index.Stroke.WIDTH_ANIMATED] = 1.0
                    current_context = "width"
                    
                    # ADD THIS: Append width_animated command after stroke
                    params_list.append(params)
                    commands.append(LottieTensor.CMD_WIDTH_ANIMATED)  # Note: need to define this constant
                    params_list.append([LottieTensor.PAD_VAL] * LottieTensor.PARAM_DIM)
                    params = [LottieTensor.PAD_VAL] * LottieTensor.PARAM_DIM  # Reset for next command
                else:
                    params[LottieTensor.Index.Stroke.WIDTH_ANIMATED] = 0.0
                
                # Set context for color keyframes if animated
                if color_animated:
                    current_context = "stroke_color"

            # 4. Add parsing for color_keyframe command: keframe的s和i_x, i_y, o_x, o_y是不能越界的，越界需要去除
            elif cmd_idx == LottieTensor.CMD_COLOR_KEYFRAME:
                # Parse color keyframe parameters
                params[LottieTensor.Index.Keyframe.T] = round(float(attrs.get("t", 0)))  #-2000-2000
                params[LottieTensor.Index.Keyframe.S1] = round(float(attrs.get("r", 0)) * 255)  # Use S1 for R
                params[LottieTensor.Index.Keyframe.S2] = round(float(attrs.get("g", 0)) * 255)  # Use S2 for G
                params[LottieTensor.Index.Keyframe.S3] = round(float(attrs.get("b", 0)) * 255)  # Use S3 for B
                params[LottieTensor.Index.Keyframe.E1] = round(float(attrs.get("a", 1)) * 255) # Use E1 for A
                
                # Parse easing parameters
                params[LottieTensor.Index.Keyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0"))*100))
                params[LottieTensor.Index.Keyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0"))*100))
                params[LottieTensor.Index.Keyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0"))*100))
                params[LottieTensor.Index.Keyframe.O_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0"))*100))


            elif cmd_idx == LottieTensor.CMD_OPACITY_ANIMATED:
                # Check if animated
                if attrs.get("true", "false").lower() == "true" or "true" in attrs_str.lower():
                    current_context = "opacity_animated"
                    
            elif cmd_idx == LottieTensor.CMD_OPACITY_KEYFRAME:
                # Parse opacity keyframe parameters
                params[LottieTensor.Index.Keyframe.T] = round(float(attrs.get("t", 0)))
                
                # Parse s parameter if present
                if "s" in attrs:
                    s_str = attrs.get("s", "0").strip('"')
                    params[LottieTensor.Index.Keyframe.S1] = round(float(s_str))
                
                # Parse easing parameters if present
                if "i_x" in attrs or "i_y" in attrs or "o_x" in attrs or "o_y" in attrs:
                    params[LottieTensor.Index.Keyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0"))*100))
                    params[LottieTensor.Index.Keyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0"))*100))
                    params[LottieTensor.Index.Keyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0"))*100))
                    params[LottieTensor.Index.Keyframe.O_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0"))*100))

            
            elif cmd_idx == LottieTensor.CMD_WIDTH_KEYFRAME:
                params[LottieTensor.Index.WidthKeyframe.T] = round(float(attrs.get("t", 0)))
                
                # 处理s参数 - 改成乘以10
                if "s" in attrs:
                    s_str = attrs.get("s", "0").strip('"')
                    try:
                        s_val = round(float(s_str) * 10)
                        s_val = max(0, min(10000, s_val))  # 裁剪
                        params[LottieTensor.Index.WidthKeyframe.S] = s_val
                    except ValueError:
                        params[LottieTensor.Index.WidthKeyframe.S] = 0.0
                
                # easing参数保持不变
                params[LottieTensor.Index.WidthKeyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0"))*100))
                params[LottieTensor.Index.WidthKeyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0"))*100))
                params[LottieTensor.Index.WidthKeyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0"))*100))
                params[LottieTensor.Index.WidthKeyframe.O_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0"))*100))



            elif cmd_idx == LottieTensor.CMD_POSITION:
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                elif attrs.get("separated", "").lower() == "true":
                    # Handle separated position (for 3D layers)
                    params[LottieTensor.Index.Transform.ANIMATED] = 2.0  # Use 2.0 to indicate separated
                
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    # Parse position values
                    pos_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                pos_parts.append(part)
                            except ValueError:
                                pass
                    
                    if len(pos_parts) >= 1:
                        params[LottieTensor.Index.Transform.X] = round(float(pos_parts[0]))
                    if len(pos_parts) >= 2:
                        params[LottieTensor.Index.Transform.Y] = round(float(pos_parts[1]))
                    if len(pos_parts) >= 3:
                        params[LottieTensor.Index.Transform.Z] = round(float(pos_parts[2]))
                        
            
            elif cmd_idx in [LottieTensor.CMD_POSITION_X, LottieTensor.CMD_POSITION_Y, LottieTensor.CMD_POSITION_Z]:
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1
                    current_context = cmd  # Set context to the specific component
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0
                    # Parse the value
                    value_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                value_parts.append(part)
                            except ValueError:
                                pass
                    if value_parts:
                        params[LottieTensor.Index.Transform.X] = round(float(value_parts[0]))
            
            elif cmd_idx == LottieTensor.CMD_SCALE:
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    # Parse scale values
                    scale_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                scale_parts.append(part)
                            except ValueError:
                                pass
                    
                    if len(scale_parts) >= 1:
                        params[LottieTensor.Index.Transform.X] = round(float(scale_parts[0]))
                    if len(scale_parts) >= 2:
                        params[LottieTensor.Index.Transform.Y] = round(float(scale_parts[1]))
                    if len(scale_parts) >= 3:
                        params[LottieTensor.Index.Transform.Z] = round(float(scale_parts[2]))
                        
            elif cmd_idx == LottieTensor.CMD_ROTATION:
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    # Parse rotation value
                    rot_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                rot_parts.append(part)
                            except ValueError:
                                pass
                    if rot_parts:
                        val = round(float(rot_parts[0]))
                        # 添加裁剪：将 rotation 限制在 -720 到 720 范围内
                        val = max(-720, min(720, val % 360 if abs(val) > 720 else val))
                        params[LottieTensor.Index.Transform.X] = val

            elif cmd_idx == LottieTensor.CMD_OPACITY:
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    # Parse opacity value
                    op_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                op_parts.append(part)
                            except ValueError:
                                pass
                    if op_parts:
                        params[LottieTensor.Index.Transform.X] = round(float(op_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_ANCHOR:
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    # Parse anchor values
                    anchor_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                anchor_parts.append(part)
                            except ValueError:
                                pass
                    
                    if len(anchor_parts) >= 1:
                        params[LottieTensor.Index.Transform.X] = round(float(anchor_parts[0]))
                    if len(anchor_parts) >= 2:
                        params[LottieTensor.Index.Transform.Y] = round(float(anchor_parts[1]))
                    if len(anchor_parts) >= 3:
                        params[LottieTensor.Index.Transform.Z] = round(float(anchor_parts[2]))
                        
            elif cmd_idx == LottieTensor.CMD_TM: 
                params[LottieTensor.Index.Tm.A] = int(attrs.get("a", 1))
                #params[LottieTensor.Index.Tm.IX] = float(attrs.get("ix", 2))
                
                # Check if animated
                a_value = int(attrs.get("a", 1))
                if a_value > 0.5:
                    current_context = "tm"  # Set context for keyframes
                else:
                    current_context = "tm_static"  # Different context for static value
                    
                # Don't set special context for a=0, let value command be parsed normally

            # Add value command parsing
            elif cmd_idx == LottieTensor.CMD_VALUE:
                # Parse the numeric value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.Value.VALUE] = round(float(value_parts[0]))



            elif cmd_idx == LottieTensor.CMD_SKEW:
                # Handle standalone skew command
                # Parse the numeric value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                else:
                    params[LottieTensor.Index.SingleValue.VALUE] = 0
                    
            elif cmd_idx == LottieTensor.CMD_SKEW_AXIS:
                # Handle standalone skew_axis command
                # Parse the numeric value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                else:
                    params[LottieTensor.Index.SingleValue.VALUE] = 0

            elif cmd_idx == LottieTensor.CMD_KEYFRAME:
                params[LottieTensor.Index.Keyframe.T] = round(float(attrs.get("t", 0)))
                
                # Check for h parameter (hold keyframe) - for ALL contexts, not just tm
                h_value = attrs.get("h", "0")
                is_hold = h_value == "1" or h_value.lower() == "true"
                
                # Store h parameter flag using dedicated H_FLAG slot
                if is_hold:
                    params[LottieTensor.Index.Keyframe.H_FLAG] = 1.0  # Using H_FLAG to store h flag
                
                # Parse s parameter based on context - check if s exists
                if "s" in attrs:
                    s_str = attrs.get("s", "0").strip('"')
                    s_parts = s_str.split()
                    
                    if current_context in ["rotation", "opacity", "position_x", "position_y", "position_z", "tm", "width", 
                                        "trim_start", "trim_end", "trim_offset", "mask_x", "rotation_animators", "opacity_animators", "tracking_animators", "rect_rounded"]:  # Added trim contexts
                        # For single-value properties, only use S1
                        if s_parts:
                            params[LottieTensor.Index.Keyframe.S1] = round(float(s_parts[0]))
                    elif current_context in ["position", "scale", "anchor", "scale_animators", "position_animators", "size"]:
                        # For position/scale/anchor, use x,y,z values
                        for i, part in enumerate(s_parts[:3]):
                            params[LottieTensor.Index.Keyframe.S1 + i] = round(float(part))
                    elif current_context == "path":
                        # Path keyframes don't have s parameter
                        pass
                    else:
                        # Default case
                        for i, part in enumerate(s_parts[:3]):
                            params[LottieTensor.Index.Keyframe.S1 + i] = round(float(part))
                
                
                # Parse e parameter based on context - ADD THIS FOR TRIM CONTEXTS
                if "e" in attrs:
                    e_str = attrs.get("e", "0").strip('"')
                    # Remove brackets if present
                    if e_str.startswith("[") and e_str.endswith("]"):
                        e_str = e_str[1:-1]
                    
                    e_parts = e_str.split(',')
                    
                    if current_context in ["trim_start", "trim_end", "trim_offset"]:
                        # For trim contexts, e is a single value
                        if e_parts:
                            params[LottieTensor.Index.Keyframe.E1] = round(float(e_parts[0].strip()))
                    elif current_context == "rotation":
                        # For rotation, e is a single value
                        if e_parts:
                            params[LottieTensor.Index.Keyframe.E1] = round(float(e_parts[0].strip()))
                    elif current_context == "scale":
                        # For scale, e has three values
                        for i, part in enumerate(e_parts[:3]):
                            params[LottieTensor.Index.Keyframe.E1 + i] = round(float(part.strip()))
                    # Add other contexts as needed
                
                # Only parse easing parameters if not a hold keyframe
                if not is_hold:
                    # Parse easing parameters based on context
                    if current_context in ["anchor", "size"]:
                        # For multi-dimensional properties, parse multiple easing values
                        i_x_values = LottieTensor._parse_multi_easing_values(attrs.get("i_x", "0"))
                        i_y_values = LottieTensor._parse_multi_easing_values(attrs.get("i_y", "0"))
                        o_x_values = LottieTensor._parse_multi_easing_values(attrs.get("o_x", "0"))
                        o_y_values = LottieTensor._parse_multi_easing_values(attrs.get("o_y", "0"))
                        
                        # Store all three values - MULTIPLY BY 100 AND ROUND
                        params[LottieTensor.Index.Keyframe.I_X] = round(i_x_values[0] * 100)
                        params[LottieTensor.Index.Keyframe.I_X2] = round(i_x_values[1] * 100)
                        params[LottieTensor.Index.Keyframe.I_X3] = round(i_x_values[2] * 100)
                        
                        params[LottieTensor.Index.Keyframe.I_Y] = round(i_y_values[0] * 100)
                        params[LottieTensor.Index.Keyframe.I_Y2] = round(i_y_values[1] * 100)
                        params[LottieTensor.Index.Keyframe.I_Y3] = round(i_y_values[2] * 100)
                        
                        params[LottieTensor.Index.Keyframe.O_X] = round(o_x_values[0] * 100)
                        params[LottieTensor.Index.Keyframe.O_X2] = round(o_x_values[1] * 100)
                        params[LottieTensor.Index.Keyframe.O_X3] = round(o_x_values[2] * 100)
                        
                        params[LottieTensor.Index.Keyframe.O_Y] = round(o_y_values[0] * 100)
                        params[LottieTensor.Index.Keyframe.O_Y2] = round(o_y_values[1] * 100)
                        params[LottieTensor.Index.Keyframe.O_Y3] = round(o_y_values[2] * 100)
                    else:
                        # For single-dimensional properties, parse single easing values - MULTIPLY BY 100 AND ROUND
                        params[LottieTensor.Index.Keyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0")) * 100))
                        params[LottieTensor.Index.Keyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0")) * 100))
                        params[LottieTensor.Index.Keyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0")) * 100))
                        params[LottieTensor.Index.Keyframe.O_Y] =round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0")) * 100))
                
                # Parse to/ti parameters (always use TO1-TO3 and TI1-TI3 for their actual values)
                to_str = attrs.get("to", "")
                ti_str = attrs.get("ti", "")
                
                if to_str:
                    to_values = LottieTensor._extract_array_values(to_str, 3)
                    for i in range(3):
                        params[LottieTensor.Index.Keyframe.TO1 + i] = to_values[i]
                
                if ti_str:
                    ti_values = LottieTensor._extract_array_values(ti_str, 3)
                    for i in range(3):
                        params[LottieTensor.Index.Keyframe.TI1 + i] = ti_values[i]
                    # Parse e parameter based on context
                
                if "e" in attrs:
                    e_str = attrs.get("e", "0").strip('"')
                    # Remove brackets if present
                    if e_str.startswith("[") and e_str.endswith("]"):
                        e_str = e_str[1:-1]
                    
                    e_parts = e_str.split(',')
                    
                    if current_context == "rotation":
                        # For rotation, e is a single value
                        if e_parts:
                            params[LottieTensor.Index.Keyframe.E1] = round(float(e_parts[0].strip()))
                    elif current_context == "scale":
                        # For scale, e has three values
                        for i, part in enumerate(e_parts[:3]):
                            params[LottieTensor.Index.Keyframe.E1 + i] = round(float(part.strip()))
                    # Add other contexts as needed

  
            elif cmd_idx == LottieTensor.CMD_GROUP:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Group")
                #string_params[f"{cmd_key}_mn"] = attrs.get("mn", "ADBE Vector Group")
                
                params[LottieTensor.Index.Group.IX] = int(attrs.get("ix", 1))  #0-1000
                params[LottieTensor.Index.Group.CIX] = int(attrs.get("cix", 2)) #1-10
                params[LottieTensor.Index.Group.BM] = int(attrs.get("bm", 0)) #0-1
                params[LottieTensor.Index.Group.HD] = 1.0 if attrs.get("hd", "false").lower() == "true" else 0.0 #0-1
                params[LottieTensor.Index.Group.NP] = int(attrs.get("np", 0))  # 0-1000
                

            elif cmd_idx == LottieTensor.CMD_PATH:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Path")
                #string_params[f"{cmd_key}_mn"] = attrs.get("mn", "ADBE Vector Path")  # Add mn
                
                params[LottieTensor.Index.Path.IX] = int(attrs.get("ix", 1)) # 0-1000
                params[LottieTensor.Index.Path.IND] = int(attrs.get("ind", 0)) 
                params[LottieTensor.Index.Path.KS_IX] = int(attrs.get("ks_ix", 2))# 2-2
                params[LottieTensor.Index.Path.CLOSED] = 1.0 if attrs.get("closed", "true").lower() == "true" else 0.0
                params[LottieTensor.Index.Path.HD] = 1.0 if attrs.get("hd", "false").lower() == "true" else 0.0  # Add HD
                
                # Track if path is animated
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Path.ANIMATED] = 1.0
                    current_context = "path"
                else:
                    params[LottieTensor.Index.Path.ANIMATED] = 0.0

                    
            elif cmd_idx == LottieTensor.CMD_POINT:
                params[LottieTensor.Index.Point.X] = round(float(attrs.get("x", 0)))
                params[LottieTensor.Index.Point.Y] = round(float(attrs.get("y", 0)))
                params[LottieTensor.Index.Point.IN_X] = round(float(attrs.get("in_x", 0)))
                params[LottieTensor.Index.Point.IN_Y] = round(float(attrs.get("in_y", 0)))
                params[LottieTensor.Index.Point.OUT_X] = round(float(attrs.get("out_x", 0)))
                params[LottieTensor.Index.Point.OUT_Y] = round(float(attrs.get("out_y", 0)))
                

            elif cmd_idx == LottieTensor.CMD_FILL:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Fill")
                
                # Check if color is animated
                color_animated = attrs.get("color_animated", "false").lower() == "true"
                params[LottieTensor.Index.Fill.COLOR_ANIMATED] = 1.0 if color_animated else 0.0
                
                # Check if opacity is animated
                opacity_animated = attrs.get("opacity_animated", "false").lower() == "true"
                params[LottieTensor.Index.Fill.OPACITY_ANIMATED] = 1.0 if opacity_animated else 0.0
                
                # Parse color keyframes if animated
                if color_animated:
                    c_kf_count = int(attrs.get("c_kf_count", 0))
                    color_keyframes = []
                    for i in range(c_kf_count):
                        kf = {
                            't': round(float(attrs.get(f"c_kf_{i}_t", 0))),
                            'r': round(float(attrs.get(f"c_kf_{i}_r", 0))*255),
                            'g': round(float(attrs.get(f"c_kf_{i}_g", 0))*255),
                            'b': round(float(attrs.get(f"c_kf_{i}_b", 0))*255),
                            # Add easing parameters for color keyframes (multiply by 100 and round)
                            'i_x': round(float(attrs.get(f"c_kf_{i}_i_x", 0)) * 100),
                            'i_y': round(float(attrs.get(f"c_kf_{i}_i_y", 0)) * 100),
                            'o_x': round(float(attrs.get(f"c_kf_{i}_o_x", 0)) * 100),
                            'o_y': round(float(attrs.get(f"c_kf_{i}_o_y", 0)) * 100)
                        }
                        color_keyframes.append(kf)
                    # Store in string_params as JSON
                    #string_params[f"{cmd_key}_color_keyframes"] = json.dumps(color_keyframes)
                else:
                    # Parse static color
                    params[LottieTensor.Index.Fill.R] = round(float(attrs.get("r", 0))*255)
                    params[LottieTensor.Index.Fill.G] = round(float(attrs.get("g", 0))*255)
                    params[LottieTensor.Index.Fill.B] = round(float(attrs.get("b", 0))*255)
                
                # Parse opacity keyframes if animated
                if opacity_animated:
                    o_kf_count = int(attrs.get("o_kf_count", 0))
                    opacity_keyframes = []
                    for i in range(o_kf_count):
                        kf = {
                            't': round(float(attrs.get(f"o_kf_{i}_t", 0))),
                            's': round(float(attrs.get(f"o_kf_{i}_s", 100))),
                            'i_x': round(float(attrs.get(f"o_kf_{i}_i_x", 0)) * 100),
                            'i_y': round(float(attrs.get(f"o_kf_{i}_i_y", 0)) * 100),
                            'o_x': round(float(attrs.get(f"o_kf_{i}_o_x", 0)) * 100),
                            'o_y': round(float(attrs.get(f"o_kf_{i}_o_y", 0)) * 100)
                        }
                        opacity_keyframes.append(kf)
                    # Store in string_params as JSON
                    #string_params[f"{cmd_key}_opacity_keyframes"] = json.dumps(opacity_keyframes)
                else:
                    # Parse static opacity
                    params[LottieTensor.Index.Fill.OPACITY] = round(float(attrs.get("opacity", 100)))
                
                # Parse other parameters
                params[LottieTensor.Index.Fill.COLOR_DIM] = int(attrs.get("color_dim", 3))
                params[LottieTensor.Index.Fill.HAS_C_A] = 1.0 if attrs.get("has_c_a", "").lower() == "true" else 0.0
                params[LottieTensor.Index.Fill.HAS_C_IX] = 1.0 if attrs.get("has_c_ix", "").lower() == "true" else 0.0
                params[LottieTensor.Index.Fill.C_IX] = int(attrs.get("c_ix", 4))
                params[LottieTensor.Index.Fill.BM] = int(attrs.get("bm", 0))
                params[LottieTensor.Index.Fill.FILL_RULE] = int(attrs.get("fill_rule", 1))
                params[LottieTensor.Index.Fill.HAS_O_A] = 1.0 if attrs.get("has_o_a", "").lower() == "true" else 0.0
                params[LottieTensor.Index.Fill.HAS_O_IX] = 1.0 if attrs.get("has_o_ix", "").lower() == "true" else 0.0
                params[LottieTensor.Index.Fill.O_IX] = int(attrs.get("o_ix", 5))
                

            elif cmd_idx == LottieTensor.CMD_BEZIER:
                # Parse the closed attribute from input
                closed_str = attrs.get("closed", "true")
                params[LottieTensor.Index.Bezier.CLOSED] = 1.0 if closed_str.lower() == "true" else 0.0
                
            #elif cmd_idx == LottieTensor.CMD_ELLIPSE:
                #name = string_params.get(f"{cmd_key}_name", "Ellipse Path 1")
                #lines.append(f'({cmd} name="{name}")')
                

            elif cmd_idx in [LottieTensor.CMD_POSITION, LottieTensor.CMD_SIZE]:
                if cmd == "size":
                    # Check if size is animated
                    if attrs.get("animated", "").lower() == "true":
                        # Don't parse values when animated
                        params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                        current_context = "size"  # Set context for size keyframes
                    else:
                        # Explicitly set ANIMATED to 0.0 for static size
                        params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                        # Parse two values for static size
                        value_parts = []
                        for part in attrs_str.split():
                            try:
                                round(float(part))
                                value_parts.append(part)
                            except ValueError:
                                pass
                        
                        if len(value_parts) >= 1:
                            params[LottieTensor.Index.Transform.X] = round(float(value_parts[0]))
                        if len(value_parts) >= 2:
                            params[LottieTensor.Index.Transform.Y] = round(float(value_parts[1]))
                            
                else:
                    # Handle position as before
                    value_parts = []
                    for part in attrs_str.split():
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                    
                    if len(value_parts) >= 1:
                        params[LottieTensor.Index.TwoValues.VALUE1] = round(float(value_parts[0]))
                    if len(value_parts) >= 2:
                        params[LottieTensor.Index.TwoValues.VALUE2] = round(float(value_parts[1]))

           
        
            elif cmd_idx == LottieTensor.CMD_RECT:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Rectangle Path 1")
                
                params[LottieTensor.Index.Rect.HD] = 1.0 if attrs.get("hd", "false").lower() == "true" else 0.0
                params[LottieTensor.Index.Rect.D] = int(attrs.get("d", 1))
                
            elif cmd_idx == LottieTensor.CMD_ROUNDED:
                # Parse rounded value and ix
                rounded_val = round(float(attrs.get("rounded", attrs_str.split()[0] if attrs_str.split() else "0")))
                params[LottieTensor.Index.SingleValue.VALUE] = rounded_val
                params[LottieTensor.Index.SingleValue.IX] = int(attrs.get("ix", 4))
                

            # ADD THIS NEW SECTION:
            elif cmd_idx == LottieTensor.CMD_RECT_ROUNDED:
                # Check if animated
                if "animated" in attrs and attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 1.0
                    current_context = "rect_rounded"  # Set context for keyframes
                else:
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 0.0
                    # Parse the value if not animated
                    value_parts = []
                    for part in attrs_str.split():
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                    if value_parts:
                        params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
            

            elif cmd_idx == LottieTensor.CMD_TRIM:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Trim Paths 1")
                params[LottieTensor.Index.Trim.IX] = int(attrs.get("ix", 1))
                
            elif cmd_idx == LottieTensor.CMD_END:
                # Handle trim sub-commands
                # Check if animated
                if "animated" in attrs and attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 1.0
                    current_context = "trim_end"  # Set context for keyframes
                    # Don't parse value when animated=true
                else:
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 0.0
                    # Parse the value
                    value_parts = []
                    for part in attrs_str.split():
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                    if value_parts:
                        params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_START:
                # Handle trim sub-commands
                # Check if animated
                if "animated" in attrs and attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 1.0
                    current_context = "trim_start"  # Set context for keyframes
                    # Don't parse value when animated=true
                else:
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 0.0
                    # Parse the value
                    value_parts = []
                    for part in attrs_str.split():
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                    if value_parts:
                        params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
            elif cmd_idx == LottieTensor.CMD_OFFSET:
                # Handle trim sub-commands
                # Check if animated
                if "animated" in attrs and attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 1.0
                    current_context = "trim_offset"  # Set context for keyframes
                    # Don't parse value when animated=true
                else:
                    params[LottieTensor.Index.SingleValue.ANIMATED] = 0.0
                    # Parse the value
                    value_parts = []
                    for part in attrs_str.split():
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                    if value_parts:
                        params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

        
            elif cmd_idx == LottieTensor.CMD_MULTIPLE:
                # Parse multiple value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_REPEATER:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Repeater 1")
                params[LottieTensor.Index.Repeater.IX] = int(attrs.get("ix", 1))
                
            elif cmd_idx == LottieTensor.CMD_COPIES:
                # Parse copies value and ix
                value_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                params[LottieTensor.Index.SingleValue.IX] = int(attrs.get("ix", 1))
                
            elif cmd_idx == LottieTensor.CMD_REPEATER_OFFSET:
                # Parse repeater_offset value and ix
                value_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                params[LottieTensor.Index.SingleValue.IX] = int(attrs.get("ix", 2))
                
            elif cmd_idx == LottieTensor.CMD_COMPOSITE:
                # Parse composite value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_TR_SCALE:
                # Parse tr_scale values
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if len(value_parts) >= 1:
                    params[LottieTensor.Index.TwoValues.VALUE1] = round(float(value_parts[0]))
                if len(value_parts) >= 2:
                    params[LottieTensor.Index.TwoValues.VALUE2] = round(float(value_parts[1]))
                    
            elif cmd_idx in [LottieTensor.CMD_TR_P_IX, LottieTensor.CMD_TR_A_IX, LottieTensor.CMD_TR_S_IX, 
                            LottieTensor.CMD_TR_R_IX, LottieTensor.CMD_TR_SO_IX, LottieTensor.CMD_TR_EO_IX]:
                # Parse single index value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_TRANSFORM_SHAPE:
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Transform")
                
                # Parse hd attribute
                params[LottieTensor.Index.TransformShape.HD] = 1.0 if attrs.get("hd", "false").lower() == "true" else 0.0
                
                # Parse position
                position_str = attrs.get("position", "0 0").strip('"')
                pos_parts = position_str.split()
                if len(pos_parts) >= 1:
                    params[LottieTensor.Index.TransformShape.POSITION_X] = round(float(pos_parts[0]))
                if len(pos_parts) >= 2:
                    params[LottieTensor.Index.TransformShape.POSITION_Y] = round(float(pos_parts[1]))
                
                # Parse scale
                scale_str = attrs.get("scale", "100 100").strip('"')
                scale_parts = scale_str.split()
                if len(scale_parts) >= 1:
                    params[LottieTensor.Index.TransformShape.SCALE_X] = round(float(scale_parts[0]))
                if len(scale_parts) >= 2:
                    params[LottieTensor.Index.TransformShape.SCALE_Y] = round(float(scale_parts[1]))
                
                # Parse rotation
                rotation_str = attrs.get("rotation", "0").strip('"')
                params[LottieTensor.Index.TransformShape.ROTATION] = round(float(rotation_str))
                
                # Parse opacity
                opacity_str = attrs.get("opacity", "100").strip('"')
                params[LottieTensor.Index.TransformShape.OPACITY] = round(float(opacity_str))
                
                # Parse anchor
                anchor_str = attrs.get("anchor", "0 0").strip('"')
                anchor_parts = anchor_str.split()
                if len(anchor_parts) >= 1:
                    params[LottieTensor.Index.TransformShape.ANCHOR_X] = round(float(anchor_parts[0]))
                if len(anchor_parts) >= 2:
                    params[LottieTensor.Index.TransformShape.ANCHOR_Y] = round(float(anchor_parts[1]))
                
                # Parse skew (only if present)
                if "skew" in attrs:
                    skew_str = attrs.get("skew", "0").strip('"')
                    params[LottieTensor.Index.TransformShape.SKEW] = round(float(skew_str))
                
                # Parse skew_axis (only if present)
                if "skew_axis" in attrs:
                    skew_axis_str = attrs.get("skew_axis", "0").strip('"')
                    params[LottieTensor.Index.TransformShape.SKEW_AXIS] = round(float(skew_axis_str))
                    

            elif cmd_idx == LottieTensor.CMD_PARENT:
                # Parse parent index
                parent_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            parent_parts.append(part)
                        except ValueError:
                            pass
                
                if parent_parts:
                    params[LottieTensor.Index.Parent.PARENT_INDEX] = round(float(parent_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_ASSET:
                if LottieTensor.tokenizer is None:
                    LottieTensor.init_tokenizer()
                
                asset_id = attrs.get("id", "comp_0")
                id_tokens = LottieTensor.tokenizer.encode(asset_id, add_special_tokens=False)[:10]  # Limit to 10 tokens
                
                for i, token_id in enumerate(id_tokens):
                    if i < 10:
                        params[LottieTensor.Index.Asset.ID_TOKEN_0 + i] = int(token_id)
                params[LottieTensor.Index.Asset.ID_TOKEN_COUNT] = int(len(id_tokens))
                
                
                #string_params[f"{cmd_key}_id"] = attrs.get("id", "comp_0")
                #string_params[f"{cmd_key}_nm"] = attrs.get("nm", "asset")

                params[LottieTensor.Index.Asset.FR] = round(float(attrs.get("fr", 30)))
            elif cmd_idx == LottieTensor.CMD_FONT:
                # 存储字符串参数
                #string_params[f"{cmd_key}_family"] = attrs.get("family", "")
                #string_params[f"{cmd_key}_style"] = attrs.get("style", "")
                if LottieTensor.tokenizer is None:
                    LottieTensor.init_tokenizer()
                
                # 编码family和style
                family = attrs.get("family", "")
                style = attrs.get("style", "")
                
                family_tokens = LottieTensor.tokenizer.encode(family, add_special_tokens=False)[:10]
                style_tokens = LottieTensor.tokenizer.encode(style, add_special_tokens=False)[:10]
                
                params[LottieTensor.Index.Font.ASCENT] = round(float(attrs.get("ascent", 75)))
                
                for i, token_id in enumerate(family_tokens):
                    if i < 10:
                        params[LottieTensor.Index.Font.FAMILY_TOKEN_0 + i] = int(token_id)
                params[LottieTensor.Index.Font.FAMILY_TOKEN_COUNT] = int(len(family_tokens))
                
                # Store style tokens
                for i, token_id in enumerate(style_tokens):
                    if i < 10:
                        params[LottieTensor.Index.Font.STYLE_TOKEN_0 + i] = int(token_id)
                params[LottieTensor.Index.Font.STYLE_TOKEN_COUNT] = int(len(style_tokens))


            elif cmd_idx == LottieTensor.CMD_CHAR:
                if LottieTensor.tokenizer is None:
                    LottieTensor.init_tokenizer()

                # 特殊处理 ch 属性，因为可能包含特殊字符如 ")"
                ch_match = re.search(r'ch="([^"]*)"', attrs_str)
                ch = ch_match.group(1) if ch_match else attrs.get("ch", "")
                
                # 解析其他属性时，需要先移除 ch 属性以避免干扰
                temp_attrs_str = attrs_str
                if ch_match:
                    temp_attrs_str = attrs_str[:ch_match.start()] + attrs_str[ch_match.end():]
                
                # 重新解析其他属性
                temp_attrs = LottieTensor._parse_attributes(temp_attrs_str)
                
                style = temp_attrs.get("style", "")
                family = temp_attrs.get("family", "")
                
                # Encode strings
                ch_tokens = LottieTensor.tokenizer.encode(ch, add_special_tokens=False)[:10]
                style_tokens = LottieTensor.tokenizer.encode(style, add_special_tokens=False)[:10]
                family_tokens = LottieTensor.tokenizer.encode(family, add_special_tokens=False)[:10]
                
                params[LottieTensor.Index.Char.SIZE] = round(float(temp_attrs.get("size", 100)))
                params[LottieTensor.Index.Char.W] = round(float(temp_attrs.get("w", 0)))
                
                # Store ch tokens
                for i, token_id in enumerate(ch_tokens):
                    if i < 10:
                        params[LottieTensor.Index.Char.CH_TOKEN_0 + i] = int(token_id)
                params[LottieTensor.Index.Char.CH_TOKEN_COUNT] = int(len(ch_tokens))
                
                # Store style tokens
                for i, token_id in enumerate(style_tokens):
                    if i < 10:
                        params[LottieTensor.Index.Char.STYLE_TOKEN_0 + i] = int(token_id)
                params[LottieTensor.Index.Char.STYLE_TOKEN_COUNT] = int(len(style_tokens))
                
                # Store family tokens
                for i, token_id in enumerate(family_tokens):
                    if i < 10:
                        params[LottieTensor.Index.Char.FAMILY_TOKEN_0 + i] = int(token_id)
                params[LottieTensor.Index.Char.FAMILY_TOKEN_COUNT] = int(len(family_tokens))

            elif cmd_idx == LottieTensor.CMD_FONT_SIZE:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.FontSize.SIZE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_FONT_FAMILY:
                # 提取引号内的字体族名称
                family_match = re.search(r'"([^"]*)"', attrs_str)
                if family_match:
                    string_params[f"{cmd_key}_family"] = family_match.group(1)
                    
            elif cmd_idx == LottieTensor.CMD_TEXT:
                # 提取引号内的文本
                text_match = re.search(r'"([^"]*)"', attrs_str)
                if text_match:
                    string_params[f"{cmd_key}_text"] = text_match.group(1)
                    
            elif cmd_idx == LottieTensor.CMD_CA:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.Ca.VALUE] = int(value_parts[0])
                    
            elif cmd_idx == LottieTensor.CMD_JUSTIFY:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.Justify.VALUE] = int(value_parts[0])
                    
            elif cmd_idx == LottieTensor.CMD_TRACKING:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.Tracking.VALUE] = int(value_parts[0])
                    
            elif cmd_idx == LottieTensor.CMD_LINE_HEIGHT:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.LineHeight.VALUE] = int(value_parts[0])
                    
            elif cmd_idx == LottieTensor.CMD_LETTER_SPACING:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.LetterSpacing.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_FILL_COLOR:  
                # 提取RGB值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round((part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if len(value_parts) >= 1:
                    params[LottieTensor.Index.FillColor.R] = round(float(value_parts[0]) * 255)
                if len(value_parts) >= 2:
                    params[LottieTensor.Index.FillColor.G] = round(float(value_parts[1]) * 255)
                if len(value_parts) >= 3:
                    params[LottieTensor.Index.FillColor.B] = round(float(value_parts[2]) * 255)
                    
            elif cmd_idx == LottieTensor.CMD_G:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.G.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_ALIGNMENT:
                params[LottieTensor.Index.Alignment.A] = round(float(attrs.get("a", 0)))
                
            elif cmd_idx == LottieTensor.CMD_ALIGNMENT_K:
                # 提取两个数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if len(value_parts) >= 1:
                    params[LottieTensor.Index.AlignmentK.VALUE1] = round(float(value_parts[0]))
                if len(value_parts) >= 2:
                    params[LottieTensor.Index.AlignmentK.VALUE2] = round(float(value_parts[1]))
                    
            elif cmd_idx == LottieTensor.CMD_ALIGNMENT_IX:
                # 提取数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.AlignmentIx.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_EFFECTS:
                # effects容器命令，不需要参数
                pass
                
            elif cmd_idx == LottieTensor.CMD_EFFECT:
                # Store string parameters
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")
                #string_params[f"{cmd_key}_match_name"] = attrs.get("match_name", "")
                
                # Store numeric parameters
                params[LottieTensor.Index.Effect.TYPE] = int(attrs.get("type", 0))
                params[LottieTensor.Index.Effect.INDEX] = round(float(attrs.get("index", 1)))
                params[LottieTensor.Index.Effect.NP] = int(attrs.get("np", 0))  # Add NP
                params[LottieTensor.Index.Effect.ENABLED] = round(float(attrs.get("enabled", 1)))  # Add ENABLED

            # Add CMD_LAYER_EFFECT parsing:
            elif cmd_idx == LottieTensor.CMD_LAYER_EFFECT:
                # Store string parameters
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")
                #string_params[f"{cmd_key}_match_name"] = attrs.get("match_name", "")
                
                # Store numeric parameters
                params[LottieTensor.Index.LayerEffect.INDEX] = round(float(attrs.get("index", 1)))
                params[LottieTensor.Index.LayerEffect.VALUE] = round(float(attrs.get("value", 0)))

 
            elif cmd_idx == LottieTensor.CMD_DROPDOWN:
                # 存储字符串参数
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")
                
                # 存储数值参数
                params[LottieTensor.Index.Dropdown.INDEX] = round(float(attrs.get("index", 1)))
                params[LottieTensor.Index.Dropdown.VALUE] = round(float(attrs.get("value", 0)))
            
            elif cmd_idx == LottieTensor.CMD_NO_VALUE:
                # 存储字符串参数
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")
                
                # 存储数值参数
                params[LottieTensor.Index.NO_VALUE.INDEX] = round(float(attrs.get("index", 1)))
                params[LottieTensor.Index.NO_VALUE.VALUE] = round(float(attrs.get("value", 0)))
             
                
            elif cmd_idx == LottieTensor.CMD_IGNORED:
                # 存储字符串参数
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")
                
                # 存储数值参数
                params[LottieTensor.Index.Ignored.INDEX] = round(float(attrs.get("index", 1)))
                params[LottieTensor.Index.Ignored.VALUE] = round(float(attrs.get("value", 0)))
                
            elif cmd_idx == LottieTensor.CMD_SLIDER:
                # 存储字符串参数
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")
                
                # 存储数值参数
                params[LottieTensor.Index.Slider.INDEX] = round(float(attrs.get("index", 1)))
                params[LottieTensor.Index.Slider.VALUE] = round(float(attrs.get("value", 0)))

            elif cmd_idx == LottieTensor.CMD_GRADIENT_FILL:
                # Store name only for gradient_fill command
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Gradient Fill 1")
                # Set context for subsequent commands
                current_context = "gradient_fill"

            elif cmd_idx == LottieTensor.CMD_OPACITY and current_context == "gradient_fill":
                # Parse opacity value for gradient_fill context
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_FILL_RULE:
                # Parse fill_rule value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            
            elif cmd_idx == LottieTensor.CMD_START_POINT:
                # Parse start_point values
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if len(value_parts) >= 1:
                    params[LottieTensor.Index.TwoValues.VALUE1] = LottieTensor._clamp_value(round(float(value_parts[0])))
                if len(value_parts) >= 2:
                    params[LottieTensor.Index.TwoValues.VALUE2] = LottieTensor._clamp_value(round(float(value_parts[1])))
                    

            elif cmd_idx == LottieTensor.CMD_END_POINT:
                # Parse end_point values
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass

                if len(value_parts) >= 1:
                    params[LottieTensor.Index.TwoValues.VALUE1] = LottieTensor._clamp_value(round(float(value_parts[0])))
                if len(value_parts) >= 2:
                    params[LottieTensor.Index.TwoValues.VALUE2] = LottieTensor._clamp_value(round(float(value_parts[1])))
                    
            elif cmd_idx == LottieTensor.CMD_GRADIENT_TYPE:
                # Parse gradient_type value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_STAR:
                # 解析 star 命令的属性
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "None")
                
                # 解析 d 和 sy 参数
                params[LottieTensor.Index.Star.D] = round(float(attrs.get("d", 1)))
                params[LottieTensor.Index.Star.SY] = round(float(attrs.get("sy", 1)))
                # IX 参数如果存在的话
                #params[LottieTensor.Index.Star.IX] = float(attrs.get("ix", 1))

            # 3. 添加 inner_radius 等子命令的解析
            elif cmd_idx == LottieTensor.CMD_INNER_RADIUS:
                # 解析数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_OUTER_RADIUS:
                # 解析数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_INNER_ROUNDNESS:
                # 解析数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_OUTER_ROUNDNESS:
                # 解析数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_POINTS_STAR:  # 这应该是 points_star
                # 解析数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_STAR_ROTATION:
                # 解析数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            
            elif cmd_idx == LottieTensor.CMD_HIGHLIGHT_LENGTH:
                # Parse highlight_length value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_HIGHLIGHT_ANGLE:
                # Parse highlight_angle value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    

            elif cmd_idx == LottieTensor.CMD_ORIGINAL_COLORS:
                colors_match = re.search(r'\[([^\]]*)\]', attrs_str)
                if colors_match:
                    colors_str = colors_match.group(1)
                    color_values = []
                    for color_part in colors_str.split(','):
                        try:
                            color_values.append(round(float(color_part.strip())*255))
                        except ValueError:
                            color_values.append(0)
                    
                    # Store up to 24 color values (increased from 18)
                    for i, val in enumerate(color_values[:48]):
                        if i < 48:  # Make sure we don't exceed our storage capacity
                            params[LottieTensor.Index.OriginalColors.COLOR_0 + i] = val
                    
                    # Store count of colors
                    params[LottieTensor.Index.OriginalColors.COUNT] = int(len(color_values))

       
            elif cmd_idx == LottieTensor.CMD_COLOR_POINTS:
                # Parse color_points value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_GRADIENT_FILL_END:
                # Reset context when gradient_fill ends
                current_context = None
            
                
            elif cmd_idx == LottieTensor.CMD_GRADIENT_STROKE:
                # Store name only - similar to gradient_fill
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Gradient Stroke 1")
                # Set context for subsequent commands
                current_context = "gradient_stroke"

            # Add handling for individual gradient_stroke sub-commands:
            elif cmd_idx == LottieTensor.CMD_OPACITY and current_context == "gradient_stroke":
                # Parse opacity value for gradient_stroke context
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_WIDTH:
                value_parts = []
                for part in attrs_str.split():
                    try:
                        float(part)  # 只检查是否是数字，不用round
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    # 乘以100保留小数精度
                    value = round(float(value_parts[0]) * 10)
                    value = max(0, min(10000, value))  # 裁剪
                    params[LottieTensor.Index.SingleValue.VALUE] = value


            elif cmd_idx == LottieTensor.CMD_LINE_CAP:
                # Parse line_cap value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_LINE_JOIN:
                # Parse line_join value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_MITER_LIMIT:
                # Parse miter_limit value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_GRADIENT_STROKE_END:
                # Reset context when gradient_stroke ends
                current_context = None

            elif cmd_idx == LottieTensor.CMD_COLOR:
                # Store string parameters
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Color")
                
                # Store numeric parameters
                params[LottieTensor.Index.Color.INDEX] = round(float(attrs.get("index", 1)))
                params[LottieTensor.Index.Color.R] = round(float(attrs.get("r", 0))*255)
                params[LottieTensor.Index.Color.G] = round(float(attrs.get("g", 0))*255)
                params[LottieTensor.Index.Color.B] = round(float(attrs.get("b", 0))*255)
            
            
            #elif cmd_idx == LottieTensor.CMD_MERGE:
                # 存储merge的name属性
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Merge Paths 1")
                
            elif cmd_idx == LottieTensor.CMD_MERGE_MODE:
                # 解析merge_mode的数值
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.MergeMode.MODE] = round(float(value_parts[0]))
                    
            

            elif cmd_idx == LottieTensor.CMD_MASK:
                # Store string attributes
                #string_params[f"{cmd_key}_nm"] = attrs.get("nm", "Mask")
                
                params[LottieTensor.Index.Mask.INDEX] = round(float(attrs.get("index", 0)))
                params[LottieTensor.Index.Mask.INV] = 1.0 if attrs.get("inv", "false").lower() == "true" else 0.0
                
                # Parse mode attribute
                mode = attrs.get("mode", "a")
                # Convert mode to numeric for storage
                mode_map = {"a": 0, "s": 1, "i": 2, "n": 3}
                mode_val = mode_map.get(mode, 0)
                params[LottieTensor.Index.Mask.MODE] = round(float(mode_val))
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT:
                params[LottieTensor.Index.MaskPt.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.MaskPt.IX] = int(attrs.get("ix", 1))
                

            elif cmd_idx == LottieTensor.CMD_MASK_PT_K_C:
                # Parse c (closed) attribute - handle both formats
                if "true" in attrs_str.lower():
                    params[LottieTensor.Index.MaskPtK.C] = 1.0
                elif "false" in attrs_str.lower():
                    params[LottieTensor.Index.MaskPtK.C] = 0.0
                else:
                    # Try to parse from c= format if present
                    c_str = attrs.get("c", "true")
                    params[LottieTensor.Index.MaskPtK.C] = 1.0 if c_str.lower() == "true" else 0.0
                    
 
            elif cmd_idx in [LottieTensor.CMD_MASK_PT_K_I, LottieTensor.CMD_MASK_PT_K_O, LottieTensor.CMD_MASK_PT_K_V]:
                # Parse all numeric values from the line
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                
                # Store up to 20 values (increased from 8)
                for i in range(min(20, len(value_parts))):
                    if i < LottieTensor.PARAM_DIM:  # Make sure we don't exceed param dimension
                        params[LottieTensor.Index.MaskPtKValues.V1 + i] = round(float(value_parts[i]))
                
                # Store the count of values in string_params for reconstruction
                params[LottieTensor.Index.MaskPtKValues.COUNT] = round(float(len(value_parts)))

            
            elif cmd_idx == LottieTensor.CMD_MASK_O:
                params[LottieTensor.Index.MaskO.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.MaskO.K] = round(float(attrs.get("k", 100)))
                params[LottieTensor.Index.MaskO.IX] = int(attrs.get("ix", 3))
                
            elif cmd_idx == LottieTensor.CMD_MASK_X:
                params[LottieTensor.Index.MaskX.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.MaskX.K] = round(float(attrs.get("k", 0)))
                params[LottieTensor.Index.MaskX.IX] = int(attrs.get("ix", 4))
                # 添加这部分：检查是否是动画
                if float(attrs.get("a", 0)) > 0.5:
                    current_context = "mask_x"
            
            elif cmd_idx == LottieTensor.CMD_MASKS_PROPERTIES:
                # Container command, no parameters needed
                pass
            elif cmd_idx in [LottieTensor.CMD_MASK_PT_K_ARRAY, LottieTensor.CMD_MASK_PT_K_ARRAY_END,
                  LottieTensor.CMD_MASK_PT_KF_S, LottieTensor.CMD_MASK_PT_KF_S_END,
                  LottieTensor.CMD_MASK_PT_KF_SHAPE_END, LottieTensor.CMD_MASK_PT_KEYFRAME_END]:
                # Container commands, no parameters
                pass
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KEYFRAME:
                params[LottieTensor.Index.MaskPtKeyframe.INDEX] = int(attrs.get("index", 0))
                params[LottieTensor.Index.MaskPtKeyframe.T] = round(float(attrs.get("t", 0)))
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KF_I:
                params[LottieTensor.Index.MaskPtKfI.X] = round(float(attrs.get("x", 0)))
                params[LottieTensor.Index.MaskPtKfI.Y] = round(float(attrs.get("y", 0)))
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KF_O:
                params[LottieTensor.Index.MaskPtKfO.X] = round(float(attrs.get("x", 0)))
                params[LottieTensor.Index.MaskPtKfO.Y] = round(float(attrs.get("y", 0)))
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KF_SHAPE:
                params[LottieTensor.Index.MaskPtKfShape.INDEX] = int(attrs.get("index", 0))
                c_str = attrs.get("c", "true")
                params[LottieTensor.Index.MaskPtKfShape.C] = 1.0 if c_str.lower() == "true" else 0.0
                
            elif cmd_idx in [LottieTensor.CMD_MASK_PT_KF_SHAPE_I, LottieTensor.CMD_MASK_PT_KF_SHAPE_O, 
                            LottieTensor.CMD_MASK_PT_KF_SHAPE_V]:
                # Parse all numeric values from the line
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                
                # Store up to 20 values (increased from 8)
                for i in range(min(20, len(value_parts))):
                    if i < LottieTensor.PARAM_DIM:  # Make sure we don't exceed param dimension
                        params[LottieTensor.Index.MaskPtKfShapeValues.V1 + i] = round(float(value_parts[i]))
                
                # Store the count in params, NOT in string_params
                params[LottieTensor.Index.MaskPtKfShapeValues.COUNT] = round(float(len(value_parts)))
                
               
            elif cmd_idx == LottieTensor.CMD_TR_POSITION:
                # Parse tr_position values
                value_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                if len(value_parts) >= 1:
                    params[LottieTensor.Index.TrPosition.X] = round(float(value_parts[0]))
                if len(value_parts) >= 2:
                    params[LottieTensor.Index.TrPosition.Y] = round(float(value_parts[1]))
                    
            elif cmd_idx == LottieTensor.CMD_TR_ANCHOR:
                # Parse tr_anchor values
                value_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                if len(value_parts) >= 1:
                    params[LottieTensor.Index.TrAnchor.X] = round(float(value_parts[0]))
                if len(value_parts) >= 2:
                    params[LottieTensor.Index.TrAnchor.Y] = round(float(value_parts[1]))
                    
            elif cmd_idx == LottieTensor.CMD_TR_ROTATION:
                # Parse tr_rotation value
                value_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                if value_parts:
                    params[LottieTensor.Index.TrRotation.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_TR_START_OPACITY:
                # Parse tr_start_opacity value
                value_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                if value_parts:
                    params[LottieTensor.Index.TrStartOpacity.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_TR_END_OPACITY:
                # Parse tr_end_opacity value
                value_parts = []
                for part in attrs_str.split():
                    if '=' not in part:
                        try:
                            round(float(part))
                            value_parts.append(part)
                        except ValueError:
                            pass
                if value_parts:
                    params[LottieTensor.Index.TrEndOpacity.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_ZIG_ZAG:
                # Store string parameters
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "Zig Zag 1")
                
                # Store numeric parameters
                params[LottieTensor.Index.ZigZag.IX] = int(attrs.get("ix", 2))
                
            elif cmd_idx == LottieTensor.CMD_FREQUENCY:
                # Parse frequency value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.Frequency.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_AMPLITUDE:
                # Parse amplitude value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.Amplitude.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_POINT_TYPE:
                # Parse point_type value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.PointType.VALUE] = round(float(value_parts[0]))
                    
            elif cmd_idx == LottieTensor.CMD_ANIMATORS:
                # Container command, no parameters
                pass
                
            #elif cmd_idx == LottieTensor.CMD_ANIMATOR:
                # Store animator name
                #string_params[f"{cmd_key}_nm"] = attrs.get("nm", "Animator 1")
                

            elif cmd_idx == LottieTensor.CMD_RANGE_SELECTOR:
                params[LottieTensor.Index.RangeSelector.T] = round(float(attrs.get("t", 0)))
                params[LottieTensor.Index.RangeSelector.R] = round(float(attrs.get("r", 1)))
                params[LottieTensor.Index.RangeSelector.B] = round(float(attrs.get("b", 1)))
                params[LottieTensor.Index.RangeSelector.SH] = round(float(attrs.get("sh", 1)))  #这里还需要check下
                params[LottieTensor.Index.RangeSelector.RN] = round(float(attrs.get("rn", 0)))

            elif cmd_idx == LottieTensor.CMD_RANGE_START:
                params[LottieTensor.Index.RangeStart.A] = round(float(attrs.get("a", 0)))
                # Check if animated
                if float(attrs.get("a", 0)) > 0.5:
                    current_context = "range_start"
                    
            elif cmd_idx == LottieTensor.CMD_RANGE_START_KEYFRAME:
                params[LottieTensor.Index.RangeStartKeyframe.T] = round(float(attrs.get("t", 0)))
                params[LottieTensor.Index.RangeStartKeyframe.S] = round(float(attrs.get("s", 0)))
                params[LottieTensor.Index.RangeStartKeyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0"))*100))
                params[LottieTensor.Index.RangeStartKeyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0"))*100))
                params[LottieTensor.Index.RangeStartKeyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0"))*100))
                params[LottieTensor.Index.RangeStartKeyframe.O_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0"))*100))

                
            elif cmd_idx == LottieTensor.CMD_AMOUNT:
                params[LottieTensor.Index.Amount.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.Amount.K] = round(float(attrs.get("k", 100)))
                params[LottieTensor.Index.Amount.IX] = int(attrs.get("ix", 4))
                
            elif cmd_idx == LottieTensor.CMD_MAX_EASE:
                params[LottieTensor.Index.MaxEase.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.MaxEase.K] = round(float(attrs.get("k", 0)))
                params[LottieTensor.Index.MaxEase.IX] = int(attrs.get("ix", 7))
                
            elif cmd_idx == LottieTensor.CMD_MIN_EASE:
                params[LottieTensor.Index.MinEase.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.MinEase.K] = round(float(attrs.get("k", 0)))
                params[LottieTensor.Index.MinEase.IX] = int(attrs.get("ix", 8))
                
            elif cmd_idx == LottieTensor.CMD_ANIMATOR_PROPERTIES:
                # Container command, no parameters
                current_context = "animator_properties"  # Set context for opacity handling
                pass
                
            elif cmd_idx == LottieTensor.CMD_ANIMATOR_PROPERTIES_END:
                current_context = None  # Reset context
                pass
                
            elif cmd_idx == LottieTensor.CMD_OPACITY and current_context == "animator_properties":
                # Special handling for opacity within animator_properties
                params[LottieTensor.Index.Amount.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.Amount.K] = round(float(attrs.get("k", 0)))
                params[LottieTensor.Index.Amount.IX] = int(attrs.get("ix", 9))
            
            elif cmd_idx == LottieTensor.CMD_RADIUS:
                # Parse radius value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.Radius.VALUE] = round(float(value_parts[0]))

            elif cmd_idx == LottieTensor.CMD_RANGE_END:
                params[LottieTensor.Index.RangeEnd.A] = round(float(attrs.get("a", 0)))
                # Check if animated
                if float(attrs.get("a", 0)) > 0.5:
                    current_context = "range_end"
                    
            elif cmd_idx == LottieTensor.CMD_RANGE_END_KEYFRAME:
                params[LottieTensor.Index.RangeEndKeyframe.T] = round(float(attrs.get("t", 0)))
                params[LottieTensor.Index.RangeEndKeyframe.S] = round(float(attrs.get("s", 0)))
                params[LottieTensor.Index.RangeEndKeyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0"))*100))
                params[LottieTensor.Index.RangeEndKeyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0"))*100))
                params[LottieTensor.Index.RangeEndKeyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0"))*100))
                params[LottieTensor.Index.RangeEndKeyframe.O_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0"))*100))
            
            
            elif cmd_idx == LottieTensor.CMD_POSITION and current_context == "animator_properties":
                # Special handling for position within animator_properties
                params[LottieTensor.Index.Amount.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.Amount.IX] = int(attrs.get("ix", 2))
                
                # Parse k parameter which can be an array
                k_str = attrs.get("k", "0")
                if k_str.startswith("[") and k_str.endswith("]"):
                    # Parse array values
                    k_str = k_str[1:-1]  # Remove brackets
                    k_parts = k_str.split(",")
                    if len(k_parts) >= 1:
                        params[LottieTensor.Index.Transform.X] = round(float(k_parts[0].strip()))
                    if len(k_parts) >= 2:
                        params[LottieTensor.Index.Transform.Y] = round(float(k_parts[1].strip()))
                    if len(k_parts) >= 3:
                        params[LottieTensor.Index.Transform.Z] = round(float(k_parts[2].strip()))
                else:
                    params[LottieTensor.Index.Amount.K] = round(float(k_str))

            elif cmd_idx == LottieTensor.CMD_ML2:
                # Parse ml2 value
                value_parts = []
                for part in attrs_str.split():
                    try:
                        round(float(part))
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    params[LottieTensor.Index.SingleValue.VALUE] = round(float(value_parts[0]))


            elif cmd_idx == LottieTensor.CMD_RANGE_OFFSET_KEYFRAME:
                params[LottieTensor.Index.RangeOffsetKeyframe.T] = round(float(attrs.get("t", 0)))
                params[LottieTensor.Index.RangeOffsetKeyframe.S] = round(float(attrs.get("s", 0)))
                params[LottieTensor.Index.RangeOffsetKeyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0"))*100))
                params[LottieTensor.Index.RangeOffsetKeyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0"))*100))
                params[LottieTensor.Index.RangeOffsetKeyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0"))*100))
                params[LottieTensor.Index.RangeOffsetKeyframe.O_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0"))*100))
                
            elif cmd_idx == LottieTensor.CMD_S_M:
                params[LottieTensor.Index.SM.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.SM.K] = round(float(attrs.get("k", 100)))
                params[LottieTensor.Index.SM.IX] = int(attrs.get("ix", 6))
                

            elif cmd_idx == LottieTensor.CMD_OPACITY_ANIMATORS:
                params[LottieTensor.Index.OpacityAnimators.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.OpacityAnimators.IX] = int(attrs.get("ix", 9))
                
                # If not animated (a=0), parse k value
                if float(attrs.get("a", 0)) < 0.5:
                    params[LottieTensor.Index.OpacityAnimators.K] = round(float(attrs.get("k", 0)))
                else:
                    # Set context for animated keyframes
                    current_context = "opacity_animators"

            elif cmd_idx == LottieTensor.CMD_POSITION_ANIMATORS_END:
                current_context = None

            # 添加 CMD_POSITION_ANIMATORS 处理：
            elif cmd_idx == LottieTensor.CMD_POSITION_ANIMATORS:
                params[LottieTensor.Index.PositionAnimators.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.PositionAnimators.IX] = int(attrs.get("ix", 2))
                
                # If not animated (a=0), parse k value
                if float(attrs.get("a", 0)) < 0.5:
                    # Parse k value which could be a single value or array
                    k_str = attrs.get("k", "0")
                    if k_str.startswith("[") and k_str.endswith("]"):
                        # Parse array values
                        k_str = k_str[1:-1]  # Remove brackets
                        k_parts = k_str.split(",")
                        if len(k_parts) >= 1:
                            params[LottieTensor.Index.PositionAnimators.K_X] = round(float(k_parts[0].strip()))
                        if len(k_parts) >= 2:
                            params[LottieTensor.Index.PositionAnimators.K_Y] = round(float(k_parts[1].strip()))
                        if len(k_parts) >= 3:
                            params[LottieTensor.Index.PositionAnimators.K_Z] = round(float(k_parts[2].strip()))
                    else:
                        # Single value - apply to all dimensions
                        try:
                            k_val = round(float(k_str))
                            params[LottieTensor.Index.PositionAnimators.K_X] = k_val
                            params[LottieTensor.Index.PositionAnimators.K_Y] = k_val
                            params[LottieTensor.Index.PositionAnimators.K_Z] = k_val
                        except ValueError:
                            # Default to 0 if parsing fails
                            params[LottieTensor.Index.PositionAnimators.K_X] = 0
                            params[LottieTensor.Index.PositionAnimators.K_Y] = 0
                            params[LottieTensor.Index.PositionAnimators.K_Z] = 0
                else:
                    # Set context for animated keyframes
                    current_context = "position_animators"


            # 添加 CMD_TRACKING_ANIMATORS 处理：
            elif cmd_idx == LottieTensor.CMD_TRACKING_ANIMATORS:
                params[LottieTensor.Index.TrackingAnimators.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.TrackingAnimators.K] = round(float(attrs.get("k", 0)))
                params[LottieTensor.Index.TrackingAnimators.IX] = int(attrs.get("ix", 89))
                
                # If animated, set context
                if float(attrs.get("a", 0)) > 0.5:
                    current_context = "tracking_animators"


            elif cmd_idx == LottieTensor.CMD_SCALE_ANIMATORS:
                params[LottieTensor.Index.ScaleAnimators.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.ScaleAnimators.IX] = int(attrs.get("ix", 3))
                
                # If not animated (a=0), parse k value
                if float(attrs.get("a", 0)) < 0.5:
                    # Parse k value which could be a single value or array
                    k_str = attrs.get("k", "100")
                    if k_str.startswith("[") and k_str.endswith("]"):
                        # Parse array values
                        k_str = k_str[1:-1]  # Remove brackets
                        k_parts = k_str.split(",")
                        if len(k_parts) >= 1:
                            params[LottieTensor.Index.ScaleAnimators.K_X] = round(float(k_parts[0].strip()))
                        if len(k_parts) >= 2:
                            params[LottieTensor.Index.ScaleAnimators.K_Y] = round(float(k_parts[1].strip()))
                        if len(k_parts) >= 3:
                            params[LottieTensor.Index.ScaleAnimators.K_Z] = round(float(k_parts[2].strip()))
                    else:
                        # Single value - apply to all dimensions
                        k_val = round(float(k_str))
                        params[LottieTensor.Index.ScaleAnimators.K_X] = k_val
                        params[LottieTensor.Index.ScaleAnimators.K_Y] = k_val
                        params[LottieTensor.Index.ScaleAnimators.K_Z] = k_val
                else:
                    # Set context for animated keyframes
                    current_context = "scale_animators"

            elif cmd_idx == LottieTensor.CMD_ROTATION_ANIMATORS:
                params[LottieTensor.Index.RotationAnimators.A] = int(attrs.get("a", 0))
                params[LottieTensor.Index.RotationAnimators.IX] = int(attrs.get("ix", 4))
                
                # If not animated (a=0), parse k value
                if float(attrs.get("a", 0)) < 0.5:
                    params[LottieTensor.Index.RotationAnimators.K] = int(attrs.get("k", 0))
                else:
                    # Set context for animated keyframes
                    current_context = "rotation_animators"

            elif cmd_idx == LottieTensor.CMD_SCALE_ANIMATORS_END:
                current_context = None
                
            elif cmd_idx == LottieTensor.CMD_ROTATION_ANIMATORS_END:
                current_context = None


            elif cmd_idx == LottieTensor.CMD_RANGE_OFFSET:
                # Parse the 'a' attribute correctly
                params[LottieTensor.Index.Amount.A] = int(attrs.get("a", 0))
                # Check if animated
                if float(attrs.get("a", 0)) > 0.5:
                    # Animated case - set context for keyframes
                    current_context = "range_offset"
                else:
                    # Static case - also parse k and ix values
                    params[LottieTensor.Index.Amount.K] = int(attrs.get("k", 0))
                    params[LottieTensor.Index.Amount.IX] = int(attrs.get("ix", 3))

            elif cmd_idx == LottieTensor.CMD_DASHES:
                # Container command for dashes
                # Parse the entire dashes string if present
                dashes_str = attrs_str.strip()
                if dashes_str:
                    string_params[f"{cmd_key}_dashes"] = dashes_str
                

            elif cmd_idx == LottieTensor.CMD_DASH:
                dash_type = attrs.get("type", "d")
                type_map = {"d": 0, "g": 1, "o": 2}
                params[LottieTensor.Index.Dash.TYPE] = int(type_map.get(dash_type, 0))
                
                # 乘以100保留小数精度
                length_val = round(float(attrs.get("length", 0)) * 10)
                length_val = max(0, min(10000, length_val))
                params[LottieTensor.Index.Dash.LENGTH] = length_val
                
                params[LottieTensor.Index.Dash.V_IX] = int(attrs.get("v_ix", 1))


                # Store name in string_params
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")

            elif cmd_idx == LottieTensor.CMD_DASH_ANIMATED:
                # Parse dash_animated attributes
                dash_type = attrs.get("type", "o")
                # Convert type to numeric
                type_map = {"d": 0, "g": 1, "o": 2}
                params[LottieTensor.Index.DashAnimated.TYPE] = int(type_map.get(dash_type, 2))
                
                # Parse v_ix
                params[LottieTensor.Index.DashAnimated.V_IX] = int(attrs.get("v_ix", 7))
                
                # Store name in string_params
                #string_params[f"{cmd_key}_name"] = attrs.get("name", "")
                
                # Set context for keyframes
                current_context = "dash_animated"

            elif cmd_idx == LottieTensor.CMD_DASH_KEYFRAME:
                params[LottieTensor.Index.DashKeyframe.T] = round(float(attrs.get("t", 0)))
                # 改成乘以10，并裁剪
                s_val = round(float(attrs.get("s", 0)) * 10)
                s_val = max(0, min(10000, s_val))
                params[LottieTensor.Index.DashKeyframe.S] = s_val
                
                # easing参数保持不变
                params[LottieTensor.Index.DashKeyframe.I_X] = round(float(LottieTensor._parse_easing_value(attrs.get("i_x", "0"))*100))
                params[LottieTensor.Index.DashKeyframe.I_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("i_y", "0"))*100))
                params[LottieTensor.Index.DashKeyframe.O_X] = round(float(LottieTensor._parse_easing_value(attrs.get("o_x", "0"))*100))
                params[LottieTensor.Index.DashKeyframe.O_Y] = round(float(LottieTensor._parse_easing_value(attrs.get("o_y", "0"))*100))
                
                
            elif cmd_idx == LottieTensor.CMD_DASH_ANIMATED_END:
                # Reset context
                current_context = None

            elif cmd_idx == LottieTensor.CMD_DASH_OFFSET:
                value_parts = []
                for part in attrs_str.split():
                    try:
                        float(part)
                        value_parts.append(part)
                    except ValueError:
                        pass
                if value_parts:
                    # 改成乘以10，并裁剪
                    value = round(float(value_parts[0]) * 10)
                    value = max(0, min(10000, value))
                    params[LottieTensor.Index.DashOffset.O] = value
                    


            elif cmd_idx == LottieTensor.CMD_DASHES_END:
                # End of dashes container
                pass
            elif cmd_idx == LottieTensor.CMD_SIZE_END:
                # End of dashes container
                pass


            elif cmd_idx == LottieTensor.CMD_RECT_SIZE:
                # 检查是否是动画
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                    current_context = "size"
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    value_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                value_parts.append(part)
                            except ValueError:
                                pass
                    
                    if len(value_parts) >= 1:
                        params[LottieTensor.Index.Transform.X] = round(float(value_parts[0]))
                    if len(value_parts) >= 2:
                        params[LottieTensor.Index.Transform.Y] = round(float(value_parts[1]))



            elif cmd_idx == LottieTensor.CMD_ELLIPSE_SIZE:
                # 检查是否是动画
                if attrs.get("animated", "").lower() == "true":
                    params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                    current_context = "size"  # 设置上下文用于关键帧
                else:
                    params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    # 解析静态值
                    value_parts = []
                    for part in attrs_str.split():
                        if '=' not in part:
                            try:
                                round(float(part))
                                value_parts.append(part)
                            except ValueError:
                                pass
                    
                    if len(value_parts) >= 1:
                        params[LottieTensor.Index.Transform.X] = round(float(value_parts[0]))
                    if len(value_parts) >= 2:
                        params[LottieTensor.Index.Transform.Y] = round(float(value_parts[1]))
                        
            params_list.append(params)


        # Convert to tensors
        commands_tensor = torch.tensor(commands).long()
        params_tensor = torch.tensor(params_list).float()
        lottie_tensor = LottieTensor(commands_tensor, params_tensor)
        #lottie_tensor.string_params = string_params
        
        return lottie_tensor


    def from_sequence_v2(sequence_str)-> 'LottieTensor':
        """
        Parse a sequence string back into a Lottie animation dictionary.
        Properly handles nested group structures using a stack.
        """
        lines = sequence_str.strip().split('\n')
        
        animation = {
            "v": "5.5.2",
            "fr": 30,
            "ip": 0,
            "op": 60,
            "w": 512,
            "h": 512,
            "nm": "Animation",
            "ddd": 0,
            "assets": [],
            "layers": [],
            "markers": [],
            "props": {},
            "fonts": None,
            "chars": None
        }
        
        # Stack for tracking nested structures
        # Each entry is (type, object, items_list)
        stack = []
        
        current_layer = None
        current_transform = None
        current_path = None
        current_path_points = []
        current_keyframes = []
        current_context = None  # 'position', 'scale', 'rotation', 'opacity', 'anchor'
        
        def parse_attrs(attr_str):
            """Parse attribute string into dict"""
            attrs = {}
            if not attr_str:
                return attrs
            
            import re
            # Handle quoted values
            pattern = r'(\w+)=(?:"([^"]*)"|(\S+))'
            for match in re.finditer(pattern, attr_str):
                key = match.group(1)
                value = match.group(2) if match.group(2) is not None else match.group(3)
                attrs[key] = value
            
            # Handle space-separated values without keys
            parts = attr_str.split()
            positional = []
            for part in parts:
                if '=' not in part:
                    try:
                        positional.append(float(part))
                    except ValueError:
                        pass
            if positional:
                attrs['_positional'] = positional
            
            return attrs
        
        def parse_command(line):
            """Parse a command line into (command, attrs_str)"""
            line = line.strip()
            if not line.startswith('(') or not line.endswith(')'):
                return None, ""
            
            content = line[1:-1].strip()
            
            # Handle end tags
            if content.startswith('/'):
                return content, ""
            
            # Handle quoted commands like "TransformShape"
            if content.startswith('"'):
                end_quote = content.find('"', 1)
                if end_quote > 0:
                    cmd = content[:end_quote+1]
                    attrs = content[end_quote+1:].strip()
                    return cmd, attrs
            
            # Regular command
            parts = content.split(' ', 1)
            cmd = parts[0]
            attrs = parts[1] if len(parts) > 1 else ""
            return cmd, attrs
        
        def get_current_items_container():
            """Get the current container for adding items"""
            if stack:
                return stack[-1][2]  # items list
            elif current_layer:
                return current_layer.get('shapes', [])
            return None
        
        def add_to_current_container(item):
            """Add item to current container"""
            container = get_current_items_container()
            if container is not None:
                container.append(item)
        
        for line in lines:
            cmd, attrs_str = parse_command(line)
            if cmd is None:
                continue
            
            attrs = parse_attrs(attrs_str)
            
            # ========== Animation ==========
            if cmd == 'animation':
                animation['v'] = attrs.get('v', '5.5.2').strip('"')
                animation['fr'] = float(attrs.get('fr', 30))
                animation['ip'] = float(attrs.get('ip', 0))
                animation['op'] = float(attrs.get('op', 60))
                animation['w'] = float(attrs.get('w', 512))
                animation['h'] = float(attrs.get('h', 512))
                animation['ddd'] = int(attrs.get('ddd', 0))
            
            # ========== Layer ==========
            elif cmd == 'layer':
                current_layer = {
                    'ddd': int(attrs.get('ddd', 0)),
                    'ind': int(float(attrs.get('index', 0))),
                    'ty': 4,  # Shape layer
                    'nm': 'Layer',
                    'sr': 1,
                    'ks': {},
                    'ao': int(attrs.get('ao', 0)),
                    'shapes': [],
                    'ip': float(attrs.get('in_point', 0)),
                    'op': float(attrs.get('out_point', 60)),
                    'st': float(attrs.get('start_time', 0)),
                    'bm': 0
                }
                animation['layers'].append(current_layer)
                stack.clear()  # New layer, clear stack
            
            elif cmd == '/layer':
                current_layer = None
                stack.clear()
            
            # ========== Transform ==========
            elif cmd == 'transform':
                current_transform = {
                    'o': {'a': 0, 'k': 100, 'ix': 11},
                    'r': {'a': 0, 'k': 0, 'ix': 10},
                    'p': {'a': 0, 'k': [0, 0, 0], 'ix': 2},
                    'a': {'a': 0, 'k': [0, 0, 0], 'ix': 1},
                    's': {'a': 0, 'k': [100, 100, 100], 'ix': 6}
                }
            
            elif cmd == '/transform':
                if current_layer and current_transform:
                    current_layer['ks'] = current_transform
                current_transform = None
                current_context = None
            
            # ========== Transform properties ==========
            elif cmd == 'position':
                current_context = 'position'
                current_keyframes = []
                if 'animated' in attrs and attrs.get('animated', '').lower() == 'true':
                    if current_transform:
                        current_transform['p'] = {'a': 1, 'k': [], 'ix': 2}
                else:
                    pos = attrs.get('_positional', [0, 0])
                    if current_transform:
                        current_transform['p'] = {'a': 0, 'k': pos + [0] if len(pos) == 2 else pos, 'ix': 2}
            
            elif cmd == '/position':
                if current_transform and current_keyframes:
                    current_transform['p'] = {'a': 1, 'k': current_keyframes, 'ix': 2}
                current_context = None
                current_keyframes = []
            
            elif cmd == 'scale':
                current_context = 'scale'
                current_keyframes = []
                if 'animated' in attrs and attrs.get('animated', '').lower() == 'true':
                    if current_transform:
                        current_transform['s'] = {'a': 1, 'k': [], 'ix': 6}
                else:
                    scale = attrs.get('_positional', [100, 100, 100])
                    if current_transform:
                        current_transform['s'] = {'a': 0, 'k': scale, 'ix': 6}
            
            elif cmd == '/scale':
                if current_transform and current_keyframes:
                    current_transform['s'] = {'a': 1, 'k': current_keyframes, 'ix': 6}
                current_context = None
                current_keyframes = []
            
            elif cmd == 'rotation':
                current_context = 'rotation'
                current_keyframes = []
                if 'animated' in attrs and attrs.get('animated', '').lower() == 'true':
                    if current_transform:
                        current_transform['r'] = {'a': 1, 'k': [], 'ix': 10}
                else:
                    rot = attrs.get('_positional', [0])
                    if current_transform:
                        current_transform['r'] = {'a': 0, 'k': rot[0] if rot else 0, 'ix': 10}
            
            elif cmd == 'opacity':
                current_context = 'opacity'
                current_keyframes = []
                if 'animated' in attrs and attrs.get('animated', '').lower() == 'true':
                    if current_transform:
                        current_transform['o'] = {'a': 1, 'k': [], 'ix': 11}
                else:
                    op = attrs.get('_positional', [100])
                    if current_transform:
                        current_transform['o'] = {'a': 0, 'k': op[0] if op else 100, 'ix': 11}
            
            elif cmd == '/opacity':
                if current_transform and current_keyframes:
                    current_transform['o'] = {'a': 1, 'k': current_keyframes, 'ix': 11}
                current_context = None
                current_keyframes = []
            
            elif cmd == 'anchor':
                pos = attrs.get('_positional', [0, 0])
                if current_transform:
                    current_transform['a'] = {'a': 0, 'k': pos + [0] if len(pos) == 2 else pos, 'ix': 1}
            
            # ========== Keyframes ==========
            elif cmd == 'keyframe':
                t = float(attrs.get('t', 0))
                
                # Parse s value
                s_str = attrs.get('s', '0')
                if s_str.startswith('"') and s_str.endswith('"'):
                    s_str = s_str[1:-1]
                s_parts = s_str.split()
                s_val = [float(x) for x in s_parts] if s_parts else [0]
                
                keyframe = {'t': t, 's': s_val}
                
                # Parse easing
                i_x = float(attrs.get('i_x', 0))
                i_y = float(attrs.get('i_y', 0))
                o_x = float(attrs.get('o_x', 0))
                o_y = float(attrs.get('o_y', 0))
                
                if i_x != 0 or i_y != 0 or o_x != 0 or o_y != 0:
                    keyframe['i'] = {'x': [i_x], 'y': [i_y]}
                    keyframe['o'] = {'x': [o_x], 'y': [o_y]}
                
                # Parse to/ti
                if 'to' in attrs:
                    to_str = attrs['to'].strip('"[]')
                    to_parts = [float(x.strip()) for x in to_str.split(',') if x.strip()]
                    if to_parts:
                        keyframe['to'] = to_parts
                
                if 'ti' in attrs:
                    ti_str = attrs['ti'].strip('"[]')
                    ti_parts = [float(x.strip()) for x in ti_str.split(',') if x.strip()]
                    if ti_parts:
                        keyframe['ti'] = ti_parts
                
                current_keyframes.append(keyframe)
            
            # ========== Group ==========
            elif cmd == 'group':
                group = {
                    'ty': 'gr',
                    'nm': 'Group',
                    'np': int(attrs.get('np', 0)),
                    'cix': int(attrs.get('cix', 2)),
                    'bm': int(attrs.get('bm', 0)),
                    'ix': int(attrs.get('ix', 1)),
                    'mn': 'ADBE Vector Group',
                    'hd': attrs.get('hd', 'false').lower() == 'true',
                    'it': []  # Items go here
                }
                
                # Add to current container
                add_to_current_container(group)
                
                # Push onto stack
                stack.append(('group', group, group['it']))
            
            elif cmd == '/group':
                if stack and stack[-1][0] == 'group':
                    stack.pop()
            
            # ========== Path ==========
            elif cmd == 'path':
                current_path = {
                    'ty': 'sh',
                    'nm': 'Path',
                    'mn': 'ADBE Vector Shape - Group',
                    'hd': attrs.get('hd', 'false').lower() == 'true',
                    'ix': int(attrs.get('ix', 1)),
                    'ind': int(attrs.get('ind', 0)),
                    'ks': {
                        'a': 0,
                        'k': {
                            'c': attrs.get('closed', 'true').lower() == 'true',
                            'v': [],
                            'i': [],
                            'o': []
                        },
                        'ix': int(attrs.get('ks_ix', 2))
                    }
                }
                current_path_points = []
            
            elif cmd == '/path':
                if current_path:
                    # Build bezier from points
                    bezier = current_path['ks']['k']
                    for pt in current_path_points:
                        bezier['v'].append([pt['x'], pt['y']])
                        bezier['i'].append([pt['in_x'], pt['in_y']])
                        bezier['o'].append([pt['out_x'], pt['out_y']])
                    
                    add_to_current_container(current_path)
                    current_path = None
                    current_path_points = []
            
            elif cmd == 'point':
                pt = {
                    'x': float(attrs.get('x', 0)),
                    'y': float(attrs.get('y', 0)),
                    'in_x': float(attrs.get('in_x', 0)),
                    'in_y': float(attrs.get('in_y', 0)),
                    'out_x': float(attrs.get('out_x', 0)),
                    'out_y': float(attrs.get('out_y', 0))
                }
                current_path_points.append(pt)
            
            # ========== Fill ==========
            elif cmd == 'fill':
                fill = {
                    'ty': 'fl',
                    'nm': 'Fill',
                    'mn': 'ADBE Vector Graphic - Fill',
                    'hd': False,
                    'c': {
                        'a': 0,
                        'k': [
                            float(attrs.get('r', 0.5)),
                            float(attrs.get('g', 0.5)),
                            float(attrs.get('b', 0.5)),
                            1
                        ],
                        'ix': int(attrs.get('c_ix', 4))
                    },
                    'o': {
                        'a': 0,
                        'k': float(attrs.get('opacity', 100)),
                        'ix': int(attrs.get('o_ix', 5))
                    },
                    'r': int(attrs.get('fill_rule', 1)),
                    'bm': int(attrs.get('bm', 0))
                }
                add_to_current_container(fill)
            
            # ========== Stroke ==========
            elif cmd == 'stroke':
                stroke = {
                    'ty': 'st',
                    'nm': 'Stroke',
                    'mn': 'ADBE Vector Graphic - Stroke',
                    'hd': False,
                    'c': {
                        'a': 0,
                        'k': [
                            float(attrs.get('r', 0)),
                            float(attrs.get('g', 0)),
                            float(attrs.get('b', 0)),
                            1
                        ],
                        'ix': int(attrs.get('c_ix', 3))
                    },
                    'o': {
                        'a': 0,
                        'k': 100,
                        'ix': 4
                    },
                    'w': {
                        'a': 0,
                        'k': float(attrs.get('width', 2)),
                        'ix': 5
                    },
                    'lc': int(attrs.get('lc', 2)),
                    'lj': int(attrs.get('lj', 2)),
                    'ml': float(attrs.get('ml', 4)),
                    'bm': int(attrs.get('bm', 0))
                }
                add_to_current_container(stroke)
            
            # ========== TransformShape (group transform) ==========
            elif cmd == '"TransformShape"':
                # Parse position
                pos_str = attrs.get('position', '0 0').strip('"')
                pos_parts = pos_str.split()
                pos = [float(x) for x in pos_parts] if pos_parts else [0, 0]
                
                # Parse scale
                scale_str = attrs.get('scale', '100 100').strip('"')
                scale_parts = scale_str.split()
                scale = [float(x) for x in scale_parts] if scale_parts else [100, 100]
                
                # Parse rotation
                rot_str = attrs.get('rotation', '0').strip('"')
                rot = float(rot_str)
                
                # Parse opacity
                op_str = attrs.get('opacity', '100').strip('"')
                opacity = float(op_str)
                
                # Parse anchor
                anchor_str = attrs.get('anchor', '0 0').strip('"')
                anchor_parts = anchor_str.split()
                anchor = [float(x) for x in anchor_parts] if anchor_parts else [0, 0]
                
                transform = {
                    'ty': 'tr',
                    'p': {'a': 0, 'k': pos, 'ix': 2},
                    'a': {'a': 0, 'k': anchor, 'ix': 1},
                    's': {'a': 0, 'k': scale, 'ix': 3},
                    'r': {'a': 0, 'k': rot, 'ix': 6},
                    'o': {'a': 0, 'k': opacity, 'ix': 7},
                    'sk': {'a': 0, 'k': 0, 'ix': 4},
                    'sa': {'a': 0, 'k': 0, 'ix': 5},
                    'nm': 'Transform'
                }
                
                # Parse skew if present
                if 'skew' in attrs:
                    skew_str = attrs.get('skew', '0').strip('"')
                    transform['sk']['k'] = float(skew_str)
                
                if 'skew_axis' in attrs:
                    sa_str = attrs.get('skew_axis', '0').strip('"')
                    transform['sa']['k'] = float(sa_str)
                
                add_to_current_container(transform)
            
            # ========== Rectangle ==========
            elif cmd == 'rect':
                rect = {
                    'ty': 'rc',
                    'nm': 'Rectangle',
                    'mn': 'ADBE Vector Shape - Rect',
                    'hd': attrs.get('hd', 'false').lower() == 'true',
                    'd': int(attrs.get('d', 1)),
                    'p': {'a': 0, 'k': [0, 0], 'ix': 3},
                    's': {'a': 0, 'k': [100, 100], 'ix': 2},
                    'r': {'a': 0, 'k': 0, 'ix': 4}
                }
                add_to_current_container(rect)
            
            elif cmd == '/rect':
                pass
            
            # ========== Ellipse ==========
            elif cmd == 'ellipse':
                ellipse = {
                    'ty': 'el',
                    'nm': 'Ellipse',
                    'mn': 'ADBE Vector Shape - Ellipse',
                    'hd': False,
                    'd': 1,
                    'p': {'a': 0, 'k': [0, 0], 'ix': 3},
                    's': {'a': 0, 'k': [100, 100], 'ix': 2}
                }
                add_to_current_container(ellipse)
            
            elif cmd == '/ellipse':
                pass
        
        return animation



    @staticmethod
    def _parse_attributes(attrs_str: str) -> Dict[str, str]:
        """Parse attribute string to dictionary - no change needed as it returns strings"""
        attrs = {}
        
        # First, handle special attributes with quotes that might contain special characters
        # Handle ch attribute specially (for char command)
        ch_match = re.search(r'ch="([^"]*)"', attrs_str)
        if ch_match:
            attrs['ch'] = ch_match.group(1)
            # Remove the ch attribute from the string to avoid re-parsing
            attrs_str = attrs_str[:ch_match.start()] + attrs_str[ch_match.end():]
        
        # Handle name attribute specially if it contains quotes
        name_match = re.search(r'name="([^"]*)"', attrs_str)
        if name_match:
            attrs['name'] = name_match.group(1)
            # Remove the name attribute from the string to avoid re-parsing
            attrs_str = attrs_str[:name_match.start()] + attrs_str[name_match.end():]
        else:
            # Try without quotes
            name_match = re.search(r'name=([^\s]+)', attrs_str)
            if name_match:
                attrs['name'] = name_match.group(1)
                attrs_str = attrs_str[:name_match.start()] + attrs_str[name_match.end():]
        
        # Parse remaining attributes
        # Pattern for key=value or key="value"
        pattern = r'([^\s=]+)=(?:"([^"]*)"|([^\s]*))'
        for match in re.finditer(pattern, attrs_str):
            key, quoted_val, unquoted_val = match.groups()
            if key not in ['name', 'ch']:  # Skip if we already handled these
                attrs[key] = quoted_val if quoted_val is not None else unquoted_val
        
        return attrs


    @staticmethod
    def _extract_array_values(array_str: str, max_values: int) -> List[int]:
        """Extract values from array string and return as int list"""
        values = [0] * max_values
        
        if array_str:
            # Handle quoted array
            if array_str.startswith('"') and array_str.endswith('"'):
                array_str = array_str[1:-1]
                
            # Handle bracketed array
            if array_str.startswith("[") and array_str.endswith("]"):
                try:
                    array_str = array_str.strip('[]')
                    parts = array_str.split(',')
                    for i, part in enumerate(parts):
                        if i >= max_values:
                            break
                        values[i] = round(float(part.strip()))
                except ValueError:
                    pass
            # Handle space-separated values
            else:
                parts = array_str.split()
                for i, part in enumerate(parts):
                    if i >= max_values:
                        break
                    try:
                        values[i] = round(float(part))
                    except ValueError:
                        pass
                        
        return values

    @staticmethod
    def _format_value(value, preserve_int=True):
        """Format value as integer with proper rounding"""
        val = float(value)
        
        # Handle special case for very small values
        if abs(val) < 1e-10:
            return 0
        
        # Always round to integer
        return val



    def to_sequence(self) -> str:
        """Convert LottieTensor to sequence string"""
        lines = []
        current_context = None
        string_params = getattr(self, 'string_params', {})
        
        for i in range(self.seq_len.item()):
            cmd_idx = int(self.commands[i].item())
            
            # Skip padding and special tokens
            if cmd_idx in [LottieTensor.CMD_PAD, LottieTensor.CMD_EOS, LottieTensor.CMD_SOS]:
                continue
                
            cmd = LottieTensor.COMMANDS[cmd_idx]
            if not cmd:  # Skip empty command entries
                continue
                
            cmd_key = f"{i}"
            
            # Handle end tags
            if cmd.startswith('/'):
                lines.append(f"({cmd})")
                # Reset context
                if cmd in ["/position", "/scale", "/opacity", "/rotation", "/keyframe", "/anchor", "/path", "/width_animated", 
                           "/range_start", "/range_end", "/range_offset", "/scale_animators", "/rotation_animators", 
                        "/position_x", "/position_y", "/position_z", "/tm", "/start", "/end", "/offset", "/color_animated", "/size", "/rounded"]:
                    current_context = None
                continue
            
            # Update context
            if cmd in ["position", "scale", "opacity", "rotation", "anchor"]:
                current_context = cmd
            elif cmd == "size":
                # Check if size is animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    current_context = "size"
            elif cmd in ["ellipse_size", "rect_size"]:
                # Check if size is animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    current_context = "size"
                    
            elif cmd in ["position_x", "position_y", "position_z"]:
                # Check if animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    current_context = cmd
            elif cmd == "path":
                # Check if path is animated (would be stored in string_params)
                if f"{cmd_key}_animated" in string_params:
                    current_context = "path"
            elif cmd == "width_keyframe":
                current_context = "width"
            elif cmd == "start":
                # Check if animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    current_context = "trim_start"
            elif cmd == "end":
                # Check if animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    current_context = "trim_end"
            elif cmd == "offset":
                # Check if animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    current_context = "trim_offset"
            elif cmd == "mask_x":
                # Check if animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.MaskX.A] > 0.5:
                    current_context = "mask_x"



            elif cmd == "scale_animators":
                params = self.params[i].tolist()
                if params[LottieTensor.Index.ScaleAnimators.A] > 0.5:
                    current_context = "scale_animators"
            elif cmd == "rotation_animators":
                params = self.params[i].tolist()
                if params[LottieTensor.Index.RotationAnimators.A] > 0.5:
                    current_context = "rotation_animators"

            elif cmd == "opacity_animators":
                params = self.params[i].tolist()
                if params[LottieTensor.Index.OpacityAnimators.A] > 0.5:
                    current_context = "opacity_animators"

            elif cmd == "position_animators":
                params = self.params[i].tolist()
                if params[LottieTensor.Index.PositionAnimators.A] > 0.5:
                    current_context = "position_animators"

            elif cmd == "tracking_animators":
                params = self.params[i].tolist()
                if params[LottieTensor.Index.TrackingAnimators.A] > 0.5:
                    current_context = "tracking_animators"
        
            elif cmd == "rect_rounded":
                # Check if animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    current_context = "rect_rounded" 

            elif cmd in ["ellipse_size", "rect_size"]:
                # Check if ellipse/rect size is animated
                params = self.params[i].tolist()
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    current_context = "size" 
                    
                           
            # Extract parameters
            params = self.params[i].tolist()
            
            # Format line based on command type
            if cmd_idx == LottieTensor.CMD_ANIMATION:
                # Use stored string values if available
                #v = string_params.get(f"{cmd_key}_v", "5.12.1")
                v = "5.12.1"
                #nm = string_params.get(f"{cmd_key}_nm", "Comp 1")
                #markers = string_params.get(f"{cmd_key}_markers", "[]")
                #props = string_params.get(f"{cmd_key}_props", "{}")
                
                fr = LottieTensor._format_value(params[LottieTensor.Index.Animation.FR]) 
                ip = LottieTensor._format_value(params[LottieTensor.Index.Animation.IP]) 
                op = LottieTensor._format_value(params[LottieTensor.Index.Animation.OP]) 
                w = LottieTensor._format_value(params[LottieTensor.Index.Animation.W])
                h = LottieTensor._format_value(params[LottieTensor.Index.Animation.H])
                ddd = int(params[LottieTensor.Index.Animation.DDD]) 
                lines.append(f'({cmd} v="{v}" fr={fr} ip={ip} op={op} w={w} h={h} ddd={ddd})')
                
            elif cmd_idx in [LottieTensor.CMD_FONTS, LottieTensor.CMD_FONTS_END, LottieTensor.CMD_CHARS, 
                            LottieTensor.CMD_CHARS_END, LottieTensor.CMD_CHAR_SHAPES,
                            LottieTensor.CMD_CHAR_SHAPES_END, LottieTensor.CMD_TEXT_KEYFRAMES, 
                            LottieTensor.CMD_TEXT_KEYFRAMES_END, LottieTensor.CMD_TEXT_DATA, 
                            LottieTensor.CMD_TEXT_DATA_END, LottieTensor.CMD_OPACITY_ANIMATED_END,
                            LottieTensor.CMD_END_END, LottieTensor.CMD_START_END, 
                            LottieTensor.CMD_OFFSET_END, LottieTensor.CMD_OPACITY_ANIMATORS_END]:
                lines.append(f"({cmd})")
                continue
            
            elif cmd_idx in [LottieTensor.CMD_POSITION_X, LottieTensor.CMD_POSITION_Y, LottieTensor.CMD_POSITION_Z]:
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    lines.append(f"({cmd} animated=true)")
                    current_context = cmd  # Set context
                else:
                    val = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                    lines.append(f"({cmd} {val})")
            #  line based on command type
            # Keep all existing formatting logic but update text_keyframe
            elif cmd_idx == LottieTensor.CMD_TEXT_KEYFRAME:
                # Initialize tokenizer if not already done
                if LottieTensor.tokenizer is None:
                    LottieTensor.init_tokenizer()
                t = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.T])
                
                # Retrieve all stored attributes
                # Retrieve numeric values
                font_size = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.FONT_SIZE])
                ca = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.CA])
                justify = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.JUSTIFY])
                tracking = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.TRACKING])
                line_height = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.LINE_HEIGHT])
                letter_spacing = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.LETTER_SPACING])
                
                # Retrieve fill_color from numeric params
                fill_r = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.FILL_COLOR_R]/255)
                fill_g = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.FILL_COLOR_G]/255)
                fill_b = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.FILL_COLOR_B]/255)
                fill_color = f"[{fill_r},{fill_g},{fill_b}]"
                
                # Retrieve string values
                #font_family = string_params.get(f"{cmd_key}_font_family", "")
                #text = string_params.get(f"{cmd_key}_text", "")
                # Decode font_family from tokens
                font_family = ""
                font_family_count = int(params[LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKEN_COUNT]) if params[LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKEN_COUNT] > -2000 else 0
                if font_family_count > 0:
                    font_family_tokens = []
                    for i in range(min(font_family_count, 10)):
                        token_val = params[LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKENS_START + i]
                        if token_val > -2000:
                            font_family_tokens.append(int(token_val))
                    if font_family_tokens:
                        try:
                            font_family = LottieTensor.tokenizer.decode(font_family_tokens)
                        except:
                            font_family = ""
                
                # Decode text from tokens
                text = ""
                text_count = int(params[LottieTensor.Index.TextKeyframe.TEXT_TOKEN_COUNT]) if params[LottieTensor.Index.TextKeyframe.TEXT_TOKEN_COUNT] > -2000 else 0
                if text_count > 0:
                    text_tokens = []
                    for i in range(min(text_count, 15)):
                        token_val = params[LottieTensor.Index.TextKeyframe.TEXT_TOKENS_START + i]
                        if token_val > -2000:
                            text_tokens.append(int(token_val))
                    if text_tokens:
                        try:
                            text = LottieTensor.tokenizer.decode(text_tokens)
                        except:
                            text = ""
                # Build the output line
                line = f'({cmd} t={t} font_size={font_size} font_family="{font_family}" text="{text}" ca={ca} justify={justify} tracking={tracking} line_height={line_height} letter_spacing={letter_spacing} fill_color={fill_color}'
                
                # Add stroke_color if present
                if params[LottieTensor.Index.TextKeyframe.HAS_STROKE_COLOR] > 0.5:
                    stroke_r = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.STROKE_COLOR_R]/255)
                    stroke_g = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.STROKE_COLOR_G]/255)
                    stroke_b = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.STROKE_COLOR_B]/255)
                    stroke_color = f"[{stroke_r},{stroke_g},{stroke_b}]"
                    line += f' stroke_color={stroke_color}'
                
                # Add stroke_width if present and not zero
                stroke_width = params[LottieTensor.Index.TextKeyframe.STROKE_WIDTH] if params[LottieTensor.Index.TextKeyframe.STROKE_WIDTH] > -2000 else 0
                if abs(stroke_width) > 1e-6:
                    line += f' stroke_width={LottieTensor._format_value(stroke_width)}'
                
                # Add offset if true
                if params[LottieTensor.Index.TextKeyframe.OFFSET] > 0.5:
                    line += ' offset=true'
                
                # Add wrap_position if present (新增)
                wrap_pos_x = params[LottieTensor.Index.TextKeyframe.WRAP_POSITION_X]
                wrap_pos_y = params[LottieTensor.Index.TextKeyframe.WRAP_POSITION_Y]
                if wrap_pos_x > -2000 and wrap_pos_y > -2000:
                    line += f' wrap_position=[{LottieTensor._format_value(wrap_pos_x)},{LottieTensor._format_value(wrap_pos_y)}]'
                
                # Add wrap_size if present (新增)
                wrap_size_x = params[LottieTensor.Index.TextKeyframe.WRAP_SIZE_X]
                wrap_size_y = params[LottieTensor.Index.TextKeyframe.WRAP_SIZE_Y]
                if wrap_size_x > -2000 and wrap_size_y > -2000:
                    line += f' wrap_size=[{LottieTensor._format_value(wrap_size_x)},{LottieTensor._format_value(wrap_size_y)}]'
                
                line += ')'
                lines.append(line)


            elif cmd_idx == LottieTensor.CMD_STAR:
                #name = string_params.get(f"{cmd_key}_name", "None")
                d = int(params[LottieTensor.Index.Star.D]) if params[LottieTensor.Index.Star.D] > -2000 else 1
                sy = int(params[LottieTensor.Index.Star.SY]) if params[LottieTensor.Index.Star.SY] > -2000 else 1
                
                lines.append(f'({cmd}  d={d} sy={sy})')

            elif cmd_idx == LottieTensor.CMD_INNER_RADIUS:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_OUTER_RADIUS:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_INNER_ROUNDNESS:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_OUTER_ROUNDNESS:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_POINTS_STAR:  # 这会输出 points_star
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'(points_star {val})')  # 强制输出为 points_star

            elif cmd_idx == LottieTensor.CMD_STAR_ROTATION:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')



            elif cmd_idx == LottieTensor.CMD_MORE_OPTIONS:
                # Reconstruct more_options line
                g = int(params[LottieTensor.Index.MoreOptions.G]) if params[LottieTensor.Index.MoreOptions.G] > -2000 else 1
                alignment_a = int(params[LottieTensor.Index.MoreOptions.ALIGNMENT_A]) if params[LottieTensor.Index.MoreOptions.ALIGNMENT_A] > -2000 else 0
                alignment_k1 = int(params[LottieTensor.Index.MoreOptions.ALIGNMENT_K1]) if params[LottieTensor.Index.MoreOptions.ALIGNMENT_K1] > -2000 else 0
                alignment_k2 = int(params[LottieTensor.Index.MoreOptions.ALIGNMENT_K2]) if params[LottieTensor.Index.MoreOptions.ALIGNMENT_K2] > -2000 else 0
                alignment_ix = int(params[LottieTensor.Index.MoreOptions.ALIGNMENT_IX]) if params[LottieTensor.Index.MoreOptions.ALIGNMENT_IX] > -2000 else 2
                
                lines.append(f'({cmd} g {g} alignment a={alignment_a} alignment_k {alignment_k1} {alignment_k2} alignment_ix {alignment_ix})')
                
            
            elif cmd_idx == LottieTensor.CMD_LAYER:
                # Use stored layer name if available
                #name = string_params.get(f"{cmd_key}_name", "Layer")
                
                index = LottieTensor._format_value(params[LottieTensor.Index.Layer.INDEX])
                in_point = LottieTensor._format_value(params[LottieTensor.Index.Layer.IN_POINT])
                out_point = LottieTensor._format_value(params[LottieTensor.Index.Layer.OUT_POINT])
                start_time = LottieTensor._format_value(params[LottieTensor.Index.Layer.START_TIME])
                
                # 开始构建输出行
                line = f'({cmd} index={index} in_point={in_point} out_point={out_point} start_time={start_time}'
                
                # 只输出非默认/非填充值的可选参数
                if params[LottieTensor.Index.Layer.DDD] > -2000:
                    ddd = int(params[LottieTensor.Index.Layer.DDD])
                    line += f' ddd={ddd}'
                
                #if params[LottieTensor.Index.Layer.HD] > -2000:
                #    hd = "true" if params[LottieTensor.Index.Layer.HD] > 0.5 else "false"
                #    line += f' hd={hd}'
                if params[LottieTensor.Index.Layer.HD] > -2000 and params[LottieTensor.Index.Layer.HD] > 0.5:
                    line += f' hd=true'
                
                if params[LottieTensor.Index.Layer.CP] > -2000:
                    cp = "true" if params[LottieTensor.Index.Layer.CP] > 0.5 else "false"
                    line += f' cp={cp}'
                    
                if params[LottieTensor.Index.Layer.CT] > -2000:
                    ct = int(params[LottieTensor.Index.Layer.CT])
                    line += f' ct={ct}'
                
                if params[LottieTensor.Index.Layer.HAS_MASK] > -2000:
                    hasMask = "true" if params[LottieTensor.Index.Layer.HAS_MASK] > 0.5 else "false"
                    line += f' hasMask={hasMask}'
                
                # masksProperties 总是作为字符串存储
                masksProperties = string_params.get(f"{cmd_key}_masksProperties", "")
                if masksProperties:
                    line += f' masksProperties={masksProperties}'
                
                if params[LottieTensor.Index.Layer.AO] > -2000:
                    ao = int(params[LottieTensor.Index.Layer.AO])
                    line += f' ao={ao}'
                
                if params[LottieTensor.Index.Layer.TT] > -2000:
                    tt = int(params[LottieTensor.Index.Layer.TT])
                    line += f' tt={tt}'
                
                if params[LottieTensor.Index.Layer.TP] > -2000:
                    tp = int(params[LottieTensor.Index.Layer.TP])
                    line += f' tp={tp}'
                
                if params[LottieTensor.Index.Layer.TD] > -2000:
                    td = int(params[LottieTensor.Index.Layer.TD])
                    line += f' td={td}'
                
                line += ')'
                lines.append(line)



            elif cmd_idx == LottieTensor.CMD_NULL_LAYER:
                # Use stored layer name if available
                #name = string_params.get(f"{cmd_key}_name", "null_layer")
                
                index = LottieTensor._format_value(params[LottieTensor.Index.NullLayer.INDEX])
                in_point = LottieTensor._format_value(params[LottieTensor.Index.NullLayer.IN_POINT])
                out_point = LottieTensor._format_value(params[LottieTensor.Index.NullLayer.OUT_POINT])
                start_time = LottieTensor._format_value(params[LottieTensor.Index.NullLayer.START_TIME])
                
                line = f'({cmd} index={index}  in_point={in_point} out_point={out_point} start_time={start_time}'
                #lines.append(f'({cmd} index={index} name="{name}" in_point={in_point} out_point={out_point} start_time={start_time} ct={ct})')
                                
                if params[LottieTensor.Index.PrecompLayer.HD] > -2000 and params[LottieTensor.Index.PrecompLayer.HD] > 0.5:
                    line += f' hd=true'
                    
                if params[LottieTensor.Index.PrecompLayer.CP] > -2000:
                    cp = "true" if params[LottieTensor.Index.PrecompLayer.CP] > 0.5 else "false"
                    line += f' cp={cp}'
                    

                if params[LottieTensor.Index.PrecompLayer.HAS_MASK] > -2000:
                    hasMask = "true" if params[LottieTensor.Index.PrecompLayer.HAS_MASK] > 0.5 else "false"
                    line += f' hasMask={hasMask}'
                

                if params[LottieTensor.Index.PrecompLayer.AO] > -2000:
                    ao = int(params[LottieTensor.Index.PrecompLayer.AO])
                    line += f' ao={ao}'
                
                if params[LottieTensor.Index.PrecompLayer.TT] > -2000:
                    tt = int(params[LottieTensor.Index.PrecompLayer.TT])
                    line += f' tt={tt}'
                
                if params[LottieTensor.Index.PrecompLayer.TP] > -2000:
                    tp = int(params[LottieTensor.Index.PrecompLayer.TP])
                    line += f' tp={tp}'
                
                if params[LottieTensor.Index.PrecompLayer.TD] > -2000:
                    td = int(params[LottieTensor.Index.PrecompLayer.TD])
                    line += f' td={td}'

                
                line += ')'
                lines.append(line)

            elif cmd_idx == LottieTensor.CMD_PRECOMP_LAYER:
                # Use stored layer name if available
                #name = string_params.get(f"{cmd_key}_name", "precomp_layer")
                
                index = LottieTensor._format_value(params[LottieTensor.Index.PrecompLayer.INDEX])
                in_point = LottieTensor._format_value(params[LottieTensor.Index.PrecompLayer.IN_POINT])
                out_point = LottieTensor._format_value(params[LottieTensor.Index.PrecompLayer.OUT_POINT])
                start_time = LottieTensor._format_value(params[LottieTensor.Index.PrecompLayer.START_TIME])
                
                # Output w and h with full precision
                #w = params[LottieTensor.Index.PrecompLayer.W]
                #h = params[LottieTensor.Index.PrecompLayer.H]
                
                # Format w and h preserving their full precision
                # Check if the value is very close to an integer
                #if abs(w - round(w)) < 1e-10:
                #    w_str = str(int(round(w)))
                #else:
                    # Keep full precision for non-integer values
                #    w_str = str(w)
                
                #if abs(h - round(h)) < 1e-10:
                #    h_str = str(int(round(h)))
                #else:
                    # Keep full precision for non-integer values
                #    h_str = str(h)
                
                
                line = f'({cmd} index={index} in_point={in_point} out_point={out_point} start_time={start_time}'



                if params[LottieTensor.Index.PrecompLayer.H] > -2000:
                    h = int(params[LottieTensor.Index.PrecompLayer.H])
                    line += f' h={h}'

                if params[LottieTensor.Index.PrecompLayer.W] > -2000:
                    w = int(params[LottieTensor.Index.PrecompLayer.W])
                    line += f' w={w}'

                if params[LottieTensor.Index.PrecompLayer.DDD] > -2000:
                    ddd = int(params[LottieTensor.Index.PrecompLayer.DDD])
                    line += f' ddd={ddd}'
                
                if params[LottieTensor.Index.PrecompLayer.HD] > -2000 and params[LottieTensor.Index.PrecompLayer.HD] > 0.5:
                    line += f' hd=true'
                    
                if params[LottieTensor.Index.PrecompLayer.CP] > -2000:
                    cp = "true" if params[LottieTensor.Index.PrecompLayer.CP] > 0.5 else "false"
                    line += f' cp={cp}'
                    
                if params[LottieTensor.Index.PrecompLayer.CT] > -2000:
                    ct = int(params[LottieTensor.Index.PrecompLayer.CT])
                    line += f' ct={ct}'
                
                if params[LottieTensor.Index.PrecompLayer.HAS_MASK] > -2000:
                    hasMask = "true" if params[LottieTensor.Index.PrecompLayer.HAS_MASK] > 0.5 else "false"
                    line += f' hasMask={hasMask}'
                
                # masksProperties 总是作为字符串存储
                masksProperties = string_params.get(f"{cmd_key}_masksProperties", "")
                if masksProperties:
                    line += f' masksProperties={masksProperties}'
                
                if params[LottieTensor.Index.PrecompLayer.AO] > -2000:
                    ao = int(params[LottieTensor.Index.PrecompLayer.AO])
                    line += f' ao={ao}'
                
                if params[LottieTensor.Index.PrecompLayer.TT] > -2000:
                    tt = int(params[LottieTensor.Index.PrecompLayer.TT])
                    line += f' tt={tt}'
                
                if params[LottieTensor.Index.PrecompLayer.TP] > -2000:
                    tp = int(params[LottieTensor.Index.PrecompLayer.TP])
                    line += f' tp={tp}'
                
                if params[LottieTensor.Index.PrecompLayer.TD] > -2000:
                    td = int(params[LottieTensor.Index.PrecompLayer.TD])
                    line += f' td={td}'

                
                line += ')'
                lines.append(line)


            elif cmd_idx == LottieTensor.CMD_REFERENCE_ID:
                # Get tokenizer
                tokenizer = LottieTensor.get_tokenizer()
                
                # Decode reference_id from tokens
                id_count = int(params[LottieTensor.Index.ReferenceId.ID_TOKEN_COUNT]) if params[LottieTensor.Index.ReferenceId.ID_TOKEN_COUNT] > -2000 else 0
                id_tokens = []
                for i in range(id_count):
                    if params[LottieTensor.Index.ReferenceId.ID_TOKEN_0 + i] > -2000:
                        id_tokens.append(int(params[LottieTensor.Index.ReferenceId.ID_TOKEN_0 + i]))
                
                reference_id = tokenizer.decode(id_tokens, skip_special_tokens=True) if id_tokens else "comp_0"
                lines.append(f'({cmd} "{reference_id}")')


      
            elif cmd_idx == LottieTensor.CMD_DIMENSIONS:
                # 输出dimensions命令
                width = LottieTensor._format_value(params[LottieTensor.Index.Dimensions.WIDTH])
                height = LottieTensor._format_value(params[LottieTensor.Index.Dimensions.HEIGHT])
                lines.append(f'({cmd} width={width} height={height})')
            
                        
            elif cmd_idx == LottieTensor.CMD_STROKE:
                #name = string_params.get(f"{cmd_key}_name", "Stroke")
                color_animated = params[LottieTensor.Index.Stroke.COLOR_ANIMATED] > 0.5
                
                line = f'({cmd}'
                
                if color_animated:
                    line += ' color_animated=true'
                else:
                    # Convert RGB values from 0-255 back to 0-1 range
                    r = LottieTensor._format_value(params[LottieTensor.Index.Stroke.R] / 255)
                    g = LottieTensor._format_value(params[LottieTensor.Index.Stroke.G] / 255)
                    b = LottieTensor._format_value(params[LottieTensor.Index.Stroke.B] / 255)
                    a = LottieTensor._format_value(params[LottieTensor.Index.Stroke.A] / 255)
                    line += f' r={r} g={g} b={b} a={a}'
                
                color_dim = int(params[LottieTensor.Index.Stroke.COLOR_DIM]) if params[LottieTensor.Index.Stroke.COLOR_DIM] > -2000 else 4
                has_c_a = "True" if params[LottieTensor.Index.Stroke.HAS_C_A] > 0.5 else "False"
                has_c_ix = "True" if params[LottieTensor.Index.Stroke.HAS_C_IX] > 0.5 else "False"
                c_ix = int(params[LottieTensor.Index.Stroke.C_IX]) if params[LottieTensor.Index.Stroke.C_IX] > -2000 else 3
                bm = int(params[LottieTensor.Index.Stroke.BM]) if params[LottieTensor.Index.Stroke.BM] > -2000 else 0
                lc = int(params[LottieTensor.Index.Stroke.LC]) if params[LottieTensor.Index.Stroke.LC] > -2000 else 1
                lj = int(params[LottieTensor.Index.Stroke.LJ]) if params[LottieTensor.Index.Stroke.LJ] > -2000 else 1
                ml = int(params[LottieTensor.Index.Stroke.ML]) if params[LottieTensor.Index.Stroke.ML] > -2000 else 4
                
                line += f' color_dim={color_dim} has_c_a={has_c_a} has_c_ix={has_c_ix}'
                
                if not color_animated:
                    line += f' c_ix={c_ix}'
                
                line += f' bm={bm} lc={lc} lj={lj} ml={ml}'
                
                # Check if width is animated
                width_animated = params[LottieTensor.Index.Stroke.WIDTH_ANIMATED] > 0.5
                if width_animated:
                    line += ' width_animated=true'
                    current_context = "width"
                
                # IMPORTANT: Close the parenthesis here
                line += ')'
                
                lines.append(line)
                
                # Add the separate (width_animated true) command after the stroke
                if width_animated:
                    lines.append('(width_animated true)')
                
                if color_animated:
                    current_context = "stroke_color"
                

            # Add dashes output in to_sequence method (after line 5800):
            elif cmd_idx == LottieTensor.CMD_DASHES:
                # Check if we have the complete dashes string stored
                dashes_str = string_params.get(f"{cmd_key}_dashes", "")
                if dashes_str:
                    # The stored string already includes quotes if needed, don't add extra quotes
                    lines.append(f'({cmd} {dashes_str})')
                else:
                    lines.append(f'({cmd})')


            elif cmd_idx == LottieTensor.CMD_DASH:
                type_map = {0: "d", 1: "g", 2: "o"}
                type_val = int(params[LottieTensor.Index.Dash.TYPE]) if params[LottieTensor.Index.Dash.TYPE] > -2000 else 0
                dash_type = type_map.get(type_val, "d")
                
                # 除以100恢复原值
                length = LottieTensor._format_value(params[LottieTensor.Index.Dash.LENGTH] / 10, preserve_int=False)
                v_ix = int(params[LottieTensor.Index.Dash.V_IX]) if params[LottieTensor.Index.Dash.V_IX] > -2000 else 1
                
                lines.append(f'({cmd} type="{dash_type}" length={length} v_ix={v_ix})')


            elif cmd_idx == LottieTensor.CMD_DASH_ANIMATED:
                # Convert numeric type back to string
                type_map = {0: "d", 1: "g", 2: "o"}
                type_val = int(params[LottieTensor.Index.DashAnimated.TYPE]) if params[LottieTensor.Index.DashAnimated.TYPE] > -2000 else 2
                dash_type = type_map.get(type_val, "o")
                
                v_ix = int(params[LottieTensor.Index.DashAnimated.V_IX]) if params[LottieTensor.Index.DashAnimated.V_IX] > -2000 else 7
                
                # Get name from string_params
                name = string_params.get(f"{cmd_key}_name", "")
                
                lines.append(f'({cmd} type="{dash_type}" name="{name}" v_ix={v_ix})')
                current_context = "dash_animated"

            elif cmd_idx == LottieTensor.CMD_DASH_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.DashKeyframe.T])
                # 除以100恢复原值
                s = LottieTensor._format_value(params[LottieTensor.Index.DashKeyframe.S] / 10, preserve_int=False)
                
                i_x = params[LottieTensor.Index.DashKeyframe.I_X]/100
                i_y = params[LottieTensor.Index.DashKeyframe.I_Y]/100
                o_x = params[LottieTensor.Index.DashKeyframe.O_X]/100
                o_y = params[LottieTensor.Index.DashKeyframe.O_Y]/100
                
                has_easing = (i_x > -2000 or i_y > -2000 or o_x > -2000 or o_y > -2000)
                
                if has_easing:
                    i_x_val = LottieTensor._format_value(i_x, preserve_int=False) if i_x > -2000 else 0
                    i_y_val = LottieTensor._format_value(i_y, preserve_int=False) if i_y > -2000 else 0
                    o_x_val = LottieTensor._format_value(o_x, preserve_int=False) if o_x > -2000 else 0
                    o_y_val = LottieTensor._format_value(o_y, preserve_int=False) if o_y > -2000 else 0
                    lines.append(f'({cmd} t={t} s={s} i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val})')
                else:
                    lines.append(f'({cmd} t={t} s={s})')


            elif cmd_idx == LottieTensor.CMD_DASH_ANIMATED_END:
                lines.append(f'({cmd})')
                current_context = None

            elif cmd_idx == LottieTensor.CMD_DASH_OFFSET:
                # 除以100恢复原值
                o = LottieTensor._format_value(params[LottieTensor.Index.DashOffset.O] / 10, preserve_int=False)
                lines.append(f'({cmd} {o})')
                
                
            elif cmd_idx == LottieTensor.CMD_DASHES_END:
                lines.append(f'({cmd})')
            elif cmd_idx == LottieTensor.CMD_DASH_ANIMATED_END:
                lines.append(f'({cmd})')
            
            elif cmd_idx == LottieTensor.CMD_SIZE_END:
                lines.append(f'({cmd})')
            # 7. Add output for color_keyframe:
            elif cmd_idx == LottieTensor.CMD_COLOR_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.T])
                r = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.S1]/255)
                g = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.S2]/255)
                b = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.S3]/255)
                a = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E1]/255)
                
                i_x = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_X]/100, preserve_int=False)
                i_y = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_Y]/100, preserve_int=False)
                o_x = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_X]/100, preserve_int=False)
                o_y = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_Y]/100, preserve_int=False)
                
                lines.append(f'({cmd} t={t} r={r} g={g} b={b} a={a} i_x={i_x} i_y={i_y} o_x={o_x} o_y={o_y})')

            elif cmd_idx == LottieTensor.CMD_OPACITY_ANIMATED:
                lines.append(f'({cmd} true)')
                current_context = "opacity_animated"
                
            elif cmd_idx == LottieTensor.CMD_OPACITY_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.T])
                
                keyframe_line = f'({cmd} t={t}'
                
                # Check if s parameter is valid
                if params[LottieTensor.Index.Keyframe.S1] > -2000:
                    s = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.S1])
                    keyframe_line += f' s={s}'
                
                # Check if easing parameters exist
                i_x = params[LottieTensor.Index.Keyframe.I_X]/100
                i_y = params[LottieTensor.Index.Keyframe.I_Y]/100
                o_x = params[LottieTensor.Index.Keyframe.O_X]/100
                o_y = params[LottieTensor.Index.Keyframe.O_Y]/100
                
                if i_x > -2000 or i_y > -2000 or o_x > -2000 or o_y > -2000:
                    i_x_val = LottieTensor._format_value(i_x, preserve_int=False) if i_x > -2000 else 0
                    i_y_val = LottieTensor._format_value(i_y, preserve_int=False) if i_y > -2000 else 0
                    o_x_val = LottieTensor._format_value(o_x, preserve_int=False) if o_x > -2000 else 0
                    o_y_val = LottieTensor._format_value(o_y, preserve_int=False) if o_y > -2000 else 0
                    keyframe_line += f' i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val}'
                
                keyframe_line += ')'
                lines.append(keyframe_line)

            elif cmd_idx == LottieTensor.CMD_WIDTH_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.WidthKeyframe.T])
                
                keyframe_line = f'({cmd} t={t}'
                
                # Check if s parameter is valid - 除以100恢复原值
                if params[LottieTensor.Index.WidthKeyframe.S] > -2000:
                    s = LottieTensor._format_value(params[LottieTensor.Index.WidthKeyframe.S] / 10, preserve_int=False)
                    keyframe_line += f' s={s}'
                
                # easing参数处理（保持不变，除以100）
                i_x = params[LottieTensor.Index.WidthKeyframe.I_X]/100
                i_y = params[LottieTensor.Index.WidthKeyframe.I_Y]/100
                o_x = params[LottieTensor.Index.WidthKeyframe.O_X]/100
                o_y = params[LottieTensor.Index.WidthKeyframe.O_Y]/100
                
                has_easing = (i_x > -2000 or i_y > -2000 or o_x > -2000 or o_y > -2000)
                
                if has_easing:
                    i_x_val = LottieTensor._format_value(i_x, preserve_int=False) if i_x > -2000 else 0
                    i_y_val = LottieTensor._format_value(i_y, preserve_int=False) if i_y > -2000 else 0
                    o_x_val = LottieTensor._format_value(o_x, preserve_int=False) if o_x > -2000 else 0
                    o_y_val = LottieTensor._format_value(o_y, preserve_int=False) if o_y > -2000 else 0
                    keyframe_line += f' i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val}'
                
                keyframe_line += ")"
                lines.append(keyframe_line)

                
            elif cmd_idx == LottieTensor.CMD_TRANSFORM:
                lines.append(f"({cmd})")
                
            elif cmd_idx == LottieTensor.CMD_POSITION:
                if cmd == "position" and current_context not in ["position", "scale", "opacity", "rotation", "anchor"]:
                    # This is a position command for shapes (ellipse, rect, etc.)
                    x = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE1])
                    y = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE2])
                    lines.append(f"({cmd} {x} {y})")
                else:
                    # This is a transform position
                    if params[LottieTensor.Index.Transform.ANIMATED] == 2.0:
                        # Separated position (for 3D layers)
                        lines.append(f"({cmd} separated=true)")
                    elif params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                        lines.append(f"({cmd} animated=true)")
                    else:
                        x = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                        y = LottieTensor._format_value(params[LottieTensor.Index.Transform.Y])
                        z = LottieTensor._format_value(params[LottieTensor.Index.Transform.Z])
                        # Check if Z is meaningful
                        if params[LottieTensor.Index.Transform.Z] > -2000 and abs(params[LottieTensor.Index.Transform.Z]) > 1e-6:
                            lines.append(f"({cmd} {x} {y} {z})")
                        else:
                            lines.append(f"({cmd} {x} {y})")
                        
            
            elif cmd_idx == LottieTensor.CMD_POSITION_X:
                # Output position_x with its value
                if params[LottieTensor.Index.SingleValue.VALUE] > -2000:
                    value = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f"({cmd} {value})")
                else:
                    lines.append(f"({cmd})")
                    
            elif cmd_idx == LottieTensor.CMD_POSITION_Y:
                # Output position_y with its value
                if params[LottieTensor.Index.SingleValue.VALUE] > -2000:
                    value = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f"({cmd} {value})")
                else:
                    lines.append(f"({cmd})")
                    
            elif cmd_idx == LottieTensor.CMD_POSITION_Z:
                # Output position_z with its value
                if params[LottieTensor.Index.SingleValue.VALUE] > -2000:
                    value = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f"({cmd} {value})")
                else:
                    lines.append(f"({cmd})")
        
            
            elif cmd_idx == LottieTensor.CMD_SCALE:
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    lines.append(f"({cmd} animated=true)")
                else:
                    x = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                    y = LottieTensor._format_value(params[LottieTensor.Index.Transform.Y])
                    z = LottieTensor._format_value(params[LottieTensor.Index.Transform.Z])
                    # Check if Z is meaningful - output Z if it's not padding value
                    if params[LottieTensor.Index.Transform.Z] > -2000:
                        lines.append(f"({cmd} {x} {y} {z})")
                    else:
                        lines.append(f"({cmd} {x} {y})")
                        
            elif cmd_idx == LottieTensor.CMD_ROTATION:
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    lines.append(f"({cmd} animated=true)")
                else:
                    angle = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                    lines.append(f"({cmd} {angle})")
                    
            elif cmd_idx == LottieTensor.CMD_OPACITY:
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    lines.append(f"({cmd} animated=true)")
                else:
                    val = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                    lines.append(f"({cmd} {val})")
                    
            elif cmd_idx == LottieTensor.CMD_ANCHOR:
                if params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    lines.append(f"({cmd} animated=true)")
                else:
                    x = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                    y = LottieTensor._format_value(params[LottieTensor.Index.Transform.Y])
                    z = LottieTensor._format_value(params[LottieTensor.Index.Transform.Z])
                    # Check if Z is meaningful
                    if params[LottieTensor.Index.Transform.Z] > -2000 and abs(params[LottieTensor.Index.Transform.Z]) > 1e-6:
                        lines.append(f"({cmd} {x} {y} {z})")
                    else:
                        lines.append(f"({cmd} {x} {y})")
                                    
            elif cmd_idx == LottieTensor.CMD_TM:
                a = int(params[LottieTensor.Index.Tm.A]) if params[LottieTensor.Index.Tm.A] > -2000 else 1
                
                # Always output a parameter
                lines.append(f'({cmd} a={a})')
                
                # Set context based on a value
                if a > 0.5:
                    current_context = "tm"  # Set context for keyframes
                else:
                    current_context = "tm_static"  # Reset context for static value
                    
            # Add value command output
            elif cmd_idx == LottieTensor.CMD_VALUE:
                val = LottieTensor._format_value(params[LottieTensor.Index.Value.VALUE])
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.T])
                
                keyframe_line = f'({cmd} t={t}'
                
                # Check if this is a hold keyframe (using H_FLAG slot)
                is_hold = params[LottieTensor.Index.Keyframe.H_FLAG] > 0.5
                
                # Check if s parameter is valid (not padding)
                has_s = params[LottieTensor.Index.Keyframe.S1] > -2000
                
                # Only add s parameter if valid and not in path context
                if has_s and current_context != "path":
                    # Format s parameter based on context
                    if current_context in ["opacity", "rotation", "position_x", "position_y", "position_z", "tm", "width",
                                           "trim_start", "trim_end", "trim_offset", "mask_x", "rotation_animators", "opacity_animators", "tracking_animators"]:
                        # For single-value properties
                        s = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.S1], preserve_int=False)
                        s_str = f'"{s}"'
                    else:
                        # For position, scale, anchor - output only non-padding values
                        s1 = params[LottieTensor.Index.Keyframe.S1]
                        s2 = params[LottieTensor.Index.Keyframe.S2]
                        s3 = params[LottieTensor.Index.Keyframe.S3]
                        
                        s_parts = []
                        s_parts.append(str(LottieTensor._format_value(s1, preserve_int=False)))
                        s_parts.append(str(LottieTensor._format_value(s2, preserve_int=False)))
                        
                        # Only add s3 if it's not padding value and not zero (for 2D animations)
                        if s3 > -2000 and abs(s3) > 1e-6:
                            s_parts.append(str(LottieTensor._format_value(s3, preserve_int=False)))
                        
                        s_str = f'"{" ".join(s_parts)}"'
                    
                    keyframe_line += f' s={s_str}'
                

                # Check and output e parameter based on context - MODIFIED TO INCLUDE TRIM CONTEXTS
                has_e = params[LottieTensor.Index.Keyframe.E1] > -2000
                
                if has_e:  # Output e regardless of hold flag
                    if current_context in ["trim_start", "trim_end", "trim_offset"]:
                        # For trim contexts, output single e value as quoted string
                        e_val = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E1], preserve_int=False)
                        keyframe_line += f' e="{e_val}"'
                    elif current_context == "rotation":
                        # For rotation, output single e value
                        e_val = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E1], preserve_int=False)
                        keyframe_line += f' e="[{e_val}]"'
                    elif current_context == "scale":
                        # For scale, output three e values
                        e1 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E1], preserve_int=False) if params[LottieTensor.Index.Keyframe.E1] > -2000 else 0
                        e2 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E2], preserve_int=False) if params[LottieTensor.Index.Keyframe.E2] > -2000 else 0
                        e3 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E3], preserve_int=False) if params[LottieTensor.Index.Keyframe.E3] > -2000 else 0
                        keyframe_line += f' e="[{e1}, {e2}, {e3}]"'
                    # Add other contexts as needed
                
                
                # Handle hold keyframe
                if is_hold:
                    keyframe_line += ' h=1'
                
                # ALWAYS check and add easing parameters, regardless of hold flag
                # The hold flag just means the value is held, but easing can still be defined
                if current_context in ["position", "anchor", "scale_animators", "position_animators", "size"]:
                    # For multi-dimensional properties, output multi-dimensional easing
                    # Check if we have multi-dimensional easing values
                    has_multi_easing = (
                        params[LottieTensor.Index.Keyframe.I_X2] > -2000 or
                        params[LottieTensor.Index.Keyframe.I_Y2] > -2000 or
                        params[LottieTensor.Index.Keyframe.O_X2] > -2000 or
                        params[LottieTensor.Index.Keyframe.O_Y2] > -2000
                    )
                    
                    if has_multi_easing:
                        # Format multi-dimensional easing - DIVIDE BY 100
                        i_x_vals = []
                        i_y_vals = []
                        o_x_vals = []
                        o_y_vals = []
                        
                        # Always include first two dimensions - DIVIDE BY 100
                        i_x1 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_X] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.I_X] > -2000 else 0
                        i_x2 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_X2] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.I_X2] > -2000 else i_x1
                        i_x_vals = [i_x1, i_x2]
                        
                        i_y1 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_Y] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.I_Y] > -2000 else 0
                        i_y2 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_Y2] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.I_Y2] > -2000 else i_y1
                        i_y_vals = [i_y1, i_y2]
                        
                        o_x1 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_X] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.O_X] > -2000 else 0
                        o_x2 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_X2] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.O_X2] > -2000 else o_x1
                        o_x_vals = [o_x1, o_x2]
                        
                        o_y1 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_Y] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.O_Y] > -2000 else 0
                        o_y2 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_Y2] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.O_Y2] > -2000 else o_y1
                        o_y_vals = [o_y1, o_y2]
                        
                        # Only add third dimension if it exists and is non-zero - DIVIDE BY 100
                        i_x3 = params[LottieTensor.Index.Keyframe.I_X3]
                        i_y3 = params[LottieTensor.Index.Keyframe.I_Y3]
                        o_x3 = params[LottieTensor.Index.Keyframe.O_X3]
                        o_y3 = params[LottieTensor.Index.Keyframe.O_Y3]
                        
                        # Check if ANY third dimension value is meaningful (not padding and not zero)
                        has_third_dim = (
                            (i_x3 > -2000 and abs(i_x3) > 1e-6) or
                            (i_y3 > -2000 and abs(i_y3) > 1e-6) or
                            (o_x3 > -2000 and abs(o_x3) > 1e-6) or
                            (o_y3 > -2000 and abs(o_y3) > 1e-6)
                        )
                        
                        if has_third_dim:
                            i_x_vals.append(LottieTensor._format_value(i_x3 / 100, preserve_int=False) if i_x3 > -2000 else i_x1)
                            i_y_vals.append(LottieTensor._format_value(i_y3 / 100, preserve_int=False) if i_y3 > -2000 else i_y1)
                            o_x_vals.append(LottieTensor._format_value(o_x3 / 100, preserve_int=False) if o_x3 > -2000 else o_x1)
                            o_y_vals.append(LottieTensor._format_value(o_y3 / 100, preserve_int=False) if o_y3 > -2000 else o_y1)
                        
                        keyframe_line += f' i_x="{" ".join(str(v) for v in i_x_vals)}" i_y="{" ".join(str(v) for v in i_y_vals)}" o_x="{" ".join(str(v) for v in o_x_vals)}" o_y="{" ".join(str(v) for v in o_y_vals)}"'
                    
                    elif params[LottieTensor.Index.Keyframe.I_X] > -2000 or params[LottieTensor.Index.Keyframe.I_Y] > -2000 or params[LottieTensor.Index.Keyframe.O_X] > -2000 or params[LottieTensor.Index.Keyframe.O_Y] > -2000:
                        # Fallback to single values if no multi-dimensional values found - DIVIDE BY 100
                        i_x_val = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_X] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.I_X] > -2000 else 0
                        i_y_val = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.I_Y] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.I_Y] > -2000 else 0
                        o_x_val = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_X] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.O_X] > -2000 else 0
                        o_y_val = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.O_Y] / 100, preserve_int=False) if params[LottieTensor.Index.Keyframe.O_Y] > -2000 else 0
                        keyframe_line += f' i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val}'
                else:
                    # For single-dimensional properties, parse single easing values - DIVIDE BY 100
                    i_x = params[LottieTensor.Index.Keyframe.I_X]
                    i_y = params[LottieTensor.Index.Keyframe.I_Y]
                    o_x = params[LottieTensor.Index.Keyframe.O_X]
                    o_y = params[LottieTensor.Index.Keyframe.O_Y]
                    
                    if i_x > -2000 or i_y > -2000 or o_x > -2000 or o_y > -2000:
                        i_x_val = LottieTensor._format_value(i_x / 100, preserve_int=False) if i_x > -2000 else 0
                        i_y_val = LottieTensor._format_value(i_y / 100, preserve_int=False) if i_y > -2000 else 0
                        o_x_val = LottieTensor._format_value(o_x / 100, preserve_int=False) if o_x > -2000 else 0
                        o_y_val = LottieTensor._format_value(o_y / 100, preserve_int=False) if o_y > -2000 else 0
                        keyframe_line += f' i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val}'
                
                # Add to/ti parameters (they are separate from hold flag)
                has_to = any(params[LottieTensor.Index.Keyframe.TO1 + j] > -2000 for j in range(3))
                has_ti = any(params[LottieTensor.Index.Keyframe.TI1 + j] > -2000 for j in range(3))
                
                if has_to:
                    to_values = []
                    for i in range(3):
                        val = params[LottieTensor.Index.Keyframe.TO1 + i]
                        if val > -2000:
                            to_values.append(LottieTensor._format_value(val, preserve_int=False))
                        else:
                            break  # Stop at first padding value
                    
                    # Only output non-zero values, but always include at least 2 dimensions if any exist
                    while len(to_values) > 2 and abs(to_values[-1]) < 1e-10:
                        to_values.pop()  # Remove trailing zeros
                    
                    # Ensure we have at least 2 values if we have any
                    while len(to_values) < 2:
                        to_values.append(0)
                    
                    keyframe_line += f' to="[{", ".join(str(v) for v in to_values)}]"'

                if has_ti:
                    ti_values = []
                    for i in range(3):
                        val = params[LottieTensor.Index.Keyframe.TI1 + i]
                        if val > -2000:
                            ti_values.append(LottieTensor._format_value(val, preserve_int=False))
                        else:
                            break  # Stop at first padding value
                    
                    # Only output non-zero values, but always include at least 2 dimensions if any exist
                    while len(ti_values) > 2 and abs(ti_values[-1]) < 1e-10:
                        ti_values.pop()  # Remove trailing zeros
                    
                    # Ensure we have at least 2 values if we have any
                    while len(ti_values) < 2:
                        ti_values.append(0)
                    
                    keyframe_line += f' ti="[{", ".join(str(v) for v in ti_values)}]"'
                                
                # Check and output e parameter based on context
                has_e = params[LottieTensor.Index.Keyframe.E1] > -2000
                
                if has_e:  # Output e regardless of hold flag
                    if current_context == "rotation":
                        # For rotation, output single e value
                        e_val = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E1], preserve_int=False)
                        keyframe_line += f' e="[{e_val}]"'
                    elif current_context == "scale":
                        # For scale, output three e values
                        e1 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E1], preserve_int=False) if params[LottieTensor.Index.Keyframe.E1] > -2000 else 0
                        e2 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E2], preserve_int=False) if params[LottieTensor.Index.Keyframe.E2] > -2000 else 0
                        e3 = LottieTensor._format_value(params[LottieTensor.Index.Keyframe.E3], preserve_int=False) if params[LottieTensor.Index.Keyframe.E3] > -2000 else 0
                        keyframe_line += f' e="[{e1}, {e2}, {e3}]"'
                    # Add other contexts as needed
                
                keyframe_line += ")"
                lines.append(keyframe_line)



            elif cmd_idx == LottieTensor.CMD_GROUP:
                #name = string_params.get(f"{cmd_key}_name", "Group")
                #mn = string_params.get(f"{cmd_key}_mn", "ADBE Vector Group")
                
                ix = int(params[LottieTensor.Index.Group.IX]) if params[LottieTensor.Index.Group.IX] > -2000 else 1
                cix = int(params[LottieTensor.Index.Group.CIX]) if params[LottieTensor.Index.Group.CIX] > -2000 else 2
                bm = int(params[LottieTensor.Index.Group.BM]) if params[LottieTensor.Index.Group.BM] > -2000 else 0
                hd = "true" if params[LottieTensor.Index.Group.HD] > 0.5 else "false"
                np = int(params[LottieTensor.Index.Group.NP]) if params[LottieTensor.Index.Group.NP] > -2000 else 0
                
                lines.append(f'({cmd} ix={ix} cix={cix} bm={bm} hd={hd} np={np})')
                

            elif cmd_idx == LottieTensor.CMD_PATH:
                #name = string_params.get(f"{cmd_key}_name", "Path")
                #mn = string_params.get(f"{cmd_key}_mn", "ADBE Vector Path")  # Add mn
                
                ix = int(params[LottieTensor.Index.Path.IX]) if params[LottieTensor.Index.Path.IX] > -2000 else 1
                ind = int(params[LottieTensor.Index.Path.IND]) if params[LottieTensor.Index.Path.IND] > -2000 else 0
                ks_ix = int(params[LottieTensor.Index.Path.KS_IX]) if params[LottieTensor.Index.Path.KS_IX] > -2000 else 2
                closed = "true" if params[LottieTensor.Index.Path.CLOSED] > 0.5 else "false"
                hd = "true" if params[LottieTensor.Index.Path.HD] > 0.5 else "false"  # Add HD
                
                # Check if path is animated
                if params[LottieTensor.Index.Path.ANIMATED] > 0.5:
                    lines.append(f'({cmd} ix={ix} ind={ind} ks_ix={ks_ix} animated="true" hd={hd})')
                    current_context = "path"
                else:
                    lines.append(f'({cmd} ix={ix} ind={ind} ks_ix={ks_ix} closed={closed} hd={hd})')

      
            elif cmd_idx == LottieTensor.CMD_POINT:
                # Check if this is a valid point (not padding)
                if params[LottieTensor.Index.Point.X] > -2000 and params[LottieTensor.Index.Point.Y] > -2000:
                    x = LottieTensor._format_value(params[LottieTensor.Index.Point.X])
                    y = LottieTensor._format_value(params[LottieTensor.Index.Point.Y])
                    in_x = LottieTensor._format_value(params[LottieTensor.Index.Point.IN_X])
                    in_y = LottieTensor._format_value(params[LottieTensor.Index.Point.IN_Y])
                    out_x = LottieTensor._format_value(params[LottieTensor.Index.Point.OUT_X])
                    out_y = LottieTensor._format_value(params[LottieTensor.Index.Point.OUT_Y])
                    lines.append(f"({cmd} x={x} y={y} in_x={in_x} in_y={in_y} out_x={out_x} out_y={out_y})")
                # else: skip padding points
                

            elif cmd_idx == LottieTensor.CMD_FILL:
                #name = string_params.get(f"{cmd_key}_name", "Fill")
                
                color_dim = int(params[LottieTensor.Index.Fill.COLOR_DIM]) if params[LottieTensor.Index.Fill.COLOR_DIM] > -2000 else 3
                has_c_a = "True" if params[LottieTensor.Index.Fill.HAS_C_A] > 0.5 else "False"
                has_c_ix = "True" if params[LottieTensor.Index.Fill.HAS_C_IX] > 0.5 else "False"
                c_ix = int(params[LottieTensor.Index.Fill.C_IX]) if params[LottieTensor.Index.Fill.C_IX] > -2000 else 4
                bm = int(params[LottieTensor.Index.Fill.BM]) if params[LottieTensor.Index.Fill.BM] > -2000 else 0
                fill_rule = int(params[LottieTensor.Index.Fill.FILL_RULE]) if params[LottieTensor.Index.Fill.FILL_RULE] > -2000 else 1
                has_o_a = "True" if params[LottieTensor.Index.Fill.HAS_O_A] > 0.5 else "False"
                has_o_ix = "True" if params[LottieTensor.Index.Fill.HAS_O_IX] > 0.5 else "False"
                o_ix = int(params[LottieTensor.Index.Fill.O_IX]) if params[LottieTensor.Index.Fill.O_IX] > -2000 else 5
                
                color_animated = params[LottieTensor.Index.Fill.COLOR_ANIMATED] > 0.5
                opacity_animated = params[LottieTensor.Index.Fill.OPACITY_ANIMATED] > 0.5
                
                line_parts = [f'({cmd}']
                
                # Handle color output
                if color_animated:
                    # Output color keyframes with easing
                    color_keyframes_json = string_params.get(f"{cmd_key}_color_keyframes", "[]")
                    color_keyframes = json.loads(color_keyframes_json)
                    for i, kf in enumerate(color_keyframes):
                        line_parts.append(f' c_kf_{i}_t={LottieTensor._format_value(kf["t"])}')
                        line_parts.append(f' c_kf_{i}_r={LottieTensor._format_value(kf["r"]/255)}')
                        line_parts.append(f' c_kf_{i}_g={LottieTensor._format_value(kf["g"]/255)}')
                        line_parts.append(f' c_kf_{i}_b={LottieTensor._format_value(kf["b"]/255)}')
                        # Add easing parameters if they exist and are non-zero (divide by 100 for float output)
                        if "i_x" in kf and (abs(kf["i_x"]) > 1e-6 or abs(kf.get("i_y", 0)) > 1e-6 or 
                                        abs(kf.get("o_x", 0)) > 1e-6 or abs(kf.get("o_y", 0)) > 1e-6):
                            line_parts.append(f' c_kf_{i}_i_x={LottieTensor._format_value(kf["i_x"] / 100, preserve_int=False)}')
                            line_parts.append(f' c_kf_{i}_i_y={LottieTensor._format_value(kf.get("i_y", 0) / 100, preserve_int=False)}')
                            line_parts.append(f' c_kf_{i}_o_x={LottieTensor._format_value(kf.get("o_x", 0) / 100, preserve_int=False)}')
                            line_parts.append(f' c_kf_{i}_o_y={LottieTensor._format_value(kf.get("o_y", 0) / 100, preserve_int=False)}')
                    line_parts.append(f' c_kf_count={len(color_keyframes)}')
                    line_parts.append(' color_animated=true')
                else:
                    # Output static color
                    r = LottieTensor._format_value(params[LottieTensor.Index.Fill.R]/255)
                    g = LottieTensor._format_value(params[LottieTensor.Index.Fill.G]/255)
                    b = LottieTensor._format_value(params[LottieTensor.Index.Fill.B]/255)
                    line_parts.append(f' r={r} g={g} b={b} color_animated=false')
                
                # Add common color parameters
                line_parts.append(f' color_dim={color_dim} has_c_a={has_c_a} has_c_ix={has_c_ix} c_ix={c_ix} bm={bm} fill_rule={fill_rule}')
                
                # Handle opacity output
                if opacity_animated:
                    # Output opacity keyframes (divide by 100 for float output)
                    opacity_keyframes_json = string_params.get(f"{cmd_key}_opacity_keyframes", "[]")
                    opacity_keyframes = json.loads(opacity_keyframes_json)
                    for i, kf in enumerate(opacity_keyframes):
                        line_parts.append(f' o_kf_{i}_t={LottieTensor._format_value(kf["t"])}')
                        line_parts.append(f' o_kf_{i}_s={LottieTensor._format_value(kf["s"])}')
                        line_parts.append(f' o_kf_{i}_i_x={LottieTensor._format_value(kf["i_x"] / 100, preserve_int=False)}')
                        line_parts.append(f' o_kf_{i}_i_y={LottieTensor._format_value(kf["i_y"] / 100, preserve_int=False)}')
                        line_parts.append(f' o_kf_{i}_o_x={LottieTensor._format_value(kf["o_x"] / 100, preserve_int=False)}')
                        line_parts.append(f' o_kf_{i}_o_y={LottieTensor._format_value(kf["o_y"] / 100, preserve_int=False)}')
                    line_parts.append(f' o_kf_count={len(opacity_keyframes)}')
                    line_parts.append(' opacity_animated=true')
                else:
                    # Output static opacity
                    opacity = LottieTensor._format_value(params[LottieTensor.Index.Fill.OPACITY])
                    line_parts.append(f' opacity={opacity} opacity_animated=false')
                
                # Add opacity-related parameters
                line_parts.append(f' has_o_a={has_o_a} has_o_ix={has_o_ix} o_ix={o_ix})')
                
                lines.append(''.join(line_parts))



            elif cmd_idx == LottieTensor.CMD_BEZIER:
                closed = "true" if params[LottieTensor.Index.Bezier.CLOSED] > 0.5 else "false"
                lines.append(f'({cmd} closed={closed})')
                
            elif cmd_idx == LottieTensor.CMD_ELLIPSE:
                #name = string_params.get(f"{cmd_key}_name", "Ellipse Path 1")
                lines.append(f'({cmd})')
                

            elif cmd_idx == LottieTensor.CMD_SIZE:
                # Check if size is animated - also check for PAD_VAL
                if params[LottieTensor.Index.Transform.ANIMATED] > -2000 and params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    lines.append(f'({cmd} animated=true)')
                    current_context = "size"
                else:
                    # 修改：使用 Transform.X 和 Transform.Y
                    x = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                    y = LottieTensor._format_value(params[LottieTensor.Index.Transform.Y])
                    lines.append(f'({cmd} {x} {y})')
                    
            
            elif cmd_idx == LottieTensor.CMD_RECT:
                #name = string_params.get(f"{cmd_key}_name", "Rectangle Path 1")
                hd = "true" if params[LottieTensor.Index.Rect.HD] > 0.5 else "false"
                d = int(params[LottieTensor.Index.Rect.D]) if params[LottieTensor.Index.Rect.D] > -2000 else 1
                lines.append(f'({cmd} hd={hd} d={d})')
                
            elif cmd_idx == LottieTensor.CMD_ROUNDED:
                rounded = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                ix = int(params[LottieTensor.Index.SingleValue.IX]) if params[LottieTensor.Index.SingleValue.IX] > -2000 else 4
                lines.append(f'({cmd} {rounded} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_TRIM:
                #name = string_params.get(f"{cmd_key}_name", "Trim Paths 1")
                ix = int(params[LottieTensor.Index.Trim.IX]) if params[LottieTensor.Index.Trim.IX] > -2000 else 1
                lines.append(f'({cmd} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_END:
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    lines.append(f'({cmd} animated=true)')
                    current_context = "trim_end"  # Set context for keyframes
                else:
                    val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_START:
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    lines.append(f'({cmd} animated=true)')
                    current_context = "trim_start"  # Set context for keyframes
                else:
                    val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_OFFSET:
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    lines.append(f'({cmd} animated=true)')
                    current_context = "trim_offset"  # Set context for keyframes
                else:
                    val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f'({cmd} {val})')



            elif cmd_idx == LottieTensor.CMD_MULTIPLE:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 1
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_REPEATER:
                #name = string_params.get(f"{cmd_key}_name", "Repeater 1")
                ix = int(params[LottieTensor.Index.Repeater.IX]) if params[LottieTensor.Index.Repeater.IX] > -2000 else 1
                lines.append(f'({cmd} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_COPIES:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                ix = int(params[LottieTensor.Index.SingleValue.IX]) if params[LottieTensor.Index.SingleValue.IX] > -2000 else 1
                lines.append(f'({cmd} {val} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_REPEATER_OFFSET:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                ix = int(params[LottieTensor.Index.SingleValue.IX]) if params[LottieTensor.Index.SingleValue.IX] > -2000 else 2
                lines.append(f'({cmd} {val} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_COMPOSITE:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 1
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_REPEATER_TRANSFORM:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_TR_P_IX:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 2
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_TR_A_IX:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 1
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_TR_SCALE:
                val1 = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE1])
                val2 = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE2])
                lines.append(f'({cmd} {val1} {val2})')
                
            elif cmd_idx == LottieTensor.CMD_TR_S_IX:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 3
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_TR_R_IX:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 4
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_TR_SO_IX:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 5
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_TR_EO_IX:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 6
                lines.append(f'({cmd} {val})')
                

            elif cmd_idx == LottieTensor.CMD_TRANSFORM_SHAPE:
                #name = string_params.get(f"{cmd_key}_name", "Transform")
                
                hd = "true" if params[LottieTensor.Index.TransformShape.HD] > 0.5 else "false"
                position_x = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.POSITION_X])
                position_y = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.POSITION_Y])
                scale_x = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.SCALE_X])
                scale_y = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.SCALE_Y])
                rotation = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.ROTATION])
                opacity = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.OPACITY])
                anchor_x = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.ANCHOR_X])
                anchor_y = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.ANCHOR_Y])
                
                # Build the output line
                line = f'({cmd} hd={hd} position="{position_x} {position_y}" scale="{scale_x} {scale_y}" rotation="{rotation}" opacity="{opacity}" anchor="{anchor_x} {anchor_y}"'
                
                # Only add skew if it's not 0 or PAD_VAL
                if params[LottieTensor.Index.TransformShape.SKEW] > -2000 and abs(params[LottieTensor.Index.TransformShape.SKEW]) > 1e-6:
                    skew = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.SKEW])
                    line += f' skew="{skew}"'
                
                # Only add skew_axis if it's not 0 or PAD_VAL
                if params[LottieTensor.Index.TransformShape.SKEW_AXIS] > -2000 and abs(params[LottieTensor.Index.TransformShape.SKEW_AXIS]) > 1e-6:
                    skew_axis = LottieTensor._format_value(params[LottieTensor.Index.TransformShape.SKEW_AXIS])
                    line += f' skew_axis="{skew_axis}"'
                
                line += ')'
                lines.append(line)

            elif cmd_idx == LottieTensor.CMD_PARENT:
                parent_index = int(params[LottieTensor.Index.Parent.PARENT_INDEX]) if params[LottieTensor.Index.Parent.PARENT_INDEX] > -2000 else 0
                lines.append(f'({cmd} {parent_index})')
            
            elif cmd_idx == LottieTensor.CMD_ASSET:
                # Get tokenizer
                tokenizer = LottieTensor.get_tokenizer()
                
                # Decode ID from tokens
                id_count = int(params[LottieTensor.Index.Asset.ID_TOKEN_COUNT]) if params[LottieTensor.Index.Asset.ID_TOKEN_COUNT] > -2000 else 0
                id_tokens = []
                for i in range(id_count):
                    if params[LottieTensor.Index.Asset.ID_TOKEN_0 + i] > -2000:
                        id_tokens.append(int(params[LottieTensor.Index.Asset.ID_TOKEN_0 + i]))
                
                asset_id = tokenizer.decode(id_tokens, skip_special_tokens=True) if id_tokens else "comp_0"
                fr = LottieTensor._format_value(params[LottieTensor.Index.Asset.FR])
                
                lines.append(f'({cmd} id="{asset_id}" fr={fr})')

            elif cmd_idx == LottieTensor.CMD_FONT:
                # Get tokenizer
                tokenizer = LottieTensor.get_tokenizer()
                
                # Decode family from tokens
                family_count = int(params[LottieTensor.Index.Font.FAMILY_TOKEN_COUNT]) if params[LottieTensor.Index.Font.FAMILY_TOKEN_COUNT] > -2000 else 0
                family_tokens = []
                for i in range(family_count):
                    if params[LottieTensor.Index.Font.FAMILY_TOKEN_0 + i] > -2000:
                        family_tokens.append(int(params[LottieTensor.Index.Font.FAMILY_TOKEN_0 + i]))
                
                # Decode style from tokens
                style_count = int(params[LottieTensor.Index.Font.STYLE_TOKEN_COUNT]) if params[LottieTensor.Index.Font.STYLE_TOKEN_COUNT] > -2000 else 0
                style_tokens = []
                for i in range(style_count):
                    if params[LottieTensor.Index.Font.STYLE_TOKEN_0 + i] > -2000:
                        style_tokens.append(int(params[LottieTensor.Index.Font.STYLE_TOKEN_0 + i]))
                
                family = tokenizer.decode(family_tokens, skip_special_tokens=True) if family_tokens else ""
                style = tokenizer.decode(style_tokens, skip_special_tokens=True) if style_tokens else ""
                ascent = LottieTensor._format_value(params[LottieTensor.Index.Font.ASCENT])
                
                lines.append(f'({cmd} family="{family}" style="{style}" ascent={ascent})')
                
            elif cmd_idx == LottieTensor.CMD_CHAR:
                # Get tokenizer
                tokenizer = LottieTensor.get_tokenizer()
                
                # Decode ch from tokens
                ch_count = int(params[LottieTensor.Index.Char.CH_TOKEN_COUNT]) if params[LottieTensor.Index.Char.CH_TOKEN_COUNT] > -2000 else 0
                ch_tokens = []
                for i in range(ch_count):
                    if params[LottieTensor.Index.Char.CH_TOKEN_0 + i] > -2000:
                        ch_tokens.append(int(params[LottieTensor.Index.Char.CH_TOKEN_0 + i]))
                
                # Decode style from tokens
                style_count = int(params[LottieTensor.Index.Char.STYLE_TOKEN_COUNT]) if params[LottieTensor.Index.Char.STYLE_TOKEN_COUNT] > -2000 else 0
                style_tokens = []
                for i in range(style_count):
                    if params[LottieTensor.Index.Char.STYLE_TOKEN_0 + i] > -2000:
                        style_tokens.append(int(params[LottieTensor.Index.Char.STYLE_TOKEN_0 + i]))
                
                # Decode family from tokens
                family_count = int(params[LottieTensor.Index.Char.FAMILY_TOKEN_COUNT]) if params[LottieTensor.Index.Char.FAMILY_TOKEN_COUNT] > -2000 else 0
                family_tokens = []
                for i in range(family_count):
                    if params[LottieTensor.Index.Char.FAMILY_TOKEN_0 + i] > -2000:
                        family_tokens.append(int(params[LottieTensor.Index.Char.FAMILY_TOKEN_0 + i]))
                
                ch = tokenizer.decode(ch_tokens, skip_special_tokens=True) if ch_tokens else ""
                style = tokenizer.decode(style_tokens, skip_special_tokens=True) if style_tokens else ""
                family = tokenizer.decode(family_tokens, skip_special_tokens=True) if family_tokens else ""
                size = LottieTensor._format_value(params[LottieTensor.Index.Char.SIZE])
                w = LottieTensor._format_value(params[LottieTensor.Index.Char.W])
                
                lines.append(f'({cmd} ch="{ch}" size={size} style="{style}" w={w} family="{family}")')
  

            elif cmd_idx == LottieTensor.CMD_TEXT_LAYER:
                #name = string_params.get(f"{cmd_key}_name", "Text Layer")
                index = LottieTensor._format_value(params[LottieTensor.Index.TextLayer.INDEX])
                in_point = LottieTensor._format_value(params[LottieTensor.Index.TextLayer.IN_POINT])
                out_point = LottieTensor._format_value(params[LottieTensor.Index.TextLayer.OUT_POINT])
                start_time = LottieTensor._format_value(params[LottieTensor.Index.TextLayer.START_TIME])
                hasMask = "True" if params[LottieTensor.Index.TextLayer.HAS_MASK] > 0.5 else "False"  # 新增
                lines.append(f'({cmd} index={index} in_point={in_point} out_point={out_point} start_time={start_time} hasMask={hasMask})')  # 修改

    
            #elif cmd_idx == LottieTensor.CMD_TEXT_KEYFRAME:
            #    t = LottieTensor._format_value(params[LottieTensor.Index.TextKeyframe.T])
            #    lines.append(f'({cmd} t={t})')
                
            elif cmd_idx == LottieTensor.CMD_FONT_SIZE:
                size = LottieTensor._format_value(params[LottieTensor.Index.FontSize.SIZE])
                lines.append(f'({cmd} {size})')
                
            elif cmd_idx == LottieTensor.CMD_FONT_FAMILY:
                family = string_params.get(f"{cmd_key}_family", "")
                lines.append(f'({cmd} "{family}")')
                
            elif cmd_idx == LottieTensor.CMD_TEXT:
                text = string_params.get(f"{cmd_key}_text", "")
                lines.append(f'({cmd} "{text}")')
                
            elif cmd_idx == LottieTensor.CMD_CA:
                value = LottieTensor._format_value(params[LottieTensor.Index.Ca.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_JUSTIFY:
                value = LottieTensor._format_value(params[LottieTensor.Index.Justify.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_TRACKING:
                value = LottieTensor._format_value(params[LottieTensor.Index.Tracking.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_LINE_HEIGHT:
                value = LottieTensor._format_value(params[LottieTensor.Index.LineHeight.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_LETTER_SPACING:
                value = LottieTensor._format_value(params[LottieTensor.Index.LetterSpacing.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_FILL_COLOR:
                r = LottieTensor._format_value(params[LottieTensor.Index.FillColor.R]/255)
                g = LottieTensor._format_value(params[LottieTensor.Index.FillColor.G]/255)
                b = LottieTensor._format_value(params[LottieTensor.Index.FillColor.B]/255)
                lines.append(f'({cmd} {r} {g} {b})')
                
            elif cmd_idx == LottieTensor.CMD_G:
                value = LottieTensor._format_value(params[LottieTensor.Index.G.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_ALIGNMENT:
                a = LottieTensor._format_value(params[LottieTensor.Index.Alignment.A])
                lines.append(f'({cmd} a={a})')
                
            elif cmd_idx == LottieTensor.CMD_ALIGNMENT_K:
                val1 = LottieTensor._format_value(params[LottieTensor.Index.AlignmentK.VALUE1])
                val2 = LottieTensor._format_value(params[LottieTensor.Index.AlignmentK.VALUE2])
                lines.append(f'({cmd} {val1} {val2})')
                
            elif cmd_idx == LottieTensor.CMD_ALIGNMENT_IX:
                value = LottieTensor._format_value(params[LottieTensor.Index.AlignmentIx.VALUE])
                lines.append(f'({cmd} {value})')
            elif cmd_idx == LottieTensor.CMD_EFFECTS:
                lines.append(f'({cmd})')
                

            elif cmd_idx == LottieTensor.CMD_EFFECT:
                #name = string_params.get(f"{cmd_key}_name", "")
                match_name = string_params.get(f"{cmd_key}_match_name", "")
                type_val = int(params[LottieTensor.Index.Effect.TYPE]) if params[LottieTensor.Index.Effect.TYPE] > -2000 else 0
                index = int(params[LottieTensor.Index.Effect.INDEX]) if params[LottieTensor.Index.Effect.INDEX] > -2000 else 1
                np = int(params[LottieTensor.Index.Effect.NP]) if params[LottieTensor.Index.Effect.NP] > -2000 else 0
                enabled = int(params[LottieTensor.Index.Effect.ENABLED]) if params[LottieTensor.Index.Effect.ENABLED] > -2000 else 1
                
                line = f'({cmd} type={type_val} index={index}'
                if np > 0:  # Only output np if it's non-zero
                    line += f' np={np}'
                line += f' match_name="{match_name}"'
                if enabled != 1:  # Only output enabled if it's not the default value
                    line += f' enabled={enabled}'
                line += ')'
                lines.append(line)

            # Add CMD_LAYER_EFFECT output:
            elif cmd_idx == LottieTensor.CMD_LAYER_EFFECT:
                #name = string_params.get(f"{cmd_key}_name", "")
                match_name = string_params.get(f"{cmd_key}_match_name", "")
                index = int(params[LottieTensor.Index.LayerEffect.INDEX]) if params[LottieTensor.Index.LayerEffect.INDEX] > -2000 else 1
                value = LottieTensor._format_value(params[LottieTensor.Index.LayerEffect.VALUE])
                lines.append(f'({cmd} index={index} value={value} match_name="{match_name}")')

    
            elif cmd_idx == LottieTensor.CMD_DROPDOWN:
                #name = string_params.get(f"{cmd_key}_name", "")
                index = int(params[LottieTensor.Index.Dropdown.INDEX]) if params[LottieTensor.Index.Dropdown.INDEX] > -2000 else 1
                value = int(params[LottieTensor.Index.Dropdown.VALUE]) if params[LottieTensor.Index.Dropdown.VALUE] > -2000 else 0
                lines.append(f'({cmd} index={index} value={value})')

            elif cmd_idx == LottieTensor.CMD_NO_VALUE:
                #@name = string_params.get(f"{cmd_key}_name", "")
                index = int(params[LottieTensor.Index.NO_VALUE.INDEX]) if params[LottieTensor.Index.NO_VALUE.INDEX] > -2000 else 1
                value = int(params[LottieTensor.Index.NO_VALUE.VALUE]) if params[LottieTensor.Index.NO_VALUE.VALUE] > -2000 else 0
                lines.append(f'({cmd} index={index} value={value})')
                

            elif cmd_idx == LottieTensor.CMD_IGNORED:
                #name = string_params.get(f"{cmd_key}_name", "")
                index = int(params[LottieTensor.Index.Ignored.INDEX]) if params[LottieTensor.Index.Ignored.INDEX] > -2000 else 1
                value = LottieTensor._format_value(params[LottieTensor.Index.Ignored.VALUE])
                lines.append(f'({cmd} index={index} value={value})')
                
            elif cmd_idx == LottieTensor.CMD_SLIDER:
                #name = string_params.get(f"{cmd_key}_name", "")
                index = int(params[LottieTensor.Index.Slider.INDEX]) if params[LottieTensor.Index.Slider.INDEX] > -2000 else 1
                value = LottieTensor._format_value(params[LottieTensor.Index.Slider.VALUE])
                lines.append(f'({cmd} index={index} value={value})')    

            elif cmd_idx == LottieTensor.CMD_GRADIENT_FILL:
                #name = string_params.get(f"{cmd_key}_name", "Gradient Fill 1")
                lines.append(f'({cmd})')
                current_context = "gradient_fill"  # Set context for subsequent commands
                
            elif cmd_idx == LottieTensor.CMD_OPACITY and current_context == "gradient_fill":
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_FILL_RULE:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 1
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_START_POINT:
                x = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE1])
                y = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE2])
                lines.append(f'({cmd} {x} {y})')
                
            elif cmd_idx == LottieTensor.CMD_END_POINT:
                x = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE1])
                y = LottieTensor._format_value(params[LottieTensor.Index.TwoValues.VALUE2])
                lines.append(f'({cmd} {x} {y})')
                
            elif cmd_idx == LottieTensor.CMD_GRADIENT_TYPE:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 1
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_HIGHLIGHT_LENGTH:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_HIGHLIGHT_ANGLE:
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_ORIGINAL_COLORS:
                count = int(params[LottieTensor.Index.OriginalColors.COUNT]) if params[LottieTensor.Index.OriginalColors.COUNT] > -2000 else 0
                
                color_values = []
                for i in range(count):
                    if params[LottieTensor.Index.OriginalColors.COLOR_0 + i] > -2000:
                        color_values.append(LottieTensor._format_value(params[LottieTensor.Index.OriginalColors.COLOR_0 + i])/255)
                
                colors_str = ", ".join(str(v) for v in color_values)
                lines.append(f'({cmd} [{colors_str}])')


            elif cmd_idx == LottieTensor.CMD_COLOR_POINTS:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 2
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_GRADIENT_FILL_END:
                lines.append(f'({cmd})')
                current_context = None  # Reset context
                
            elif cmd_idx == LottieTensor.CMD_GRADIENT_STROKE:
                #name = string_params.get(f"{cmd_key}_name", "Gradient Stroke 1")
                lines.append(f'({cmd})')
                current_context = "gradient_stroke"  # Set context for subsequent commands

            elif cmd_idx == LottieTensor.CMD_OPACITY and current_context == "gradient_stroke":
                val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                lines.append(f'({cmd} {val})')
                current_context = "gradient_stroke"  # Set context for subsequent commands


            elif cmd_idx == LottieTensor.CMD_WIDTH:
                if params[LottieTensor.Index.SingleValue.VALUE] > -2000:
                    # 除以100恢复原值
                    val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE] / 10, preserve_int=False)
                    lines.append(f'({cmd} {val})')
                    
                #if current_context == "gradient_stroke":
                    # Check if value exists (not PAD_VAL)
                #    if params[LottieTensor.Index.SingleValue.VALUE] > -2000:
                #        val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                #        lines.append(f'({cmd} {val})')
                #    else:
                        # No value, output just the command
                #        lines.append(f'({cmd})')
                #else:
                    # Handle width in other contexts if needed
                #    lines.append(f'({cmd})')
                    
            elif cmd_idx == LottieTensor.CMD_LINE_CAP:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 2
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_LINE_JOIN:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 2
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_MITER_LIMIT:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 0
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_GRADIENT_STROKE_END:
                lines.append(f'({cmd})')
                current_context = None  # Reset context
  
            elif cmd_idx == LottieTensor.CMD_COLOR:
                #name = string_params.get(f"{cmd_key}_name", "Color")
                index = int(params[LottieTensor.Index.Color.INDEX]) if params[LottieTensor.Index.Color.INDEX] > -2000 else 1
                r = LottieTensor._format_value(params[LottieTensor.Index.Color.R]/255)
                g = LottieTensor._format_value(params[LottieTensor.Index.Color.G]/255)
                b = LottieTensor._format_value(params[LottieTensor.Index.Color.B]/255)
                lines.append(f'({cmd} index={index} r={r} g={g} b={b})')
                
            
            elif cmd_idx == LottieTensor.CMD_MERGE:
                #name = string_params.get(f"{cmd_key}_name", "Merge Paths 1")
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_MERGE_MODE:
                mode = int(params[LottieTensor.Index.MergeMode.MODE]) if params[LottieTensor.Index.MergeMode.MODE] > -2000 else 1
                lines.append(f'({cmd} {mode})')
            
            
            elif cmd_idx == LottieTensor.CMD_SOLID_LAYER:
                #name = string_params.get(f"{cmd_key}_name", "Solid Layer")
                #color = string_params.get(f"{cmd_key}_color", "#000000")
                r = int(min(255, max(0, params[LottieTensor.Index.SolidLayer.COLOR_R])))
                g = int(min(255, max(0, params[LottieTensor.Index.SolidLayer.COLOR_G])))
                b = int(min(255, max(0, params[LottieTensor.Index.SolidLayer.COLOR_B])))
                a = int(min(255, max(0, params[LottieTensor.Index.SolidLayer.COLOR_A])))

                # You can use RGB values directly or convert back to hex if needed
                color_rgb = (r, g, b, a)
                # Or convert back to hex format if required: 
                color = f"#{r:02x}{g:02x}{b:02x}{a:02x}"
                
                index = LottieTensor._format_value(params[LottieTensor.Index.SolidLayer.INDEX])
                in_point = LottieTensor._format_value(params[LottieTensor.Index.SolidLayer.IN_POINT])
                out_point = LottieTensor._format_value(params[LottieTensor.Index.SolidLayer.OUT_POINT])
                start_time = LottieTensor._format_value(params[LottieTensor.Index.SolidLayer.START_TIME])
                width = LottieTensor._format_value(params[LottieTensor.Index.SolidLayer.WIDTH])
                height = LottieTensor._format_value(params[LottieTensor.Index.SolidLayer.HEIGHT])
                hasMask = "True" if params[LottieTensor.Index.SolidLayer.HAS_MASK] > 0.5 else "False"
                
                lines.append(f'({cmd} index={index} in_point={in_point} out_point={out_point} start_time={start_time} color="{color}" width={width} height={height} hasMask={hasMask})')
                
            elif cmd_idx == LottieTensor.CMD_MASKS_PROPERTIES:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_MASK:
                #nm = string_params.get(f"{cmd_key}_nm", "Mask 1")
                
                index = int(params[LottieTensor.Index.Mask.INDEX]) if params[LottieTensor.Index.Mask.INDEX] > -2000 else 0
                inv = "true" if params[LottieTensor.Index.Mask.INV] > 0.5 else "false"
                
                # Convert mode value back to string
                mode_val = int(params[LottieTensor.Index.Mask.MODE]) if params[LottieTensor.Index.Mask.MODE] > -2000 else 0
                mode_map = {0: "a", 1: "s", 2: "i", 3: "n"}
                mode = mode_map.get(mode_val, "a")
                
                lines.append(f'({cmd} index={index} inv={inv} mode={mode})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT:
                a = int(params[LottieTensor.Index.MaskPt.A]) if params[LottieTensor.Index.MaskPt.A] > -2000 else 1
                ix = int(params[LottieTensor.Index.MaskPt.IX]) if params[LottieTensor.Index.MaskPt.IX] > -2000 else 1
                lines.append(f'({cmd} a={a} ix={ix})')
                

            elif cmd_idx == LottieTensor.CMD_MASK_PT_K_C:
                c = "true" if params[LottieTensor.Index.MaskPtK.C] > 0.5 else "false"
                lines.append(f'({cmd} {c})')  # Changed from c={c} to just {c}
                


            elif cmd_idx in [LottieTensor.CMD_MASK_PT_K_I, LottieTensor.CMD_MASK_PT_K_O, LottieTensor.CMD_MASK_PT_K_V]:
                count = int(params[LottieTensor.Index.MaskPtKValues.COUNT]) if params[LottieTensor.Index.MaskPtKValues.COUNT] > -2000 else 0
                
                if count == 0:
                    # Fallback: find last non-padding value
                    for i in range(19, -1, -1):
                        val = params[LottieTensor.Index.MaskPtKValues.V1 + i]
                        if val > -2000:
                            count = i + 1
                            break
                
                values = []
                for i in range(count):
                    val = params[LottieTensor.Index.MaskPtKValues.V1 + i]
                    if val > -2000:
                        values.append(LottieTensor._format_value(val))
                    else:
                        values.append(0.0)
                
                lines.append(f'({cmd} {" ".join(str(v) for v in values)})')
      
            elif cmd_idx == LottieTensor.CMD_MASK_O:
                a = int(params[LottieTensor.Index.MaskO.A]) if params[LottieTensor.Index.MaskO.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.MaskO.K]) if params[LottieTensor.Index.MaskO.K] > -2000 else 100
                ix = int(params[LottieTensor.Index.MaskO.IX]) if params[LottieTensor.Index.MaskO.IX] > -2000 else 3
                lines.append(f'({cmd} a={a} k={k} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_X:
                a = int(params[LottieTensor.Index.MaskX.A]) if params[LottieTensor.Index.MaskX.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.MaskX.K]) if params[LottieTensor.Index.MaskX.K] > -2000 else 0
                ix = int(params[LottieTensor.Index.MaskX.IX]) if params[LottieTensor.Index.MaskX.IX] > -2000 else 4
                lines.append(f'({cmd} a={a} k={k} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_END:
                lines.append(f'({cmd})')
            
            elif cmd_idx == LottieTensor.CMD_MASK_PT_K:
                lines.append(f'({cmd})')    
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_END:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_K_END:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_MASKS_PROPERTIES_END:
                lines.append(f'({cmd})')

            
            elif cmd_idx in [LottieTensor.CMD_MASK_PT_K_ARRAY, LottieTensor.CMD_MASK_PT_K_ARRAY_END,
                            LottieTensor.CMD_MASK_PT_KF_S, LottieTensor.CMD_MASK_PT_KF_S_END,
                            LottieTensor.CMD_MASK_PT_KF_SHAPE_END, LottieTensor.CMD_MASK_PT_KEYFRAME_END]:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KEYFRAME:
                index = int(params[LottieTensor.Index.MaskPtKeyframe.INDEX]) if params[LottieTensor.Index.MaskPtKeyframe.INDEX] > -2000 else 0
                t = LottieTensor._format_value(params[LottieTensor.Index.MaskPtKeyframe.T])
                lines.append(f'({cmd} index={index} t={t})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KF_I:
                x = LottieTensor._format_value(params[LottieTensor.Index.MaskPtKfI.X])
                y = LottieTensor._format_value(params[LottieTensor.Index.MaskPtKfI.Y])
                lines.append(f'({cmd} x={x} y={y})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KF_O:
                x = LottieTensor._format_value(params[LottieTensor.Index.MaskPtKfO.X])
                y = LottieTensor._format_value(params[LottieTensor.Index.MaskPtKfO.Y])
                lines.append(f'({cmd} x={x} y={y})')
                
            elif cmd_idx == LottieTensor.CMD_MASK_PT_KF_SHAPE:
                index = int(params[LottieTensor.Index.MaskPtKfShape.INDEX]) if params[LottieTensor.Index.MaskPtKfShape.INDEX] > -2000 else 0
                c = "true" if params[LottieTensor.Index.MaskPtKfShape.C] > 0.5 else "false"
                lines.append(f'({cmd} index={index} c={c})')
                

            elif cmd_idx in [LottieTensor.CMD_MASK_PT_KF_SHAPE_I, LottieTensor.CMD_MASK_PT_KF_SHAPE_O,
                            LottieTensor.CMD_MASK_PT_KF_SHAPE_V]:
                # Get the count from params, not from string_params
                count = int(params[LottieTensor.Index.MaskPtKfShapeValues.COUNT]) if params[LottieTensor.Index.MaskPtKfShapeValues.COUNT] > -2000 else 0
                
                if count == 0:
                    # If no count stored, find the last non-padding value
                    for i in range(19, -1, -1):  # Check V1 through V20
                        if i < LottieTensor.PARAM_DIM:
                            val = params[LottieTensor.Index.MaskPtKfShapeValues.V1 + i]
                            if val > -2000:
                                count = i + 1
                                break
                    if count == 0:
                        count = 8  # Default to 8 if no valid values found
                
                # Output the exact number of values
                values = []
                for i in range(count):
                    if i < 20:
                        val = params[LottieTensor.Index.MaskPtKfShapeValues.V1 + i]
                        if val > -2000:
                            values.append(LottieTensor._format_value(val))
                        else:
                            values.append(0.0)
                    else:
                        values.append(0.0)
                
                lines.append(f'({cmd} {" ".join(str(v) for v in values)})')

            elif cmd_idx == LottieTensor.CMD_TR_POSITION:
                x = LottieTensor._format_value(params[LottieTensor.Index.TrPosition.X])
                y = LottieTensor._format_value(params[LottieTensor.Index.TrPosition.Y])
                lines.append(f'({cmd} {x} {y})')
                
            elif cmd_idx == LottieTensor.CMD_TR_ANCHOR:
                x = LottieTensor._format_value(params[LottieTensor.Index.TrAnchor.X])
                y = LottieTensor._format_value(params[LottieTensor.Index.TrAnchor.Y])
                lines.append(f'({cmd} {x} {y})')
                
            elif cmd_idx == LottieTensor.CMD_TR_ROTATION:
                val = LottieTensor._format_value(params[LottieTensor.Index.TrRotation.VALUE])
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_TR_START_OPACITY:
                val = LottieTensor._format_value(params[LottieTensor.Index.TrStartOpacity.VALUE])
                lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_TR_END_OPACITY:
                if params[LottieTensor.Index.TrEndOpacity.VALUE] > -2000:
                    val = LottieTensor._format_value(params[LottieTensor.Index.TrEndOpacity.VALUE])
                    lines.append(f'({cmd} {val})')
                else:
                    lines.append(f'({cmd})')   
            
            elif cmd_idx == LottieTensor.CMD_ZIG_ZAG:
                #name = string_params.get(f"{cmd_key}_name", "Zig Zag 1")
                ix = int(params[LottieTensor.Index.ZigZag.IX]) if params[LottieTensor.Index.ZigZag.IX] > -2000 else 2
                lines.append(f'({cmd} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_FREQUENCY:
                value = LottieTensor._format_value(params[LottieTensor.Index.Frequency.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_AMPLITUDE:
                value = LottieTensor._format_value(params[LottieTensor.Index.Amplitude.VALUE])
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_POINT_TYPE:
                value = int(params[LottieTensor.Index.PointType.VALUE]) if params[LottieTensor.Index.PointType.VALUE] > -2000 else 2
                lines.append(f'({cmd} {value})')
                
            elif cmd_idx == LottieTensor.CMD_ZIG_ZAG_END:
                lines.append(f'({cmd})')

            elif cmd_idx == LottieTensor.CMD_ANIMATORS:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_ANIMATOR:
                #nm = string_params.get(f"{cmd_key}_nm", "Animator 1")
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_RANGE_SELECTOR:
                t = int(params[LottieTensor.Index.RangeSelector.T]) if params[LottieTensor.Index.RangeSelector.T] > -2000 else 0
                r = int(params[LottieTensor.Index.RangeSelector.R]) if params[LottieTensor.Index.RangeSelector.R] > -2000 else 1
                b = int(params[LottieTensor.Index.RangeSelector.B]) if params[LottieTensor.Index.RangeSelector.B] > -2000 else 1
                sh = int(params[LottieTensor.Index.RangeSelector.SH]) if params[LottieTensor.Index.RangeSelector.SH] > -2000 else 1
                rn = int(params[LottieTensor.Index.RangeSelector.RN]) if params[LottieTensor.Index.RangeSelector.RN] > -2000 else 0
                lines.append(f'({cmd} t={t} r={r} b={b} sh={sh} rn={rn})')

            elif cmd_idx == LottieTensor.CMD_RANGE_START:
                a = int(params[LottieTensor.Index.RangeStart.A]) if params[LottieTensor.Index.RangeStart.A] > -2000 else 0
                lines.append(f'({cmd} a={a})')
                if a > 0.5:
                    current_context = "range_start"


            elif cmd_idx == LottieTensor.CMD_RANGE_START_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.RangeStartKeyframe.T])
                s = LottieTensor._format_value(params[LottieTensor.Index.RangeStartKeyframe.S])
                
                # Check if this is the last keyframe (no easing values or all zeros)
                i_x = params[LottieTensor.Index.RangeStartKeyframe.I_X]/100
                i_y = params[LottieTensor.Index.RangeStartKeyframe.I_Y]/100
                o_x = params[LottieTensor.Index.RangeStartKeyframe.O_X]/100
                o_y = params[LottieTensor.Index.RangeStartKeyframe.O_Y]/100
                
                has_meaningful_easing = (
                    (i_x > -2000 and abs(i_x) > 1e-6) or
                    (i_y > -2000 and abs(i_y) > 1e-6) or
                    (o_x > -2000 and abs(o_x) > 1e-6) or
                    (o_y > -2000 and abs(o_y) > 1e-6)
                )
                
                if has_meaningful_easing:
                    i_x_val = LottieTensor._format_value(i_x, preserve_int=False) if i_x > -2000 else 0
                    i_y_val = LottieTensor._format_value(i_y, preserve_int=False) if i_y > -2000 else 0
                    o_x_val = LottieTensor._format_value(o_x, preserve_int=False) if o_x > -2000 else 0
                    o_y_val = LottieTensor._format_value(o_y, preserve_int=False) if o_y > -2000 else 0
                    lines.append(f'({cmd} t={t} s={s} i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val})')
                else:
                    lines.append(f'({cmd} t={t} s={s})')
                    
            elif cmd_idx == LottieTensor.CMD_RANGE_START_END:
                lines.append(f'({cmd})')
                current_context = None
                
            elif cmd_idx == LottieTensor.CMD_AMOUNT:
                a = int(params[LottieTensor.Index.Amount.A]) if params[LottieTensor.Index.Amount.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.Amount.K]) if params[LottieTensor.Index.Amount.K] > -2000 else 100
                ix = int(params[LottieTensor.Index.Amount.IX]) if params[LottieTensor.Index.Amount.IX] > -2000 else 4
                lines.append(f'({cmd} a={a} k={k} ix={ix})')
                
            elif cmd_idx == LottieTensor.CMD_MAX_EASE:
                a = int(params[LottieTensor.Index.MaxEase.A]) if params[LottieTensor.Index.MaxEase.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.MaxEase.K]) if params[LottieTensor.Index.MaxEase.K] > -2000 else 0
                ix = int(params[LottieTensor.Index.MaxEase.IX]) if params[LottieTensor.Index.MaxEase.IX] > -2000 else 7
                lines.append(f'({cmd} a={a} k={k} ix={ix})')
                

            elif cmd_idx == LottieTensor.CMD_MIN_EASE:
                a = int(params[LottieTensor.Index.MinEase.A]) if params[LottieTensor.Index.MinEase.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.MinEase.K]) if params[LottieTensor.Index.MinEase.K] > -2000 else 0
                ix = int(params[LottieTensor.Index.MinEase.IX]) if params[LottieTensor.Index.MinEase.IX] > -2000 else 8
                lines.append(f'({cmd} a={a} k={k} ix={ix})')


            elif cmd_idx == LottieTensor.CMD_ANIMATOR_PROPERTIES:
                lines.append(f'({cmd})')
                current_context = "animator_properties"
                
            elif cmd_idx == LottieTensor.CMD_ANIMATOR_PROPERTIES_END:
                lines.append(f'({cmd})')
                current_context = None
                
            elif cmd_idx == LottieTensor.CMD_OPACITY and current_context == "animator_properties":
                # Special handling for opacity within animator_properties
                a = int(params[LottieTensor.Index.Amount.A]) if params[LottieTensor.Index.Amount.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.Amount.K]) if params[LottieTensor.Index.Amount.K] > -2000 else 0
                ix = int(params[LottieTensor.Index.Amount.IX]) if params[LottieTensor.Index.Amount.IX] > -2000 else 9
                lines.append(f'({cmd} a={a} k={k} ix={ix})')
            
            elif cmd_idx == LottieTensor.CMD_RANGE_SELECTOR_END:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_ANIMATOR_END:
                lines.append(f'({cmd})')
                
            elif cmd_idx == LottieTensor.CMD_ANIMATORS_END:
                lines.append(f'({cmd})')

            elif cmd_idx == LottieTensor.CMD_RADIUS:
                val = LottieTensor._format_value(params[LottieTensor.Index.Radius.VALUE])
                lines.append(f'({cmd} {val})')

            elif cmd_idx == LottieTensor.CMD_RANGE_END:
                a = int(params[LottieTensor.Index.RangeEnd.A]) if params[LottieTensor.Index.RangeEnd.A] > -2000 else 0
                lines.append(f'({cmd} a={a})')
                if a > 0.5:
                    current_context = "range_end"


            elif cmd_idx == LottieTensor.CMD_RANGE_END_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.RangeEndKeyframe.T])
                s = LottieTensor._format_value(params[LottieTensor.Index.RangeEndKeyframe.S])
                
                # Check if this is the last keyframe (no easing values or all zeros)
                i_x = params[LottieTensor.Index.RangeEndKeyframe.I_X]/100
                i_y = params[LottieTensor.Index.RangeEndKeyframe.I_Y]/100
                o_x = params[LottieTensor.Index.RangeEndKeyframe.O_X]/100
                o_y = params[LottieTensor.Index.RangeEndKeyframe.O_Y]/100
                
                has_meaningful_easing = (
                    (i_x > -2000 and abs(i_x) > 1e-6) or
                    (i_y > -2000 and abs(i_y) > 1e-6) or
                    (o_x > -2000 and abs(o_x) > 1e-6) or
                    (o_y > -2000 and abs(o_y) > 1e-6)
                )
                
                if has_meaningful_easing:
                    i_x_val = LottieTensor._format_value(i_x, preserve_int=False) if i_x > -2000 else 0
                    i_y_val = LottieTensor._format_value(i_y, preserve_int=False) if i_y > -2000 else 0
                    o_x_val = LottieTensor._format_value(o_x, preserve_int=False) if o_x > -2000 else 0
                    o_y_val = LottieTensor._format_value(o_y, preserve_int=False) if o_y > -2000 else 0
                    lines.append(f'({cmd} t={t} s={s} i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val})')
                else:
                    lines.append(f'({cmd} t={t} s={s})')
                    
            elif cmd_idx == LottieTensor.CMD_RANGE_END_END:
                lines.append(f'({cmd})')
                current_context = None

            # Fix position output in animator_properties context

            elif cmd_idx == LottieTensor.CMD_POSITION and current_context == "animator_properties":
                # Special handling for position within animator_properties
                a = int(params[LottieTensor.Index.Amount.A]) if params[LottieTensor.Index.Amount.A] > -2000 else 0
                ix = int(params[LottieTensor.Index.Amount.IX]) if params[LottieTensor.Index.Amount.IX] > -2000 else 2
                
                # Check if we have array values stored
                x = params[LottieTensor.Index.Transform.X]
                y = params[LottieTensor.Index.Transform.Y]
                z = params[LottieTensor.Index.Transform.Z]
                
                if x > -2000 or y > -2000:  # Changed condition - check x or y
                    # Format as array
                    x_val = LottieTensor._format_value(x) if x > -2000 else 0
                    y_val = LottieTensor._format_value(y) if y > -2000 else 0
                    
                    # Only include z if it's meaningful
                    if z > -2000 and abs(z) > 1e-6:
                        lines.append(f'({cmd} a={a} k=[{x_val}, {y_val}, {LottieTensor._format_value(z)}] ix={ix})')
                    else:
                        lines.append(f'({cmd} a={a} k=[{x_val}, {y_val}, 0] ix={ix})')
                else:
                    # Format as single value
                    k = LottieTensor._format_value(params[LottieTensor.Index.Amount.K]) if params[LottieTensor.Index.Amount.K] > -2000 else 0
                    lines.append(f'({cmd} a={a} k={k} ix={ix})')

            
            elif cmd_idx == LottieTensor.CMD_ML2:
                val = int(params[LottieTensor.Index.SingleValue.VALUE]) if params[LottieTensor.Index.SingleValue.VALUE] > -2000 else 4
                lines.append(f'({cmd} {val})')


            elif cmd_idx == LottieTensor.CMD_RANGE_OFFSET_KEYFRAME:
                t = LottieTensor._format_value(params[LottieTensor.Index.RangeOffsetKeyframe.T])
                s = LottieTensor._format_value(params[LottieTensor.Index.RangeOffsetKeyframe.S])
                
                # Check if this is the last keyframe (no easing values or all zeros)
                i_x = params[LottieTensor.Index.RangeOffsetKeyframe.I_X]/100
                i_y = params[LottieTensor.Index.RangeOffsetKeyframe.I_Y]/100
                o_x = params[LottieTensor.Index.RangeOffsetKeyframe.O_X]/100
                o_y = params[LottieTensor.Index.RangeOffsetKeyframe.O_Y]/100
                
                has_meaningful_easing = (
                    (i_x > -2000 and abs(i_x) > 1e-6) or
                    (i_y > -2000 and abs(i_y) > 1e-6) or
                    (o_x > -2000 and abs(o_x) > 1e-6) or
                    (o_y > -2000 and abs(o_y) > 1e-6)
                )
                
                if has_meaningful_easing:
                    i_x_val = LottieTensor._format_value(i_x, preserve_int=False) if i_x > -2000 else 0
                    i_y_val = LottieTensor._format_value(i_y, preserve_int=False) if i_y > -2000 else 0
                    o_x_val = LottieTensor._format_value(o_x, preserve_int=False) if o_x > -2000 else 0
                    o_y_val = LottieTensor._format_value(o_y, preserve_int=False) if o_y > -2000 else 0
                    lines.append(f'({cmd} t={t} s={s} i_x={i_x_val} i_y={i_y_val} o_x={o_x_val} o_y={o_y_val})')
                else:
                    lines.append(f'({cmd} t={t} s={s})')
                    
            elif cmd_idx == LottieTensor.CMD_RANGE_OFFSET_END:
                lines.append(f'({cmd})')
                current_context = None
                
            elif cmd_idx == LottieTensor.CMD_S_M:
                a = int(params[LottieTensor.Index.SM.A]) if params[LottieTensor.Index.SM.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.SM.K]) if params[LottieTensor.Index.SM.K] > -2000 else 100
                ix = int(params[LottieTensor.Index.SM.IX]) if params[LottieTensor.Index.SM.IX] > -2000 else 6
                lines.append(f'({cmd} a={a} k={k} ix={ix})')
                

            # 修改 CMD_OPACITY_ANIMATORS 的输出：
            elif cmd_idx == LottieTensor.CMD_OPACITY_ANIMATORS:
                a = int(params[LottieTensor.Index.OpacityAnimators.A]) if params[LottieTensor.Index.OpacityAnimators.A] > -2000 else 0
                
                if a > 0.5:
                    # Animated case - only output a
                    lines.append(f'({cmd} a={a})')
                    current_context = "opacity_animators"
                else:
                    # Static case with k value
                    k = LottieTensor._format_value(params[LottieTensor.Index.OpacityAnimators.K]) if params[LottieTensor.Index.OpacityAnimators.K] > -2000 else 0
                    ix = int(params[LottieTensor.Index.OpacityAnimators.IX]) if params[LottieTensor.Index.OpacityAnimators.IX] > -2000 else 9
                    lines.append(f'({cmd} a={a} k={k} ix={ix})')

            # 添加 CMD_POSITION_ANIMATORS 的输出：
            elif cmd_idx == LottieTensor.CMD_POSITION_ANIMATORS:
                a = int(params[LottieTensor.Index.PositionAnimators.A]) if params[LottieTensor.Index.PositionAnimators.A] > -2000 else 0
                ix = int(params[LottieTensor.Index.PositionAnimators.IX]) if params[LottieTensor.Index.PositionAnimators.IX] > -2000 else 2
                
                if a > 0.5:
                    # Animated case
                    lines.append(f'({cmd} a={a})')
                    current_context = "position_animators"
                else:
                    # Static case with k value
                    k_x = params[LottieTensor.Index.PositionAnimators.K_X]
                    k_y = params[LottieTensor.Index.PositionAnimators.K_Y]
                    k_z = params[LottieTensor.Index.PositionAnimators.K_Z]
                    
                    if k_x > -2000 and k_y > -2000:
                        # Format as array
                        x_val = LottieTensor._format_value(k_x) if k_x > -2000 else 0
                        y_val = LottieTensor._format_value(k_y) if k_y > -2000 else 0
                        z_val = LottieTensor._format_value(k_z) if k_z > -2000 else 0
                        lines.append(f'({cmd} a={a} k=[{x_val}, {y_val}, {z_val}] ix={ix})')
                    else:
                        lines.append(f'({cmd} a={a} k=[0.0, 0.0, 0.0] ix={ix})')

            # 添加 CMD_TRACKING_ANIMATORS 的输出：
            elif cmd_idx == LottieTensor.CMD_TRACKING_ANIMATORS:
                a = int(params[LottieTensor.Index.TrackingAnimators.A]) if params[LottieTensor.Index.TrackingAnimators.A] > -2000 else 0
                k = LottieTensor._format_value(params[LottieTensor.Index.TrackingAnimators.K]) if params[LottieTensor.Index.TrackingAnimators.K] > -2000 else 0
                ix = int(params[LottieTensor.Index.TrackingAnimators.IX]) if params[LottieTensor.Index.TrackingAnimators.IX] > -2000 else 89
                
                if a > 0.5:
                    # Animated case
                    lines.append(f'({cmd} a={a})')
                    current_context = "tracking_animators"
                else:
                    # Static case
                    lines.append(f'({cmd} a={a} k={k} ix={ix})')

            # 添加结束命令的输出：
            elif cmd_idx == LottieTensor.CMD_POSITION_ANIMATORS_END:
                lines.append(f'({cmd})')
                current_context = None


            # Add output formatting (after CMD_OPACITY_ANIMATORS, around line 5590)
            elif cmd_idx == LottieTensor.CMD_SCALE_ANIMATORS:
                a = int(params[LottieTensor.Index.ScaleAnimators.A]) if params[LottieTensor.Index.ScaleAnimators.A] > -2000 else 0
                
                if a > 0.5:
                    # Animated case
                    lines.append(f'({cmd} a={a})')
                    current_context = "scale_animators"
                else:
                    # Static case with k value
                    k_x = params[LottieTensor.Index.ScaleAnimators.K_X]
                    k_y = params[LottieTensor.Index.ScaleAnimators.K_Y]
                    k_z = params[LottieTensor.Index.ScaleAnimators.K_Z]
                    
                    if k_x > -2000 and k_y > -2000 and k_z > -2000:
                        # Check if all values are the same
                        if abs(k_x - k_y) < 1e-6 and abs(k_y - k_z) < 1e-6:
                            # Output single value
                            lines.append(f'({cmd} a={a} k={LottieTensor._format_value(k_x)})')
                        else:
                            # Output array
                            lines.append(f'({cmd} a={a} k=[{LottieTensor._format_value(k_x)}, {LottieTensor._format_value(k_y)}, {LottieTensor._format_value(k_z)}])')
                    else:
                        lines.append(f'({cmd} a={a} k=100)')

            elif cmd_idx == LottieTensor.CMD_SCALE_ANIMATORS_END:
                lines.append(f'({cmd})')
                current_context = None

            elif cmd_idx == LottieTensor.CMD_ROTATION_ANIMATORS:
                a = int(params[LottieTensor.Index.RotationAnimators.A]) if params[LottieTensor.Index.RotationAnimators.A] > -2000 else 0
                
                if a > 0.5:
                    # Animated case
                    lines.append(f'({cmd} a={a})')
                    current_context = "rotation_animators"
                else:
                    # Static case with k value
                    k = LottieTensor._format_value(params[LottieTensor.Index.RotationAnimators.K]) if params[LottieTensor.Index.RotationAnimators.K] > -2000 else 0
                    lines.append(f'({cmd} a={a} k={k})')

            elif cmd_idx == LottieTensor.CMD_WIDTH_ANIMATED:
                # This is a standalone width_animated command
                # The context should already be set from the stroke command
                # No parameters needed for this command
                pass
            
            elif cmd_idx == LottieTensor.CMD_RANGE_OFFSET:
                # Use Amount indices for range_offset
                a = int(params[LottieTensor.Index.Amount.A]) if params[LottieTensor.Index.Amount.A] > -2000 else 0
                
                if a > 0.5:  # This should be checking a, not params[LottieTensor.Index.Amount.A] again
                    # Animated case - only output a
                    lines.append(f'({cmd} a={a})')
                    current_context = "range_offset"
                else:
                    # Static case - output a, k, and ix
                    k = LottieTensor._format_value(params[LottieTensor.Index.Amount.K]) if params[LottieTensor.Index.Amount.K] > -2000 else 0
                    ix = int(params[LottieTensor.Index.Amount.IX]) if params[LottieTensor.Index.Amount.IX] > -2000 else 3
                    lines.append(f'({cmd} a={a} k={k} ix={ix})')

            

            elif cmd_idx == LottieTensor.CMD_ROTATION_ANIMATORS_END:
                lines.append(f'({cmd})')
                current_context = None
    
            elif cmd_idx == LottieTensor.CMD_RECT_SIZE:
                # Output rect_size with two values
                if params[LottieTensor.Index.Transform.ANIMATED] > -2000 and params[LottieTensor.Index.Transform.ANIMATED] > 0.5:
                    lines.append(f'({cmd} animated=true)')
                    current_context = "size"
                else:
                    # 修改：使用 Transform.X 和 Transform.Y
                    val1 = LottieTensor._format_value(params[LottieTensor.Index.Transform.X])
                    val2 = LottieTensor._format_value(params[LottieTensor.Index.Transform.Y])
                    lines.append(f'({cmd} {val1} {val2})')
                    
                    
            
            elif cmd_idx == LottieTensor.CMD_ELLIPSE_SIZE:
                # Output rect_size with two values
                # 检查是否是动画
                animated_val = params[LottieTensor.Index.Transform.ANIMATED]
                if animated_val > -2000 and animated_val > 0.5:
                    lines.append(f'({cmd} animated=true)')
                    current_context = "size"  # 确保设置上下文
                else:
                    # 静态值 - 检查 X 和 Y 是否为有效值
                    x_val = params[LottieTensor.Index.Transform.X]
                    y_val = params[LottieTensor.Index.Transform.Y]
                    # 如果 X 和 Y 都是默认值 0 且 ANIMATED 未设置，可能是数据丢失
                    val1 = LottieTensor._format_value(x_val if x_val > -2000 else 0)
                    val2 = LottieTensor._format_value(y_val if y_val > -2000 else 0)
                    lines.append(f'({cmd} {val1} {val2})')

            
            elif cmd_idx == LottieTensor.CMD_RECT_ROUNDED:
                if params[LottieTensor.Index.SingleValue.ANIMATED] > 0.5:
                    lines.append(f'({cmd} animated=true)')
                    current_context = "rect_rounded"  # Set context for keyframes
                else:
                    val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f'({cmd} {val})')
        
            elif cmd_idx == LottieTensor.CMD_RECT_ROUNDED_END:
                lines.append(f'({cmd})')
                current_context = None    
            
            elif cmd_idx == LottieTensor.CMD_SKEW:
                if params[LottieTensor.Index.SingleValue.VALUE] > -2000:
                    val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f'({cmd} {val})')
                
            elif cmd_idx == LottieTensor.CMD_SKEW_AXIS:
                if params[LottieTensor.Index.SingleValue.VALUE] > -2000:
                    val = LottieTensor._format_value(params[LottieTensor.Index.SingleValue.VALUE])
                    lines.append(f'({cmd} {val})')        
            
            else:
                # Default case for any unhandled commands
                lines.append(f"({cmd})")
        
        return '\n'.join(lines)
    
    # Keep other methods unchanged
    def to_tensor(self) -> torch.Tensor:
        """Convert LottieTensor to a single tensor"""
        return torch.cat([self.commands.float(), self.params], dim=1)
    
    @staticmethod
    def from_tensor(tensor: torch.Tensor) -> 'LottieTensor':
        """Create LottieTensor from tensor"""
        commands = tensor[:, 0:1].long()
        params = tensor[:, 1:1+LottieTensor.PARAM_DIM].float()
        
        return LottieTensor(commands, params, PAD_VAL=-2001)
    
    def add_sos(self):
        """Add start-of-sequence token"""
        self.commands = torch.cat([self.sos_token, self.commands])
        pad_params = torch.ones((1, self.PARAM_DIM)) * self.PAD_VAL
        self.params = torch.cat([pad_params, self.params])
        self.seq_len += 1
        return self
    
    def add_eos(self):
        """Add end-of-sequence token"""
        self.commands = torch.cat([self.commands, self.eos_token])
        pad_params = torch.ones((1, self.PARAM_DIM)) * self.PAD_VAL
        self.params = torch.cat([self.params, pad_params])
        self.seq_len += 1
        return self
    
    def pad(self, seq_len: int):
        """Pad sequence to specified length"""
        pad_len = max(seq_len - len(self.commands), 0)
        if pad_len > 0:
            pad_commands = torch.ones((pad_len, 1)) * LottieTensor.CMD_PAD
            pad_params = torch.ones((pad_len, self.PARAM_DIM)) * self.PAD_VAL
            
            self.commands = torch.cat([self.commands, pad_commands.long()])
            self.params = torch.cat([self.params, pad_params])
        return self

    @staticmethod
    def _clamp_value(value: float, min_val: float = -2000, max_val: float = 2000) -> float:
        """Clamp a value between min and max bounds"""
        return max(min_val, min(max_val, value))

    @staticmethod
    def _index_clamp_value(value: float, min_val: float = -100, max_val: float = 100) -> float:
        """Clamp a value between min and max bounds"""
        return max(min_val, min(max_val, value))


    @classmethod
    def init_tokenizer(cls, model_path=None):
        """Initialize tokenizer once for the class - 支持多路径fallback"""
        if cls.tokenizer is None:
            from transformers import AutoTokenizer
            if model_path is None:
                # 尝试多个可能的路径
                possible_paths = [
                    '/mnt/jfs-test/Qwen2.5-VL-3B-Instruct',
                    '/data/models/Qwen2.5-VL-3B-Instruct',
                    'Qwen/Qwen2.5-VL-3B-Instruct',  # HuggingFace Hub
                ]
                for path in possible_paths:
                    try:
                        cls.tokenizer = AutoTokenizer.from_pretrained(path)
                        # 只在主进程打印一次
                        import os
                        if os.environ.get('RANK', '0') == '0':
                            print(f"Tokenizer loaded successfully from: {path}")
                        return
                    except Exception as e:
                        continue
                raise ValueError(f"Failed to load tokenizer from any known path: {possible_paths}")
            else:
                cls.tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    @classmethod
    def get_tokenizer(cls):
        if cls.tokenizer is None:
            from transformers import AutoTokenizer
            cls.tokenizer = AutoTokenizer.from_pretrained('/mnt/jfs-test/Qwen2.5-VL-3B-Instruct')
        return cls.tokenizer
    

    @staticmethod
    def get_param_offset(cmd_idx: int, param_idx: int) -> int:
        """
        Get the offset for a parameter based on its command and parameter index.
        Returns the offset to add to the parameter value.
        """
        # 1. 查缓存
        cache_key = (cmd_idx, param_idx)
        if cache_key in LottieTensor._OFFSET_CACHE:
            return LottieTensor._OFFSET_CACHE[cache_key]
        

        # 更新后的offset范围，确保没有overlap
        TIME_OFFSET = 155000              # -2000 to 2000: range [153000, 157000] (4001 values)
        SPACE_OFFSET = 159100             # -2000 to 2000: range [157100, 161100] (4001 values)
        AMPLITUDE_OFFSET = 161200         # 0 to 20: range [161200, 161220] (21 values)
        ANCHOR_OFFSET = 161300            # -2000 to 2000: range [161300, 165300] (4001 values)
        ANIMATED_OFFSET = 165400          # 0 to 1: range [165400, 165401] (2 values)
        H_FLAG_OFFSET = 165402            # 0 to 1: range [165402, 165403] (2 values)
        OFFSET_VAL_OFFSET = 165404        # 0 to 1: range [165404, 165405] (2 values)
        CA_OFFSET = 165406                # 0 to 2: range [165406, 165408] (3 values)
        JUSTIFY_OFFSET = 165409           # 0 to 6: range [165409, 165415] (7 values)
        TEXT_TRACKING_OFFSET = 165416     # -100 to 500: range [165416, 166016] (601 values)
        HAS_STROKE_COLOR_OFFSET = 166017  # 0 to 1: range [166017, 166018] (2 values)
        IX_OFFSET = 166019                # 0 to 1000: range [166019, 167019] (1001 values)
        BM_OFFSET = 167020                # 0 to 20: range [167020, 167040] (21 values)
        CLOSED_OFFSET = 167041            # 0 to 1: range [167041, 167042] (2 values)
        DIRECTION_OFFSET = 167043         # 0 to 5: range [167043, 167048] (6 values)
        STAR_TYPE_OFFSET = 167049         # 0 to 5: range [167049, 167054] (6 values)
        MULTIPLE_OFFSET = 167055          # 0 to 5: range [167055, 167060] (6 values)
        COMPOSITE_OFFSET = 167061         # 0 to 5: range [167061, 167066] (6 values)
        SKEW_OFFSET = 167067              # -25 to 25: range [167067, 167117] (51 values)
        SKEW_AXIS_OFFSET = 167118         # -25 to 25: range [167118, 167168] (51 values)
        SCALE_OFFSET = 167169             # -1000 to 2000: range [167169, 170169] (3001 values)
        ROTATION_OFFSET = 170170          # -720 to 720: range [170170, 171610] (1441 values)
        EASE_OFFSET = 171611              # -100 to 100: range [171611, 171811] (201 values)
        SMOOTH_OFFSET = 171812            # 0 to 100: range [171812, 171912] (101 values)
        TRACKING_OFFSET = 171913          # -50 to 50: range [171913, 172013] (101 values)
        INDEX_OFFSET = 172014             # 0 to 1000: range [172014, 173014] (1001 values)
        DDD_OFFSET = 173015               # 0 to 1: range [173015, 173016] (2 values)
        HD_OFFSET = 173017                # 0 to 1: range [173017, 173018] (2 values)
        CP_OFFSET = 173019                # 0 to 50: range [173019, 173069] (51 values)
        HAS_MASK_OFFSET = 173070          # 0 to 1: range [173070, 173071] (2 values)
        AO_OFFSET = 173072                # 0 to 1: range [173072, 173073] (2 values)
        TT_OFFSET = 173074                # 0 to 5: range [173074, 173079] (6 values)
        TP_OFFSET = 173080                # 0 to 100: range [173080, 173180] (101 values)
        TD_OFFSET = 173181                # 0 to 2: range [173181, 173183] (3 values)
        CT_OFFSET = 173184                # 0 to 1: range [173184, 173185] (2 values)
        NUMBER_OFFSET = 173186            # 0 to 500: range [173186, 173686] (501 values)
        DIM_OFFSET = 173687               # 0 to 10: range [173687, 173697] (11 values)
        HAS_C_A_OFFSET = 173698           # 0 to 1: range [173698, 173699] (2 values)
        HAS_C_IX_OFFSET = 173700          # 0 to 1: range [173700, 173701] (2 values)
        HAS_O_A_OFFSET = 173702           # 0 to 1: range [173702, 173703] (2 values)
        HAS_O_IX_OFFSET = 173704          # 0 to 1: range [173704, 173705] (2 values)
        FILL_RULE_OFFSET = 173706         # 0 to 4: range [173706, 173710] (5 values)
        TYPE_OFFSET = 173711              # 0 to 40: range [173711, 173751] (41 values)
        TEXT_RANGE_UNITS_OFFSET = 173752  # 0 to 10: range [173752, 173762] (11 values)
        INV_OFFSET = 173763               # 0 to 1: range [173763, 173764] (2 values)
        MODE_OFFSET = 173765              # 0 to 10: range [173765, 173775] (11 values)
        TEXT_SHAPE_TYPE_OFFSET = 173776   # 0 to 10: range [173776, 173786] (11 values)
        TEXT_RANDOM_OFFSET = 173787       # 0 to 1: range [173787, 173788] (2 values)
        COLOR_POINTS_OFFSET = 173789      # 0 to 50: range [173789, 173839] (51 values)
        ROUND_OFFSET = 173840             # -100 to 1000: range [173840, 174940] (1101 values)
        RADIUS_OFFSET = 174941            # 0 to 300: range [174941, 175241] (301 values)
        FREQUENCY_OFFSET = 175242         # 0 to 150: range [175242, 175392] (151 values)
        SPEED_OFFSET = 175393             # -1000 to 1000: range [175393, 177393] (2001 values)
        FONT_OFFSET = 177394              # -100 to 2000: range [177394, 179494] (2101 values)
        COLOR_OFFSET = 179495             # 0 to 255: range [179495, 179750] (256 values)
        LINE_CAP_OFFSET = 179752          # 1 to 3: range [179752, 179754] (3 values)
        LINE_JOIN_OFFSET = 179757         # 1 to 3: range [179757, 179759] (3 values)
        MITER_LIMIT_OFFSET = 179760       # 0 to 100: range [179760, 179860] (101 values)
        EFFECT_OFFSET = 179861            # -250 to 1000: range [179861, 181111] (1251 values)
        OPACITY_OFFSET = 181112           # 0 to 100: range [181112, 181212] (101 values)
        WIDTH_VALUE_OFFSET = 181300       # 0 to 10000: range [181300, 191300] (10001 values for 0-100.00)

        NO_OFFSET = 0
        
        # Time dictionary parameters - all time-related values
        time_params = {
            LottieTensor.CMD_ANIMATION: [
                LottieTensor.Index.Animation.IP, 
                LottieTensor.Index.Animation.OP
            ],
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.IN_POINT, 
                LottieTensor.Index.Layer.OUT_POINT, 
                LottieTensor.Index.Layer.START_TIME
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.IN_POINT, 
                LottieTensor.Index.NullLayer.OUT_POINT, 
                LottieTensor.Index.NullLayer.START_TIME
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.IN_POINT, 
                LottieTensor.Index.PrecompLayer.OUT_POINT, 
                LottieTensor.Index.PrecompLayer.START_TIME
            ],
            LottieTensor.CMD_TEXT_LAYER: [
                LottieTensor.Index.TextLayer.IN_POINT, 
                LottieTensor.Index.TextLayer.OUT_POINT, 
                LottieTensor.Index.TextLayer.START_TIME
            ],
            LottieTensor.CMD_SOLID_LAYER: [
                LottieTensor.Index.SolidLayer.IN_POINT, 
                LottieTensor.Index.SolidLayer.OUT_POINT, 
                LottieTensor.Index.SolidLayer.START_TIME
            ],
            LottieTensor.CMD_KEYFRAME: [
                LottieTensor.Index.Keyframe.T
            ],
            LottieTensor.CMD_WIDTH_KEYFRAME: [
                LottieTensor.Index.WidthKeyframe.T
            ],
            LottieTensor.CMD_COLOR_KEYFRAME: [
                LottieTensor.Index.Keyframe.T
            ],
            LottieTensor.CMD_OPACITY_KEYFRAME: [
                LottieTensor.Index.Keyframe.T
            ],
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.T
            ],
            LottieTensor.CMD_MASK_PT_KEYFRAME: [
                LottieTensor.Index.MaskPtKeyframe.T
            ],
            LottieTensor.CMD_RANGE_START_KEYFRAME: [
                LottieTensor.Index.RangeStartKeyframe.T
            ],
            LottieTensor.CMD_RANGE_END_KEYFRAME: [
                LottieTensor.Index.RangeEndKeyframe.T
            ],
            LottieTensor.CMD_RANGE_OFFSET_KEYFRAME: [
                LottieTensor.Index.RangeOffsetKeyframe.T
            ],
            LottieTensor.CMD_DASH_KEYFRAME: [
                LottieTensor.Index.DashKeyframe.T
            ],
        }
        
        # Space dictionary parameters - all spatial/positional values
        space_params = {
            LottieTensor.CMD_ANIMATION: [
                LottieTensor.Index.Animation.W, 
                LottieTensor.Index.Animation.H
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.W, 
                LottieTensor.Index.PrecompLayer.H
            ],
            LottieTensor.CMD_SOLID_LAYER: [
                LottieTensor.Index.SolidLayer.WIDTH, 
                LottieTensor.Index.SolidLayer.HEIGHT
            ],
            LottieTensor.CMD_DIMENSIONS: [
                LottieTensor.Index.Dimensions.WIDTH, 
                LottieTensor.Index.Dimensions.HEIGHT
            ],
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.STROKE_WIDTH,
                LottieTensor.Index.TextKeyframe.WRAP_POSITION_X,
                LottieTensor.Index.TextKeyframe.WRAP_POSITION_Y,
                LottieTensor.Index.TextKeyframe.WRAP_SIZE_X,
                LottieTensor.Index.TextKeyframe.WRAP_SIZE_Y
            ],
            LottieTensor.CMD_KEYFRAME: [
                LottieTensor.Index.Keyframe.S1, LottieTensor.Index.Keyframe.S2, LottieTensor.Index.Keyframe.S3,
                LottieTensor.Index.Keyframe.E1, LottieTensor.Index.Keyframe.E2, LottieTensor.Index.Keyframe.E3,
                LottieTensor.Index.Keyframe.TO1, LottieTensor.Index.Keyframe.TO2, LottieTensor.Index.Keyframe.TO3,
                LottieTensor.Index.Keyframe.TI1, LottieTensor.Index.Keyframe.TI2, LottieTensor.Index.Keyframe.TI3
            ],
            #LottieTensor.CMD_WIDTH_KEYFRAME: [
            #    LottieTensor.Index.WidthKeyframe.S,
            #],
            LottieTensor.CMD_OPACITY_KEYFRAME: [
                LottieTensor.Index.Keyframe.S1,
            ],
            LottieTensor.CMD_POSITION: [
                LottieTensor.Index.Transform.X, LottieTensor.Index.Transform.Y, LottieTensor.Index.Transform.Z,
                LottieTensor.Index.TwoValues.VALUE1, LottieTensor.Index.TwoValues.VALUE2
            ],
            LottieTensor.CMD_POSITION_X: [
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_POSITION_Y: [
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_POSITION_Z: [
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_POINT: [
                LottieTensor.Index.Point.X, LottieTensor.Index.Point.Y,
                LottieTensor.Index.Point.IN_X, LottieTensor.Index.Point.IN_Y,
                LottieTensor.Index.Point.OUT_X, LottieTensor.Index.Point.OUT_Y
            ],
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.POSITION_X, LottieTensor.Index.TransformShape.POSITION_Y,
            ],
            LottieTensor.CMD_SIZE: [
                LottieTensor.Index.Transform.X, LottieTensor.Index.Transform.Y  # 修改
            ],
            LottieTensor.CMD_RECT_SIZE: [
                LottieTensor.Index.Transform.X, LottieTensor.Index.Transform.Y  # 修改
            ],
            LottieTensor.CMD_ELLIPSE_SIZE: [
                LottieTensor.Index.Transform.X, LottieTensor.Index.Transform.Y  # 修改
            ],
            LottieTensor.CMD_START_POINT: [
                LottieTensor.Index.TwoValues.VALUE1, LottieTensor.Index.TwoValues.VALUE2
            ],
            LottieTensor.CMD_END_POINT: [
                LottieTensor.Index.TwoValues.VALUE1, LottieTensor.Index.TwoValues.VALUE2
            ],
            LottieTensor.CMD_POINTS_STAR: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_START: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_END: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_OFFSET: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            #LottieTensor.CMD_WIDTH: [
            #    LottieTensor.Index.SingleValue.VALUE
            #],
            #LottieTensor.CMD_DASH: [
            #    LottieTensor.Index.Dash.LENGTH
            #],
            #LottieTensor.CMD_DASH_OFFSET: [
            #    LottieTensor.Index.DashOffset.O
            #],
            #LottieTensor.CMD_DASH_KEYFRAME: [
            #    LottieTensor.Index.DashKeyframe.S,
            # ],
            LottieTensor.CMD_TR_POSITION: [
                LottieTensor.Index.TrPosition.X, LottieTensor.Index.TrPosition.Y
            ],
            LottieTensor.CMD_REPEATER_OFFSET: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_RANGE_START_KEYFRAME: [
                LottieTensor.Index.RangeStartKeyframe.S,
            ],
            LottieTensor.CMD_RANGE_END_KEYFRAME: [
                LottieTensor.Index.RangeEndKeyframe.S,
            ],
            LottieTensor.CMD_RANGE_OFFSET_KEYFRAME: [
                LottieTensor.Index.RangeOffsetKeyframe.S,
            ],
            LottieTensor.CMD_POSITION_ANIMATORS: [
                LottieTensor.Index.PositionAnimators.K_X,
                LottieTensor.Index.PositionAnimators.K_Y,
                LottieTensor.Index.PositionAnimators.K_Z
            ],
            LottieTensor.CMD_MASK_X: [
                LottieTensor.Index.MaskX.K
            ],
            LottieTensor.CMD_MASK_PT_K_I: list(range(20)),
            LottieTensor.CMD_MASK_PT_K_O: list(range(20)),
            LottieTensor.CMD_MASK_PT_K_V: list(range(20)),
            LottieTensor.CMD_MASK_PT_KF_I: [
                LottieTensor.Index.MaskPtKfI.X, LottieTensor.Index.MaskPtKfI.Y
            ],
            LottieTensor.CMD_MASK_PT_KF_O: [
                LottieTensor.Index.MaskPtKfO.X, LottieTensor.Index.MaskPtKfO.Y
            ],
            LottieTensor.CMD_MASK_PT_KF_SHAPE_I: list(range(20)),
            LottieTensor.CMD_MASK_PT_KF_SHAPE_O: list(range(20)),
            LottieTensor.CMD_MASK_PT_KF_SHAPE_V: list(range(20)),
            LottieTensor.CMD_VALUE: [
                LottieTensor.Index.Value.VALUE
            ],
            LottieTensor.CMD_MORE_OPTIONS: [
                LottieTensor.Index.MoreOptions.ALIGNMENT_K1,
                LottieTensor.Index.MoreOptions.ALIGNMENT_K2
            ],
            LottieTensor.CMD_ALIGNMENT_K: [
                LottieTensor.Index.AlignmentK.VALUE1,
                LottieTensor.Index.AlignmentK.VALUE2
            ],
            LottieTensor.CMD_CHAR: [
                LottieTensor.Index.Char.W
            ],
            LottieTensor.CMD_GRADIENT_FILL: [
                LottieTensor.Index.GradientFill.START_POINT_X,
                LottieTensor.Index.GradientFill.START_POINT_Y,
                LottieTensor.Index.GradientFill.END_POINT_X,
                LottieTensor.Index.GradientFill.END_POINT_Y,
                LottieTensor.Index.GradientFill.HIGHLIGHT_LENGTH,
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.WIDTH,
                LottieTensor.Index.GradientStroke.START_POINT_X,
                LottieTensor.Index.GradientStroke.START_POINT_Y,
                LottieTensor.Index.GradientStroke.END_POINT_X,
                LottieTensor.Index.GradientStroke.END_POINT_Y,
                LottieTensor.Index.GradientStroke.HIGHLIGHT_LENGTH,
            ],
            LottieTensor.CMD_HIGHLIGHT_LENGTH: [
                LottieTensor.Index.SingleValue.VALUE
            ],
        }
        width_value_params = {
            LottieTensor.CMD_WIDTH: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_DASH: [
                LottieTensor.Index.Dash.LENGTH
            ],
            LottieTensor.CMD_DASH_OFFSET: [
                LottieTensor.Index.DashOffset.O
            ],
            LottieTensor.CMD_WIDTH_KEYFRAME: [
                LottieTensor.Index.WidthKeyframe.S,
            ],
            LottieTensor.CMD_DASH_KEYFRAME: [
                LottieTensor.Index.DashKeyframe.S,
            ],
        }
        
        amplitude_params = {
            LottieTensor.CMD_AMPLITUDE: [
                LottieTensor.Index.Amplitude.VALUE
            ], 
        }
        
        anchor_params = {
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.ANCHOR_X, LottieTensor.Index.TransformShape.ANCHOR_Y,
            ],
            LottieTensor.CMD_TR_ANCHOR: [
                LottieTensor.Index.TrAnchor.X, LottieTensor.Index.TrAnchor.Y
            ],
            LottieTensor.CMD_ANCHOR: [
                LottieTensor.Index.Transform.X, LottieTensor.Index.Transform.Y, LottieTensor.Index.Transform.Z
            ],
        }

        animated_params = {
            LottieTensor.CMD_MORE_OPTIONS: [
                LottieTensor.Index.MoreOptions.ALIGNMENT_A,
            ],
            LottieTensor.CMD_ELLIPSE_SIZE: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_RECT_SIZE: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_POSITION: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_POSITION_X: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_POSITION_Y: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_POSITION_Z: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_SCALE: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_ROTATION: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_OPACITY: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_ANCHOR: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_SIZE: [
                LottieTensor.Index.Transform.ANIMATED
            ],
            LottieTensor.CMD_PATH: [
                LottieTensor.Index.Path.ANIMATED,
            ],
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.COLOR_ANIMATED,
                LottieTensor.Index.Fill.OPACITY_ANIMATED,
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.WIDTH_ANIMATED,
                LottieTensor.Index.Stroke.COLOR_ANIMATED
            ],
            LottieTensor.CMD_RECT_ROUNDED: [
                LottieTensor.Index.SingleValue.ANIMATED
            ],
            LottieTensor.CMD_START: [
                LottieTensor.Index.SingleValue.ANIMATED
            ],
            LottieTensor.CMD_END: [
                LottieTensor.Index.SingleValue.ANIMATED
            ],
            LottieTensor.CMD_OFFSET: [
                LottieTensor.Index.SingleValue.ANIMATED
            ],
            LottieTensor.CMD_MASK_PT: [
                LottieTensor.Index.MaskPt.A,
            ],
            LottieTensor.CMD_MASK_O: [
                LottieTensor.Index.MaskO.A,
            ],
            LottieTensor.CMD_MASK_X: [
                LottieTensor.Index.MaskX.A,
            ],
            LottieTensor.CMD_TM: [
                LottieTensor.Index.Tm.A
            ],
            LottieTensor.CMD_RANGE_START: [
                LottieTensor.Index.RangeStart.A
            ],
            LottieTensor.CMD_RANGE_END: [
                LottieTensor.Index.RangeEnd.A
            ],
            LottieTensor.CMD_RANGE_OFFSET: [
                LottieTensor.Index.Amount.A,
            ],
            LottieTensor.CMD_AMOUNT: [
                LottieTensor.Index.Amount.A,
            ],
            LottieTensor.CMD_MAX_EASE: [
                LottieTensor.Index.MaxEase.A,
            ],
            LottieTensor.CMD_MIN_EASE: [
                LottieTensor.Index.MinEase.A,
            ],
            LottieTensor.CMD_S_M: [
                LottieTensor.Index.SM.A,
            ],
            LottieTensor.CMD_OPACITY_ANIMATORS: [
                LottieTensor.Index.OpacityAnimators.A,
            ],
            LottieTensor.CMD_POSITION_ANIMATORS: [
                LottieTensor.Index.PositionAnimators.A,
            ],
            LottieTensor.CMD_SCALE_ANIMATORS: [
                LottieTensor.Index.ScaleAnimators.A,
            ],
            LottieTensor.CMD_ROTATION_ANIMATORS: [
                LottieTensor.Index.RotationAnimators.A,
            ],
            LottieTensor.CMD_TRACKING_ANIMATORS: [
                LottieTensor.Index.TrackingAnimators.A,
            ],
            LottieTensor.CMD_ALIGNMENT: [
                LottieTensor.Index.Alignment.A
            ],
        }
        
        h_flag_params = {
            LottieTensor.CMD_KEYFRAME: [
                LottieTensor.Index.Keyframe.H_FLAG
            ],
        }
        
        offset_val_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.OFFSET,
            ],
        }
        
        ca_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.CA,
            ],
            LottieTensor.CMD_CA: [
                LottieTensor.Index.Ca.VALUE
            ],
        }
        
        justify_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.JUSTIFY,
            ],
            LottieTensor.CMD_JUSTIFY: [
                LottieTensor.Index.Justify.VALUE
            ],
        }
        
        text_tracking_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.TRACKING,
            ],
            LottieTensor.CMD_TRACKING: [
                LottieTensor.Index.Tracking.VALUE
            ],
        }
        
        has_stroke_color_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.HAS_STROKE_COLOR,
            ],
        }
        
        ix_params = {
            LottieTensor.CMD_PATH: [
                LottieTensor.Index.Path.IX,
                LottieTensor.Index.Path.KS_IX,
            ],
            LottieTensor.CMD_GROUP: [
                LottieTensor.Index.Group.IX,
                LottieTensor.Index.Group.CIX,
            ],
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.C_IX,
                LottieTensor.Index.Fill.O_IX,
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.C_IX,
            ],
            LottieTensor.CMD_RECT: [
                LottieTensor.Index.Rect.IX,
            ],
            LottieTensor.CMD_ROUNDED: [
                LottieTensor.Index.SingleValue.IX
            ],
            LottieTensor.CMD_TRIM: [
                LottieTensor.Index.Trim.IX
            ],
            LottieTensor.CMD_REPEATER: [
                LottieTensor.Index.Repeater.IX
            ],
            LottieTensor.CMD_COPIES: [
                LottieTensor.Index.SingleValue.IX
            ],
            LottieTensor.CMD_REPEATER_OFFSET: [
                LottieTensor.Index.SingleValue.IX
            ],
            LottieTensor.CMD_TR_P_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_A_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_S_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_R_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_SO_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_EO_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.ML2_IX,
            ],
            LottieTensor.CMD_MASK_PT: [
                LottieTensor.Index.MaskPt.IX,
            ],
            LottieTensor.CMD_MASK_O: [
                LottieTensor.Index.MaskO.IX,
            ],
            LottieTensor.CMD_MASK_X: [
                LottieTensor.Index.MaskX.IX,
            ],
            LottieTensor.CMD_ZIG_ZAG: [
                LottieTensor.Index.ZigZag.IX
            ],
            LottieTensor.CMD_RANGE_OFFSET: [
                LottieTensor.Index.Amount.IX
            ],
            LottieTensor.CMD_AMOUNT: [
                LottieTensor.Index.Amount.IX
            ],
            LottieTensor.CMD_MAX_EASE: [
                LottieTensor.Index.MaxEase.IX
            ],
            LottieTensor.CMD_MIN_EASE: [
                LottieTensor.Index.MinEase.IX
            ],
            LottieTensor.CMD_S_M: [
                LottieTensor.Index.SM.IX
            ],
            LottieTensor.CMD_OPACITY_ANIMATORS: [
                LottieTensor.Index.OpacityAnimators.IX
            ],
            LottieTensor.CMD_POSITION_ANIMATORS: [
                LottieTensor.Index.PositionAnimators.IX
            ],
            LottieTensor.CMD_SCALE_ANIMATORS: [
                LottieTensor.Index.ScaleAnimators.IX
            ],
            LottieTensor.CMD_ROTATION_ANIMATORS: [
                LottieTensor.Index.RotationAnimators.IX
            ],
            LottieTensor.CMD_TRACKING_ANIMATORS: [
                LottieTensor.Index.TrackingAnimators.IX
            ],
            LottieTensor.CMD_ALIGNMENT_IX: [
                LottieTensor.Index.AlignmentIx.VALUE
            ],
            LottieTensor.CMD_MORE_OPTIONS: [
                LottieTensor.Index.MoreOptions.ALIGNMENT_IX
            ],
            LottieTensor.CMD_DASH: [
                LottieTensor.Index.Dash.V_IX
            ],
            LottieTensor.CMD_DASH_ANIMATED: [
                LottieTensor.Index.DashAnimated.V_IX,
            ],
        }
        
        bm_params = {
            LottieTensor.CMD_GROUP: [
                LottieTensor.Index.Group.BM,
            ],
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.BM,
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.BM,
            ],
        }
        
        closed_params = {
            LottieTensor.CMD_PATH: [
                LottieTensor.Index.Path.CLOSED,
            ], 
            LottieTensor.CMD_BEZIER: [
                LottieTensor.Index.Bezier.CLOSED
            ],
            LottieTensor.CMD_MASK_PT_K_C: [
                LottieTensor.Index.MaskPtK.C
            ],
            LottieTensor.CMD_MASK_PT_KF_SHAPE: [
                LottieTensor.Index.MaskPtKfShape.C,
            ],
        }
        
        direction_params = {
            LottieTensor.CMD_RECT: [
                LottieTensor.Index.Rect.D,
            ],
            LottieTensor.CMD_STAR: [
                LottieTensor.Index.Star.D,
            ],
        }
        
        star_type_params = {
            LottieTensor.CMD_STAR: [
                LottieTensor.Index.Star.SY
            ],
        }
        
        multiple_params = {
            LottieTensor.CMD_MULTIPLE: [
                LottieTensor.Index.SingleValue.VALUE
            ], 
        }
        
        composite_params = {
            LottieTensor.CMD_COMPOSITE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
        }
        
        skew_params = {
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.SKEW,
            ],  
            LottieTensor.CMD_SKEW: [
                LottieTensor.Index.SingleValue.VALUE
            ],
        }

        skew_axis_params = {
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.SKEW_AXIS,
            ],  
            LottieTensor.CMD_SKEW_AXIS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
        }
        
        scale_params = {
            LottieTensor.CMD_SCALE: [
                LottieTensor.Index.Transform.X, LottieTensor.Index.Transform.Y, LottieTensor.Index.Transform.Z
            ],
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.SCALE_X, LottieTensor.Index.TransformShape.SCALE_Y,
            ],  
            LottieTensor.CMD_TR_SCALE: [
                LottieTensor.Index.TwoValues.VALUE1, LottieTensor.Index.TwoValues.VALUE2
            ],
            LottieTensor.CMD_SCALE_ANIMATORS: [
                LottieTensor.Index.ScaleAnimators.K_X,
                LottieTensor.Index.ScaleAnimators.K_Y,
                LottieTensor.Index.ScaleAnimators.K_Z
            ],
        }
        
        rotation_params = {
            LottieTensor.CMD_ROTATION: [
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.ROTATION
            ],
            LottieTensor.CMD_STAR_ROTATION: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_ROTATION: [
                LottieTensor.Index.TrRotation.VALUE
            ],
            LottieTensor.CMD_ROTATION_ANIMATORS: [
                LottieTensor.Index.RotationAnimators.K
            ],
            LottieTensor.CMD_GRADIENT_FILL: [
                LottieTensor.Index.GradientFill.HIGHLIGHT_ANGLE,
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.HIGHLIGHT_ANGLE
            ],
            LottieTensor.CMD_HIGHLIGHT_ANGLE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
        }
        
        ease_params = {
            LottieTensor.CMD_MAX_EASE: [
                LottieTensor.Index.MaxEase.K
            ],
            LottieTensor.CMD_MIN_EASE: [
                LottieTensor.Index.MinEase.K
            ],
        }
        
        smooth_params = {
            LottieTensor.CMD_S_M: [
                LottieTensor.Index.SM.K
            ],
        }
        
        tracking_params = {
            LottieTensor.CMD_TRACKING_ANIMATORS: [
                LottieTensor.Index.TrackingAnimators.K
            ],
        }
        
        index_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.INDEX,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.INDEX,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.INDEX,
            ],
            LottieTensor.CMD_TEXT_LAYER: [
                LottieTensor.Index.TextLayer.INDEX,
            ],   
            LottieTensor.CMD_SOLID_LAYER: [
                LottieTensor.Index.SolidLayer.INDEX,
            ],
            LottieTensor.CMD_PARENT: [
                LottieTensor.Index.Parent.PARENT_INDEX
            ],
            LottieTensor.CMD_PATH: [
                LottieTensor.Index.Path.IND,
            ],
            LottieTensor.CMD_COLOR: [
                LottieTensor.Index.Color.INDEX
            ],
            LottieTensor.CMD_MASK: [
                LottieTensor.Index.Mask.INDEX,
            ],
            LottieTensor.CMD_MASK_PT_KEYFRAME: [
                LottieTensor.Index.MaskPtKeyframe.INDEX
            ],
            LottieTensor.CMD_MASK_PT_KF_SHAPE: [
                LottieTensor.Index.MaskPtKfShape.INDEX,
            ],
            LottieTensor.CMD_EFFECT: [
                LottieTensor.Index.Effect.INDEX,
            ],
            LottieTensor.CMD_LAYER_EFFECT: [
                LottieTensor.Index.LayerEffect.INDEX,
            ],
            LottieTensor.CMD_DROPDOWN: [
                LottieTensor.Index.Dropdown.INDEX,
            ],
            LottieTensor.CMD_NO_VALUE: [
                LottieTensor.Index.NO_VALUE.INDEX,
            ],
            LottieTensor.CMD_IGNORED: [
                LottieTensor.Index.Ignored.INDEX,
            ],
            LottieTensor.CMD_SLIDER: [
                LottieTensor.Index.Slider.INDEX,
            ],
        }
        
        ddd_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.DDD,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.DDD,
            ],
            LottieTensor.CMD_ANIMATION: [
                LottieTensor.Index.Animation.DDD
            ],
        }
        
        hd_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.HD,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.HD,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.HD,
            ],
            LottieTensor.CMD_PATH: [
                LottieTensor.Index.Path.HD,
            ],
            LottieTensor.CMD_GROUP: [
                LottieTensor.Index.Group.HD,
            ],
            LottieTensor.CMD_RECT: [
                LottieTensor.Index.Rect.HD,
            ],
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.HD
            ],
        }
        
        cp_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.CP,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.CP,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.CP,
            ],
        }
        
        has_mask_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.HAS_MASK,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.HAS_MASK,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.HAS_MASK,
            ],
            LottieTensor.CMD_TEXT_LAYER: [
                LottieTensor.Index.TextLayer.HAS_MASK,
            ], 
            LottieTensor.CMD_SOLID_LAYER: [
                LottieTensor.Index.SolidLayer.HAS_MASK
            ],
        }
        
        ao_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.AO,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.AO,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.AO,
            ],
        }
        
        tt_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.TT,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.TT,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.TT,
            ],
        }
        
        tp_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.TP,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.TP,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.TP,
            ],
        }
        
        td_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.TD,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.TD,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.TD,
            ],
        }

        ct_params = {
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.CT,
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.CT,
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.CT,
            ],
        }
        
        number_params = {
            LottieTensor.CMD_COPIES: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_AMOUNT: [
                LottieTensor.Index.Amount.K
            ],
            LottieTensor.CMD_RANGE_OFFSET: [
                LottieTensor.Index.Amount.K
            ],
            LottieTensor.CMD_GROUP: [
                LottieTensor.Index.Group.NP
            ],
            LottieTensor.CMD_EFFECT: [
                LottieTensor.Index.Effect.NP,
            ],
        }
        
        dim_params = {
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.COLOR_DIM,
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.COLOR_DIM,
            ], 
        }
        
        has_c_a_params = {
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.HAS_C_A,
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.HAS_C_A,
            ],
        }
        
        has_c_ix_params = {
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.HAS_C_IX,
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.HAS_C_IX,
            ],
        }
        
        has_o_a_params = {
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.HAS_O_A,
            ],
        }
        
        has_o_ix_params = {
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.HAS_O_IX,
            ],
        }
        
        fill_rule_params = {
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.FILL_RULE,
            ],
            LottieTensor.CMD_GRADIENT_FILL: [
                LottieTensor.Index.GradientFill.FILL_RULE,
            ],
            LottieTensor.CMD_FILL_RULE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
        }
        
        type_params = {
            LottieTensor.CMD_GRADIENT_FILL: [
                LottieTensor.Index.GradientFill.GRADIENT_TYPE,
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.GRADIENT_TYPE,
            ],
            LottieTensor.CMD_GRADIENT_TYPE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_POINT_TYPE: [
                LottieTensor.Index.PointType.VALUE
            ],
            LottieTensor.CMD_RANGE_SELECTOR: [
                LottieTensor.Index.RangeSelector.T,
            ],
            LottieTensor.CMD_DASH: [
                LottieTensor.Index.Dash.TYPE,
            ],
            LottieTensor.CMD_DASH_ANIMATED: [
                LottieTensor.Index.DashAnimated.TYPE,
            ],
            LottieTensor.CMD_EFFECT: [
                LottieTensor.Index.Effect.TYPE,
            ],
        }
        
        text_range_units = {
            LottieTensor.CMD_RANGE_SELECTOR: [
                LottieTensor.Index.RangeSelector.R,
            ],
        }
        
        inv_params = {
            LottieTensor.CMD_MASK: [
                LottieTensor.Index.Mask.INV,
            ],
        }
        
        mode_params = {
            LottieTensor.CMD_MERGE_MODE: [
                LottieTensor.Index.MergeMode.MODE
            ],
            LottieTensor.CMD_MASK: [
                LottieTensor.Index.Mask.MODE,
            ],
            LottieTensor.CMD_RANGE_SELECTOR: [
                LottieTensor.Index.RangeSelector.B,
            ],
        }
        
        text_shape_type = {
            LottieTensor.CMD_RANGE_SELECTOR: [
                LottieTensor.Index.RangeSelector.SH,
            ],
        }
        
        text_random = {
            LottieTensor.CMD_RANGE_SELECTOR: [
                LottieTensor.Index.RangeSelector.RN 
            ],
        }
        
        color_points_params = {
            LottieTensor.CMD_GRADIENT_FILL: [
                LottieTensor.Index.GradientFill.COLOR_POINTS
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.COLOR_POINTS
            ],
            LottieTensor.CMD_COLOR_POINTS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
        }
        
        round_params = {
            LottieTensor.CMD_ROUNDED: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_RECT_ROUNDED: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_INNER_ROUNDNESS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_OUTER_ROUNDNESS: [
                LottieTensor.Index.SingleValue.VALUE
            ],    
        }
        
        radius_params = {
            LottieTensor.CMD_INNER_RADIUS: [
                LottieTensor.Index.SingleValue.VALUE
            ],  
            LottieTensor.CMD_OUTER_RADIUS: [
                LottieTensor.Index.SingleValue.VALUE
            ], 
            LottieTensor.CMD_RADIUS: [
                LottieTensor.Index.Radius.VALUE
            ],
        }
        
        frequency_params = {
            LottieTensor.CMD_ANIMATION: [
                LottieTensor.Index.Animation.FR,
            ],    
            LottieTensor.CMD_FREQUENCY: [
                LottieTensor.Index.Frequency.VALUE
            ],
            LottieTensor.CMD_ASSET: [
                LottieTensor.Index.Asset.FR
            ],
        }
        
        speed_params = {
            LottieTensor.CMD_KEYFRAME: [
                LottieTensor.Index.Keyframe.I_X, LottieTensor.Index.Keyframe.I_Y,
                LottieTensor.Index.Keyframe.O_X, LottieTensor.Index.Keyframe.O_Y,
                LottieTensor.Index.Keyframe.I_X2, LottieTensor.Index.Keyframe.I_Y2,
                LottieTensor.Index.Keyframe.O_X2, LottieTensor.Index.Keyframe.O_Y2,
                LottieTensor.Index.Keyframe.I_X3, LottieTensor.Index.Keyframe.I_Y3,
                LottieTensor.Index.Keyframe.O_X3, LottieTensor.Index.Keyframe.O_Y3,
            ],
            LottieTensor.CMD_WIDTH_KEYFRAME: [
                LottieTensor.Index.WidthKeyframe.I_X, LottieTensor.Index.WidthKeyframe.I_Y,
                LottieTensor.Index.WidthKeyframe.O_X, LottieTensor.Index.WidthKeyframe.O_Y
            ],
            LottieTensor.CMD_OPACITY_KEYFRAME: [
                LottieTensor.Index.Keyframe.I_X, LottieTensor.Index.Keyframe.I_Y,
                LottieTensor.Index.Keyframe.O_X, LottieTensor.Index.Keyframe.O_Y
            ],
            LottieTensor.CMD_COLOR_KEYFRAME: [
                LottieTensor.Index.Keyframe.I_X, LottieTensor.Index.Keyframe.I_Y,
                LottieTensor.Index.Keyframe.O_X, LottieTensor.Index.Keyframe.O_Y
            ],
            LottieTensor.CMD_DASH_KEYFRAME: [
                LottieTensor.Index.DashKeyframe.I_X, LottieTensor.Index.DashKeyframe.I_Y,
                LottieTensor.Index.DashKeyframe.O_X, LottieTensor.Index.DashKeyframe.O_Y
            ],
            LottieTensor.CMD_RANGE_START_KEYFRAME: [
                LottieTensor.Index.RangeStartKeyframe.I_X, LottieTensor.Index.RangeStartKeyframe.I_Y,
                LottieTensor.Index.RangeStartKeyframe.O_X, LottieTensor.Index.RangeStartKeyframe.O_Y
            ],
            LottieTensor.CMD_RANGE_END_KEYFRAME: [
                LottieTensor.Index.RangeEndKeyframe.I_X, LottieTensor.Index.RangeEndKeyframe.I_Y,
                LottieTensor.Index.RangeEndKeyframe.O_X, LottieTensor.Index.RangeEndKeyframe.O_Y
            ],
            LottieTensor.CMD_RANGE_OFFSET_KEYFRAME: [
                LottieTensor.Index.RangeOffsetKeyframe.I_X, LottieTensor.Index.RangeOffsetKeyframe.I_Y,
                LottieTensor.Index.RangeOffsetKeyframe.O_X, LottieTensor.Index.RangeOffsetKeyframe.O_Y
            ],
        }
        
        font_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.FONT_SIZE,
                LottieTensor.Index.TextKeyframe.LINE_HEIGHT,
                LottieTensor.Index.TextKeyframe.LETTER_SPACING
            ],
            LottieTensor.CMD_FONT_SIZE: [
                LottieTensor.Index.FontSize.SIZE
            ],
            LottieTensor.CMD_LINE_HEIGHT: [
                LottieTensor.Index.LineHeight.VALUE
            ],
            LottieTensor.CMD_LETTER_SPACING: [
                LottieTensor.Index.LetterSpacing.VALUE
            ],
            LottieTensor.CMD_FONT: [
                LottieTensor.Index.Font.ASCENT
            ],
            LottieTensor.CMD_CHAR: [
                LottieTensor.Index.Char.SIZE
            ],
        }
        
        color_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: [
                LottieTensor.Index.TextKeyframe.FILL_COLOR_R,
                LottieTensor.Index.TextKeyframe.FILL_COLOR_G,
                LottieTensor.Index.TextKeyframe.FILL_COLOR_B,
                LottieTensor.Index.TextKeyframe.STROKE_COLOR_R,
                LottieTensor.Index.TextKeyframe.STROKE_COLOR_G,
                LottieTensor.Index.TextKeyframe.STROKE_COLOR_B
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.R,
                LottieTensor.Index.Stroke.G,
                LottieTensor.Index.Stroke.B,
                LottieTensor.Index.Stroke.A
            ],
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.R,
                LottieTensor.Index.Fill.G,
                LottieTensor.Index.Fill.B,
            ],
            LottieTensor.CMD_FILL_COLOR: [
                LottieTensor.Index.FillColor.R,
                LottieTensor.Index.FillColor.G,
                LottieTensor.Index.FillColor.B
            ],
            LottieTensor.CMD_SOLID_LAYER: [
                LottieTensor.Index.SolidLayer.COLOR_R,
                LottieTensor.Index.SolidLayer.COLOR_G,
                LottieTensor.Index.SolidLayer.COLOR_B,
                LottieTensor.Index.SolidLayer.COLOR_A
            ],
            LottieTensor.CMD_COLOR: [
                LottieTensor.Index.Color.R,
                LottieTensor.Index.Color.G,
                LottieTensor.Index.Color.B
            ],
            LottieTensor.CMD_COLOR_KEYFRAME: [
                LottieTensor.Index.Keyframe.S1,
                LottieTensor.Index.Keyframe.S2,
                LottieTensor.Index.Keyframe.S3,
                LottieTensor.Index.Keyframe.E1
            ],
            LottieTensor.CMD_ORIGINAL_COLORS: list(range(LottieTensor.Index.OriginalColors.COUNT)),
            LottieTensor.CMD_GRADIENT_FILL: list(range(LottieTensor.Index.GradientFill.ORIGINAL_COLOR_0, 
                                                        LottieTensor.Index.GradientFill.ORIGINAL_COLOR_23 + 1)),
            LottieTensor.CMD_GRADIENT_STROKE: list(range(LottieTensor.Index.GradientStroke.ORIGINAL_COLOR_0,
                                                        LottieTensor.Index.GradientStroke.ORIGINAL_COLOR_23 + 1)),
        }
        
        line_cap_params = {
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.LC,
            ],
            LottieTensor.CMD_LINE_CAP: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.LINE_CAP,
            ],
        }
        line_join_params = {
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.LJ,
            ],
            LottieTensor.CMD_LINE_JOIN: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.LINE_JOIN,
            ],
        }
        
        miter_limit_params = {
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.ML
            ],
            LottieTensor.CMD_MITER_LIMIT: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_ML2: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.MITER_LIMIT,
                LottieTensor.Index.GradientStroke.ML2
            ],
        }
        
        enabled_params = {
            LottieTensor.CMD_EFFECT: [
                LottieTensor.Index.Effect.ENABLED
            ],
        }
        
        effect_params = {
            LottieTensor.CMD_LAYER_EFFECT: [
                LottieTensor.Index.LayerEffect.VALUE
            ],
            LottieTensor.CMD_DROPDOWN: [
                LottieTensor.Index.Dropdown.VALUE
            ],
            LottieTensor.CMD_NO_VALUE: [
                LottieTensor.Index.NO_VALUE.VALUE
            ],
            LottieTensor.CMD_IGNORED: [
                LottieTensor.Index.Ignored.VALUE
            ],
            LottieTensor.CMD_SLIDER: [
                LottieTensor.Index.Slider.VALUE
            ],
        }
        
        opacity_params = {
            LottieTensor.CMD_GRADIENT_FILL: [
                LottieTensor.Index.GradientFill.OPACITY
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [
                LottieTensor.Index.GradientStroke.OPACITY
            ],
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.OPACITY
            ],
            LottieTensor.CMD_OPACITY: [
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.OPACITY,
            ],
            LottieTensor.CMD_TR_START_OPACITY: [
                LottieTensor.Index.TrStartOpacity.VALUE
            ],
            LottieTensor.CMD_TR_END_OPACITY: [
                LottieTensor.Index.TrEndOpacity.VALUE
            ],
            LottieTensor.CMD_OPACITY_ANIMATORS: [
                LottieTensor.Index.OpacityAnimators.K
            ],
            LottieTensor.CMD_MASK_O: [
                LottieTensor.Index.MaskO.K
            ],
        }
        
        # Tokenizer parameters (no offset)
        tokenizer_params = {
            LottieTensor.CMD_TEXT_KEYFRAME: list(range(LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKENS_START, 
                                                        LottieTensor.Index.TextKeyframe.TEXT_TOKEN_COUNT + 1)),
            LottieTensor.CMD_ASSET: list(range(LottieTensor.Index.Asset.ID_TOKEN_0, 
                                            LottieTensor.Index.Asset.ID_TOKEN_COUNT + 1)),
            LottieTensor.CMD_REFERENCE_ID: list(range(LottieTensor.Index.ReferenceId.ID_TOKEN_0, 
                                                    LottieTensor.Index.ReferenceId.ID_TOKEN_COUNT + 1)),
            LottieTensor.CMD_FONT: list(range(LottieTensor.Index.Font.FAMILY_TOKEN_0, 
                                            LottieTensor.Index.Font.STYLE_TOKEN_COUNT + 1)),
            LottieTensor.CMD_CHAR: list(range(LottieTensor.Index.Char.CH_TOKEN_0, 
                                            LottieTensor.Index.Char.FAMILY_TOKEN_COUNT + 1)),
        }
        # 添加 width_value_params 的判断（在其他判断之前）
        if cmd_idx in width_value_params and param_idx in width_value_params[cmd_idx]:
            return WIDTH_VALUE_OFFSET
        
        elif cmd_idx in tokenizer_params and param_idx in tokenizer_params[cmd_idx]:
            return NO_OFFSET  # No offset for tokenizer tokens
        elif cmd_idx in time_params and param_idx in time_params[cmd_idx]:
            return TIME_OFFSET
        elif cmd_idx in space_params and param_idx in space_params[cmd_idx]:
            return SPACE_OFFSET
        elif cmd_idx in amplitude_params and param_idx in amplitude_params[cmd_idx]:
            return AMPLITUDE_OFFSET
        elif cmd_idx in anchor_params and param_idx in anchor_params[cmd_idx]:
            return ANCHOR_OFFSET
        elif cmd_idx in animated_params and param_idx in animated_params[cmd_idx]:
            return ANIMATED_OFFSET
        elif cmd_idx in h_flag_params and param_idx in h_flag_params[cmd_idx]:
            return H_FLAG_OFFSET
        elif cmd_idx in offset_val_params and param_idx in offset_val_params[cmd_idx]:
            return OFFSET_VAL_OFFSET
        elif cmd_idx in ca_params and param_idx in ca_params[cmd_idx]:
            return CA_OFFSET
        elif cmd_idx in justify_params and param_idx in justify_params[cmd_idx]:
            return JUSTIFY_OFFSET
        elif cmd_idx in text_tracking_params and param_idx in text_tracking_params[cmd_idx]:
            return TEXT_TRACKING_OFFSET
        elif cmd_idx in has_stroke_color_params and param_idx in has_stroke_color_params[cmd_idx]:
            return HAS_STROKE_COLOR_OFFSET
        elif cmd_idx in ix_params and param_idx in ix_params[cmd_idx]:
            return IX_OFFSET
        elif cmd_idx in bm_params and param_idx in bm_params[cmd_idx]:
            return BM_OFFSET
        elif cmd_idx in closed_params and param_idx in closed_params[cmd_idx]:
            return CLOSED_OFFSET
        elif cmd_idx in direction_params and param_idx in direction_params[cmd_idx]:
            return DIRECTION_OFFSET
        elif cmd_idx in star_type_params and param_idx in star_type_params[cmd_idx]:
            return STAR_TYPE_OFFSET
        elif cmd_idx in multiple_params and param_idx in multiple_params[cmd_idx]:
            return MULTIPLE_OFFSET
        elif cmd_idx in composite_params and param_idx in composite_params[cmd_idx]:
            return COMPOSITE_OFFSET
        elif cmd_idx in skew_params and param_idx in skew_params[cmd_idx]:
            return SKEW_OFFSET
        elif cmd_idx in skew_axis_params and param_idx in skew_axis_params[cmd_idx]:
            return SKEW_AXIS_OFFSET
        elif cmd_idx in scale_params and param_idx in scale_params[cmd_idx]:
            return SCALE_OFFSET
        elif cmd_idx in rotation_params and param_idx in rotation_params[cmd_idx]:
            return ROTATION_OFFSET
        elif cmd_idx in ease_params and param_idx in ease_params[cmd_idx]:
            return EASE_OFFSET
        elif cmd_idx in smooth_params and param_idx in smooth_params[cmd_idx]:
            return SMOOTH_OFFSET
        elif cmd_idx in tracking_params and param_idx in tracking_params[cmd_idx]:
            return TRACKING_OFFSET
        elif cmd_idx in index_params and param_idx in index_params[cmd_idx]:
            return INDEX_OFFSET
        elif cmd_idx in ddd_params and param_idx in ddd_params[cmd_idx]:
            return DDD_OFFSET
        elif cmd_idx in hd_params and param_idx in hd_params[cmd_idx]:
            return HD_OFFSET
        elif cmd_idx in cp_params and param_idx in cp_params[cmd_idx]:
            return CP_OFFSET
        elif cmd_idx in has_mask_params and param_idx in has_mask_params[cmd_idx]:
            return HAS_MASK_OFFSET
        elif cmd_idx in ao_params and param_idx in ao_params[cmd_idx]:
            return AO_OFFSET
        elif cmd_idx in tt_params and param_idx in tt_params[cmd_idx]:
            return TT_OFFSET
        elif cmd_idx in tp_params and param_idx in tp_params[cmd_idx]:
            return TP_OFFSET
        elif cmd_idx in td_params and param_idx in td_params[cmd_idx]:
            return TD_OFFSET
        elif cmd_idx in ct_params and param_idx in ct_params[cmd_idx]:
            return CT_OFFSET
        elif cmd_idx in number_params and param_idx in number_params[cmd_idx]:
            return NUMBER_OFFSET
        elif cmd_idx in dim_params and param_idx in dim_params[cmd_idx]:
            return DIM_OFFSET
        elif cmd_idx in has_c_a_params and param_idx in has_c_a_params[cmd_idx]:
            return HAS_C_A_OFFSET
        elif cmd_idx in has_c_ix_params and param_idx in has_c_ix_params[cmd_idx]:
            return HAS_C_IX_OFFSET
        elif cmd_idx in has_o_a_params and param_idx in has_o_a_params[cmd_idx]:
            return HAS_O_A_OFFSET
        elif cmd_idx in has_o_ix_params and param_idx in has_o_ix_params[cmd_idx]:
            return HAS_O_IX_OFFSET
        elif cmd_idx in fill_rule_params and param_idx in fill_rule_params[cmd_idx]:
            return FILL_RULE_OFFSET
        elif cmd_idx in type_params and param_idx in type_params[cmd_idx]:
            return TYPE_OFFSET
        elif cmd_idx in text_range_units and param_idx in text_range_units[cmd_idx]:
            return TEXT_RANGE_UNITS_OFFSET
        elif cmd_idx in inv_params and param_idx in inv_params[cmd_idx]:
            return INV_OFFSET
        elif cmd_idx in mode_params and param_idx in mode_params[cmd_idx]:
            return MODE_OFFSET
        elif cmd_idx in text_shape_type and param_idx in text_shape_type[cmd_idx]:
            return TEXT_SHAPE_TYPE_OFFSET
        elif cmd_idx in text_random and param_idx in text_random[cmd_idx]:
            return TEXT_RANDOM_OFFSET
        elif cmd_idx in color_points_params and param_idx in color_points_params[cmd_idx]:
            return COLOR_POINTS_OFFSET
        elif cmd_idx in round_params and param_idx in round_params[cmd_idx]:
            return ROUND_OFFSET
        elif cmd_idx in radius_params and param_idx in radius_params[cmd_idx]:
            return RADIUS_OFFSET
        elif cmd_idx in frequency_params and param_idx in frequency_params[cmd_idx]:
            return FREQUENCY_OFFSET
        elif cmd_idx in speed_params and param_idx in speed_params[cmd_idx]:
            return SPEED_OFFSET
        elif cmd_idx in font_params and param_idx in font_params[cmd_idx]:
            return FONT_OFFSET
        elif cmd_idx in color_params and param_idx in color_params[cmd_idx]:
            return COLOR_OFFSET
        elif cmd_idx in line_cap_params and param_idx in line_cap_params[cmd_idx]:
            return LINE_CAP_OFFSET
        elif cmd_idx in line_join_params and param_idx in line_join_params[cmd_idx]:
            return LINE_JOIN_OFFSET
        elif cmd_idx in miter_limit_params and param_idx in miter_limit_params[cmd_idx]:
            return MITER_LIMIT_OFFSET
        elif cmd_idx in effect_params and param_idx in effect_params[cmd_idx]:
            return EFFECT_OFFSET
        elif cmd_idx in opacity_params and param_idx in opacity_params[cmd_idx]:
            return OPACITY_OFFSET
    
        else:
            return 0  # Default to no offset if not found
        
        LottieTensor._OFFSET_CACHE[cache_key] = offset
        return offset


    @staticmethod
    def get_command_param_indices(cmd_idx: int) -> List[int]:
        """
        Get the list of parameter indices for a command in their fixed order.
        Returns empty list for commands without parameters.
        """
        param_orders = {
            LottieTensor.CMD_ANIMATION: [
                LottieTensor.Index.Animation.FR,
                LottieTensor.Index.Animation.IP,
                LottieTensor.Index.Animation.OP,
                LottieTensor.Index.Animation.W,
                LottieTensor.Index.Animation.H,
                LottieTensor.Index.Animation.DDD
            ],
            LottieTensor.CMD_LAYER: [
                LottieTensor.Index.Layer.INDEX,
                LottieTensor.Index.Layer.IN_POINT,
                LottieTensor.Index.Layer.OUT_POINT,
                LottieTensor.Index.Layer.START_TIME,
                LottieTensor.Index.Layer.DDD,
                LottieTensor.Index.Layer.HD,
                LottieTensor.Index.Layer.CP,
                LottieTensor.Index.Layer.HAS_MASK,
                LottieTensor.Index.Layer.AO,
                LottieTensor.Index.Layer.TT,
                LottieTensor.Index.Layer.TP,
                LottieTensor.Index.Layer.TD,
                LottieTensor.Index.Layer.CT
            ],
            LottieTensor.CMD_NULL_LAYER: [
                LottieTensor.Index.NullLayer.INDEX,
                LottieTensor.Index.NullLayer.IN_POINT,
                LottieTensor.Index.NullLayer.OUT_POINT,
                LottieTensor.Index.NullLayer.START_TIME,
                LottieTensor.Index.NullLayer.CT,
                LottieTensor.Index.NullLayer.HD,
                LottieTensor.Index.NullLayer.HAS_MASK,
                LottieTensor.Index.NullLayer.AO,
                LottieTensor.Index.NullLayer.TT,
                LottieTensor.Index.NullLayer.TP,
                LottieTensor.Index.NullLayer.TD,
                LottieTensor.Index.NullLayer.CP
            ],
            LottieTensor.CMD_PRECOMP_LAYER: [
                LottieTensor.Index.PrecompLayer.INDEX,
                LottieTensor.Index.PrecompLayer.IN_POINT,
                LottieTensor.Index.PrecompLayer.OUT_POINT,
                LottieTensor.Index.PrecompLayer.START_TIME,
                LottieTensor.Index.PrecompLayer.W,
                LottieTensor.Index.PrecompLayer.H,
                LottieTensor.Index.PrecompLayer.CT,
                LottieTensor.Index.PrecompLayer.HAS_MASK,
                LottieTensor.Index.PrecompLayer.AO,
                LottieTensor.Index.PrecompLayer.TT,
                LottieTensor.Index.PrecompLayer.TP,
                LottieTensor.Index.PrecompLayer.TD,
                LottieTensor.Index.PrecompLayer.DDD,
                LottieTensor.Index.PrecompLayer.HD,
                LottieTensor.Index.PrecompLayer.CP
            ],
            LottieTensor.CMD_TEXT_LAYER: [
                LottieTensor.Index.TextLayer.INDEX,
                LottieTensor.Index.TextLayer.IN_POINT,
                LottieTensor.Index.TextLayer.OUT_POINT,
                LottieTensor.Index.TextLayer.START_TIME,
                LottieTensor.Index.TextLayer.HAS_MASK
            ],
            LottieTensor.CMD_SOLID_LAYER: [
                LottieTensor.Index.SolidLayer.INDEX,
                LottieTensor.Index.SolidLayer.IN_POINT,
                LottieTensor.Index.SolidLayer.OUT_POINT,
                LottieTensor.Index.SolidLayer.START_TIME,
                LottieTensor.Index.SolidLayer.WIDTH,
                LottieTensor.Index.SolidLayer.HEIGHT,
                LottieTensor.Index.SolidLayer.HAS_MASK,
                LottieTensor.Index.SolidLayer.COLOR_R,
                LottieTensor.Index.SolidLayer.COLOR_G,
                LottieTensor.Index.SolidLayer.COLOR_B,
                LottieTensor.Index.SolidLayer.COLOR_A
            ],
            LottieTensor.CMD_TRANSFORM: [],
            LottieTensor.CMD_POSITION: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X,
                LottieTensor.Index.Transform.Y,
                LottieTensor.Index.Transform.Z
            ],
            LottieTensor.CMD_POSITION_X: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_POSITION_Y: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_POSITION_Z: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_SCALE: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X,
                LottieTensor.Index.Transform.Y,
                LottieTensor.Index.Transform.Z
            ],
            LottieTensor.CMD_ROTATION: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_OPACITY: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X
            ],
            LottieTensor.CMD_ANCHOR: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X,
                LottieTensor.Index.Transform.Y,
                LottieTensor.Index.Transform.Z
            ],
            LottieTensor.CMD_KEYFRAME: [
                LottieTensor.Index.Keyframe.T,
                LottieTensor.Index.Keyframe.S1,
                LottieTensor.Index.Keyframe.S2,
                LottieTensor.Index.Keyframe.S3,
                LottieTensor.Index.Keyframe.I_X,
                LottieTensor.Index.Keyframe.I_Y,
                LottieTensor.Index.Keyframe.O_X,
                LottieTensor.Index.Keyframe.O_Y,
                LottieTensor.Index.Keyframe.TO1,
                LottieTensor.Index.Keyframe.TO2,
                LottieTensor.Index.Keyframe.TO3,
                LottieTensor.Index.Keyframe.TI1,
                LottieTensor.Index.Keyframe.TI2,
                LottieTensor.Index.Keyframe.TI3,
                LottieTensor.Index.Keyframe.I_X2,
                LottieTensor.Index.Keyframe.I_X3,
                LottieTensor.Index.Keyframe.I_Y2,
                LottieTensor.Index.Keyframe.I_Y3,
                LottieTensor.Index.Keyframe.O_X2,
                LottieTensor.Index.Keyframe.O_X3,
                LottieTensor.Index.Keyframe.O_Y2,
                LottieTensor.Index.Keyframe.O_Y3,
                LottieTensor.Index.Keyframe.H_FLAG,
                LottieTensor.Index.Keyframe.E1,
                LottieTensor.Index.Keyframe.E2,
                LottieTensor.Index.Keyframe.E3
            ],
            LottieTensor.CMD_GROUP: [
                LottieTensor.Index.Group.IX,
                LottieTensor.Index.Group.CIX,
                LottieTensor.Index.Group.BM,
                LottieTensor.Index.Group.HD,
                LottieTensor.Index.Group.NP
            ],
            LottieTensor.CMD_PATH: [
                LottieTensor.Index.Path.IX,
                LottieTensor.Index.Path.IND,
                LottieTensor.Index.Path.KS_IX,
                LottieTensor.Index.Path.CLOSED,
                LottieTensor.Index.Path.HD,
                LottieTensor.Index.Path.ANIMATED
            ],
            LottieTensor.CMD_POINT: [
                LottieTensor.Index.Point.X,
                LottieTensor.Index.Point.Y,
                LottieTensor.Index.Point.IN_X,
                LottieTensor.Index.Point.IN_Y,
                LottieTensor.Index.Point.OUT_X,
                LottieTensor.Index.Point.OUT_Y
            ],
            LottieTensor.CMD_FILL: [
                LottieTensor.Index.Fill.R,
                LottieTensor.Index.Fill.G,
                LottieTensor.Index.Fill.B,
                LottieTensor.Index.Fill.COLOR_DIM,
                LottieTensor.Index.Fill.HAS_C_A,
                LottieTensor.Index.Fill.HAS_C_IX,
                LottieTensor.Index.Fill.C_IX,
                LottieTensor.Index.Fill.BM,
                LottieTensor.Index.Fill.FILL_RULE,
                LottieTensor.Index.Fill.OPACITY,
                LottieTensor.Index.Fill.COLOR_ANIMATED,
                LottieTensor.Index.Fill.OPACITY_ANIMATED,
                LottieTensor.Index.Fill.HAS_O_A,
                LottieTensor.Index.Fill.HAS_O_IX,
                LottieTensor.Index.Fill.O_IX
            ],
            LottieTensor.CMD_STROKE: [
                LottieTensor.Index.Stroke.R,
                LottieTensor.Index.Stroke.G,
                LottieTensor.Index.Stroke.B,
                LottieTensor.Index.Stroke.COLOR_DIM,
                LottieTensor.Index.Stroke.HAS_C_A,
                LottieTensor.Index.Stroke.HAS_C_IX,
                LottieTensor.Index.Stroke.C_IX,
                LottieTensor.Index.Stroke.BM,
                LottieTensor.Index.Stroke.LC,
                LottieTensor.Index.Stroke.LJ,
                LottieTensor.Index.Stroke.ML,
                LottieTensor.Index.Stroke.WIDTH_ANIMATED,
                LottieTensor.Index.Stroke.COLOR_ANIMATED,
                LottieTensor.Index.Stroke.A
            ],
            LottieTensor.CMD_TRANSFORM_SHAPE: [
                LottieTensor.Index.TransformShape.POSITION_X,
                LottieTensor.Index.TransformShape.POSITION_Y,
                LottieTensor.Index.TransformShape.SCALE_X,
                LottieTensor.Index.TransformShape.SCALE_Y,
                LottieTensor.Index.TransformShape.ROTATION,
                LottieTensor.Index.TransformShape.OPACITY,
                LottieTensor.Index.TransformShape.ANCHOR_X,
                LottieTensor.Index.TransformShape.ANCHOR_Y,
                LottieTensor.Index.TransformShape.SKEW,
                LottieTensor.Index.TransformShape.SKEW_AXIS,
                LottieTensor.Index.TransformShape.HD
            ],
            LottieTensor.CMD_RECT: [
                LottieTensor.Index.Rect.HD,
                LottieTensor.Index.Rect.D
            ],
            LottieTensor.CMD_ELLIPSE: [],
            LottieTensor.CMD_BEZIER: [
                LottieTensor.Index.Bezier.CLOSED
            ],
            LottieTensor.CMD_SIZE: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X,    # 修改：从 TwoValues.VALUE1 改为 Transform.X
                LottieTensor.Index.Transform.Y     # 修改：从 TwoValues.VALUE2 改为 Transform.Y
            ],
            LottieTensor.CMD_RECT_SIZE: [
                LottieTensor.Index.Transform.ANIMATED, 
                LottieTensor.Index.Transform.X,    # 修改
                LottieTensor.Index.Transform.Y     # 修改
            ],
            LottieTensor.CMD_ELLIPSE_SIZE: [
                LottieTensor.Index.Transform.ANIMATED,
                LottieTensor.Index.Transform.X,    # 修改
                LottieTensor.Index.Transform.Y     # 修改
            ],

            LottieTensor.CMD_ROUNDED: [
                LottieTensor.Index.SingleValue.VALUE,
                LottieTensor.Index.SingleValue.IX
            ],
            LottieTensor.CMD_RECT_ROUNDED: [
                LottieTensor.Index.SingleValue.ANIMATED,
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TRIM: [
                LottieTensor.Index.Trim.IX
            ],
            LottieTensor.CMD_START: [
                LottieTensor.Index.SingleValue.ANIMATED,
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_END: [
                LottieTensor.Index.SingleValue.ANIMATED,
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_OFFSET: [
                LottieTensor.Index.SingleValue.ANIMATED,
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_PARENT: [
                LottieTensor.Index.Parent.PARENT_INDEX
            ],
            LottieTensor.CMD_REFERENCE_ID: list(range(11)),  # 11 tokens
            LottieTensor.CMD_DIMENSIONS: [
                LottieTensor.Index.Dimensions.WIDTH,
                LottieTensor.Index.Dimensions.HEIGHT
            ],
            LottieTensor.CMD_ASSET: list(range(12)),  # FR + 10 tokens + count
            LottieTensor.CMD_TEXT_KEYFRAME: list(range(47)),  # All text keyframe params
            LottieTensor.CMD_FONT: list(range(23)),  # All font params
            LottieTensor.CMD_CHAR: list(range(35)),  # All char params
            LottieTensor.CMD_WIDTH_KEYFRAME: [
                LottieTensor.Index.WidthKeyframe.T,
                LottieTensor.Index.WidthKeyframe.S,
                LottieTensor.Index.WidthKeyframe.I_X,
                LottieTensor.Index.WidthKeyframe.I_Y,
                LottieTensor.Index.WidthKeyframe.O_X,
                LottieTensor.Index.WidthKeyframe.O_Y
            ],
            LottieTensor.CMD_COLOR_KEYFRAME: [
                LottieTensor.Index.Keyframe.T,
                LottieTensor.Index.Keyframe.S1,
                LottieTensor.Index.Keyframe.S2,
                LottieTensor.Index.Keyframe.S3,
                LottieTensor.Index.Keyframe.E1,
                LottieTensor.Index.Keyframe.I_X,
                LottieTensor.Index.Keyframe.I_Y,
                LottieTensor.Index.Keyframe.O_X,
                LottieTensor.Index.Keyframe.O_Y
            ],
            LottieTensor.CMD_OPACITY_KEYFRAME: [
                LottieTensor.Index.Keyframe.T,
                LottieTensor.Index.Keyframe.S1,
                LottieTensor.Index.Keyframe.I_X,
                LottieTensor.Index.Keyframe.I_Y,
                LottieTensor.Index.Keyframe.O_X,
                LottieTensor.Index.Keyframe.O_Y
            ],
            LottieTensor.CMD_OPACITY_ANIMATED: [],
            LottieTensor.CMD_TM: [
                LottieTensor.Index.Tm.A
            ],
            LottieTensor.CMD_VALUE: [
                LottieTensor.Index.Value.VALUE
            ],
            LottieTensor.CMD_SKEW: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_SKEW_AXIS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_STAR: [
                LottieTensor.Index.Star.D,
                LottieTensor.Index.Star.SY
            ],
            LottieTensor.CMD_INNER_RADIUS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_OUTER_RADIUS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_INNER_ROUNDNESS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_OUTER_ROUNDNESS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_POINTS_STAR: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_STAR_ROTATION: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_MULTIPLE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_REPEATER: [
                LottieTensor.Index.Repeater.IX
            ],
            LottieTensor.CMD_COPIES: [
                LottieTensor.Index.SingleValue.VALUE,
                LottieTensor.Index.SingleValue.IX
            ],
            LottieTensor.CMD_REPEATER_OFFSET: [
                LottieTensor.Index.SingleValue.VALUE,
                LottieTensor.Index.SingleValue.IX
            ],
            LottieTensor.CMD_COMPOSITE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_REPEATER_TRANSFORM: [],
            LottieTensor.CMD_TR_P_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_A_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_SCALE: [
                LottieTensor.Index.TwoValues.VALUE1,
                LottieTensor.Index.TwoValues.VALUE2
            ],
            LottieTensor.CMD_TR_S_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_R_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_SO_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_TR_EO_IX: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_MORE_OPTIONS: [
                LottieTensor.Index.MoreOptions.G,
                LottieTensor.Index.MoreOptions.ALIGNMENT_A,
                LottieTensor.Index.MoreOptions.ALIGNMENT_K1,
                LottieTensor.Index.MoreOptions.ALIGNMENT_K2,
                LottieTensor.Index.MoreOptions.ALIGNMENT_IX
            ],
            LottieTensor.CMD_GRADIENT_FILL: [],
            LottieTensor.CMD_START_POINT: [
                LottieTensor.Index.TwoValues.VALUE1,
                LottieTensor.Index.TwoValues.VALUE2
            ],
            LottieTensor.CMD_END_POINT: [
                LottieTensor.Index.TwoValues.VALUE1,
                LottieTensor.Index.TwoValues.VALUE2
            ],
            LottieTensor.CMD_GRADIENT_TYPE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_HIGHLIGHT_LENGTH: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_HIGHLIGHT_ANGLE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_ORIGINAL_COLORS: list(range(48)),  # All color values + count
            LottieTensor.CMD_COLOR_POINTS: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_GRADIENT_STROKE: [],
            LottieTensor.CMD_WIDTH: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_LINE_CAP: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_LINE_JOIN: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_MITER_LIMIT: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_ML2: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_COLOR: [
                LottieTensor.Index.Color.INDEX,
                LottieTensor.Index.Color.R,
                LottieTensor.Index.Color.G,
                LottieTensor.Index.Color.B
            ],
            LottieTensor.CMD_EFFECT: [
                LottieTensor.Index.Effect.TYPE,
                LottieTensor.Index.Effect.INDEX,
                LottieTensor.Index.Effect.NP,
                LottieTensor.Index.Effect.ENABLED
            ],
            LottieTensor.CMD_LAYER_EFFECT: [
                LottieTensor.Index.LayerEffect.INDEX,
                LottieTensor.Index.LayerEffect.VALUE
            ],
            LottieTensor.CMD_DROPDOWN: [
                LottieTensor.Index.Dropdown.INDEX,
                LottieTensor.Index.Dropdown.VALUE
            ],
            LottieTensor.CMD_NO_VALUE: [
                LottieTensor.Index.NO_VALUE.INDEX,
                LottieTensor.Index.NO_VALUE.VALUE
            ],
            LottieTensor.CMD_IGNORED: [
                LottieTensor.Index.Ignored.INDEX,
                LottieTensor.Index.Ignored.VALUE
            ],
            LottieTensor.CMD_SLIDER: [
                LottieTensor.Index.Slider.INDEX,
                LottieTensor.Index.Slider.VALUE
            ],
            LottieTensor.CMD_FILL_RULE: [
                LottieTensor.Index.SingleValue.VALUE
            ],
            LottieTensor.CMD_MERGE: [],
            LottieTensor.CMD_MERGE_MODE: [
                LottieTensor.Index.MergeMode.MODE
            ],
            LottieTensor.CMD_MASKS_PROPERTIES: [],
            LottieTensor.CMD_MASK: [
                LottieTensor.Index.Mask.INDEX,
                LottieTensor.Index.Mask.INV,
                LottieTensor.Index.Mask.MODE
            ],
            LottieTensor.CMD_MASK_PT: [
                LottieTensor.Index.MaskPt.A,
                LottieTensor.Index.MaskPt.IX
            ],
            LottieTensor.CMD_MASK_PT_K: [],
            LottieTensor.CMD_MASK_PT_K_C: [
                LottieTensor.Index.MaskPtK.C
            ],
            LottieTensor.CMD_MASK_PT_K_I: list(range(21)),  # V1-V20 + COUNT
            LottieTensor.CMD_MASK_PT_K_O: list(range(21)),
            LottieTensor.CMD_MASK_PT_K_V: list(range(21)),
            LottieTensor.CMD_MASK_O: [
                LottieTensor.Index.MaskO.A,
                LottieTensor.Index.MaskO.K,
                LottieTensor.Index.MaskO.IX
            ],
            LottieTensor.CMD_MASK_X: [
                LottieTensor.Index.MaskX.A,
                LottieTensor.Index.MaskX.K,
                LottieTensor.Index.MaskX.IX
            ],
            LottieTensor.CMD_MASK_PT_K_ARRAY: [],
            LottieTensor.CMD_MASK_PT_KEYFRAME: [
                LottieTensor.Index.MaskPtKeyframe.INDEX,
                LottieTensor.Index.MaskPtKeyframe.T
            ],
            LottieTensor.CMD_MASK_PT_KF_I: [
                LottieTensor.Index.MaskPtKfI.X,
                LottieTensor.Index.MaskPtKfI.Y
            ],
            LottieTensor.CMD_MASK_PT_KF_O: [
                LottieTensor.Index.MaskPtKfO.X,
                LottieTensor.Index.MaskPtKfO.Y
            ],
            LottieTensor.CMD_MASK_PT_KF_S: [],
            LottieTensor.CMD_MASK_PT_KF_SHAPE: [
                LottieTensor.Index.MaskPtKfShape.INDEX,
                LottieTensor.Index.MaskPtKfShape.C
            ],
            LottieTensor.CMD_MASK_PT_KF_SHAPE_I: list(range(21)),
            LottieTensor.CMD_MASK_PT_KF_SHAPE_O: list(range(21)),
            LottieTensor.CMD_MASK_PT_KF_SHAPE_V: list(range(21)),
            LottieTensor.CMD_TR_POSITION: [
                LottieTensor.Index.TrPosition.X,
                LottieTensor.Index.TrPosition.Y
            ],
            LottieTensor.CMD_TR_ANCHOR: [
                LottieTensor.Index.TrAnchor.X,
                LottieTensor.Index.TrAnchor.Y
            ],
            LottieTensor.CMD_TR_ROTATION: [
                LottieTensor.Index.TrRotation.VALUE
            ],
            LottieTensor.CMD_TR_START_OPACITY: [
                LottieTensor.Index.TrStartOpacity.VALUE
            ],
            LottieTensor.CMD_TR_END_OPACITY: [
                LottieTensor.Index.TrEndOpacity.VALUE
            ],
            LottieTensor.CMD_ZIG_ZAG: [
                LottieTensor.Index.ZigZag.IX
            ],
            LottieTensor.CMD_FREQUENCY: [
                LottieTensor.Index.Frequency.VALUE
            ],
            LottieTensor.CMD_AMPLITUDE: [
                LottieTensor.Index.Amplitude.VALUE
            ],
            LottieTensor.CMD_POINT_TYPE: [
                LottieTensor.Index.PointType.VALUE
            ],
            LottieTensor.CMD_ANIMATORS: [],
            LottieTensor.CMD_ANIMATOR: [],
            LottieTensor.CMD_RANGE_SELECTOR: [
                LottieTensor.Index.RangeSelector.T,
                LottieTensor.Index.RangeSelector.R,
                LottieTensor.Index.RangeSelector.B,
                LottieTensor.Index.RangeSelector.SH,
                LottieTensor.Index.RangeSelector.RN
            ],
            LottieTensor.CMD_RANGE_START: [
                LottieTensor.Index.RangeStart.A
            ],
            LottieTensor.CMD_RANGE_START_KEYFRAME: [
                LottieTensor.Index.RangeStartKeyframe.T,
                LottieTensor.Index.RangeStartKeyframe.S,
                LottieTensor.Index.RangeStartKeyframe.I_X,
                LottieTensor.Index.RangeStartKeyframe.I_Y,
                LottieTensor.Index.RangeStartKeyframe.O_X,
                LottieTensor.Index.RangeStartKeyframe.O_Y
            ],
            LottieTensor.CMD_AMOUNT: [
                LottieTensor.Index.Amount.A,
                LottieTensor.Index.Amount.K,
                LottieTensor.Index.Amount.IX
            ],
            LottieTensor.CMD_MAX_EASE: [
                LottieTensor.Index.MaxEase.A,
                LottieTensor.Index.MaxEase.K,
                LottieTensor.Index.MaxEase.IX
            ],
            LottieTensor.CMD_MIN_EASE: [
                LottieTensor.Index.MinEase.A,
                LottieTensor.Index.MinEase.K,
                LottieTensor.Index.MinEase.IX
            ],
            LottieTensor.CMD_ANIMATOR_PROPERTIES: [],
            LottieTensor.CMD_RADIUS: [
                LottieTensor.Index.Radius.VALUE
            ],
            LottieTensor.CMD_RANGE_END: [
                LottieTensor.Index.RangeEnd.A
            ],
            LottieTensor.CMD_RANGE_END_KEYFRAME: [
                LottieTensor.Index.RangeEndKeyframe.T,
                LottieTensor.Index.RangeEndKeyframe.S,
                LottieTensor.Index.RangeEndKeyframe.I_X,
                LottieTensor.Index.RangeEndKeyframe.I_Y,
                LottieTensor.Index.RangeEndKeyframe.O_X,
                LottieTensor.Index.RangeEndKeyframe.O_Y
            ],
            LottieTensor.CMD_RANGE_OFFSET: [
                LottieTensor.Index.Amount.A,
                LottieTensor.Index.Amount.K,
                LottieTensor.Index.Amount.IX
            ],
            LottieTensor.CMD_RANGE_OFFSET_KEYFRAME: [
                LottieTensor.Index.RangeOffsetKeyframe.T,
                LottieTensor.Index.RangeOffsetKeyframe.S,
                LottieTensor.Index.RangeOffsetKeyframe.I_X,
                LottieTensor.Index.RangeOffsetKeyframe.I_Y,
                LottieTensor.Index.RangeOffsetKeyframe.O_X,
                LottieTensor.Index.RangeOffsetKeyframe.O_Y
            ],
            LottieTensor.CMD_S_M: [
                LottieTensor.Index.SM.A,
                LottieTensor.Index.SM.K,
                LottieTensor.Index.SM.IX
            ],
            LottieTensor.CMD_OPACITY_ANIMATORS: [
                LottieTensor.Index.OpacityAnimators.A,
                LottieTensor.Index.OpacityAnimators.K,
                LottieTensor.Index.OpacityAnimators.IX
            ],
            LottieTensor.CMD_SCALE_ANIMATORS: [
                LottieTensor.Index.ScaleAnimators.A,
                LottieTensor.Index.ScaleAnimators.K_X,
                LottieTensor.Index.ScaleAnimators.K_Y,
                LottieTensor.Index.ScaleAnimators.K_Z,
                LottieTensor.Index.ScaleAnimators.IX
            ],
            LottieTensor.CMD_ROTATION_ANIMATORS: [
                LottieTensor.Index.RotationAnimators.A,
                LottieTensor.Index.RotationAnimators.K,
                LottieTensor.Index.RotationAnimators.IX
            ],
            LottieTensor.CMD_POSITION_ANIMATORS: [
                LottieTensor.Index.PositionAnimators.A,
                LottieTensor.Index.PositionAnimators.K_X,
                LottieTensor.Index.PositionAnimators.K_Y,
                LottieTensor.Index.PositionAnimators.K_Z,
                LottieTensor.Index.PositionAnimators.IX
            ],
            LottieTensor.CMD_TRACKING_ANIMATORS: [
                LottieTensor.Index.TrackingAnimators.A,
                LottieTensor.Index.TrackingAnimators.K,
                LottieTensor.Index.TrackingAnimators.IX
            ],
            LottieTensor.CMD_DASHES: [],
            LottieTensor.CMD_DASH: [
                LottieTensor.Index.Dash.TYPE,
                LottieTensor.Index.Dash.LENGTH,
                LottieTensor.Index.Dash.V_IX
            ],
            LottieTensor.CMD_DASH_ANIMATED: [
                LottieTensor.Index.DashAnimated.TYPE,
                LottieTensor.Index.DashAnimated.V_IX
            ],
            LottieTensor.CMD_DASH_KEYFRAME: [
                LottieTensor.Index.DashKeyframe.T,
                LottieTensor.Index.DashKeyframe.S,
                LottieTensor.Index.DashKeyframe.I_X,
                LottieTensor.Index.DashKeyframe.I_Y,
                LottieTensor.Index.DashKeyframe.O_X,
                LottieTensor.Index.DashKeyframe.O_Y
            ],
            LottieTensor.CMD_DASH_OFFSET: [
                LottieTensor.Index.DashOffset.O
            ],
            LottieTensor.CMD_WIDTH_ANIMATED: [],
            # All end commands have empty param lists
            LottieTensor.CMD_POSITION_END: [],
            LottieTensor.CMD_SCALE_END: [],
            LottieTensor.CMD_ROTATION_END: [],
            LottieTensor.CMD_OPACITY_END: [],
            LottieTensor.CMD_ANCHOR_END: [],
            LottieTensor.CMD_GROUP_END: [],
            LottieTensor.CMD_TRANSFORM_END: [],
            LottieTensor.CMD_LAYER_END: [],
            LottieTensor.CMD_PATH_END: [],
            LottieTensor.CMD_RECT_END: [],
            LottieTensor.CMD_ELLIPSE_END: [],
            LottieTensor.CMD_STAR_END: [],
            LottieTensor.CMD_TRIM_END: [],
            LottieTensor.CMD_REPEATER_END: [],
            LottieTensor.CMD_REPEATER_TRANSFORM_END: [],
            LottieTensor.CMD_GRADIENT_FILL_END: [],
            LottieTensor.CMD_GRADIENT_STROKE_END: [],
            LottieTensor.CMD_MERGE_END: [],
            LottieTensor.CMD_ROUNDED_CORNERS_END: [],
            LottieTensor.CMD_TWIST_END: [],
            LottieTensor.CMD_BEZIER_END: [],
            LottieTensor.CMD_TEXT_LAYER_END: [],
            LottieTensor.CMD_TEXT_DATA_END: [],
            LottieTensor.CMD_SOLID_LAYER_END: [],
            LottieTensor.CMD_NULL_LAYER_END: [],
            LottieTensor.CMD_PRECOMP_LAYER_END: [],
            LottieTensor.CMD_POSITION_X_END: [],
            LottieTensor.CMD_POSITION_Y_END: [],
            LottieTensor.CMD_POSITION_Z_END: [],
            LottieTensor.CMD_SCALE_X_END: [],
            LottieTensor.CMD_SCALE_Y_END: [],
            LottieTensor.CMD_SCALE_Z_END: [],
            LottieTensor.CMD_ROTATION_X_END: [],
            LottieTensor.CMD_ROTATION_Y_END: [],
            LottieTensor.CMD_ROTATION_Z_END: [],
            LottieTensor.CMD_EFFECTS_END: [],
            LottieTensor.CMD_EFFECT_END: [],
            LottieTensor.CMD_KEYFRAME_END: [],
            LottieTensor.CMD_WIDTH_ANIMATED_END: [],
            LottieTensor.CMD_FONTS_END: [],
            LottieTensor.CMD_CHARS_END: [],
            LottieTensor.CMD_CHAR_END: [],
            LottieTensor.CMD_CHAR_SHAPES_END: [],
            LottieTensor.CMD_TEXT_KEYFRAMES_END: [],
            LottieTensor.CMD_TEXT_DOC_END: [],
            LottieTensor.CMD_MORE_OPTIONS_END: [],
            LottieTensor.CMD_OPACITY_ANIMATED_END: [],
            LottieTensor.CMD_MASKS_PROPERTIES_END: [],
            LottieTensor.CMD_MASK_END: [],
            LottieTensor.CMD_MASK_PT_END: [],
            LottieTensor.CMD_MASK_PT_K_END: [],
            LottieTensor.CMD_TM_END: [],
            LottieTensor.CMD_MASK_PT_K_ARRAY_END: [],
            LottieTensor.CMD_MASK_PT_KEYFRAME_END: [],
            LottieTensor.CMD_MASK_PT_KF_S_END: [],
            LottieTensor.CMD_MASK_PT_KF_SHAPE_END: [],
            LottieTensor.CMD_VALUE_END: [],
            LottieTensor.CMD_ZIG_ZAG_END: [],
            LottieTensor.CMD_ANIMATORS_END: [],
            LottieTensor.CMD_ANIMATOR_END: [],
            LottieTensor.CMD_RANGE_SELECTOR_END: [],
            LottieTensor.CMD_RANGE_START_END: [],
            LottieTensor.CMD_RANGE_END_END: [],
            LottieTensor.CMD_END_END: [],
            LottieTensor.CMD_START_END: [],
            LottieTensor.CMD_OFFSET_END: [],
            LottieTensor.CMD_RANGE_OFFSET_END: [],
            LottieTensor.CMD_SCALE_ANIMATORS_END: [],
            LottieTensor.CMD_ROTATION_ANIMATORS_END: [],
            LottieTensor.CMD_POSITION_ANIMATORS_END: [],
            LottieTensor.CMD_OPACITY_ANIMATORS_END: [],
            LottieTensor.CMD_COLOR_ANIMATED_END: [],
            LottieTensor.CMD_DASHES_END: [],
            LottieTensor.CMD_DASH_ANIMATED_END: [],
            LottieTensor.CMD_SIZE_END: [],
            LottieTensor.CMD_RECT_ROUNDED_END: [],
            LottieTensor.CMD_ANIMATOR_PROPERTIES_END: [],
            LottieTensor.CMD_ASSET_END: [],
            LottieTensor.CMD_EFFECTS: [],
            LottieTensor.CMD_FONTS: [],
            LottieTensor.CMD_CHARS: [],
            LottieTensor.CMD_CHAR_SHAPES: [],
            LottieTensor.CMD_TEXT_KEYFRAMES: [],
            LottieTensor.CMD_TEXT_DATA: [],
            LottieTensor.CMD_DOCUMENT: [],
            LottieTensor.CMD_TEXT_DOC: [],
        }
        
        # Commands without parameters
        empty_param_cmds = {k for k, v in param_orders.items() if not v}
        
        return param_orders.get(cmd_idx, [])


    @staticmethod
    def get_vocab_range_for_offset(offset: int) -> tuple:
        """Get the vocabulary range (start, end) for a given offset."""
        vocab_ranges = {
            0: (1, 151643),               # NO_OFFSET (tokenizer tokens)
            155000: (153000, 157000),     # TIME_OFFSET: -2000 to 2000
            159100: (157100, 161100),     # SPACE_OFFSET: -2000 to 2000
            161200: (161200, 161220),     # AMPLITUDE_OFFSET: 0 to 20
            161300: (161300, 165300),     # ANCHOR_OFFSET: -2000 to 2000
            165400: (165400, 165401),     # ANIMATED_OFFSET: 0 to 1
            165402: (165402, 165403),     # H_FLAG_OFFSET: 0 to 1
            165404: (165404, 165405),     # OFFSET_VAL_OFFSET: 0 to 1
            165406: (165406, 165408),     # CA_OFFSET: 0 to 2
            165409: (165409, 165415),     # JUSTIFY_OFFSET: 0 to 6
            165416: (165416, 166016),     # TEXT_TRACKING_OFFSET: -100 to 500
            166017: (166017, 166018),     # HAS_STROKE_COLOR_OFFSET: 0 to 1
            166019: (166019, 167019),     # IX_OFFSET: 0 to 1000
            167020: (167020, 167040),     # BM_OFFSET: 0 to 20
            167041: (167041, 167042),     # CLOSED_OFFSET: 0 to 1
            167043: (167043, 167048),     # DIRECTION_OFFSET: 0 to 5
            167049: (167049, 167054),     # STAR_TYPE_OFFSET: 0 to 5
            167055: (167055, 167060),     # MULTIPLE_OFFSET: 0 to 5
            167061: (167061, 167066),     # COMPOSITE_OFFSET: 0 to 5
            167067: (167067, 167117),     # SKEW_OFFSET: -25 to 25
            167118: (167118, 167168),     # SKEW_AXIS_OFFSET: -25 to 25
            167169: (167169, 170169),     # SCALE_OFFSET: -1000 to 2000
            170170: (170170, 171610),     # ROTATION_OFFSET: -720 to 720
            171611: (171611, 171811),     # EASE_OFFSET: -100 to 100
            171812: (171812, 171912),     # SMOOTH_OFFSET: 0 to 100
            171913: (171913, 172013),     # TRACKING_OFFSET: -50 to 50
            172014: (172014, 173014),     # INDEX_OFFSET: 0 to 1000
            173015: (173015, 173016),     # DDD_OFFSET: 0 to 1
            173017: (173017, 173018),     # HD_OFFSET: 0 to 1
            173019: (173019, 173069),     # CP_OFFSET: 0 to 50
            173070: (173070, 173071),     # HAS_MASK_OFFSET: 0 to 1
            173072: (173072, 173073),     # AO_OFFSET: 0 to 1
            173074: (173074, 173079),     # TT_OFFSET: 0 to 5
            173080: (173080, 173180),     # TP_OFFSET: 0 to 100
            173181: (173181, 173183),     # TD_OFFSET: 0 to 2
            173184: (173184, 173185),     # CT_OFFSET: 0 to 1
            173186: (173186, 173686),     # NUMBER_OFFSET: 0 to 500
            173687: (173687, 173697),     # DIM_OFFSET: 0 to 10
            173698: (173698, 173699),     # HAS_C_A_OFFSET: 0 to 1
            173700: (173700, 173701),     # HAS_C_IX_OFFSET: 0 to 1
            173702: (173702, 173703),     # HAS_O_A_OFFSET: 0 to 1
            173704: (173704, 173705),     # HAS_O_IX_OFFSET: 0 to 1
            173706: (173706, 173710),     # FILL_RULE_OFFSET: 0 to 4
            173711: (173711, 173751),     # TYPE_OFFSET: 0 to 40
            173752: (173752, 173762),     # TEXT_RANGE_UNITS_OFFSET: 0 to 10
            173763: (173763, 173764),     # INV_OFFSET: 0 to 1
            173765: (173765, 173775),     # MODE_OFFSET: 0 to 10
            173776: (173776, 173786),     # TEXT_SHAPE_TYPE_OFFSET: 0 to 10
            173787: (173787, 173788),     # TEXT_RANDOM_OFFSET: 0 to 1
            173789: (173789, 173839),     # COLOR_POINTS_OFFSET: 0 to 50
            173840: (173840, 174940),     # ROUND_OFFSET: -100 to 1000
            174941: (174941, 175241),     # RADIUS_OFFSET: 0 to 300
            175242: (175242, 175392),     # FREQUENCY_OFFSET: 0 to 150
            175393: (175393, 177393),     # SPEED_OFFSET: -1000 to 1000
            177394: (177394, 179494),     # FONT_OFFSET: -100 to 2000
            179495: (179495, 179750),     # COLOR_OFFSET: 0 to 255
            179752: (179752, 179754),     # LINE_CAP_OFFSET: 1 to 3
            179757: (179757, 179759),     # LINE_JOIN_OFFSET: 1 to 3
            179760: (179760, 179860),     # MITER_LIMIT_OFFSET: 0 to 100
            179861: (179861, 181111),     # EFFECT_OFFSET: -250 to 1000
            181112: (181112, 181212),     # OPACITY_OFFSET: 0 to 100
            181300: (181300, 191300),     # WIDTH_VALUE_OFFSET: 0 to 10000 (新增)
        }
        return vocab_ranges.get(offset, (0, 0))



    @staticmethod
    def _find_nearest_layer_end(flattened: List[int], max_length: int, command_offset: int) -> int:
        """
        在flattened list中查找最接近max_length的layer end位置

        智能截断规则：
        1. 从max_length位置向前搜索，找最近的layer end
        2. 必须确保至少有ANIMATION命令和一个完整的layer
        3. layer end包括: LAYER_END, PRECOMP_LAYER_END, TEXT_LAYER_END, NULL_LAYER_END, SOLID_LAYER_END
        4. 如果找不到合适的位置，返回-1（表示放弃样本）

        Args:
            flattened: 扁平化的token列表
            max_length: 目标最大长度
            command_offset: 命令token的offset (151936)

        Returns:
            最近的layer end位置（截断到这里），如果找不到返回-1
        """
        # Layer end命令集合
        LAYER_END_CMDS = {
            LottieTensor.CMD_LAYER_END,           # 27
            LottieTensor.CMD_PRECOMP_LAYER_END,   # 46
            LottieTensor.CMD_TEXT_LAYER_END,      # 90
            LottieTensor.CMD_NULL_LAYER_END,      # 44
            LottieTensor.CMD_SOLID_LAYER_END,     # 95
        }

        # 向前搜索范围：从max_length向前最多搜索2000个token
        # 2000个token大约能包含1-2个完整的layer
        search_start = max(0, max_length - 2000)

        best_pos = -1

        # 从max_length位置向前搜索
        for i in range(min(max_length - 1, len(flattened) - 1), search_start - 1, -1):
            token = flattened[i]

            # 检查是否是命令token
            if token >= command_offset and token < command_offset + len(LottieTensor.COMMANDS):
                cmd_idx = token - command_offset

                if cmd_idx in LAYER_END_CMDS:
                    # 找到layer end，截断点是这个token之后
                    candidate_pos = i + 1

                    # 验证截断后的序列是否完整（必须有ANIMATION和至少一个layer）
                    if LottieTensor._validate_truncated_sequence(flattened[:candidate_pos], command_offset):
                        best_pos = candidate_pos
                        break

        return best_pos

    @staticmethod
    def _validate_truncated_sequence(flattened: List[int], command_offset: int) -> bool:
        """
        验证截断后的序列是否完整有效

        要求：
        1. 必须有ANIMATION命令
        2. 必须至少有一个完整的layer（有layer start和layer end配对）
        3. layers不能为空
        4. 【新增】必须有主layers（不能只有assets中的layers）

        Args:
            flattened: 截断后的token列表
            command_offset: 命令token的offset

        Returns:
            是否是有效的序列
        """
        has_animation = False
        layer_count = 0
        asset_depth = 0  # 跟踪是否在asset内部
        main_layer_count = 0  # 主layers计数（不在asset内的layer）

        # Layer start和end命令
        LAYER_START_CMDS = {
            LottieTensor.CMD_LAYER,         # 26 - ShapeLayer
            LottieTensor.CMD_PRECOMP_LAYER, # 45
            LottieTensor.CMD_TEXT_LAYER,    # 89
            LottieTensor.CMD_NULL_LAYER,    # 43
            LottieTensor.CMD_SOLID_LAYER,   # 94
        }

        LAYER_END_CMDS = {
            LottieTensor.CMD_LAYER_END,
            LottieTensor.CMD_PRECOMP_LAYER_END,
            LottieTensor.CMD_TEXT_LAYER_END,
            LottieTensor.CMD_NULL_LAYER_END,
            LottieTensor.CMD_SOLID_LAYER_END,
        }

        layer_stack = 0  # 跟踪layer的嵌套深度

        for token in flattened:
            if token >= command_offset and token < command_offset + len(LottieTensor.COMMANDS):
                cmd_idx = token - command_offset

                if cmd_idx == LottieTensor.CMD_ANIMATION:
                    has_animation = True
                elif cmd_idx == LottieTensor.CMD_ASSET:  # 进入asset
                    asset_depth += 1
                elif cmd_idx == LottieTensor.CMD_ASSET_END:  # 离开asset
                    if asset_depth > 0:
                        asset_depth -= 1
                elif cmd_idx in LAYER_START_CMDS:
                    layer_stack += 1
                elif cmd_idx in LAYER_END_CMDS:
                    if layer_stack > 0:
                        layer_stack -= 1
                        layer_count += 1  # 完成一个完整的layer
                        # 如果不在asset内部，这是主layer
                        if asset_depth == 0:
                            main_layer_count += 1

        # 验证条件：
        # 1. 有ANIMATION命令
        # 2. 至少有一个完整的layer（layer_count >= 1）
        # 3. 所有layer都已正确闭合（layer_stack == 0）
        # 4. 【新增】至少有一个主layer（main_layer_count >= 1），防止只有assets没有主layers
        return has_animation and layer_count >= 1 and layer_stack == 0 and main_layer_count >= 1



    def flatten_to_list(lottie_tensor: 'LottieTensor', max_length: int = None) -> List[int]:
        """
        Flatten LottieTensor to a 1D list with proper offsets.
        紧凑格式：不使用 SKIP_TOKEN，只输出有意义的参数。
        """
        COMMAND_OFFSET = 151936
        NUMBER_OFFSET = 173186
        NUM_COMMANDS = len(LottieTensor.COMMANDS)
        
        # Essential parameter counts - params before this index must always be output
        ESSENTIAL_PARAM_COUNT = {
            LottieTensor.CMD_ANIMATION: 6,
            LottieTensor.CMD_LAYER: 4,
            LottieTensor.CMD_NULL_LAYER: 4,
            LottieTensor.CMD_PRECOMP_LAYER: 4,
            LottieTensor.CMD_TEXT_LAYER: 4,
            LottieTensor.CMD_SOLID_LAYER: 6,
            LottieTensor.CMD_KEYFRAME: 1,
            LottieTensor.CMD_WIDTH_KEYFRAME: 2,
            LottieTensor.CMD_COLOR_KEYFRAME: 5,
            LottieTensor.CMD_OPACITY_KEYFRAME: 2,
            LottieTensor.CMD_POINT: 2,
            LottieTensor.CMD_FILL: 3,
            LottieTensor.CMD_STROKE: 3,
            LottieTensor.CMD_TRANSFORM_SHAPE: 8,
            LottieTensor.CMD_GROUP: 1,
            LottieTensor.CMD_PATH: 4,
            LottieTensor.CMD_POSITION: 1,
            LottieTensor.CMD_SCALE: 1,
            LottieTensor.CMD_ROTATION: 1,
            LottieTensor.CMD_OPACITY: 1,
            LottieTensor.CMD_ANCHOR: 1,
            LottieTensor.CMD_SIZE: 1,
            LottieTensor.CMD_RECT: 1,
            LottieTensor.CMD_STAR: 2,
            LottieTensor.CMD_TRIM: 1,
            LottieTensor.CMD_REPEATER: 1,
            LottieTensor.CMD_MASK: 3,
            LottieTensor.CMD_MASK_PT: 2,
            LottieTensor.CMD_MASK_O: 3,
            LottieTensor.CMD_MASK_X: 3,
            LottieTensor.CMD_RANGE_SELECTOR: 5,
            LottieTensor.CMD_RANGE_START: 1,
            LottieTensor.CMD_RANGE_END: 1,
            LottieTensor.CMD_RANGE_OFFSET: 1,
            LottieTensor.CMD_AMOUNT: 3,
            LottieTensor.CMD_EFFECT: 2,
            LottieTensor.CMD_COLOR: 4,
            LottieTensor.CMD_GRADIENT_TYPE: 1,
            LottieTensor.CMD_TR_SCALE: 2,
            LottieTensor.CMD_TR_POSITION: 2,
            LottieTensor.CMD_TR_ANCHOR: 2,
            LottieTensor.CMD_ORIGINAL_COLORS: 0,
            LottieTensor.CMD_DASH_KEYFRAME: 2,
            LottieTensor.CMD_RANGE_START_KEYFRAME: 2,
            LottieTensor.CMD_RANGE_END_KEYFRAME: 2,
            LottieTensor.CMD_RANGE_OFFSET_KEYFRAME: 2,
            LottieTensor.CMD_ELLIPSE_SIZE: 1,
            LottieTensor.CMD_RECT_SIZE: 1,
        }
        
        # Parameters with default value 0 (not PAD_VAL)
        ZERO_DEFAULT_PARAMS = {
            LottieTensor.CMD_KEYFRAME: {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 22, 23, 24, 25},
            LottieTensor.CMD_WIDTH_KEYFRAME: {2, 3, 4, 5},
            LottieTensor.CMD_COLOR_KEYFRAME: {5, 6, 7, 8},
            LottieTensor.CMD_OPACITY_KEYFRAME: {2, 3, 4, 5},
            LottieTensor.CMD_DASH_KEYFRAME: {2, 3, 4, 5},
            LottieTensor.CMD_RANGE_START_KEYFRAME: {2, 3, 4, 5},
            LottieTensor.CMD_RANGE_END_KEYFRAME: {2, 3, 4, 5},
            LottieTensor.CMD_RANGE_OFFSET_KEYFRAME: {2, 3, 4, 5},
            LottieTensor.CMD_POINT: {2, 3, 4, 5},
            LottieTensor.CMD_ANIMATION: {5},
            LottieTensor.CMD_LAYER: {4, 5, 6, 7, 8, 9, 10, 11, 12},
            LottieTensor.CMD_NULL_LAYER: {4, 5, 6, 7, 8, 9, 10, 11},
            LottieTensor.CMD_PRECOMP_LAYER: {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
            LottieTensor.CMD_FILL: {3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14},  # Removed 8 (FILL_RULE) - should not default to 0
            LottieTensor.CMD_STROKE: {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13},
            LottieTensor.CMD_GROUP: {1, 2, 3, 4},
            LottieTensor.CMD_PATH: {4, 5},
            LottieTensor.CMD_TRANSFORM_SHAPE: {8, 9, 10},
            LottieTensor.CMD_RECT: {1},
            LottieTensor.CMD_POSITION: {1, 2, 3},
            LottieTensor.CMD_SCALE: {1, 2, 3},
            LottieTensor.CMD_ROTATION: {1},
            LottieTensor.CMD_OPACITY: {1},
            LottieTensor.CMD_ANCHOR: {1, 2, 3},
            LottieTensor.CMD_MASK_PT_K_I: set(range(21)),
            LottieTensor.CMD_MASK_PT_K_O: set(range(21)),
            LottieTensor.CMD_MASK_PT_K_V: set(range(21)),
            LottieTensor.CMD_MASK_PT_KF_SHAPE_I: set(range(21)),
            LottieTensor.CMD_MASK_PT_KF_SHAPE_O: set(range(21)),
            LottieTensor.CMD_MASK_PT_KF_SHAPE_V: set(range(21)),
        }
        
        # SIZE类命令集合
        SIZE_COMMANDS = {
            LottieTensor.CMD_SIZE,
            LottieTensor.CMD_ELLIPSE_SIZE,
            LottieTensor.CMD_RECT_SIZE
        }
        
        TOKENIZER_COMMANDS = {
            LottieTensor.CMD_FONT: {
                'regular': [LottieTensor.Index.Font.ASCENT],
                'token_groups': [
                    (LottieTensor.Index.Font.FAMILY_TOKEN_COUNT, 
                    LottieTensor.Index.Font.FAMILY_TOKEN_0, 10),
                    (LottieTensor.Index.Font.STYLE_TOKEN_COUNT,
                    LottieTensor.Index.Font.STYLE_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_CHAR: {
                'regular': [
                    LottieTensor.Index.Char.SIZE,
                    LottieTensor.Index.Char.W
                ],
                'token_groups': [
                    (LottieTensor.Index.Char.CH_TOKEN_COUNT,
                    LottieTensor.Index.Char.CH_TOKEN_0, 10),
                    (LottieTensor.Index.Char.STYLE_TOKEN_COUNT,
                    LottieTensor.Index.Char.STYLE_TOKEN_0, 10),
                    (LottieTensor.Index.Char.FAMILY_TOKEN_COUNT,
                    LottieTensor.Index.Char.FAMILY_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_ASSET: {
                'regular': [LottieTensor.Index.Asset.FR],
                'token_groups': [
                    (LottieTensor.Index.Asset.ID_TOKEN_COUNT,
                    LottieTensor.Index.Asset.ID_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_REFERENCE_ID: {
                'regular': [],
                'token_groups': [
                    (LottieTensor.Index.ReferenceId.ID_TOKEN_COUNT,
                    LottieTensor.Index.ReferenceId.ID_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_TEXT_KEYFRAME: {
                'regular': list(range(LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKENS_START)),
                'token_groups': [
                    (LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKEN_COUNT,
                    LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKENS_START, 10),
                    (LottieTensor.Index.TextKeyframe.TEXT_TOKEN_COUNT,
                    LottieTensor.Index.TextKeyframe.TEXT_TOKENS_START, 15)
                ]
            }
        }
        
        # 【修复】改进的 ANIMATED 值判断函数 - 使用更严格的阈值
        def is_animated_value(value):
            """判断一个值是否表示动画状态"""
            if value == LottieTensor.PAD_VAL:
                return False
            # 使用 0.5 作为阈值，任何 >= 0.5 的值都视为 animated
            return value >= 0.5
        
        def get_param_default(cmd_idx, param_pos, params):
            """Get default value for a parameter."""
            
            # 对于SIZE类命令的特殊处理
            if cmd_idx in SIZE_COMMANDS:
                # 检查ANIMATED状态
                animated_val = params[LottieTensor.Index.Transform.ANIMATED] if len(params) > 0 else LottieTensor.PAD_VAL
                is_animated = animated_val != LottieTensor.PAD_VAL and is_animated_value(animated_val)
                
                if param_pos == 0:  # ANIMATED参数本身
                    return LottieTensor.PAD_VAL
                elif param_pos in {1, 2}:  # X 和 Y 参数
                    if is_animated:
                        # ANIMATED=1时，X和Y不应该输出（由keyframe提供）
                        return LottieTensor.PAD_VAL
                    else:
                        # ANIMATED=0时，X和Y默认为0
                        return 0.0
            
            zero_set = ZERO_DEFAULT_PARAMS.get(cmd_idx, set())
            if param_pos in zero_set:
                return 0.0
            return LottieTensor.PAD_VAL
        
        def is_meaningful_value(value, default):
            """Check if a value is meaningful (not default)."""
            if value == LottieTensor.PAD_VAL:
                return False
            if default == LottieTensor.PAD_VAL:
                return True
            return abs(value - default) > 1e-6
        
        flattened = []
        
        SIZE_END_COMMANDS = {
            LottieTensor.CMD_SIZE: LottieTensor.CMD_SIZE_END,
            LottieTensor.CMD_ELLIPSE_SIZE: LottieTensor.CMD_SIZE_END,
            LottieTensor.CMD_RECT_SIZE: LottieTensor.CMD_SIZE_END,
        }
        # 【新增】前瞻检测：记录每个SIZE命令后面是否有keyframe
        size_cmd_has_keyframe = {}
        for i in range(lottie_tensor.seq_len.item()):
            cmd_idx = int(lottie_tensor.commands[i].item())
            if cmd_idx in SIZE_COMMANDS:
                # 检查后续是否有keyframe（在遇到结束标记或其他形状命令之前）
                has_kf = False
                end_cmd = SIZE_END_COMMANDS.get(cmd_idx, LottieTensor.CMD_SIZE_END)
                
                # 定义会结束 size 上下文的命令
                context_end_cmds = {
                    end_cmd,
                    LottieTensor.CMD_FILL,
                    LottieTensor.CMD_STROKE,
                    LottieTensor.CMD_GROUP_END,
                    LottieTensor.CMD_ELLIPSE_END,
                    LottieTensor.CMD_RECT_END,
                }
                
                for j in range(i + 1, lottie_tensor.seq_len.item()):
                    next_cmd = int(lottie_tensor.commands[j].item())
                    if next_cmd in context_end_cmds:
                        break
                    if next_cmd == LottieTensor.CMD_KEYFRAME:
                        has_kf = True
                        break
                size_cmd_has_keyframe[i] = has_kf

        
        for i in range(lottie_tensor.seq_len.item()):
            cmd_idx = int(lottie_tensor.commands[i].item())
            
            if cmd_idx in [LottieTensor.CMD_EOS, LottieTensor.CMD_SOS, LottieTensor.CMD_PAD]:
                continue
            
            # Add command token
            flattened.append(cmd_idx + COMMAND_OFFSET)
            
            params = lottie_tensor.params[i].tolist()
            
            if cmd_idx in TOKENIZER_COMMANDS:
                # Handle tokenizer commands specially
                cmd_info = TOKENIZER_COMMANDS[cmd_idx]

                # 【方案C】对TOKENIZER_COMMANDS，总是写入所有regular params（包括PAD_VAL）
                # 原因：regular params数量少（20个），但跳过PAD_VAL会导致unflatten无法可靠解码
                # 其他命令仍然动态截断以节省token
                for param_idx in cmd_info['regular']:
                    if param_idx < len(params):
                        value = params[param_idx]
                        offset = LottieTensor.get_param_offset(cmd_idx, param_idx)
                        flattened.append(int(round(value)) + offset)

                for count_idx, token_start, max_tokens in cmd_info['token_groups']:
                    actual_count = 0
                    for j in range(max_tokens):
                        if token_start + j < len(params):
                            token_val = int(params[token_start + j])
                            if token_val != LottieTensor.PAD_VAL and token_val > 0:
                                actual_count = j + 1

                    flattened.append(actual_count + NUMBER_OFFSET)

                    for j in range(int(max(0, actual_count))):
                        if token_start + j < len(params):
                            token_val = int(params[token_start + j])
                            if token_val != LottieTensor.PAD_VAL and token_val > 0:
                                flattened.append(token_val)
            else:
                # Handle regular commands
                param_indices = LottieTensor.get_command_param_indices(cmd_idx)
                
                if param_indices:
                    essential_count = ESSENTIAL_PARAM_COUNT.get(cmd_idx, len(param_indices))
                    
                    # 【关键修复】对于SIZE类命令的特殊处理
                    if cmd_idx in SIZE_COMMANDS:
                        animated_val = params[LottieTensor.Index.Transform.ANIMATED]
                        
                        # 【修复】综合判断是否是动画：
                        # 1. ANIMATED参数明确设为1
                        # 2. 或者后续有keyframe命令（前瞻检测结果）
                        is_animated_by_param = animated_val != LottieTensor.PAD_VAL and is_animated_value(animated_val)
                        is_animated_by_keyframe = size_cmd_has_keyframe.get(i, False)
                        is_animated = is_animated_by_param or is_animated_by_keyframe
                        
                        if is_animated:
                            # 动画模式：只输出ANIMATED参数，值固定为1
                            offset = LottieTensor.get_param_offset(cmd_idx, param_indices[0])
                            flattened.append(1 + offset)  # 固定输出整数1
                            continue  # 跳过后续处理

                    # 统一使用动态截断逻辑
                    last_meaningful = -1
                    for j, param_idx in enumerate(param_indices):
                        if param_idx < len(params):
                            value = params[param_idx]
                            default = get_param_default(cmd_idx, j, params)
                            if is_meaningful_value(value, default):
                                last_meaningful = j

                    output_count = max(essential_count, last_meaningful + 1) if last_meaningful >= 0 else essential_count
                    output_count = min(output_count, len(param_indices))

                    # 写入参数
                    for j in range(output_count):
                        param_idx = param_indices[j]
                        if param_idx < len(params):
                            value = params[param_idx]

                            if value == LottieTensor.PAD_VAL:
                                default = get_param_default(cmd_idx, j, params)
                                value = default if default != LottieTensor.PAD_VAL else 0.0

                            offset = LottieTensor.get_param_offset(cmd_idx, param_idx)
                            flattened.append(int(round(value)) + offset)

        # 智能截断逻辑
        if max_length and len(flattened) > max_length:
            # 如果长度在 max_length 和 2*max_length 之间，智能截断到最近的layer end
            if len(flattened) <= 3 * max_length:
                truncate_point = LottieTensor._find_nearest_layer_end(flattened, max_length, COMMAND_OFFSET)
                if truncate_point > 0:
                    flattened = flattened[:truncate_point]
                else:
                    # ❌ 找不到合适的layer end，放弃这个样本（返回None标记）
                    return None
            else:
                # 超过2倍长度，也放弃（太长了）
                return None

        return flattened


    @staticmethod
    def from_list(flattened: List[int]) -> 'LottieTensor':
        """
        Reconstruct LottieTensor from a flattened 1D list.
        紧凑格式解码：通过判断是否为命令Token来区分边界。
        """
        # 【新增】确保tokenizer可用于文本解码
        if LottieTensor.tokenizer is None:
            try:
                LottieTensor.init_tokenizer()
            except Exception as e:
                print(f"Warning: Failed to initialize tokenizer in from_list: {e}")

        COMMAND_OFFSET = 151936
        NUMBER_OFFSET = 173186
        NUM_COMMANDS = len(LottieTensor.COMMANDS)
        
        # SIZE类命令集合
        SIZE_COMMANDS = {
            LottieTensor.CMD_SIZE,
            LottieTensor.CMD_ELLIPSE_SIZE,
            LottieTensor.CMD_RECT_SIZE
        }
        
        # 【修复】ANIMATED 阈值常量
        ANIMATED_THRESHOLD = 0.5
        
        # Default values for parameters when not provided
        PARAM_DEFAULTS = {}
        
        # Keyframe easing defaults
        #for i in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 22, 23, 24, 25]:
        for i in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 22]:
            PARAM_DEFAULTS[(LottieTensor.CMD_KEYFRAME, i)] = 0.0
        
        for i in range(2, 6):
            PARAM_DEFAULTS[(LottieTensor.CMD_WIDTH_KEYFRAME, i)] = 0.0
        
        for i in range(5, 9):
            PARAM_DEFAULTS[(LottieTensor.CMD_COLOR_KEYFRAME, i)] = 0.0
        
        for i in range(2, 6):
            PARAM_DEFAULTS[(LottieTensor.CMD_OPACITY_KEYFRAME, i)] = 0.0
        
        for i in range(2, 6):
            PARAM_DEFAULTS[(LottieTensor.CMD_POINT, i)] = 0.0
        
        PARAM_DEFAULTS[(LottieTensor.CMD_ANIMATION, 5)] = 0.0
        
        for i in range(4, 13):
            PARAM_DEFAULTS[(LottieTensor.CMD_LAYER, i)] = 0.0
        
        for i in range(4, 12):
            PARAM_DEFAULTS[(LottieTensor.CMD_NULL_LAYER, i)] = 0.0
        
        for i in range(4, 15):
            PARAM_DEFAULTS[(LottieTensor.CMD_PRECOMP_LAYER, i)] = 0.0
        
        for i in range(3, 15):
            PARAM_DEFAULTS[(LottieTensor.CMD_FILL, i)] = 0.0
        
        for i in range(3, 14):
            PARAM_DEFAULTS[(LottieTensor.CMD_STROKE, i)] = 0.0
        
        for i in range(1, 5):
            PARAM_DEFAULTS[(LottieTensor.CMD_GROUP, i)] = 0.0
        
        for i in range(4, 6):
            PARAM_DEFAULTS[(LottieTensor.CMD_PATH, i)] = 0.0
        
        for i in range(8, 11):
            PARAM_DEFAULTS[(LottieTensor.CMD_TRANSFORM_SHAPE, i)] = 0.0
        
        for i in range(1, 4):
            PARAM_DEFAULTS[(LottieTensor.CMD_POSITION, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_SCALE, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_ANCHOR, i)] = 0.0
        PARAM_DEFAULTS[(LottieTensor.CMD_ROTATION, 1)] = 0.0
        PARAM_DEFAULTS[(LottieTensor.CMD_OPACITY, 1)] = 0.0
        
        PARAM_DEFAULTS[(LottieTensor.CMD_RECT, 1)] = 0.0
        
        for i in range(21):
            PARAM_DEFAULTS[(LottieTensor.CMD_MASK_PT_K_I, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_MASK_PT_K_O, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_MASK_PT_K_V, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_MASK_PT_KF_SHAPE_I, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_MASK_PT_KF_SHAPE_O, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_MASK_PT_KF_SHAPE_V, i)] = 0.0
        
        for i in range(2, 6):
            PARAM_DEFAULTS[(LottieTensor.CMD_DASH_KEYFRAME, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_RANGE_START_KEYFRAME, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_RANGE_END_KEYFRAME, i)] = 0.0
            PARAM_DEFAULTS[(LottieTensor.CMD_RANGE_OFFSET_KEYFRAME, i)] = 0.0
        
        TOKENIZER_COMMANDS = {
            LottieTensor.CMD_FONT: {
                'regular': [LottieTensor.Index.Font.ASCENT],
                'token_groups': [
                    (LottieTensor.Index.Font.FAMILY_TOKEN_COUNT, 
                    LottieTensor.Index.Font.FAMILY_TOKEN_0, 10),
                    (LottieTensor.Index.Font.STYLE_TOKEN_COUNT,
                    LottieTensor.Index.Font.STYLE_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_CHAR: {
                'regular': [
                    LottieTensor.Index.Char.SIZE,
                    LottieTensor.Index.Char.W
                ],
                'token_groups': [
                    (LottieTensor.Index.Char.CH_TOKEN_COUNT,
                    LottieTensor.Index.Char.CH_TOKEN_0, 10),
                    (LottieTensor.Index.Char.STYLE_TOKEN_COUNT,
                    LottieTensor.Index.Char.STYLE_TOKEN_0, 10),
                    (LottieTensor.Index.Char.FAMILY_TOKEN_COUNT,
                    LottieTensor.Index.Char.FAMILY_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_ASSET: {
                'regular': [LottieTensor.Index.Asset.FR],
                'token_groups': [
                    (LottieTensor.Index.Asset.ID_TOKEN_COUNT,
                    LottieTensor.Index.Asset.ID_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_REFERENCE_ID: {
                'regular': [],
                'token_groups': [
                    (LottieTensor.Index.ReferenceId.ID_TOKEN_COUNT,
                    LottieTensor.Index.ReferenceId.ID_TOKEN_0, 10)
                ]
            },
            LottieTensor.CMD_TEXT_KEYFRAME: {
                'regular': list(range(LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKENS_START)),
                'token_groups': [
                    (LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKEN_COUNT,
                    LottieTensor.Index.TextKeyframe.FONT_FAMILY_TOKENS_START, 10),
                    (LottieTensor.Index.TextKeyframe.TEXT_TOKEN_COUNT,
                    LottieTensor.Index.TextKeyframe.TEXT_TOKENS_START, 15)
                ]
            }
        }
        
        def is_command_token(token):
            """Check if a token is a command token."""
            return COMMAND_OFFSET <= token < COMMAND_OFFSET + NUM_COMMANDS
        
        def get_default_value(cmd_idx, param_pos, params):
            """Get default value for a parameter."""
            
            # SIZE类命令的特殊处理
            if cmd_idx in SIZE_COMMANDS:
                animated_val = params[LottieTensor.Index.Transform.ANIMATED]
                is_animated = animated_val != LottieTensor.PAD_VAL and animated_val >= ANIMATED_THRESHOLD
                
                if param_pos in {1, 2}:  # X 和 Y 参数
                    if is_animated:
                        # ANIMATED=1时，X和Y应该保持PAD_VAL（由keyframe提供）
                        return LottieTensor.PAD_VAL
                    else:
                        # ANIMATED=0时，X和Y默认为0
                        return 0.0
            
            key = (cmd_idx, param_pos)
            return PARAM_DEFAULTS.get(key, LottieTensor.PAD_VAL)
        
        # 【新增】辅助函数：检查后续是否有keyframe命令（在遇到对应的END命令之前）
        def has_following_keyframe(flattened_list, start_idx, cmd_idx):
            """检查从start_idx开始，是否有keyframe命令出现在结束标记之前"""
            # SIZE命令的结束标记
            SIZE_END_COMMANDS = {
                LottieTensor.CMD_SIZE: LottieTensor.CMD_SIZE_END,
                LottieTensor.CMD_ELLIPSE_SIZE: LottieTensor.CMD_SIZE_END,
                LottieTensor.CMD_RECT_SIZE: LottieTensor.CMD_SIZE_END,
            }
            
            end_cmd = SIZE_END_COMMANDS.get(cmd_idx, LottieTensor.CMD_SIZE_END)
            
            # 会结束 size 上下文的命令集合
            context_end_cmds = {
                end_cmd,
                LottieTensor.CMD_FILL,
                LottieTensor.CMD_STROKE,
                LottieTensor.CMD_GROUP_END,
                LottieTensor.CMD_ELLIPSE_END,
                LottieTensor.CMD_RECT_END,
            }
            
            for k in range(start_idx, len(flattened_list)):
                if is_command_token(flattened_list[k]):
                    cmd = flattened_list[k] - COMMAND_OFFSET
                    if cmd in context_end_cmds:
                        return False
                    if cmd == LottieTensor.CMD_KEYFRAME:
                        return True
            return False
        
        commands = []
        params_list = []
        
        i = 0
        while i < len(flattened):
            if is_command_token(flattened[i]):
                cmd_idx = flattened[i] - COMMAND_OFFSET
                commands.append(cmd_idx)
                cmd_start_i = i  # 记录命令的起始位置
                i += 1
                
                params = [LottieTensor.PAD_VAL] * LottieTensor.PARAM_DIM
                
                if cmd_idx in TOKENIZER_COMMANDS:
                    cmd_info = TOKENIZER_COMMANDS[cmd_idx]
                    regular_params = cmd_info['regular']
                    
                    # 【方案C】读取所有regular params - 固定长度，每个都读取
                    for param_idx in regular_params:
                        if i < len(flattened) and not is_command_token(flattened[i]):
                            offset = LottieTensor.get_param_offset(cmd_idx, param_idx)
                            params[param_idx] = float(flattened[i] - offset)
                            i += 1
                    
                    for count_idx, token_start, max_tokens in cmd_info['token_groups']:
                        if i < len(flattened) and not is_command_token(flattened[i]):
                            count = flattened[i] - NUMBER_OFFSET
                            params[count_idx] = float(count)
                            i += 1
                            
                            for j in range(int(max(0, count))):
                                if i < len(flattened) and not is_command_token(flattened[i]):
                                    if token_start + j < LottieTensor.PARAM_DIM:
                                        params[token_start + j] = float(flattened[i])
                                    i += 1
                                else:
                                    break
                else:
                    param_indices = LottieTensor.get_command_param_indices(cmd_idx)
                    
                    # Read parameters until next command
                    param_pos = 0
                    while (param_pos < len(param_indices) and 
                        i < len(flattened) and 
                        not is_command_token(flattened[i])):
                        
                        param_idx = param_indices[param_pos]
                        offset = LottieTensor.get_param_offset(cmd_idx, param_idx)
                        params[param_idx] = float(flattened[i] - offset)
                        param_pos += 1
                        i += 1
                    
                    # 【关键修复】对于SIZE类命令的特殊后处理
                    if cmd_idx in SIZE_COMMANDS:
                        animated_val = params[LottieTensor.Index.Transform.ANIMATED]
                        
                        # 情况1：只读到了ANIMATED参数且值为1
                        if param_pos == 1 and animated_val != LottieTensor.PAD_VAL and animated_val >= ANIMATED_THRESHOLD:
                            params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                        
                        # 情况2：没有读到有效的ANIMATED参数，通过前瞻检测判断
                        elif animated_val == LottieTensor.PAD_VAL or animated_val < ANIMATED_THRESHOLD:
                            # 使用修改后的函数，传入命令类型
                            if has_following_keyframe(flattened, i, cmd_idx):
                                params[LottieTensor.Index.Transform.ANIMATED] = 1.0
                            elif param_pos >= 2:
                                # 读到了多个参数，是静态 size
                                params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                                
                        # 情况3：读到了多个参数（静态size），确保ANIMATED=0
                        elif param_pos >= 2 and (animated_val == LottieTensor.PAD_VAL or animated_val < ANIMATED_THRESHOLD):
                            params[LottieTensor.Index.Transform.ANIMATED] = 0.0
                    
                    # Fill in defaults for remaining parameters
                    for j in range(param_pos, len(param_indices)):
                        param_idx = param_indices[j]
                        
                        # 获取默认值，需要传入当前params来判断ANIMATED状态
                        default_val = get_default_value(cmd_idx, j, params)
                        
                        if default_val != LottieTensor.PAD_VAL:
                            params[param_idx] = default_val
                
                params_list.append(params)
            else:
                i += 1
        
        if commands:
            commands_tensor = torch.tensor(commands).reshape(-1, 1).long()
            params_tensor = torch.tensor(params_list).float()
        else:
            commands_tensor = torch.zeros((0, 1)).long()
            params_tensor = torch.zeros((0, LottieTensor.PARAM_DIM)).float()
        
        return LottieTensor(commands_tensor, params_tensor)


