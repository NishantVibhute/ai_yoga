from core.angles import calculate_angle
from core.landmarks import *


class PoseEngineStanding:

    def evaluate_tadasana(self, landmarks):

        green_parts = []
        red_parts = []
        feedback = []

        score = 0

        # ---------------------------
        # LANDMARKS
        # ---------------------------

        nose = landmarks[NOSE]

        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]

        left_elbow = landmarks[LEFT_ELBOW]
        right_elbow = landmarks[RIGHT_ELBOW]

        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]

        left_hip = landmarks[LEFT_HIP]
        right_hip = landmarks[RIGHT_HIP]

        left_knee = landmarks[LEFT_KNEE]
        right_knee = landmarks[RIGHT_KNEE]

        left_ankle = landmarks[LEFT_ANKLE]
        right_ankle = landmarks[RIGHT_ANKLE]

        # ---------------------------
        # FULL BODY CHECK
        # ---------------------------

        full_body_visible = (
            left_ankle.visibility > 0.7 and
            right_ankle.visibility > 0.7 and
            left_knee.visibility > 0.7 and
            right_knee.visibility > 0.7
        )

        if not full_body_visible:

            return {
                "score": 0,
                "green_parts": [],
                "red_parts": [],
                "feedback": [
                    "Move back. Full body should be visible."
                ],
                "is_correct": False
            }

        # ===========================
        # LEFT ARM STRAIGHT
        # ===========================

        left_arm_angle = calculate_angle(
            [left_shoulder.x, left_shoulder.y],
            [left_elbow.x, left_elbow.y],
            [left_wrist.x, left_wrist.y]
        )

        if left_arm_angle > 165:
            score += 1
            green_parts.append("left_arm")
        else:
            red_parts.append("left_arm")
            feedback.append("Straighten left arm")

        # ===========================
        # RIGHT ARM STRAIGHT
        # ===========================

        right_arm_angle = calculate_angle(
            [right_shoulder.x, right_shoulder.y],
            [right_elbow.x, right_elbow.y],
            [right_wrist.x, right_wrist.y]
        )

        if right_arm_angle > 165:
            score += 1
            green_parts.append("right_arm")
        else:
            red_parts.append("right_arm")
            feedback.append("Straighten right arm")

        # ===========================
        # LEFT LEG STRAIGHT
        # ===========================

        left_leg_angle = calculate_angle(
            [left_hip.x, left_hip.y],
            [left_knee.x, left_knee.y],
            [left_ankle.x, left_ankle.y]
        )

        if left_leg_angle > 170:
            score += 1
            green_parts.append("left_leg")
        else:
            red_parts.append("left_leg")
            feedback.append("Straighten left leg")

        # ===========================
        # RIGHT LEG STRAIGHT
        # ===========================

        right_leg_angle = calculate_angle(
            [right_hip.x, right_hip.y],
            [right_knee.x, right_knee.y],
            [right_ankle.x, right_ankle.y]
        )

        if right_leg_angle > 170:
            score += 1
            green_parts.append("right_leg")
        else:
            red_parts.append("right_leg")
            feedback.append("Straighten right leg")

        # ===========================
        # ARMS ABOVE HEAD
        # ===========================

        arms_up = (
            left_wrist.y < nose.y and
            right_wrist.y < nose.y
        )

        if arms_up:
            score += 1
        else:
            feedback.append(
                "Raise arms above head"
            )

        # ===========================
        # WRISTS TOGETHER
        # ===========================

        wrist_distance = abs(
            left_wrist.x -
            right_wrist.x
        )

        if wrist_distance < 0.08:
            score += 1
        else:
            feedback.append(
                "Bring hands together"
            )

        # ===========================
        # BODY VERTICAL
        # ===========================

        shoulder_center = [
            (left_shoulder.x + right_shoulder.x) / 2,
            (left_shoulder.y + right_shoulder.y) / 2
        ]

        hip_center = [
            (left_hip.x + right_hip.x) / 2,
            (left_hip.y + right_hip.y) / 2
        ]

        ankle_center = [
            (left_ankle.x + right_ankle.x) / 2,
            (left_ankle.y + right_ankle.y) / 2
        ]

        body_angle = calculate_angle(
            shoulder_center,
            hip_center,
            ankle_center
        )

        if body_angle > 170:
            score += 1
            green_parts.append("torso")
        else:
            red_parts.append("torso")
            feedback.append(
                "Stand straight"
            )

        # ===========================
        # SHOULDERS LEVEL
        # ===========================

        shoulder_diff = abs(
            left_shoulder.y -
            right_shoulder.y
        )

        if shoulder_diff < 0.03:
            score += 1
        else:
            feedback.append(
                "Level your shoulders"
            )

        # ===========================
        # SCORE
        # ===========================

        max_score = 8

        percentage = (
            score / max_score
        ) * 100

        return {
            "score": percentage,
            "green_parts": green_parts,
            "red_parts": red_parts,
            "feedback": feedback,
            "is_correct": percentage >= 85
        }

    def evaluate_vrikshasana(self, landmarks):

        green_parts = []
        red_parts = []
        feedback = []

        score = 0

        nose = landmarks[NOSE]

        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]

        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]

        left_hip = landmarks[LEFT_HIP]
        right_hip = landmarks[RIGHT_HIP]

        left_knee = landmarks[LEFT_KNEE]
        right_knee = landmarks[RIGHT_KNEE]

        left_ankle = landmarks[LEFT_ANKLE]
        right_ankle = landmarks[RIGHT_ANKLE]

        # =====================================
        # ARMS UP
        # =====================================

        arms_up = (
            left_wrist.y < nose.y and
            right_wrist.y < nose.y
        )

        if arms_up:
            score += 1
            green_parts.append("left_arm")
            green_parts.append("right_arm")
        else:
            red_parts.append("left_arm")
            red_parts.append("right_arm")
            feedback.append(
                "Raise arms above head"
            )

        # =====================================
        # HANDS TOGETHER
        # =====================================

        wrist_distance = abs(
            left_wrist.x -
            right_wrist.x
        )

        if wrist_distance < 0.08:
            score += 1
        else:
            feedback.append(
                "Join palms together"
            )

        # =====================================
        # LEG ANGLES
        # =====================================

        left_leg_angle = calculate_angle(
            [left_hip.x, left_hip.y],
            [left_knee.x, left_knee.y],
            [left_ankle.x, left_ankle.y]
        )

        right_leg_angle = calculate_angle(
            [right_hip.x, right_hip.y],
            [right_knee.x, right_knee.y],
            [right_ankle.x, right_ankle.y]
        )

        # Determine standing leg

        left_is_standing = left_leg_angle > right_leg_angle

        if left_is_standing:

            # LEFT LEG STRAIGHT

            if left_leg_angle > 165:

                score += 1
                green_parts.append("left_leg")

            else:

                red_parts.append("left_leg")

                feedback.append(
                    "Straighten standing leg"
                )

            # RIGHT LEG BENT

            if 40 <= right_leg_angle <= 120:

                score += 1
                green_parts.append("right_leg")

            else:

                red_parts.append("right_leg")

                feedback.append(
                    "Lift foot higher"
                )

            standing_ankle = [
                left_ankle.x,
                left_ankle.y
            ]

        else:

            # RIGHT LEG STRAIGHT

            if right_leg_angle > 165:

                score += 1
                green_parts.append("right_leg")

            else:

                red_parts.append("right_leg")

                feedback.append(
                    "Straighten standing leg"
                )

            # LEFT LEG BENT

            if 40 <= left_leg_angle <= 120:

                score += 1
                green_parts.append("left_leg")

            else:

                red_parts.append("left_leg")

                feedback.append(
                    "Lift foot higher"
                )

            standing_ankle = [
                right_ankle.x,
                right_ankle.y
            ]

        # =====================================
        # BODY UPRIGHT
        # =====================================

        shoulder_center = [
            (left_shoulder.x + right_shoulder.x) / 2,
            (left_shoulder.y + right_shoulder.y) / 2
        ]

        hip_center = [
            (left_hip.x + right_hip.x) / 2,
            (left_hip.y + right_hip.y) / 2
        ]

        body_angle = calculate_angle(
            shoulder_center,
            hip_center,
            standing_ankle
        )

        if body_angle > 170:

            score += 1
            green_parts.append("torso")

        else:

            red_parts.append("torso")

            feedback.append(
                "Keep body upright"
            )

        # =====================================
        # SCORE
        # =====================================

        percentage = (score / 5) * 100

        return {
            "score": percentage,
            "green_parts": green_parts,
            "red_parts": red_parts,
            "feedback": feedback,
            "is_correct": percentage >= 85
        }
    

    def evaluate_padahastasana(self, landmarks):

        green_parts = []
        red_parts = []
        feedback = []

        score = 0

        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]

        left_hip = landmarks[LEFT_HIP]
        right_hip = landmarks[RIGHT_HIP]

        left_knee = landmarks[LEFT_KNEE]
        right_knee = landmarks[RIGHT_KNEE]

        left_ankle = landmarks[LEFT_ANKLE]
        right_ankle = landmarks[RIGHT_ANKLE]

        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]

        nose = landmarks[NOSE]

        # ==========================
        # LEGS STRAIGHT
        # ==========================

        left_leg = calculate_angle(
            [left_hip.x, left_hip.y],
            [left_knee.x, left_knee.y],
            [left_ankle.x, left_ankle.y]
        )

        right_leg = calculate_angle(
            [right_hip.x, right_hip.y],
            [right_knee.x, right_knee.y],
            [right_ankle.x, right_ankle.y]
        )

        if left_leg > 165 and right_leg > 165:

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
                "Straighten legs"
            )

        # ==========================
        # HANDS TO FLOOR
        # ==========================

        hands_down = (
            left_wrist.y > left_knee.y and
            right_wrist.y > right_knee.y
        )

        if hands_down:

            score += 1

            green_parts.extend([
                "left_arm",
                "right_arm"
            ])

        else:

            red_parts.extend([
                "left_arm",
                "right_arm"
            ])

            feedback.append(
                "Touch the floor"
            )

        # ==========================
        # HEAD RELAXED DOWN
        # ==========================

        if nose.y > left_hip.y:

            score += 1

            green_parts.append(
                "head"
            )

        else:

            red_parts.append(
                "head"
            )

            feedback.append(
                "Relax head downward"
            )

        # ==========================
        # FORWARD FOLD
        # ==========================

        body_fold = calculate_angle(
            [left_shoulder.x, left_shoulder.y],
            [left_hip.x, left_hip.y],
            [left_knee.x, left_knee.y]
        )

        if body_fold < 100:

            score += 1

            green_parts.append(
                "torso"
            )

        else:

            red_parts.append(
                "torso"
            )

            feedback.append(
                "Bend deeper forward"
            )

        # ==========================
        # HIPS HIGH
        # ==========================

        if left_hip.y < left_knee.y:

            score += 1

        else:

            feedback.append(
                "Lift hips upward"
            )

        # ==========================
        # SCORE
        # ==========================

        percentage = (score / 5) * 100

        return {
            "score": percentage,
            "green_parts": green_parts,
            "red_parts": red_parts,
            "feedback": feedback,
            "is_correct": percentage >= 80
        }
    
    def evaluate_ardha_chakrasana(self, landmarks):

        green_parts = []
        red_parts = []
        feedback = []

        score = 0

        nose = landmarks[NOSE]

        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]

        left_elbow = landmarks[LEFT_ELBOW]
        right_elbow = landmarks[RIGHT_ELBOW]

        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]

        left_hip = landmarks[LEFT_HIP]
        right_hip = landmarks[RIGHT_HIP]

        left_knee = landmarks[LEFT_KNEE]
        right_knee = landmarks[RIGHT_KNEE]

        left_ankle = landmarks[LEFT_ANKLE]
        right_ankle = landmarks[RIGHT_ANKLE]

        # ==========================
        # LEGS STRAIGHT
        # ==========================

        left_leg = calculate_angle(
            [left_hip.x, left_hip.y],
            [left_knee.x, left_knee.y],
            [left_ankle.x, left_ankle.y]
        )

        right_leg = calculate_angle(
            [right_hip.x, right_hip.y],
            [right_knee.x, right_knee.y],
            [right_ankle.x, right_ankle.y]
        )

        if left_leg > 165 and right_leg > 165:

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
                "Straighten legs"
            )

        # ==========================
        # ARMS STRAIGHT
        # ==========================

        left_arm = calculate_angle(
            [left_shoulder.x, left_shoulder.y],
            [left_elbow.x, left_elbow.y],
            [left_wrist.x, left_wrist.y]
        )

        right_arm = calculate_angle(
            [right_shoulder.x, right_shoulder.y],
            [right_elbow.x, right_elbow.y],
            [right_wrist.x, right_wrist.y]
        )

        if left_arm > 160 and right_arm > 160:

            green_parts.extend([
                "left_arm",
                "right_arm"
            ])

        else:

            red_parts.extend([
                "left_arm",
                "right_arm"
            ])

        # ==========================
        # BACKWARD BEND
        # ==========================

        shoulder_center = [
            (left_shoulder.x + right_shoulder.x) / 2,
            (left_shoulder.y + right_shoulder.y) / 2
        ]

        hip_center = [
            (left_hip.x + right_hip.x) / 2,
            (left_hip.y + right_hip.y) / 2
        ]

        ankle_center = [
            (left_ankle.x + right_ankle.x) / 2,
            (left_ankle.y + right_ankle.y) / 2
        ]

        body_angle = calculate_angle(
            shoulder_center,
            hip_center,
            ankle_center
        )

        if body_angle < 155:

            score += 1
            green_parts.append("torso")

        else:

            red_parts.append("torso")

            feedback.append(
                "Bend backward more"
            )

        # ==========================
        # HEAD BACK
        # ==========================

        if nose.x < hip_center[0]:

            score += 1
            green_parts.append("head")

        else:

            red_parts.append("head")

            feedback.append(
                "Tilt head backward"
            )

        # ==========================
        # CHEST OPEN
        # ==========================

        shoulder_width = abs(
            left_shoulder.x -
            right_shoulder.x
        )

        if shoulder_width > 0.20:

            score += 1

        else:

            feedback.append(
                "Open chest"
            )

        # ==========================
        # HIPS FORWARD
        # ==========================

        if hip_center[0] > ankle_center[0]:

            score += 1

        else:

            feedback.append(
                "Push hips forward"
            )

        percentage = (score / 5) * 100

        return {
            "score": percentage,
            "green_parts": green_parts,
            "red_parts": red_parts,
            "feedback": feedback,
            "is_correct": percentage >= 80
        }
    
    def evaluate_trikonasana(self, landmarks):

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

        # Arms Straight

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

        if left_arm > 165 and right_arm > 165:

            score += 1
            green_parts.extend(
                ["left_arm", "right_arm"]
            )

        else:

            red_parts.extend(
                ["left_arm", "right_arm"]
            )

            feedback.append(
                "Straighten both arms"
            )

        # Arms aligned

        wrist_line = abs(
            lw.y - rw.y
        )

        if wrist_line < 0.15:

            score += 1

        else:

            feedback.append(
                "Align arms in one line"
            )

        # Side bend

        shoulder_center = [
            (ls.x + rs.x) / 2,
            (ls.y + rs.y) / 2
        ]

        hip_center = [
            (lh.x + rh.x) / 2,
            (lh.y + rh.y) / 2
        ]

        body_shift = abs(
            shoulder_center[0] -
            hip_center[0]
        )

        if body_shift > 0.12:

            score += 1
            green_parts.append("torso")

        else:

            red_parts.append("torso")

            feedback.append(
                "Bend sideways more"
            )

        # Wide stance

        foot_distance = abs(
            la.x - ra.x
        )

        if foot_distance > 0.35:

            score += 1
            green_parts.extend(
                ["left_leg", "right_leg"]
            )

        else:

            red_parts.extend(
                ["left_leg", "right_leg"]
            )

            feedback.append(
                "Keep feet wider apart"
            )

        # Looking upward

        if abs(nose.x - shoulder_center[0]) > 0.05:

            score += 1

        else:

            feedback.append(
                "Look toward upper hand"
            )

        percentage = (score / 5) * 100

        return {
            "score": percentage,
            "green_parts": green_parts,
            "red_parts": red_parts,
            "feedback": feedback,
            "is_correct": percentage >= 80
        }
    

    