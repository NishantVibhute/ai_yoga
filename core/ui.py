import cv2


class UI:

    def draw_menu(
        self,
        dashboard
    ):

        cv2.putText(
            dashboard,
            "AI YOGA COACH",
            (500,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255,255,255),
            3
        )

        cv2.putText(
            dashboard,
            "1. Tadasana",
            (500,250),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,255),
            2
        )

        cv2.putText(
            dashboard,
            "Press Number To Select",
            (500,500),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        return dashboard