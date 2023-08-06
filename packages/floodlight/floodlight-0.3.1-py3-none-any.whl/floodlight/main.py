from floodlight.io.tracab import read_tracab_files, _read_dat_jersey_numbers
from floodlight.io.kinexon import read_kinexon_file
from floodlight.io.dfl import (
    read_position_data_xml,
    read_event_data_xml,
    read_pitch_from_mat_info_xml,
)
from floodlight.io.secondspectrum import read_secspec_files
from floodlight.io.opta import read_f24

from floodlight import Pitch

# from floodlight.models.geometry import CentroidModel#, StretchIndexModel, PlayerDistanceModel


# PATHS
sample_kinexon_path = "C:\\Users\\Lenovo\\sciebo\\floodlight\\Kinexon\\Game 1.csv"

sample_f24_path = (
    "C:\\Users\\Lenovo\\sciebo\\floodlight\\Opta\\f24-4-2017-958085-eventdetails.xml"
)

sample_dfl_data_path = "C:\\Users\\Lenovo\\draabe\\repositories\\floodlight\\data\\DFL"

sample_tracab_dat_path = (
    "C:\\Users\\Lenovo\\draabe\\repositories\\floodlight\\data\\1040191\\1040191.dat"
)
sample_tracab_meta_path = "C:\\Users\\Lenovo\\draabe\\repositories\\floodlight\\data\\1040191\\1040191_metadata.xml"

sample_tracab_shortened_dat_path = (
    "C:\\Users\\Lenovo\\sciebo\\floodlight\\Tracab (ChyronHego)\\1044528_shortened.dat"
)
sample_tracab_shortened_meta_path = (
    "C:\\Users\\Lenovo\\sciebo\\floodlight\\Tracab (ChyronHego)\\1044528_metadata.xml"
)

sample_dfl_data_path = "C:\\Users\\Lenovo\\draabe\\repositories\\floodlight\\data\\DFL"
sample_dfl_matchinfo_path = "C:\\Users\\Lenovo\\draabe\\repositories\\floodlight\\data\\DFL\\DFL_02_01_matchinformation_DFL-COM-000001_DFL-MAT-0025CU.xml"
sample_dfl_events_path = "C:\\Users\\Lenovo\\draabe\\repositories\\floodlight\\data\\DFL\\DFL_03_02_events_raw_DFL-COM-000001_DFL-MAT-0025CU.xml"
sample_dfl_positions_path = "C:\\Users\\Lenovo\\draabe\\repositories\\floodlight\\data\\DFL\\DFL_04_02_positions_raw_DFL-COM-000001_DFL-MAT-0025CU.xml"


sample_secspec_data_path = "C:\\Users\\Lenovo\\draabe\\data\\secspecsample\\"
sample_secspec_metajson = sample_secspec_data_path + "g2261165_SecondSpectrum_meta.json"
sample_secspec_positions_path = (
    sample_secspec_data_path + "g2261165_SecondSpectrum_tracking-produced.jsonl"
)


# TRACAB DATA
# (
#     home_ht1,
#     home_ht2,
#     away_ht1,
#     away_ht2,
#     ball_ht1,
#     ball_ht2,
#     possession_ht1,
#     possession_ht2,
#     ballstatus_ht1,
#     ballstatus_ht2,
#     pitch
# ) = read_tracab_files(sample_tracab_dat_path, sample_tracab_meta_path)

# OPTA DATA
# home_ht1, home_ht2, away_ht1, away_ht2, pitch = read_f24(sample_f24_path)

# DFL DATA
# events_home_ht1, events_home_ht2, events_away_ht1, events_away_ht2 = read_event_data_xml(sample_dfl_events_path)
# pitch = read_pitch_from_mat_info_xml(sample_dfl_matchinfo_path)
# (
#     home_ht1,
#     home_ht2,
#     away_ht1,
#     away_ht2,
#     ball_ht1,
#     ball_ht2,
#     possession_ht1,
#     possession_ht2,
#     ballstatus_ht1,
#     ballstatus_ht2,
#     pitch
# ) = read_position_data_xml(sample_dfl_positions_path, sample_dfl_matchinfo_path)


# SECOND SPECTRUM DATA
(
    home_ht1,
    home_ht2,
    away_ht1,
    away_ht2,
    ball_ht1,
    ball_ht2,
    possession_ht1,
    possession_ht2,
    ballstatus_ht1,
    ballstatus_ht2,
    pitch,
) = read_secspec_files(sample_secspec_positions_path, sample_secspec_metajson)


# KINEXON DATA
# xy0, xy1, xy3 = read_kinexon_file(sample_kinexon_path)
#
# pitch = Pitch((0, 40), (0, 20), 'percent', 'flexible', 40, 20, 'handball')
# cm = CentroidModel()
# cm.fit(xy0)
# cent = cm.get_centroid()

# sim = StretchIndexModel()
# sim.fit(xy0, cent)
# stretch = sim.get_stretch_index()
#
# pdm = PlayerDistanceModel(pitch)
# pdm.fit(xy0)
# dist = pdm.get_player_distances()
# pdm.fit(xy0, xy1)
# dist2 = pdm.get_player_distances()
