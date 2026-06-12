import cv2
import numpy as np

from core.detector import PoseDetector
from core.renderer import Renderer
from core.pose_engine_standing import PoseEngineStanding
from core.pose_engine_sitting import PoseEngineSitting
from core.voice import VoiceCoach
from poses.categories import CATEGORIES

detector = PoseDetector()
renderer = Renderer()
engine_standing = PoseEngineStanding()
engine_sitting = PoseEngineSitting()

import time


show_category_menu = True
show_pose_menu = False

selected_category = None
selected_pose = None

current_poses = None

show_menu = True
show_info = False
show_detection = False
hold_start = None
pose_completed = False
completed_message = False
last_feedback = ""
last_countdown = None
last_status = ""
last_score = 0
last_feedbacks = []

voice = VoiceCoach()

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "gu": "Gujarati",
    "ta": "Tamil"
}



cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow(
    "Yoga AI Coach",
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    "Yoga AI Coach",
    1600,
    900
)

POSE_EVALUATORS = {
    "tadasana": engine_standing.evaluate_tadasana,
    "vrikshasana": engine_standing.evaluate_vrikshasana,
    "padahastasana": engine_standing.evaluate_padahastasana,
    "ardhachakrasana": engine_standing.evaluate_ardha_chakrasana,
    "trikonasana": engine_standing.evaluate_trikonasana,

    "bhadrasana": engine_sitting.evaluate_bhadrasana
}

show_menu = True
selected_pose = None

