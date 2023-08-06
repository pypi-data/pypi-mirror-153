from looqbox.view.response_board import ResponseBoard
from looqbox.view.response_board import ResponseFrame
from looqbox.objects.looq_object import LooqObject

__all__ = ["frame_to_board", "response_to_frame"]


def frame_to_board(object_frame):

    if not isinstance(object_frame, list):
        object_frame = [object_frame]

    board = ResponseBoard([frame for frame in object_frame])

    return board


def response_to_frame(obj):

    if not isinstance(obj, list):
        obj = [obj]

    list_to_frame = [looq_object for looq_object in obj if isinstance(looq_object, LooqObject)]

    frame = ResponseFrame(list_to_frame, stacked=False)

    return [frame]
