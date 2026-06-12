from core.angles import calculate_angle
from core.landmarks import *


class PoseEngineSitting:

   def evaluate_bhadrasana(self, landmarks):

    green_parts = []
    red_parts = []
    feedback = []

    score = 0

    nose = landmarks[NOSE]

    ls = landmarks[LEFT_SHOULDER]
    rs = landmarks[RIGHT_SHOULDER]

    le = landmarks[LEFT_ELBOW]
    re = landmarks[RIGHT_ELBOW]

    lw = landmarks[LEFT_WRIST]
    rw = landmarks[RIGHT_WRIST]

    lh = landmarks[LEFT_HIP]
    rh = landmarks[RIGHT_HIP]

    lk = landmarks[LEFT_KNEE]
    rk = landmarks[RIGHT_KNEE]

    la = landmarks[LEFT_ANKLE]
    ra = landmarks[RIGHT_ANKLE]

    # ==========================
    # TORSO UPRIGHT
    # ==========================

    shoulder_center = [
        (ls.x + rs.x) / 2,
        (ls.y + rs.y) / 2
    ]

    hip_center = [
        (lh.x + rh.x) / 2,
        (lh.y + rh.y) / 2
    ]

    body_angle = abs(
        shoulder_center[0] -
        hip_center[0]
    )

    if body_angle < 0.08:

        score += 1
        green_parts.append("torso")

    else:

        red_parts.append("torso")

        feedback.append(
            "Sit upright"
        )

    # ==========================
    # FEET TOGETHER
    # ==========================

    ankle_distance = abs(
        la.x - ra.x
    )

    if ankle_distance < 0.12:

        score += 1

    else:

        feedback.append(
            "Bring feet together"
        )

    # ==========================
    # KNEES OPEN
    # ==========================

    knee_distance = abs(
        lk.x - rk.x
    )

    if knee_distance > ankle_distance:

        score += 1

        green_parts.extend([
            "left_leg",
            "right_leg"
        ])

    else:

        red_parts.extend([
            "left_leg",
            "right_leg"
        ])

        feedback.append(
            "Open knees outward"
        )

    # ==========================
    # FEET CLOSE TO BODY
    # ==========================

    avg_ankle_y = (
        la.y + ra.y
    ) / 2

    avg_hip_y = (
        lh.y + rh.y
    ) / 2

    if abs(avg_ankle_y - avg_hip_y) < 0.25:

        score += 1

    else:

        feedback.append(
            "Pull feet closer"
        )

    # ==========================
    # HEAD STRAIGHT
    # ==========================

    if abs(nose.x - shoulder_center[0]) < 0.08:

        green_parts.append("head")

    else:

        red_parts.append("head")

        feedback.append(
            "Keep head straight"
        )

    # ==========================
    # ARMS RELAXED
    # ==========================

    left_arm = calculate_angle(
        [ls.x, ls.y],
        [le.x, le.y],
        [lw.x, lw.y]
    )

    right_arm = calculate_angle(
        [rs.x, rs.y],
        [re.x, re.y],
        [rw.x, rw.y]
    )

    if left_arm > 120 and right_arm > 120:

        green_parts.extend([
            "left_arm",
            "right_arm"
        ])

    else:

        red_parts.extend([
            "left_arm",
            "right_arm"
        ])

    percentage = (score / 4) * 100

    return {
        "score": percentage,
        "green_parts": green_parts,
        "red_parts": red_parts,
        "feedback": feedback,
        "is_correct": percentage >= 80
    }