def draw_dashboard(
    frame,
    pose_name,
    score,
    remaining,
    feedbacks,
    pose_completed,
    voice_enabled
):

    # ==========================
    # PROFESSIONAL DASHBOARD
    # ==========================

    dashboard = np.zeros(
        (900, 1600, 3),
        dtype=np.uint8
    )

    # ==========================
    # CAMERA VIEW
    # ==========================

    camera_view = cv2.resize(
        frame,
        (1050, 900)
    )

    dashboard[:, :1050] = camera_view

    cv2.rectangle(
        dashboard,
        (0, 0),
        (1050, 900),
        (0, 255, 255),
        3
    )

    # ==========================
    # RIGHT PANEL GRADIENT
    # ==========================

    for i in range(900):

        shade = 20 + int(i * 0.08)

        cv2.line(
            dashboard,
            (1050, i),
            (1600, i),
            (shade, shade, shade),
            1
        )

    # ==========================
    # HEADER
    # ==========================

    cv2.putText(
        dashboard,
        "AI YOGA COACH",
        (1120, 55),
        cv2.FONT_HERSHEY_TRIPLEX,
        1,
        (255,255,255),
        2
    )

    cv2.line(
        dashboard,
        (1080, 80),
        (1560, 80),
        (80,80,80),
        2
    )

    # ==========================
    # POSE CARD
    # ==========================

    cv2.rectangle(
        dashboard,
        (1070,100),
        (1560,200),
        (45,45,45),
        -1
    )

    cv2.putText(
        dashboard,
        "CURRENT POSE",
        (1100,130),
        cv2.FONT_HERSHEY_DUPLEX,
        0.6,
        (180,180,180),
        1
    )

    score_color = ( (0,255,0) if score >= 85 else (0,0,255) )
    
    cv2.putText(
        dashboard,
        pose_name,
        (1100,180),
        cv2.FONT_HERSHEY_DUPLEX,
        1.2,
        (0,255,255),
        2
    )

   # ==================================
    # SCORE + POSE PREVIEW CARD
    # ==================================

    cv2.rectangle(
        dashboard,
        (1070,220),
        (1560,430),
        (45,45,45),
        -1
    )

    # Divider
    cv2.line(
        dashboard,
        (1330,240),
        (1330,410),
        (80,80,80),
        2
    )

    # -------------------------
    # ACCURACY SECTION
    # -------------------------

    cv2.putText(
        dashboard,
        "ACCURACY",
        (1100,260),
        cv2.FONT_HERSHEY_DUPLEX,
        0.7,
        (180,180,180),
        1
    )

    cv2.putText(
        dashboard,
        f"{score}%",
        (1100,340),
        cv2.FONT_HERSHEY_DUPLEX,
        2.2,
        score_color,
        3
    )

    bar_x = 1100
    bar_y = 380
    bar_w = 180
    bar_h = 18

    cv2.rectangle(
        dashboard,
        (bar_x, bar_y),
        (bar_x + bar_w, bar_y + bar_h),
        (70,70,70),
        -1
    )

    fill = int(
        (score / 100) * bar_w
    )

    cv2.rectangle(
        dashboard,
        (bar_x, bar_y),
        (bar_x + fill, bar_y + bar_h),
        score_color,
        -1
    )

    # -------------------------
    # POSE IMAGE ONLY
    # -------------------------

    pose_img = cv2.imread(
        pose_data["image"]
    )

    if pose_img is not None:

        pose_img = cv2.resize(
            pose_img,
            (170,170)
        )

        dashboard[
            240:410,
            1360:1530
        ] = pose_img

    else:

        cv2.rectangle(
            dashboard,
            (1360,240),
            (1530,410),
            (60,60,60),
            -1
        )
    # ==========================
    # TIMER CARD
    # ==========================

    cv2.rectangle(
        dashboard,
        (1070,430),
        (1560,580),
        (45,45,45),
        -1
    )

    cv2.putText(
        dashboard,
        "HOLD TIMER",
        (1100,470),
        cv2.FONT_HERSHEY_DUPLEX,
        0.7,
        (180,180,180),
        1
    )

    center = (1320, 510)

    cv2.circle(
        dashboard,
        center,
        60,
        (100,100,100),
        5
    )

    cv2.putText(
        dashboard,
        str(remaining),
        (1285,525),
        cv2.FONT_HERSHEY_DUPLEX,
        1.8,
        (0,255,255),
        3
    )

    voice_status = (
    f"{voice.language.upper()}"
)

    voice_color = (
        (0,255,0)
        if voice.enabled
        else (0,0,255)
    )

    cv2.putText(
        dashboard,
        f"VOICE : {voice_status}",
        (1430,520),
        cv2.FONT_HERSHEY_DUPLEX,
        0.7,
        voice_color,
        2
    )

    cv2.putText(
        dashboard,
        "L Language",
        (1480, 888),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255,255,255),
        1
    )

    # ==========================
    # FEEDBACK CARD
    # ==========================

    cv2.rectangle(
        dashboard,
        (1070,600),
        (1560,780),
        (45,45,45),
        -1
    )

    cv2.putText(
        dashboard,
        "INSTRUCTIONS",
        (1100,640),
        cv2.FONT_HERSHEY_DUPLEX,
        0.7,
        (255,255,255),
        2
    )

    y = 690

    if pose_completed:

        cv2.putText(
            dashboard,
            "Excellent Posture",
            (1100, y),
            cv2.FONT_HERSHEY_DUPLEX,
            0.8,
            (0,255,0),
            2
        )

    elif not feedbacks:

        cv2.putText(
            dashboard,
            "Hold Position",
            (1100, y),
            cv2.FONT_HERSHEY_DUPLEX,
            0.8,
            (0,255,255),
            2
        )

    else:

        for item in feedbacks[:4]:

            cv2.rectangle(
                dashboard,
                (1090,y-25),
                (1540,y+10),
                (60,60,60),
                -1
            )

            cv2.putText(
                dashboard,
                f"- {item}",
                (1110,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255,255,255),
                1
            )

            y += 40

    # ==========================
    # STATUS BAR
    # ==========================

    status_color = (
        (0,180,0)
        if score >= 85
        else (0,0,180)
    )

    status_text = (
        "HOLD POSITION"
        if score >= 85
        else "ADJUST POSITION"
    )

    cv2.rectangle(
        dashboard,
        (1070,800),
        (1560,860),
        status_color,
        -1
    )

    cv2.putText(
        dashboard,
        status_text,
        (1180,840),
        cv2.FONT_HERSHEY_DUPLEX,
        0.9,
        (255,255,255),
        2
    )

    # ==========================
    # CONTROLS
    # ==========================

    cv2.rectangle(
        dashboard,
        (1070,870),
        (1560,895),
        (35,35,35),
        -1
    )

    cv2.putText(
        dashboard,
        "B Back",
        (1090,888),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255,255,255),
        1
    )

    cv2.putText(
        dashboard,
        "M Menu",
        (1230,888),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255,255,255),
        1
    )

    cv2.putText(
        dashboard,
        "V Voice",
        (1380,888),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255,255,255),
        1
    )

    # ==========================
    # COMPLETED OVERLAY
    # ==========================

    if pose_completed:
        score = last_score
        feedbacks = last_feedbacks

        overlay = dashboard.copy()

        cv2.rectangle(
            overlay,
            (250,200),
            (1350,650),
            (0,0,0),
            -1
        )

        dashboard = cv2.addWeighted(
            overlay,
            0.8,
            dashboard,
            0.2,
            0
        )

        cv2.putText(
            dashboard,
            "YOGA COMPLETED",
            (450,380),
            cv2.FONT_HERSHEY_DUPLEX,
            2,
            (0,255,0),
            4
        )

        cv2.putText(
            dashboard,
            "Press R To Repeat",
            (550,480),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        cv2.putText(
            dashboard,
            "Press B To Back",
            (550,540),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        cv2.putText(
            dashboard,
            "Press M For Menu",
            (550,600),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

    return dashboard

def reset_pose_state():

    global hold_start
    global pose_completed
    global completed_message
    global last_feedback
    global last_countdown
    global last_status
    global last_score 
    global last_feedbacks

    hold_start = None
    pose_completed = False
    completed_message = False

    last_feedback = ""
    last_countdown = None
    last_status = ""
    last_score = 0
    last_feedbacks = []

while True:

    # ==========================
    # MENU SCREEN
    # ==========================
    if show_category_menu:

        menu = np.zeros(
            (900, 1600, 3),
            dtype=np.uint8
        )

        # =========================
        # BACKGROUND GRADIENT
        # =========================

        for i in range(900):

            color = int(
                20 + (i / 900) * 50
            )

            cv2.line(
                menu,
                (0, i),
                (1600, i),
                (color, color, color + 20),
                1
            )

        # =========================
        # HEADER
        # =========================

        cv2.rectangle(
            menu,
            (250, 40),
            (1350, 180),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            menu,
            (250, 40),
            (1350, 180),
            (0, 255, 255),
            2
        )

        cv2.putText(
            menu,
            "SELECT CATEGORY",
            (450, 120),
            cv2.FONT_HERSHEY_DUPLEX,
            2,
            (255, 255, 255),
            3
        )

        cv2.putText(
            menu,
            "Choose Your Yoga Training Program",
            (500, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (180, 180, 180),
            2
        )

        # =========================
        # CATEGORY CARDS
        # =========================

        y = 240

        for category_id, category_data in CATEGORIES.items():

            cv2.rectangle(
                menu,
                (350, y),
                (1250, y + 90),
                (40, 40, 40),
                -1
            )

            cv2.rectangle(
                menu,
                (350, y),
                (1250, y + 90),
                (0, 255, 255),
                2
            )

            # Number Badge
            cv2.circle(
                menu,
                (420, y + 45),
                30,
                (0, 255, 255),
                -1
            )

            cv2.putText(
                menu,
                category_id,
                (408, y + 58),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (0, 0, 0),
                2
            )

            cv2.putText(
                menu,
                category_data["name"],
                (490, y + 58),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (255, 255, 255),
                2
            )

            y += 120

        # =========================
        # INSTRUCTION PANEL
        # =========================

        cv2.rectangle(
            menu,
            (450, 720),
            (1150, 810),
            (35, 35, 35),
            -1
        )

        cv2.rectangle(
            menu,
            (450, 720),
            (1150, 810),
            (255, 255, 255),
            1
        )

        cv2.putText(
            menu,
            "PRESS NUMBER KEY TO SELECT CATEGORY",
            (500, 760),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (0, 255, 0),
            2
        )

        cv2.putText(
            menu,
            "ESC : Exit",
            (680, 795),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (200, 200, 200),
            2
        )

        # =========================
        # FOOTER
        # =========================

        cv2.rectangle(
            menu,
            (0, 860),
            (1600, 900),
            (25, 25, 25),
            -1
        )

        cv2.putText(
            menu,
            f"LANG : {LANGUAGE_NAMES[voice.language]}",
            (40, 888),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            1
        )

        cv2.putText(
            menu,
            "AI Yoga Coach | Category Selection",
            (600, 888),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (150, 150, 150),
            1
        )

        cv2.imshow(
            "Yoga AI Coach",
            menu
        )

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

        elif key == ord("l"):

            voice.toggle_language()

            voice.speak(
                LANGUAGE_NAMES[
                    voice.language
                ]
            )

            continue

        selected = chr(key) if key < 256 else ""

        if selected in CATEGORIES:

            selected_category = selected

            current_poses = CATEGORIES[
                selected_category
            ]["poses"]

            show_category_menu = False
            show_menu = True

        continue


    if show_menu:

        menu = np.zeros((900, 1600, 3), dtype=np.uint8)

        # Background Gradient
        for i in range(900):
            color = int(20 + (i / 900) * 50)
            cv2.line(
                menu,
                (0, i),
                (1600, i),
                (color, color, color + 20),
                1
            )

        # Main Title Card
        cv2.rectangle(
            menu,
            (250, 40),
            (1350, 180),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            menu,
            (250, 40),
            (1350, 180),
            (0, 255, 255),
            2
        )

        cv2.putText(
            menu,
            "AI YOGA COACH",
            (500, 125),
            cv2.FONT_HERSHEY_DUPLEX,
            2.2,
            (255, 255, 255),
            3
        )

        cv2.putText(
            menu,
            "Real-Time Pose Detection & Guidance",
            (520, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (180, 180, 180),
            2
        )

        # Pose Cards
        start_x = 250
        start_y = 250

        card_w = 500
        card_h = 100

        gap = 25

        pose_list = list(
            current_poses.items()
        )

        for idx, (pose_id, pose_data) in enumerate(pose_list):

            row = idx // 2
            col = idx % 2

            x = start_x + col * (card_w + 80)
            y = start_y + row * (card_h + gap)

            cv2.rectangle(
                menu,
                (x, y),
                (x + card_w, y + card_h),
                (45, 45, 45),
                -1
            )

            cv2.rectangle(
                menu,
                (x, y),
                (x + card_w, y + card_h),
                (0, 255, 255),
                2
            )

            # Number Badge
            cv2.circle(
                menu,
                (x + 50, y + 50),
                30,
                (0, 255, 255),
                -1
            )

            cv2.putText(
                menu,
                pose_id,
                (x + 38, y + 60),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (0, 0, 0),
                2
            )

            cv2.putText(
                menu,
                pose_data["name"],
                (x + 100, y + 60),
                cv2.FONT_HERSHEY_DUPLEX,
                0.9,
                (255, 255, 255),
                2
            )

        # Instructions Panel
        cv2.rectangle(
            menu,
            (450, 700),
            (1150, 810),
            (35, 35, 35),
            -1
        )

        cv2.rectangle(
            menu,
            (450, 700),
            (1150, 810),
            (255, 255, 255),
            1
        )

        cv2.putText(
            menu,
            "PRESS NUMBER KEY TO START",
            (540, 745),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            menu,
            "ESC : Exit Application",
            (620, 785),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (200, 200, 200),
            2
        )

        # Footer Bar
        cv2.rectangle(
            menu,
            (0, 860),
            (1600, 900),
            (25, 25, 25),
            -1
        )

        cv2.putText(
            menu,
            f"LANG : {LANGUAGE_NAMES[voice.language]}",
            (40, 888),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            1
        )


        cv2.putText(
            menu,
            "AI Yoga Coach | Real-Time Pose Analysis | OpenCV + MediaPipe",
            (420, 888),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (150, 150, 150),
            1
        )

        cv2.imshow(
            "Yoga AI Coach",
            menu
        )

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

        elif key == ord("l"):

            voice.toggle_language()

            voice.speak(
                LANGUAGE_NAMES[
                    voice.language
                ]
            )

            continue

        elif key == ord("b"):
            reset_pose_state()
            show_menu = False
            show_category_menu = True

            continue

        selected = chr(key) if key < 256 else ""

        if selected in current_poses:
            reset_pose_state()
            selected_pose = selected
            show_menu = False
            show_info = True

        continue


    if show_info:

        pose_data = current_poses[selected_pose]

        info = np.zeros((900, 1600, 3), dtype=np.uint8)

        # Background Gradient
        for i in range(900):
            color = int(20 + (i / 900) * 50)
            cv2.line(
                info,
                (0, i),
                (1600, i),
                (color, color, color + 20),
                1
            )

        # =========================
        # HEADER
        # =========================

        cv2.rectangle(
            info,
            (50, 30),
            (1550, 140),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            info,
            (50, 30),
            (1550, 140),
            (0, 255, 255),
            2
        )

        cv2.putText(
            info,
            pose_data["name"],
            (80, 105),
            cv2.FONT_HERSHEY_DUPLEX,
            1.8,
            (255, 255, 255),
            3
        )

        # =========================
        # BENEFITS CARD
        # =========================

        cv2.rectangle(
            info,
            (50, 180),
            (750, 450),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            info,
            (50, 180),
            (750, 450),
            (0, 255, 255),
            2
        )

        cv2.putText(
            info,
            "BENEFITS",
            (80, 230),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 255),
            2
        )

        y = 290

        for item in pose_data["benefits"]:

            cv2.putText(
                info,
                f"- {item}",
                (90, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            y += 50

        # =========================
        # INSTRUCTIONS CARD
        # =========================

        cv2.rectangle(
            info,
            (50, 500),
            (750, 820),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            info,
            (50, 500),
            (750, 820),
            (0, 255, 255),
            2
        )

        cv2.putText(
            info,
            "INSTRUCTIONS",
            (80, 550),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 255),
            2
        )

        y = 610

        for item in pose_data["instructions"]:

            cv2.putText(
                info,
                f"- {item}",
                (90, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2
            )

            y += 50

        # =========================
        # IMAGE PANEL
        # =========================

        cv2.rectangle(
            info,
            (850, 180),
            (1500, 700),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            info,
            (850, 180),
            (1500, 700),
            (0, 255, 255),
            2
        )

        cv2.putText(
            info,
            "REFERENCE POSE",
            (1030, 220),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 255),
            2
        )

        pose_img = cv2.imread(
            pose_data["image"]
        )

        if pose_img is not None:

            pose_img = cv2.resize(
                pose_img,
                (500, 400)
            )

            info[
                250:650,
                925:1425
            ] = pose_img

        # =========================
        # HOLD TIME CARD
        # =========================

        cv2.rectangle(
            info,
            (850, 730),
            (1120, 820),
            (0, 180, 255),
            -1
        )

        cv2.putText(
            info,
            f"{pose_data['hold_time']} Sec",
            (915, 790),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.putText(
            info,
            "HOLD TIME",
            (905, 760),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        # =========================
        # START BUTTON
        # =========================

        cv2.rectangle(
            info,
            (1180, 730),
            (1500, 780),
            (0, 180, 0),
            -1
        )

        cv2.putText(
            info,
            "PRESS S TO START",
            (1210, 765),
            cv2.FONT_HERSHEY_DUPLEX,
            0.75,
            (255, 255, 255),
            2
        )

        # =========================
        # BACK BUTTON
        # =========================

        cv2.rectangle(
            info,
            (1180, 790),
            (1500, 840),
            (80, 80, 80),
            -1
        )

        cv2.putText(
            info,
            "PRESS B TO GO BACK",
            (1195, 823),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        # =========================
        # FOOTER
        # =========================

        cv2.rectangle(
            info,
            (0, 860),
            (1600, 900),
            (25, 25, 25),
            -1
        )

        cv2.putText(
            info,
            f"LANG : {LANGUAGE_NAMES[voice.language]}",
            (40, 888),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            1
        )

        cv2.putText(
            info,
            "AI Yoga Coach | Review Pose Information Before Starting",
            (450, 888),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (160, 160, 160),
            1
        )

        cv2.imshow(
            "Yoga AI Coach",
            info
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            reset_pose_state()
            show_info = False
            show_detection = True

        elif key == ord("b"):
            reset_pose_state()
            show_info = False
            show_menu = True
        
        elif key == ord("l"):

            voice.toggle_language()

            voice.speak(
                LANGUAGE_NAMES[
                    voice.language
                ]
            )

            continue

        elif key == 27:
            break

        continue
    
    
    # ==========================
    # CAMERA
    # ==========================
    if show_detection:

        pose_data = current_poses[selected_pose]

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(
            frame,
            1
        )

        results = detector.process(
            frame
        )

        frame = renderer.draw_skeleton(
            frame,
            results
        )
        remaining = "--"
        score = 0
        feedbacks = []

        if results.pose_landmarks and not pose_completed:
         

            evaluation = POSE_EVALUATORS[
                pose_data["evaluator"]
            ](
                results.pose_landmarks.landmark
            )

            frame = renderer.draw_colored_parts(
                frame,
                results.pose_landmarks.landmark,
                evaluation["green_parts"],
                evaluation["red_parts"]
            )

            score = int(
                evaluation["score"]
            )

            remaining = "--"

            if score >= 85:

                if hold_start is None:

                    hold_start = time.time()

            else:

                hold_start = None
                pose_completed = False

            if score >= 85:

                if last_status != "GOOD":

                    voice.speak( voice.translate("Good posture"))
                    last_status = "GOOD"

            else:

                if last_status != "BAD":

                    voice.speak( voice.translate("Adjust your posture"))
                    last_status = "BAD"

     
            if hold_start is not None:

                elapsed = time.time() - hold_start

                hold_time = pose_data["hold_time"]

                remaining = max(
                    0,
                    hold_time - int(elapsed)
                )

                if remaining in [5,4,3,2,1]:

                    if remaining != last_countdown:

                        voice.speak(str(remaining))
                        last_countdown = remaining

                if elapsed >= hold_time and not pose_completed:

                    pose_completed = True
                    completed_message = True
                    voice.speak(
                       
                        voice.translate(
                            "Pose completed",
                        
                        )
                    )

            feedbacks = evaluation[
                "feedback"
            ]

            
            if feedbacks:

                current_feedback = feedbacks[0]

                if current_feedback != last_feedback:

                    voice.speak(voice.translate(
                            current_feedback
                            ))
                    last_feedback = current_feedback


        dashboard = draw_dashboard(
            frame,
            pose_data["name"],
            score,
            remaining,
            feedbacks,
            pose_completed,
            voice.enabled
        )

        cv2.imshow(
            "Yoga AI Coach",
            dashboard
        ) 
        

    key = cv2.waitKey(1) & 0xFF

    # ESC = Exit
    if key == 27:
        break

    

    
    # B = Back
    elif key == ord("b"):

        reset_pose_state()

        show_detection = False
        show_info = True

        continue

    elif key == ord("m"):

        reset_pose_state()

        selected_pose = None

        show_detection = False
        show_info = False
        show_menu = False
        show_category_menu = True

        continue
    elif key == ord("v"):

        voice.toggle()
    
    elif key == ord("l"):

        last_feedback = ""
        voice.toggle_language()
    elif key == ord("r"):

        reset_pose_state()

        

        voice.speak(
            LANGUAGE_NAMES[
                voice.language
            ]
        )




cap.release()
cv2.destroyAllWindows()
