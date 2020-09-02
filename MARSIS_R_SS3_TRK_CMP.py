""" Library MARSIS_R_SS3_TRK_CMP translated from Matlab code.
use import MARSIS_R_SS3_TRK_CMP """

RecordBytes = 24823

# Parameter 1 (index = Parameter - 1)
Parameter = [ 'CENTRAL_FREQUENCY' ]; OffsetBytes = [ 0 ]; OffsetBits = [ 0 ]; Items = [ 2 ]; Precision = [ 'float32' ]
OutputPrecision = [ 'float32' ]; MachineFormat = [ 'ieee-le' ]; ItemBytes = [ 4 ]; ItemBits = [ 0 ]
# Parameter 2
Parameter.append( 'SLOPE' ); OffsetBytes.append( 8 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 3
Parameter.append( 'SCET_FRAME_WHOLE' ); OffsetBytes.append( 12 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'uint32' )
OutputPrecision.append( 'uint32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 4
Parameter.append( 'SCET_FRAME_FRAC' ); OffsetBytes.append( 16 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'uint16' )
OutputPrecision.append( 'uint16' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 2 ); ItemBits.append( 0 )
# Parameter 5
Parameter.append( 'H_SCET_PAR' ); OffsetBytes.append( 18 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 6
Parameter.append( 'VT_SCET_PAR' ); OffsetBytes.append( 22 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 7
Parameter.append( 'VR_SCET_PAR' ); OffsetBytes.append( 26 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 8
Parameter.append( 'DELTA_S_SCET_PAR' ); OffsetBytes.append( 30 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 9
Parameter.append( 'NA_SCET_PAR' ); OffsetBytes.append( 34 ); OffsetBits.append( 0 ); Items.append( 2 ); Precision.append( 'uint16' )
OutputPrecision.append( 'uint16' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 2 ); ItemBits.append( 0 )
# Parameter 10
Parameter.append( 'ECHO_MODULUS_MINUS1_F1_DIP' ); OffsetBytes.append( 38 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 11
Parameter.append( 'ECHO_PHASE_MINUS1_F1_DIP' ); OffsetBytes.append( 2086 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 12
Parameter.append( 'ECHO_MODULUS_ZERO_F1_DIP' ); OffsetBytes.append( 4134 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 13
Parameter.append( 'ECHO_PHASE_ZERO_F1_DIP' ); OffsetBytes.append( 6182 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 14
Parameter.append( 'ECHO_MODULUS_PLUS1_F1_DIP' ); OffsetBytes.append( 8230 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 15
Parameter.append( 'ECHO_PHASE_PLUS1_F1_DIP' ); OffsetBytes.append( 10278 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 16
Parameter.append( 'ECHO_MODULUS_MINUS1_F2_DIP' ); OffsetBytes.append( 12326 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 17
Parameter.append( 'ECHO_PHASE_MINUS1_F2_DIP' ); OffsetBytes.append( 14374 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 18
Parameter.append( 'ECHO_MODULUS_ZERO_F2_DIP' ); OffsetBytes.append( 16422 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 19
Parameter.append( 'ECHO_PHASE_ZERO_F2_DIP' ); OffsetBytes.append( 18470 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 20
Parameter.append( 'ECHO_MODULUS_PLUS1_F2_DIP' ); OffsetBytes.append( 20518 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 21
Parameter.append( 'ECHO_PHASE_PLUS1_F2_DIP' ); OffsetBytes.append( 22566 ); OffsetBits.append( 0 ); Items.append( 512 ); Precision.append( 'float32' )
OutputPrecision.append( 'float32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 22
Parameter.append( 'GEOMETRY_EPHEMERIS_TIME' ); OffsetBytes.append( 24614 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 23
Parameter.append( 'GEOMETRY_EPOCH' ); OffsetBytes.append( 24622 ); OffsetBits.append( 0 ); Items.append( 23 ); Precision.append( 'char' )
OutputPrecision.append( 'char' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 1 ); ItemBits.append( 0 )
# Parameter 24
Parameter.append( 'MARS_SOLAR_LONGITUDE' ); OffsetBytes.append( 24645 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 25
Parameter.append( 'MARS_SUN_DISTANCE' ); OffsetBytes.append( 24653 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 26
Parameter.append( 'ORBIT_NUMBER' ); OffsetBytes.append( 24661 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'uint32' )
OutputPrecision.append( 'uint32' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 4 ); ItemBits.append( 0 )
# Parameter 27
Parameter.append( 'TARGET_NAME' ); OffsetBytes.append( 24665 ); OffsetBits.append( 0 ); Items.append( 6 ); Precision.append( 'char' )
OutputPrecision.append( 'char' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 1 ); ItemBits.append( 0 )
# Parameter 28
Parameter.append( 'TARGET_SC_POSITION_VECTOR' ); OffsetBytes.append( 24671 ); OffsetBits.append( 0 ); Items.append( 3 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 29
Parameter.append( 'SPACECRAFT_ALTITUDE' ); OffsetBytes.append( 24695 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 30
Parameter.append( 'SUB_SC_LONGITUDE' ); OffsetBytes.append( 24703 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 31
Parameter.append( 'SUB_SC_LATITUDE' ); OffsetBytes.append( 24711 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 32
Parameter.append( 'TARGET_SC_VELOCITY_VECTOR' ); OffsetBytes.append( 24719 ); OffsetBits.append( 0 ); Items.append( 3 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 33
Parameter.append( 'TARGET_SC_RADIAL_VELOCITY' ); OffsetBytes.append( 24743 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 34
Parameter.append( 'TARGET_SC_TANG_VELOCITY' ); OffsetBytes.append( 24751 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 35
Parameter.append( 'LOCAL_TRUE_SOLAR_TIME' ); OffsetBytes.append( 24759 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 36
Parameter.append( 'SOLAR_ZENITH_ANGLE' ); OffsetBytes.append( 24767 ); OffsetBits.append( 0 ); Items.append( 1 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 37
Parameter.append( 'DIPOLE_UNIT_VECTOR' ); OffsetBytes.append( 24775 ); OffsetBits.append( 0 ); Items.append( 3 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
# Parameter 38
Parameter.append( 'MONOPOLE_UNIT_VECTOR' ); OffsetBytes.append( 24799 ); OffsetBits.append( 0 ); Items.append( 3 ); Precision.append( 'float64' )
OutputPrecision.append( 'float64' ); MachineFormat.append( 'ieee-le' ); ItemBytes.append( 8 ); ItemBits.append( 0 )
