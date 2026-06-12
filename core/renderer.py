import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class Renderer:

    def draw_skeleton(self, frame, results):

        if not results.pose_landmarks:
            return frame

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 255, 255),
                thickness=2,
                circle_radius=3
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 255, 255),
                thickness=2
            )
        )

        return frame

    def draw_colored_parts(
        self,
        frame,
        landmarks,
        green_parts,
        red_parts
    ):

        h, w, _ = frame.shape

        def point(lm):
            return (
                int(lm.x * w),
                int(lm.y * h)
            )

        # LEFT ARM
        ls = point(landmarks[11])
        le = point(landmarks[13])
        lw = point(landmarks[15])

        # RIGHT ARM
        rs = point(landmarks[12])
        re = point(landmarks[14])
        rw = point(landmarks[16])

        # LEFT LEG
        lh = point(landmarks[23])
        lk = point(landmarks[25])
        la = point(landmarks[27])

        # RIGHT LEG
        rh = point(landmarks[24])
        rk = point(landmarks[26])
        ra = point(landmarks[28])

        # -----------------------
        # LEFT ARM
        # -----------------------
        if "left_arm" in green_parts:
            color = (0, 255, 0)
        elif "left_arm" in red_parts:
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)

        cv2.line(frame, ls, le, color, 8)
        cv2.line(frame, le, lw, color, 8)

        # -----------------------
        # RIGHT ARM
        # -----------------------
        if "right_arm" in green_parts:
            color = (0, 255, 0)
        elif "right_arm" in red_parts:
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)

        cv2.line(frame, rs, re, color, 8)
        cv2.line(frame, re, rw, color, 8)

        # -----------------------
        # LEFT LEG
        # -----------------------
        if "left_leg" in green_parts:
            color = (0, 255, 0)
        elif "left_leg" in red_parts:
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)

        cv2.line(frame, lh, lk, color, 8)
        cv2.line(frame, lk, la, color, 8)

        # -----------------------
        # RIGHT LEG
        # -----------------------
        if "right_leg" in green_parts:
            color = (0, 255, 0)
        elif "right_leg" in red_parts:
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)

        cv2.line(frame, rh, rk, color, 8)
        cv2.line(frame, rk, ra, color, 8)

        return frame