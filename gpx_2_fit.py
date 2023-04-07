import os
import gpxpy
from geopy.distance import geodesic

from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.event_message import EventMessage
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.record_message import RecordMessage
from fit_tool.profile.profile_type import FileType, Manufacturer, Event, EventType

from config import GPX_INPUT_DIR, FIT_OUTPUT_DIR, SPORT_TYPE


def gpx2fit(gpx_file_path: str):
    """This example shows how to encode an activity into the FIT format and write it to a file. For simplicity, this
    example uses the FitFileBuilder to construct the FIT file, however in practice you might want to encode and
    write record messages to the file immediately for robustness and better memory usage. An example of how to do this
    is in the unit tests.
    """

    # set fit file name
    fit_file_name = (
        gpx_file_path.split("/")[1].replace(".gpx", ".fit").replace(".GPX", ".fit")
    )

    # Set auto_define to true, so that the builder creates the required Definition Messages for us.
    builder = FitFileBuilder(auto_define=True, min_string_size=50)

    # Read position data from a GPX file
    gpx_file = open(gpx_file_path, "r")
    gpx = gpxpy.parse(gpx_file)

    # check file, at least one track, one segment, one point
    if (
        len(gpx.tracks) == 0
        or len(gpx.tracks[0].segments) == 0
        or len(gpx.tracks[0].segments[0].points) == 0
    ):
        print("invalid gpx file: ", gpx_file_path)
        return

    first_point_time = gpx.tracks[0].segments[0].points[0].time
    # now_timestamp_millis = round(datetime.datetime(2022, 5, 10, 5, 5, 5).timestamp()) * 1000
    now_timestamp_millis = first_point_time.timestamp() * 1000

    # build fit header
    message = FileIdMessage()
    message.type = FileType.ACTIVITY

    message.manufacturer = Manufacturer.STAGES_CYCLING.value
    message.product = 0
    message.time_created = now_timestamp_millis
    message.serial_number = 0x12345678

    builder.add(message)

    # ------ add sport type
    from fit_tool.profile.messages.session_message import SessionMessage

    message = SessionMessage()
    message.sport = SPORT_TYPE

    builder.add(message)

    # It is a best practice to include timer start and stop events in all Activity files. A timer start event
    # should occur before the first Record message in the file, and a timer stop event should occur after the
    # last Record message in the file when the activity recording is complete. Timer stop and start events
    # should be used anytime the activity recording has been paused and resumed. Record messages should not be
    # encoded to the file when the timer is paused.
    start_timestamp = now_timestamp_millis
    message = EventMessage()
    message.event = Event.TIMER
    message.event_type = EventType.START
    message.timestamp = start_timestamp

    builder.add(message)

    distance = 0.0
    timestamp = start_timestamp

    records = []

    prev_coordinate = None

    for index, track_point in enumerate(gpx.tracks[0].segments[0].points):
        current_coordinate = (track_point.latitude, track_point.longitude)

        # calculate distance from previous coordinate and accumulate distance
        if prev_coordinate:
            delta = geodesic(prev_coordinate, current_coordinate).meters
        else:
            delta = 0.0
        distance += delta

        timestamp = track_point.time.timestamp() * 1000

        message = RecordMessage()
        message.position_lat = track_point.latitude
        message.position_long = track_point.longitude
        message.distance = distance
        message.timestamp = timestamp
        # message.power = round(20 * math.sin(2 * math.pi * index / 50) + 200)
        records.append(message)

        prev_coordinate = current_coordinate

    builder.add_all(records)

    message = EventMessage()
    message.event = Event.TIMER
    message.event_type = EventType.STOP
    message.timestamp = timestamp
    builder.add(message)

    # Finally build the FIT file object and write it to a file
    fit_file = builder.build()

    out_path = FIT_OUTPUT_DIR + "/" + fit_file_name
    fit_file.to_file(out_path)


def get_file_list() -> list[str]:
    files = os.listdir(GPX_INPUT_DIR)
    result_files = []
    for file in files:
        if file.endswith(".gpx"):
            result_files.append(os.path.join(GPX_INPUT_DIR, file))

    return result_files


def main():
    print("Start Processing!")
    files = get_file_list()

    for file in files:
        gpx2fit(file)


if __name__ == "__main__":
    main()
